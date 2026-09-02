"""
analytics/detector_models.py

Реализация конкретных стратегий обнаружения аномалий.
Выделено из detector.py для соблюдения принципа единой ответственности.
"""

import logging
from collections import deque

import numpy as np

from analytics.detector_types import DetectionResult, DetectionType, DetectorConfig

logger = logging.getLogger(__name__)


class HoltDetector:
    """
    Модель Хольта (двойное экспоненциальное сглаживание).
    Для периодических сигналов (синус, пила, треугольник) автоматически
    переключается на Rolling Z-Score (скользящую медиану), чтобы избежать
    ложных срабатываний из-за фазового сдвига прогноза.
    """

    def __init__(self, min_allowed: float, max_allowed: float, config: DetectorConfig) -> None:
        self.min_allowed = float(min_allowed)
        self.max_allowed = float(max_allowed)
        self._config = config

        self._values: deque[float] = deque(maxlen=self._config.window_size)
        self._times: deque[int] = deque(maxlen=self._config.window_size)
        self._last_time_ms: int | None = None

        self._l: float | None = None
        self._b: float | None = 0.0
        self._sigma_noise: float = 1.0
        self._last_trend_direction: str | None = None
        self._last_trend_slope: float | None = None

    def process(self, time_ms: int, value: float) -> list[DetectionResult]:
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

            # КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ: Для периодических сигналов используем скользящую медиану
            # вместо 1-step forecast, чтобы избежать фазового сдвига и ложных тревог на пиках.
            if self._config.signal_type in {"sine", "sawtooth", "triangle"}:
                results.extend(self._process_periodic(time_ms, value))
            else:
                results.extend(self._process_trend(time_ms, value, dt_sec))

        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обработки точки в HoltDetector ({time_ms} мс): {e}")
        return results

    def _process_periodic(self, time_ms: int, value: float) -> list[DetectionResult]:
        results: list[DetectionResult] = []
        arr = np.array(self._values, dtype=np.float64)
        median = float(np.median(arr))
        mad = float(np.median(np.abs(arr - median)))
        sigma = max(1e-3, 1.4826 * mad)

        residual = abs(value - median)
        threshold = self._config.sigma_factor * sigma * (1.0 + self._config.noise_tolerance)

        if residual > threshold:
            results.append(DetectionResult(
                time_ms=time_ms,
                detection_type=DetectionType.STATISTICAL,
                description=f"Аномалия (отклонение от медианы): |{value:.4f} - {median:.4f}| > {threshold:.4f}",
                value=value
            ))

        # Для периодических сигналов тренд проверяем по наклону медианы (упрощенно)
        # или оставляем стандартную проверку, если она не мешает
        return results

    def _process_trend(self, time_ms: int, value: float, dt_sec: float) -> list[DetectionResult]:
        results: list[DetectionResult] = []
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
                description=f"Аномалия (остаток прогноза): |{value:.4f} - {forecast:.4f}| > {k:.1f} * {sigma_pred:.4f}",
                value=value
            ))

        results.extend(self._check_trend(time_ms))
        return results

    def _update_sigma_noise(self) -> None:
        try:
            arr = np.array(self._values, dtype=np.float64)
            median = np.median(arr)
            mad = np.median(np.abs(arr - median))
            estimated_sigma = 1.4826 * float(mad)
            min_sigma = max(1e-3, (self.max_allowed - self.min_allowed) * 0.05)
            self._sigma_noise = max(estimated_sigma, min_sigma)
        except Exception:  # noqa: BLE001
            self._sigma_noise = 1.0

    def _holt_step(self, value: float, dt_sec: float) -> tuple[float, float, float]:
        if self._config.signal_type in {"square", "sawtooth", "triangle", "unknown"}:
            alpha, beta = 0.5, 0.1
        else:
            alpha = 0.1 if self._config.signal_type in {"sine", "noise"} else 0.2
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
            min_significant_slope = (self.max_allowed - self.min_allowed) * 0.001
            if self._b is None or abs(self._b) < min_significant_slope:
                return results

            direction = "growth" if self._b > 0 else "decay"
            bound = self.max_allowed if direction == "growth" else self.min_allowed
            bound_name = "верхний" if direction == "growth" else "нижний"

            current_value = float(self._values[-1])
            time_to_breach_sec = (bound - current_value) / self._b if self._b != 0 else float('inf')

            MAX_BREACH_TIME_SEC = 2 * 365 * 24 * 3600
            if time_to_breach_sec <= 0 or time_to_breach_sec > MAX_BREACH_TIME_SEC:
                return results

            should_report = (
                    self._last_trend_direction is None or
                    direction != self._last_trend_direction or
                    (self._last_trend_slope is not None and abs(self._b) > abs(
                        self._last_trend_slope) + min_significant_slope)
            )

            if should_report:
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
            logger.error(f"Ошибка обнаружения тренда (Хольта): {e}")
        return results

    def reset(self) -> None:
        self._values.clear()
        self._times.clear()
        self._last_time_ms = None
        self._l = None
        self._b = 0.0
        self._sigma_noise = 1.0
        self._last_trend_direction = None
        self._last_trend_slope = None


