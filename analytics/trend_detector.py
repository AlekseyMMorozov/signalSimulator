"""
analytics/trend_detector.py

Детектор тренда на основе модели Хольта (двойное экспоненциальное сглаживание).
Обнаруживает медленный дрейф (низкочастотную составляющую) сигнала,
оценивая уровень и наклон в реальном времени.

Математическая основа:
    Уровень:  l_t = α·x_t + (1-α)·(l_{t-1} + b_{t-1}·dt)
    Наклон:   b_t = β·(l_t - l_{t-1})/dt + (1-β)·b_{t-1}

Критерий значимости тренда:
    Фиксированный: |b_t| > trend_threshold
    Автоматический: |b_t| > trend_auto_sigma · σ_noise / √N_eff

Поддерживает:
- Робастную оценку шума через MAD
- Прогноз времени выхода за допустимые пределы
- Подтверждение временем (time-to-live) для подавления ложных срабатываний
- Адаптацию коэффициентов под тип сигнала
"""

import logging
from collections import deque

import numpy as np

from analytics.detector_types import DetectionResult, DetectionType, DetectorConfig

logger = logging.getLogger(__name__)


class TrendDetector:
    """
    Детектор тренда на основе модели Хольта.

    Оценивает уровень и наклон сигнала в реальном времени (O(1) по памяти).
    Фиксирует тренд, когда наклон статистически значимо отличается от нуля
    и подтверждён несколькими последовательными точками (time-to-live).

    Attributes:
        min_allowed: Минимально допустимое значение сигнала.
        max_allowed: Максимально допустимое значение сигнала.
    """

    # Количество последовательных точек для подтверждения тренда
    TREND_TTL_REQUIRED = 5

    # Коэффициенты Хольта по типам сигналов
    HOLT_PARAMS = {
        "linear": {"alpha": 0.2, "beta": 0.05},
        "exponential": {"alpha": 0.2, "beta": 0.05},
        "sine": {"alpha": 0.1, "beta": 0.02},
        "noise": {"alpha": 0.1, "beta": 0.02},
        "constant": {"alpha": 0.1, "beta": 0.02},
        "default": {"alpha": 0.3, "beta": 0.1},
    }

    def __init__(self, min_allowed: float, max_allowed: float,
                 config: DetectorConfig | None = None) -> None:
        """
        Инициализация детектора тренда.

        Args:
            min_allowed: Минимально допустимое значение сигнала.
            max_allowed: Максимально допустимое значение сигнала.
            config: Конфигурация детектора. Если None — используется по умолчанию.
        """
        self.min_allowed = float(min_allowed)
        self.max_allowed = float(max_allowed)
        self._config = config if config is not None else DetectorConfig()

        # Буферы для оценки шума
        self._values: deque[float] = deque(maxlen=self._config.window_size)
        self._times: deque[int] = deque(maxlen=self._config.window_size)

        # Состояние модели Хольта
        self._level: float | None = None
        self._slope: float = 0.0
        self._sigma_noise: float = 1.0
        self._last_time_ms: int | None = None

        # Time-to-live для подтверждения тренда
        self._trend_ttl_counter: int = 0
        self._last_reported_direction: str | None = None
        self._last_reported_slope: float | None = None

        logger.info(
            f"TrendDetector инициализирован. "
            f"Диапазон: [{self.min_allowed:.4f}, {self.max_allowed:.4f}], "
            f"окно: {self._config.window_size}."
        )

    def set_config(self, config: DetectorConfig) -> None:
        """
        Обновить конфигурацию детектора.

        Args:
            config: Новая конфигурация.
        """
        try:
            self._config = config
            self._values = deque(self._values, maxlen=config.window_size)
            self._times = deque(self._times, maxlen=config.window_size)
            self.reset()
            logger.info("Конфигурация TrendDetector обновлена.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обновления конфигурации TrendDetector: {e}")

    def get_config(self) -> DetectorConfig:
        """Возвращает текущую конфигурацию детектора."""
        return self._config

    def process(self, time_ms: int, value: float) -> list[DetectionResult]:
        """
        Обработать новую точку и проверить наличие тренда.

        Args:
            time_ms: Логическое время в миллисекундах.
            value: Значение сигнала (или информативный параметр от препроцессора).

        Returns:
            Список обнаружений (обычно 0 или 1 элемент).
        """
        results: list[DetectionResult] = []
        try:
            self._values.append(value)
            self._times.append(time_ms)

            # Первая точка — инициализация уровня
            if self._last_time_ms is None:
                self._last_time_ms = time_ms
                self._level = value
                self._slope = 0.0
                return results

            dt_sec = (time_ms - self._last_time_ms) / 1000.0
            self._last_time_ms = time_ms

            if dt_sec <= 0:
                return results

            # Недостаточно данных для анализа
            if len(self._values) < self._config.min_samples:
                return results

            # Обновляем оценку шума
            self._update_sigma_noise()

            # Шаг модели Хольта
            self._holt_step(value, dt_sec)

            # Проверка значимости тренда
            results.extend(self._check_trend(time_ms, value))

        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обработки точки в TrendDetector ({time_ms} мс): {e}")

        return results

    def _holt_step(self, value: float, dt_sec: float) -> None:
        """
        Один шаг двойного экспоненциального сглаживания Хольта.

        Обновляет уровень и наклон на основе нового значения.

        Args:
            value: Текущее значение сигнала.
            dt_sec: Время с предыдущей точки в секундах.
        """
        params = self.HOLT_PARAMS.get(
            self._config.signal_type,
            self.HOLT_PARAMS["default"]
        )
        alpha = params["alpha"]
        beta = params["beta"]

        level_prev = self._level if self._level is not None else value
        slope_prev = self._slope

        # Прогноз на текущий момент
        forecast = level_prev + slope_prev * dt_sec

        # Обновление уровня
        new_level = alpha * value + (1.0 - alpha) * forecast

        # Обновление наклона
        new_slope = beta * (new_level - level_prev) / dt_sec + (1.0 - beta) * slope_prev

        self._level = new_level
        self._slope = new_slope

    def _update_sigma_noise(self) -> None:
        """Обновить робастную оценку шума через MAD."""
        try:
            arr = np.array(self._values, dtype=np.float64)
            median = float(np.median(arr))
            mad = float(np.median(np.abs(arr - median)))
            estimated_sigma = 1.4826 * mad

            # Минимальный порог шума — 5% от диапазона
            min_sigma = max(1e-3, (self.max_allowed - self.min_allowed) * 0.05)
            self._sigma_noise = max(estimated_sigma, min_sigma)
        except Exception:  # noqa: BLE001
            self._sigma_noise = 1.0

    def _check_trend(self, time_ms: int, current_value: float) -> list[DetectionResult]:
        """
        Проверить статистическую значимость тренда с подтверждением временем.

        Args:
            time_ms: Текущее логическое время.
            current_value: Текущее значение сигнала.

        Returns:
            Список обнаружений тренда.
        """
        results: list[DetectionResult] = []
        try:
            # Определяем порог значимости
            threshold = self._get_significance_threshold()

            # Проверяем значимость наклона
            if abs(self._slope) < threshold:
                # Тренд не значим — сбрасываем счётчик TTL
                self._trend_ttl_counter = 0
                return results

            # Наклон значим — увеличиваем счётчик подтверждения
            self._trend_ttl_counter += 1

            # Проверяем, что тренд подтверждён достаточным числом точек
            if self._trend_ttl_counter < self.TREND_TTL_REQUIRED:
                return results

            # Определяем направление и границу
            direction = "growth" if self._slope > 0 else "decay"
            bound = self.max_allowed if direction == "growth" else self.min_allowed
            bound_name = "верхний" if direction == "growth" else "нижний"

            # Прогноз времени выхода за предел
            if abs(self._slope) < 1e-9:
                return results

            time_to_breach_sec = (bound - current_value) / self._slope

            # Игнорируем нереалистичные прогнозы
            max_breach_time_sec = 2 * 365 * 24 * 3600  # 2 года
            if time_to_breach_sec <= 0 or time_to_breach_sec > max_breach_time_sec:
                return results

            # Проверяем, не дублируем ли предыдущее обнаружение
            min_significant_change = threshold * 0.5
            is_duplicate = (
                self._last_reported_direction == direction
                and self._last_reported_slope is not None
                and abs(abs(self._slope) - abs(self._last_reported_slope)) < min_significant_change
            )

            if is_duplicate:
                return results

            # Формируем обнаружение
            time_str = self._format_time(time_to_breach_sec)
            dir_str = "рост" if direction == "growth" else "убывание"

            results.append(DetectionResult(
                time_ms=time_ms,
                detection_type=DetectionType.TREND,
                description=(
                    f"Тренд ({dir_str}): наклон {self._slope:.6f} ед/сек. "
                    f"Прогноз выхода за {bound_name} предел через {time_str}."
                ),
                value=current_value,
                metadata={
                    "direction": direction,
                    "slope": self._slope,
                    "time_to_breach_sec": time_to_breach_sec,
                    "sigma_noise": self._sigma_noise,
                    "ttl_confirmed": self._trend_ttl_counter,
                }
            ))

            # Запоминаем для дедупликации
            self._last_reported_direction = direction
            self._last_reported_slope = self._slope

            logger.debug(
                f"Тренд обнаружен: направление={direction}, "
                f"наклон={self._slope:.6f}, TTL={self._trend_ttl_counter}."
            )

        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка проверки тренда: {e}")

        return results

    def _get_significance_threshold(self) -> float:
        """
        Вычислить порог значимости наклона.

        Если задан фиксированный порог — используется он.
        Иначе — автоматический расчёт на основе шума и размера окна.

        Returns:
            Порог значимости наклона (ед/сек).
        """
        if self._config.trend_threshold is not None:
            return self._config.trend_threshold

        # Автоматический режим: σ_noise / √N_eff * trend_auto_sigma
        n_eff = max(1, len(self._values))
        auto_threshold = (
            self._config.trend_auto_sigma * self._sigma_noise / np.sqrt(n_eff)
        )

        # Минимальный порог — 0.1% от диапазона
        min_threshold = (self.max_allowed - self.min_allowed) * 0.001
        return max(auto_threshold, min_threshold)

    @staticmethod
    def _format_time(seconds: float) -> str:
        """Форматировать время в человекочитаемую строку."""
        if seconds < 60:
            return f"{seconds:.1f} сек"
        elif seconds < 3600:
            return f"{seconds / 60:.1f} мин"
        elif seconds < 86400:
            return f"{seconds / 3600:.1f} ч"
        else:
            return f"{seconds / 86400:.1f} дней"

    def reset(self) -> None:
        """Сброс состояния детектора."""
        self._values.clear()
        self._times.clear()
        self._level = None
        self._slope = 0.0
        self._sigma_noise = 1.0
        self._last_time_ms = None
        self._trend_ttl_counter = 0
        self._last_reported_direction = None
        self._last_reported_slope = None
        logger.debug("TrendDetector сброшен.")

    def get_state(self) -> dict:
        """
        Получить текущее состояние детектора для отладки и визуализации.

        Returns:
            Словарь с текущими параметрами.
        """
        return {
            "level": self._level,
            "slope": self._slope,
            "sigma_noise": self._sigma_noise,
            "trend_ttl_counter": self._trend_ttl_counter,
            "threshold": self._get_significance_threshold(),
            "last_direction": self._last_reported_direction,
        }
