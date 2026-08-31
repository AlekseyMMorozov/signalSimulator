"""
analytics/detector.py

Продвинутая статистическая модель обнаружения аномалий и трендов в реальном времени.
Реализует робастную оценку шума (MAD) с защитой от "холодного старта",
двойное экспоненциальное сглаживание (модель Хольта) для прогноза и тренда,
анализ остатков для точечных аномалий и учет пропадания данных.
Все параметры настраиваются через DetectorConfig.
"""

import logging
from collections import deque
from dataclasses import dataclass
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
    metadata: dict[str, Any] | None = None

    def __str__(self) -> str:
        meta_str = f", {self.metadata}" if self.metadata else ""
        return f"[{self.detection_type.name}] {self.time_ms} мс: {self.description} (значение: {self.value}){meta_str}"

    def __getitem__(self, key: str) -> Any:
        """Поддержка доступа как к словарю для обратной совместимости."""
        if key == "type":
            return self.detection_type.name
        if key == "time_ms":
            return self.time_ms
        if key == "description":
            return self.description
        if key == "value":
            return self.value
        if key == "metadata":
            return self.metadata
        raise KeyError(key)


@dataclass
class DetectorConfig:
    """Конфигурация детектора, сериализуемая в словарь."""
    window_size: int = 50
    sigma_factor: float = 3.0
    trend_threshold: float | None = None
    trend_auto_sigma: float = 3.0
    min_samples: int = 20
    signal_type: str = "unknown"
    noise_tolerance: float = 0.0
    tau_corr: float = 10.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "window_size": self.window_size,
            "sigma_factor": self.sigma_factor,
            "trend_threshold": self.trend_threshold,
            "trend_auto_sigma": self.trend_auto_sigma,
            "min_samples": self.min_samples,
            "signal_type": self.signal_type,
            "noise_tolerance": self.noise_tolerance,
            "tau_corr": self.tau_corr,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DetectorConfig":
        try:
            defaults = cls()
            return cls(
                window_size=int(data.get("window_size", defaults.window_size)),
                sigma_factor=float(data.get("sigma_factor", defaults.sigma_factor)),
                trend_threshold=data.get("trend_threshold", defaults.trend_threshold),
                trend_auto_sigma=float(data.get("trend_auto_sigma", defaults.trend_auto_sigma)),
                min_samples=int(data.get("min_samples", defaults.min_samples)),
                signal_type=str(data.get("signal_type", defaults.signal_type)),
                noise_tolerance=float(data.get("noise_tolerance", defaults.noise_tolerance)),
                tau_corr=float(data.get("tau_corr", defaults.tau_corr)),
            )
        except (ValueError, TypeError) as e:
            logger.error(f"Ошибка парсинга конфигурации детектора: {e}. Используются значения по умолчанию.")
            return cls()