class BimodalDetector:
    """
    Бимодальная модель для сигналов с двумя устойчивыми уровнями (меандр, ступеньки).
    Игнорирует фронты, анализируя отклонения от локальных уровней и тренды по каждому уровню отдельно.
    """

    def __init__(self, min_allowed: float, max_allowed: float, config: DetectorConfig) -> None:
        self.min_allowed = float(min_allowed)
        self.max_allowed = float(max_allowed)
        self._config = config

        self._values: deque[float] = deque(maxlen=self._config.window_size)
        self._times: deque[int] = deque(maxlen=self._config.window_size)

        self._bimodal_initialized: bool = False
        self._level_a: float = 0.0
        self._level_b: float = 0.0
        self._mad_a: float = 1.0
        self._mad_b: float = 1.0
        self._level_a_points: deque[tuple[int, float]] = deque(maxlen=100)
        self._level_b_points: deque[tuple[int, float]] = deque(maxlen=100)
        self._last_bimodal_level: str | None = None
        self._front_cooldown: int = 0
        self._last_bimodal_trend_level: str | None = None
        self._last_bimodal_trend_direction: str | None = None
        self._last_bimodal_trend_slope: float | None = None

    def process(self, time_ms: int, value: float) -> list[DetectionResult]:
        results: list[DetectionResult] = []
        try:
            self._values.append(value)
            self._times.append(time_ms)

            if not self._bimodal_initialized:
                if len(self._values) >= self._config.min_samples:
                    self._initialize_bimodal_levels()
                else:
                    return results

            level, distance = self._assign_to_level(value)

            if level is None:
                self._last_bimodal_level = None
                self._front_cooldown = 3
                return results

            if self._front_cooldown > 0:
                self._front_cooldown -= 1
                self._add_point_to_level(level, time_ms, value)
                return results

            self._add_point_to_level(level, time_ms, value)
            self._update_level_stats(level)

            if level == "a":
                residual = abs(value - self._level_a)
                threshold = self._config.sigma_factor * self._mad_a
                level_value = self._level_a
            else:
                residual = abs(value - self._level_b)
                threshold = self._config.sigma_factor * self._mad_b
                level_value = self._level_b

            if residual > threshold > 1e-6:
                results.append(DetectionResult(
                    time_ms=time_ms,
                    detection_type=DetectionType.STATISTICAL,
                    description=f"Аномалия (отклонение от уровня {level.upper()}): |{value:.4f} - {level_value:.4f}| > {self._config.sigma_factor:.1f} * {threshold / self._config.sigma_factor:.4f}",
                    value=value,
                    metadata={"level": level, "residual": residual, "threshold": threshold}
                ))

            self._last_bimodal_level = level
            results.extend(self._check_trend(time_ms, level))

        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обработки точки в BimodalDetector ({time_ms} мс): {e}")
        return results

    def _initialize_bimodal_levels(self) -> None:
        try:
            arr = np.array(self._values, dtype=np.float64)
            q25 = float(np.percentile(arr, 25))
            q75 = float(np.percentile(arr, 75))

            if abs(q75 - q25) < (self.max_allowed - self.min_allowed) * 0.05:
                self._level_a = float(np.min(arr))
                self._level_b = float(np.max(arr))
            else:
                self._level_a = q25
                self._level_b = q75

            self._mad_a = max(1e-3, (self.max_allowed - self.min_allowed) * 0.01)
            self._mad_b = max(1e-3, (self.max_allowed - self.min_allowed) * 0.01)

            for t, v in zip(self._times, self._values):
                level, _ = self._assign_to_level(v)
                if level == "a":
                    self._level_a_points.append((t, v))
                elif level == "b":
                    self._level_b_points.append((t, v))

            self._bimodal_initialized = True
            logger.debug(
                f"Бимодальная модель инициализирована. Уровень A: {self._level_a:.4f}, Уровень B: {self._level_b:.4f}.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка инициализации бимодальных уровней: {e}")

    def _assign_to_level(self, value: float) -> tuple[str | None, float]:
        dist_a = abs(value - self._level_a)
        dist_b = abs(value - self._level_b)
        level_gap = abs(self._level_b - self._level_a)
        mid = (self._level_a + self._level_b) / 2.0
        dead_zone = level_gap * 0.2

        if abs(value - mid) < dead_zone and level_gap > 1e-6:
            return None, 0.0

        if dist_a < dist_b:
            return "a", dist_a
        return "b", dist_b

    def _add_point_to_level(self, level: str, time_ms: int, value: float) -> None:
        if level == "a":
            self._level_a_points.append((time_ms, value))
        else:
            self._level_b_points.append((time_ms, value))

    def _update_level_stats(self, level: str) -> None:
        try:
            points = self._level_a_points if level == "a" else self._level_b_points
            if len(points) < 3:
                return

            values = np.array([v for _, v in points], dtype=np.float64)
            median = float(np.median(values))
            mad = float(np.median(np.abs(values - median)))

            if level == "a":
                self._level_a = median
                self._mad_a = max(1e-3, 1.4826 * mad)
            else:
                self._level_b = median
                self._mad_b = max(1e-3, 1.4826 * mad)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обновления статистики уровня {level}: {e}")

    def _check_trend(self, time_ms: int, level: str) -> list[DetectionResult]:
        results: list[DetectionResult] = []
        try:
            points = self._level_a_points if level == "a" else self._level_b_points
            if len(points) < 5:
                return results

            recent = list(points)[-20:]
            times = np.array([t for t, _ in recent], dtype=np.float64)
            values = np.array([v for _, v in recent], dtype=np.float64)

            t0 = times[0]
            t_sec = (times - t0) / 1000.0

            if len(t_sec) < 2:
                return results

            t_mean = np.mean(t_sec)
            v_mean = np.mean(values)
            numerator = np.sum((t_sec - t_mean) * (values - v_mean))
            denominator = np.sum((t_sec - t_mean) ** 2)

            if abs(denominator) < 1e-9:
                return results

            slope = float(numerator / denominator)
            min_significant_slope = (self.max_allowed - self.min_allowed) * 0.001
            if abs(slope) < min_significant_slope:
                return results

            direction = "growth" if slope > 0 else "decay"
            current_value = float(values[-1])
            bound = self.max_allowed if direction == "growth" else self.min_allowed
            bound_name = "верхний" if direction == "growth" else "нижний"

            time_to_breach_sec = (bound - current_value) / slope if abs(slope) > 1e-9 else float('inf')
            MAX_BREACH_TIME_SEC = 2 * 365 * 24 * 3600

            if time_to_breach_sec <= 0 or time_to_breach_sec > MAX_BREACH_TIME_SEC:
                return results

            should_report = (
                    self._last_bimodal_trend_level != level or
                    self._last_bimodal_trend_direction != direction or
                    (self._last_bimodal_trend_slope is not None and abs(slope) > abs(
                        self._last_bimodal_trend_slope) + min_significant_slope)
            )

            if should_report:
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
                    description=f"Тренд ({dir_str}) на уровне {level.upper()}: наклон {slope:.6f} ед/сек. Прогноз выхода за {bound_name} предел через {time_str}.",
                    value=current_value,
                    metadata={"direction": direction, "level": level, "time_to_breach_sec": time_to_breach_sec}
                ))
                self._last_bimodal_trend_level = level
                self._last_bimodal_trend_direction = direction
                self._last_bimodal_trend_slope = slope
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обнаружения тренда (бимодальная модель): {e}")
        return results

    def reset(self) -> None:
        self._values.clear()
        self._times.clear()
        self._bimodal_initialized = False
        self._level_a = 0.0
        self._level_b = 0.0
        self._mad_a = 1.0
        self._mad_b = 1.0
        self._level_a_points.clear()
        self._level_b_points.clear()
        self._last_bimodal_level = None
        self._front_cooldown = 0
        self._last_bimodal_trend_level = None
        self._last_bimodal_trend_direction = None
        self._last_bimodal_trend_slope = None

