"""
analytics/detector.py

Лёгкая статистическая модель обнаружения аномалий и трендов в реальном времени.
Реализует три уровня анализа: пороговый контроль, статистическая проверка
(отклонение от скользящего среднего) и обнаружение тренда (линейная регрессия).
Все параметры настраиваются через DetectorConfig для управления из интерфейса.
Реализует логику "срабатывания по фронту", отсечение шумовых микронаклонов
и прогноз времени пересечения допустимых границ.
"""

import logging
from collections import deque
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)


class DetectionType(Enum):
    """Типы обнаружений."""

    THRESHOLD = auto()
    STATISTICAL = auto()
    TREND = auto()


@dataclass
class DetectionResult:
    """
    Результат обнаружения.

    Содержит время, тип обнаружения, описание, текущее значение
    и произвольные метаданные (например, направление тренда).
    """
    time_ms: int
    detection_type: DetectionType
    description: str
    value: float
    metadata: dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        """Строковое представление результата."""
        return f"{self.time_ms} мс | {self.detection_type.name} | {self.description}"


@dataclass
class DetectorConfig:
    """
    Конфигурация детектора.

    Все параметры могут быть изменены из интерфейса настроек.
    Сериализуется в словарь для сохранения в конфигурации.
    """
    window_size: int = 50
    sigma_factor: float = 3.0
    trend_threshold: float | None = None
    trend_auto_sigma: float = 3.0
    min_samples: int = 10

    def to_dict(self) -> dict[str, Any]:
        """Сериализация конфигурации в словарь."""
        return {
            "window_size": self.window_size,
            "sigma_factor": self.sigma_factor,
            "trend_threshold": self.trend_threshold,
            "trend_auto_sigma": self.trend_auto_sigma,
            "min_samples": self.min_samples,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DetectorConfig":
        """Создание конфигурации из словаря (мягкая валидация)."""
        try:
            defaults = cls()
            return cls(
                window_size=int(data.get("window_size", defaults.window_size)),
                sigma_factor=float(data.get("sigma_factor", defaults.sigma_factor)),
                trend_threshold=data.get("trend_threshold", defaults.trend_threshold),
                trend_auto_sigma=float(data.get("trend_auto_sigma", defaults.trend_auto_sigma)),
                min_samples=int(data.get("min_samples", defaults.min_samples)),
            )
        except (ValueError, TypeError) as e:
            logger.error(f"Ошибка парсинга конфигурации детектора: {e}. Используются значения по умолчанию.")
            return cls()


class AnomalyDetector:
    """
    Лёгкая статистическая модель для обнаружения аномалий и трендов.

    Создаётся отдельно для каждого графика. Метод `process(time_ms, value)`
    вызывается на каждой новой точке и возвращает список обнаружений.
    Параметры настраиваются через `DetectorConfig` и могут быть изменены
    в любой момент через `set_config` (для интерфейса настроек).
    Реализует логику "срабатывания по фронту", игнорирование микронаклонов
    и расчет прогнозируемого времени выхода за допустимые пределы.
    """

    def __init__(
        self,
        min_allowed: float,
        max_allowed: float,
        config: DetectorConfig | None = None
    ) -> None:
        """
        Инициализация детектора.

        Args:
            min_allowed: Минимально допустимое значение сигнала.
            max_allowed: Максимально допустимое значение сигнала.
            config: Конфигурация детектора. По умолчанию — стандартная.
        """
        self.min_allowed = float(min_allowed)
        self.max_allowed = float(max_allowed)
        self._config = config if config is not None else DetectorConfig()
        self._times: deque[int] = deque()
        self._values: deque[float] = deque()

        # Состояние для логики "срабатывания по фронту" (предотвращение шума)
        self._threshold_state: str = "normal"  # "normal", "below_min", "above_max"
        self._last_trend_direction: str | None = None  # "growth", "decay"
        self._last_trend_slope: float | None = None

        logger.info(
            f"AnomalyDetector инициализирован. Пределы: [{self.min_allowed}, {self.max_allowed}], "
            f"окно: {self._config.window_size}, sigma: {self._config.sigma_factor}."
        )

    def set_config(self, config: DetectorConfig) -> None:
        """Обновить конфигурацию детектора (вызывается из интерфейса настроек)."""
        try:
            self._config = config
            self._trim_window()
            logger.info(f"Конфигурация детектора обновлена: {config.to_dict()}.")
        except Exception as e:
            logger.error(f"Ошибка обновления конфигурации детектора: {e}")

    def get_config(self) -> DetectorConfig:
        """Получить текущую конфигурацию детектора."""
        return self._config

    def process(self, time_ms: int, value: float) -> list[DetectionResult]:
        """
        Обработать новую точку данных.

        Добавляет точку в скользящее окно и выполняет все три уровня анализа.

        Args:
            time_ms: Логическое время точки в миллисекундах.
            value: Значение сигнала.

        Returns:
            Список обнаружений (может быть пустым).
        """
        try:
            self._times.append(time_ms)
            self._values.append(value)
            self._trim_window()

            results: list[DetectionResult] = []
            results.extend(self._check_threshold(time_ms, value))

            # Для статистики и тренда требуется минимальное количество точек
            min_samples_for_trend = max(20, self._config.window_size // 2)
            if len(self._values) >= min_samples_for_trend:
                results.extend(self._check_statistical(time_ms, value))
                results.extend(self._check_trend(time_ms))
            return results
        except Exception as e:
            logger.error(f"Ошибка обработки точки в {time_ms} мс: {e}")
            return []

    def reset(self) -> None:
        """Сброс скользящего окна и состояния детектора."""
        self._times.clear()
        self._values.clear()
        self._threshold_state = "normal"
        self._last_trend_direction = None
        self._last_trend_slope = None
        logger.debug("Состояние и скользящее окно детектора очищены.")

    def _trim_window(self) -> None:
        """Обрезать скользящее окно до размера из конфигурации."""
        try:
            window_size = max(1, self._config.window_size)
            while len(self._values) > window_size:
                self._values.popleft()
                self._times.popleft()
        except Exception as e:
            logger.error(f"Ошибка обрезки скользящего окна: {e}")

    def _check_threshold(self, time_ms: int, value: float) -> list[DetectionResult]:
        """
        Пороговый контроль: выход за допустимые пределы.
        Реализует логику срабатывания по фронту (только при переходе границы).
        """
        results: list[DetectionResult] = []
        try:
            if value < self.min_allowed:
                if self._threshold_state != "below_min":
                    results.append(DetectionResult(
                        time_ms=time_ms,
                        detection_type=DetectionType.THRESHOLD,
                        description=f"Значение ниже минимума: {value:.4f} < {self.min_allowed:.4f}",
                        value=value,
                        metadata={"bound": "min", "min_allowed": self.min_allowed},
                    ))
                    self._threshold_state = "below_min"
            elif value > self.max_allowed:
                if self._threshold_state != "above_max":
                    results.append(DetectionResult(
                        time_ms=time_ms,
                        detection_type=DetectionType.THRESHOLD,
                        description=f"Значение выше максимума: {value:.4f} > {self.max_allowed:.4f}",
                        value=value,
                        metadata={"bound": "max", "max_allowed": self.max_allowed},
                    ))
                    self._threshold_state = "above_max"
            else:
                # Значение в норме, сбрасываем состояние для будущего обнаружения
                if self._threshold_state != "normal":
                    self._threshold_state = "normal"
        except Exception as e:
            logger.error(f"Ошибка порогового контроля: {e}")
        return results

    def _check_statistical(self, time_ms: int, value: float) -> list[DetectionResult]:
        """Статистическая проверка: отклонение от скользящего среднего."""
        results: list[DetectionResult] = []
        try:
            values = np.array(self._values, dtype=np.float64)
            if len(values) < 2:
                return results
            mean = float(np.mean(values))
            std = float(np.std(values, ddof=1))
            if std <= 0:
                return results
            deviation = abs(value - mean)
            if deviation > self._config.sigma_factor * std:
                direction = "выше" if value > mean else "ниже"
                results.append(DetectionResult(
                    time_ms=time_ms,
                    detection_type=DetectionType.STATISTICAL,
                    description=(
                        f"Отклонение {direction} среднего: |{value:.4f} - {mean:.4f}| "
                        f"> {self._config.sigma_factor} * {std:.4f}"
                    ),
                    value=value,
                    metadata={"mean": mean, "std": std, "deviation": deviation},
                ))
        except Exception as e:
            logger.error(f"Ошибка статистической проверки: {e}")
        return results

    def _check_trend(self, time_ms: int) -> list[DetectionResult]:
        """
        Обнаружение тренда: линейная регрессия по скользящему окну.
        Реализует отсечение шумовых микронаклонов, расчет времени до пересечения
        границы и логику срабатывания по фронту / ухудшению тренда.
        """
        results: list[DetectionResult] = []
        try:
            times = np.array(self._times, dtype=np.float64) / 1000.0
            values = np.array(self._values, dtype=np.float64)

            slope, intercept = np.polyfit(times, values, 1)

            # 1. Отсечение шумовых микронаклонов (плоский сигнал с погрешностью float)
            if abs(slope) < 1e-6:
                return results

            # 2. Определение значимости тренда
            significant = False
            threshold = 0.0
            if self._config.trend_threshold is not None:
                threshold = self._config.trend_threshold
                significant = abs(slope) > threshold
            else:
                n = len(times)
                y_pred = slope * times + intercept
                residuals = values - y_pred
                s_res = float(np.sqrt(np.sum(residuals ** 2) / (n - 2)))
                s_x = float(np.sqrt(np.sum((times - np.mean(times)) ** 2)))
                if s_x > 0:
                    se_slope = s_res / s_x
                    threshold = self._config.trend_auto_sigma * se_slope
                    significant = abs(slope) > threshold

            if not significant:
                self._last_trend_direction = None
                self._last_trend_slope = None
                return results

            # 3. Расчет времени до пересечения границы (в секундах)
            current_value = float(values[-1])
            direction = "growth" if slope > 0 else "decay"

            if direction == "growth":
                bound = self.max_allowed
                bound_name = "верхний"
            else:
                bound = self.min_allowed
                bound_name = "нижний"

            time_to_breach_sec = (bound - current_value) / slope

            # 4. Фильтр по сроку: максимум 2 года (63 072 000 секунд)
            MAX_BREACH_TIME_SEC = 2 * 365 * 24 * 3600

            # Сообщаем только если пересечение произойдет в будущем и раньше максимального срока
            if time_to_breach_sec <= 0 or time_to_breach_sec > MAX_BREACH_TIME_SEC:
                self._last_trend_direction = None
                self._last_trend_slope = None
                return results

            # 5. Логика предотвращения шума: отчет только при смене направления или ухудшении
            should_report = False
            if self._last_trend_direction is None or direction != self._last_trend_direction:
                should_report = True
            elif direction == self._last_trend_direction:
                if self._last_trend_slope is not None:
                    if abs(slope) > abs(self._last_trend_slope) + 1e-6:
                        should_report = True

            if should_report:
                # Форматирование времени для человека
                if time_to_breach_sec < 3600:
                    time_str = f"{time_to_breach_sec / 60:.1f} мин"
                elif time_to_breach_sec < 86400:
                    time_str = f"{time_to_breach_sec / 3600:.1f} ч"
                elif time_to_breach_sec < 31536000:
                    time_str = f"{time_to_breach_sec / 86400:.1f} дн"
                else:
                    time_str = f"{time_to_breach_sec / 31536000:.1f} лет"

                dir_str = "рост" if direction == "growth" else "убывание"
                results.append(DetectionResult(
                    time_ms=time_ms,
                    detection_type=DetectionType.TREND,
                    description=f"Обнаружен тренд ({dir_str}): наклон {slope:.6f} ед/сек. Прогноз выхода за {bound_name} предел через {time_str}.",
                    value=current_value,
                    metadata={
                        "slope": slope,
                        "intercept": intercept,
                        "direction": direction,
                        "threshold": threshold,
                        "time_to_breach_sec": time_to_breach_sec,
                    },
                ))
                self._last_trend_direction = direction
                self._last_trend_slope = slope
            else:
                # Если не сообщаем, но тренд в том же направлении, обновляем slope для отслеживания ухудшения
                self._last_trend_slope = slope

        except Exception as e:
            logger.error(f"Ошибка обнаружения тренда: {e}")
        return results