class AnomalyDetector:
    """
    Легкая модель обнаружения аномалий (O(1) по памяти на точку).
    Использует модель Хольта для прогноза, MAD для оценки шума и анализ остатков.
    """

    def __init__(self, min_allowed: float, max_allowed: float, config: DetectorConfig | None = None) -> None:
        self.min_allowed = float(min_allowed)
        self.max_allowed = float(max_allowed)
        self._config = config if config is not None else DetectorConfig()

        self._values: deque[float] = deque(maxlen=self._config.window_size)
        self._times: deque[int] = deque(maxlen=self._config.window_size)

        self._last_time_ms: int | None = None
        self._l: float | None = None
        self._b: float | None = 0.0
        self._sigma_noise: float = 1.0

        self._threshold_state: str = "normal"
        self._last_trend_direction: str | None = None
        self._last_trend_slope: float | None = None

        logger.info(f"AnomalyDetector инициализирован. Тип: {self._config.signal_type}, окно: {self._config.window_size}.")

    def set_config(self, config: DetectorConfig) -> None:
        try:
            self._config = config
            self._values = deque(self._values, maxlen=self._config.window_size)
            self._times = deque(self._times, maxlen=self._config.window_size)
            self.reset()
            logger.info("Конфигурация детектора обновлена.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обновления конфигурации детектора: {e}")

    def process(self, time_ms: int, value: float) -> list[DetectionResult]:
        """Обработать новую точку. Возвращает список обнаружений."""
        results: list[DetectionResult] = []
        try:
            self._values.append(value)
            self._times.append(time_ms)

            if self._last_time_ms is None:
                self._last_time_ms = time_ms
                self._l = value
                self._b = 0.0
                return results

            dt_sec = (time_ms - self._last_time_ms) / 1000.0
            self._last_time_ms = time_ms

            if len(self._values) < self._config.min_samples:
                return results

            self._update_sigma_noise()
            forecast, new_l, new_b = self._holt_step(value, dt_sec)
            self._l, self._b = new_l, new_b

            residual = value - forecast
            sigma_pred = self._sigma_noise * np.sqrt(1.0 + max(0, dt_sec) / self._config.tau_corr)
            k = self._config.sigma_factor * (1.0 + self._config.noise_tolerance)

            if abs(residual) > k * sigma_pred:
                results.append(DetectionResult(
                    time_ms=time_ms,
                    detection_type=DetectionType.STATISTICAL,
                    description=f"Аномалия (остаток): |{value:.4f} - {forecast:.4f}| > {k:.1f} * {sigma_pred:.4f}",
                    value=value
                ))

            trend_results = self._check_trend(time_ms)
            results.extend(trend_results)

            if value < self.min_allowed and self._threshold_state != "below_min":
                results.append(DetectionResult(
                    time_ms=time_ms,
                    detection_type=DetectionType.THRESHOLD,
                    description=f"Ниже минимума: {value:.4f} < {self.min_allowed:.4f}",
                    value=value
                ))
                self._threshold_state = "below_min"
            elif value > self.max_allowed and self._threshold_state != "above_max":
                results.append(DetectionResult(
                    time_ms=time_ms,
                    detection_type=DetectionType.THRESHOLD,
                    description=f"Выше максимума: {value:.4f} > {self.max_allowed:.4f}",
                    value=value
                ))
                self._threshold_state = "above_max"
            elif self.min_allowed <= value <= self.max_allowed:
                self._threshold_state = "normal"

        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обработки точки в {time_ms} мс: {e}")
        return results

    def reset(self) -> None:
        self._values.clear()
        self._times.clear()
        self._last_time_ms = None
        self._l = None
        self._b = 0.0
        self._threshold_state = "normal"
        self._last_trend_direction = None
        self._last_trend_slope = None

    def _update_sigma_noise(self) -> None:
        try:
            arr = np.array(self._values, dtype=np.float64)
            median = np.median(arr)
            mad = np.median(np.abs(arr - median))
            estimated_sigma = 1.4826 * mad

            # Защита от "холодного старта" и идеально стабильных сигналов:
            # минимальный шум не должен быть меньше 0.5% от диапазона или 1e-3,
            # чтобы избежать ложных срабатываний при нулевом MAD.
            min_sigma = max(1e-3, (self.max_allowed - self.min_allowed) * 0.005)
            self._sigma_noise = max(estimated_sigma, min_sigma)
        except Exception:  # noqa: BLE001
            self._sigma_noise = 1.0

    def _holt_step(self, value: float, dt_sec: float) -> tuple[float, float, float]:
        alpha = 0.1 if self._config.signal_type in ["sine", "square", "sawtooth", "triangle", "noise"] else 0.2
        beta = 0.05

        l_prev = self._l if self._l is not None else value
        b_prev = self._b if self._b is not None else 0.0

        forecast = l_prev + b_prev * dt_sec
        new_l = alpha * value + (1 - alpha) * forecast
        new_b = beta * (new_l - l_prev) + (1 - beta) * b_prev

        return forecast, new_l, new_b

    def _check_trend(self, time_ms: int) -> list[DetectionResult]:
        results: list[DetectionResult] = []
        try:
            if self._b is None or abs(self._b) < 1e-6:
                return results

            direction = "growth" if self._b > 0 else "decay"
            bound = self.max_allowed if direction == "growth" else self.min_allowed
            bound_name = "верхний" if direction == "growth" else "нижний"

            current_value = float(self._values[-1])
            time_to_breach_sec = (bound - current_value) / self._b if self._b != 0 else float('inf')

            MAX_BREACH_TIME_SEC = 2 * 365 * 24 * 3600
            if time_to_breach_sec <= 0 or time_to_breach_sec > MAX_BREACH_TIME_SEC:
                return results

            should_report = False
            if self._last_trend_direction is None or direction != self._last_trend_direction or (self._last_trend_slope is not None and abs(self._b) > abs(self._last_trend_slope) + 1e-6):
                should_report = True

            if should_report:
                # Улучшенное форматирование времени: секунды, если меньше минуты
                if time_to_breach_sec < 60:
                    time_str = f"{time_to_breach_sec:.1f} сек"
                elif time_to_breach_sec < 3600:
                    time_str = f"{time_to_breach_sec / 60:.1f} мин"
                else:
                    time_str = f"{time_to_breach_sec / 3600:.1f} ч"

                dir_str = "рост" if direction == "growth" else "убывание"
                results.append(DetectionResult(
                    time_ms=time_ms,
                    detection_type=DetectionType.TREND,
                    description=f"Тренд ({dir_str}): наклон {self._b:.6f} ед/сек. Прогноз выхода за {bound_name} предел через {time_str}.",
                    value=current_value,
                    metadata={"direction": direction, "time_to_breach_sec": time_to_breach_sec}
                ))
                self._last_trend_direction = direction
                self._last_trend_slope = self._b
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обнаружения тренда: {e}")
        return results
