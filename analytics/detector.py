"""
analytics/detector.py

Продвинутая статистическая модель обнаружения аномалий и трендов в реальном времени.
Поддерживает две стратегии детекции:
- Модель Хольта (двойное экспоненциальное сглаживание) — для плавных сигналов
  (синус, пила, треугольник, шум, экспонента, линейный тренд).
- Бимодальная модель — для сигналов с двумя устойчивыми уровнями и резкими
  переходами (меандр, ступеньки). Игнорирует фронты, анализирует отклонения
  от локальных уровней и тренды по каждому уровню отдельно.

Выбор стратегии определяется полем signal_model в DetectorConfig:
- "auto" (по умолчанию) — автоматический выбор по типу сигнала.
- "holt" — принудительное использование модели Хольта.
- "bimodal" — принудительное использование бимодальной модели.
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
    signal_model: str = "auto"
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
            "signal_model": self.signal_model,
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
                signal_model=str(data.get("signal_model", defaults.signal_model)),
                noise_tolerance=float(data.get("noise_tolerance", defaults.noise_tolerance)),
                tau_corr=float(data.get("tau_corr", defaults.tau_corr)),
            )
        except (ValueError, TypeError) as e:
            logger.error(f"Ошибка парсинга конфигурации детектора: {e}. Используются значения по умолчанию.")
            return cls()


class AnomalyDetector:
    """
    Легкая модель обнаружения аномалий (O(1) по памяти на точку).
    Поддерживает две стратегии: модель Хольта для плавных сигналов
    и бимодальную модель для меандра/ступенек.
    """

    # Типы сигналов, для которых автоматически выбирается бимодальная модель
    BIMODAL_SIGNAL_TYPES = {"square", "step"}

    def __init__(self, min_allowed: float, max_allowed: float, config: DetectorConfig | None = None) -> None:
        self.min_allowed = float(min_allowed)
        self.max_allowed = float(max_allowed)
        self._config = config if config is not None else DetectorConfig()

        # Общие атрибуты
        self._values: deque[float] = deque(maxlen=self._config.window_size)
        self._times: deque[int] = deque(maxlen=self._config.window_size)
        self._last_time_ms: int | None = None
        self._threshold_state: str = "normal"

        # Атрибуты модели Хольта
        self._l: float | None = None
        self._b: float | None = 0.0
        self._sigma_noise: float = 1.0
        self._last_trend_direction: str | None = None
        self._last_trend_slope: float | None = None

        # Атрибуты бимодальной модели
        self._bimodal_initialized: bool = False
        self._level_a: float = 0.0  # нижний уровень
        self._level_b: float = 0.0  # верхний уровень
        self._mad_a: float = 1.0
        self._mad_b: float = 1.0
        self._level_a_points: deque[tuple[int, float]] = deque(maxlen=100)
        self._level_b_points: deque[tuple[int, float]] = deque(maxlen=100)
        self._last_bimodal_level: str | None = None  # "a", "b", или None (фронт)
        self._front_cooldown: int = 0  # счётчик точек после фронта
        self._last_bimodal_trend_level: str | None = None
        self._last_bimodal_trend_direction: str | None = None
        self._last_bimodal_trend_slope: float | None = None

        # Определяем активную модель
        self._active_model = self._resolve_model()
        logger.info(
            f"AnomalyDetector инициализирован. Тип: {self._config.signal_type}, "
            f"модель: {self._active_model}, окно: {self._config.window_size}."
        )

    def _resolve_model(self) -> str:
        """Определить активную модель детекции на основе конфигурации."""
        if self._config.signal_model == "bimodal":
            return "bimodal"
        if self._config.signal_model == "holt":
            return "holt"
        # Авто-режим: выбор по типу сигнала
        if self._config.signal_type in self.BIMODAL_SIGNAL_TYPES:
            return "bimodal"
        return "holt"

    def set_config(self, config: DetectorConfig) -> None:
        try:
            self._config = config
            self._values = deque(self._values, maxlen=self._config.window_size)
            self._times = deque(self._times, maxlen=self._config.window_size)
            self._active_model = self._resolve_model()
            self.reset()
            logger.info(f"Конфигурация детектора обновлена. Активная модель: {self._active_model}.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обновления конфигурации детектора: {e}")

    def get_config(self) -> DetectorConfig:
        """Возвращает текущую конфигурацию детектора."""
        return self._config

    def process(self, time_ms: int, value: float) -> list[DetectionResult]:
        """Обработать новую точку. Возвращает список обнаружений."""
        results: list[DetectionResult] = []
        try:
            self._values.append(value)
            self._times.append(time_ms)

            if self._last_time_ms is None:
                self._last_time_ms = time_ms
                if self._active_model == "holt":
                    self._l = value
                    self._b = 0.0
                return results

            dt_sec = (time_ms - self._last_time_ms) / 1000.0
            self._last_time_ms = time_ms

            if len(self._values) < self._config.min_samples:
                return results

            # Пороговые проверки (общие для обеих моделей)
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

            # Статистические проверки и тренды — по активной модели
            if self._active_model == "bimodal":
                bimodal_results = self._process_bimodal(time_ms, value)
                results.extend(bimodal_results)
            else:
                holt_results = self._process_holt(time_ms, value, dt_sec)
                results.extend(holt_results)

        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обработки точки в {time_ms} мс: {e}")
        return results

    def reset(self) -> None:
        self._values.clear()
        self._times.clear()
        self._last_time_ms = None
        self._threshold_state = "normal"

        # Сброс модели Хольта
        self._l = None
        self._b = 0.0
        self._sigma_noise = 1.0
        self._last_trend_direction = None
        self._last_trend_slope = None

        # Сброс бимодальной модели
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

    # === Модель Хольта (для плавных сигналов) ===

    def _process_holt(self, time_ms: int, value: float, dt_sec: float) -> list[DetectionResult]:
        """Обработка точки моделью Хольта."""
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
                description=f"Аномалия (остаток): |{value:.4f} - {forecast:.4f}| > {k:.1f} * {sigma_pred:.4f}",
                value=value
            ))

        trend_results = self._check_trend_holt(time_ms)
        results.extend(trend_results)
        return results

    def _update_sigma_noise(self) -> None:
        try:
            arr = np.array(self._values, dtype=np.float64)
            median = np.median(arr)
            mad = np.median(np.abs(arr - median))
            estimated_sigma = 1.4826 * mad
            min_sigma = max(1e-3, (self.max_allowed - self.min_allowed) * 0.05)
            self._sigma_noise = max(estimated_sigma, min_sigma)
        except Exception:  # noqa: BLE001
            self._sigma_noise = 1.0

    def _holt_step(self, value: float, dt_sec: float) -> tuple[float, float, float]:
        if self._config.signal_type in ["square", "sawtooth", "triangle", "unknown"]:
            alpha = 0.5
            beta = 0.1
        else:
            alpha = 0.1 if self._config.signal_type in ["sine", "noise"] else 0.2
            beta = 0.05

        l_prev = self._l if self._l is not None else value
        b_prev = self._b if self._b is not None else 0.0

        forecast = l_prev + b_prev * dt_sec
        new_l = alpha * value + (1 - alpha) * forecast
        new_b = beta * (new_l - l_prev) + (1 - beta) * b_prev

        return forecast, new_l, new_b

    def _check_trend_holt(self, time_ms: int) -> list[DetectionResult]:
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

            should_report = False
            if self._last_trend_direction is None or direction != self._last_trend_direction or (self._last_trend_slope is not None and abs(self._b) > abs(self._last_trend_slope) + min_significant_slope):
                should_report = True

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

    # === Бимодальная модель (для меандра/ступенек) ===

    def _process_bimodal(self, time_ms: int, value: float) -> list[DetectionResult]:
        """Обработка точки бимодальной моделью."""
        results: list[DetectionResult] = []

        # Инициализация уровней при первом заполнении окна
        if not self._bimodal_initialized:
            if len(self._values) >= self._config.min_samples:
                self._initialize_bimodal_levels()
            else:
                return results

        # Отнесение точки к уровню
        level, distance = self._assign_to_level(value)

        # Обработка фронта (точка далеко от обоих уровней)
        if level is None:
            self._last_bimodal_level = None
            self._front_cooldown = 3  # игнорируем 3 точки после фронта
            return results

        # Период адаптации после фронта
        if self._front_cooldown > 0:
            self._front_cooldown -= 1
            # Всё равно накапливаем точку в уровень для статистики
            self._add_point_to_level(level, time_ms, value)
            return results

        # Накопление точки в соответствующий уровень
        self._add_point_to_level(level, time_ms, value)

        # Обновление статистики уровня
        self._update_level_stats(level)

        # Проверка аномалии (отклонение от уровня)
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

        # Проверка тренда по уровню
        trend_results = self._check_trend_bimodal(time_ms, level)
        results.extend(trend_results)

        return results

    def _initialize_bimodal_levels(self) -> None:
        """Инициализация двух уровней по накопленным данным (квантили 25% и 75%)."""
        try:
            arr = np.array(self._values, dtype=np.float64)
            q25 = float(np.percentile(arr, 25))
            q75 = float(np.percentile(arr, 75))

            # Если квантили слишком близки (сигнал почти постоянный), используем min/max
            if abs(q75 - q25) < (self.max_allowed - self.min_allowed) * 0.05:
                self._level_a = float(np.min(arr))
                self._level_b = float(np.max(arr))
            else:
                self._level_a = q25
                self._level_b = q75

            # Начальная оценка MAD
            self._mad_a = max(1e-3, (self.max_allowed - self.min_allowed) * 0.01)
            self._mad_b = max(1e-3, (self.max_allowed - self.min_allowed) * 0.01)

            # Распределяем накопленные точки по уровням
            for t, v in zip(self._times, self._values):
                level, _ = self._assign_to_level(v)
                if level == "a":
                    self._level_a_points.append((t, v))
                elif level == "b":
                    self._level_b_points.append((t, v))

            self._bimodal_initialized = True
            logger.debug(
                f"Бимодальная модель инициализирована. Уровень A: {self._level_a:.4f}, "
                f"Уровень B: {self._level_b:.4f}."
            )
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка инициализации бимодальных уровней: {e}")

    def _assign_to_level(self, value: float) -> tuple[str | None, float]:
        """Определить, к какому уровню относится точка. Возвращает (level, distance)."""
        dist_a = abs(value - self._level_a)
        dist_b = abs(value - self._level_b)

        # Расстояние между уровнями
        level_gap = abs(self._level_b - self._level_a)
        # Если точка находится в "мёртвой зоне" между уровнями (фронт), возвращаем None
        # Мёртвая зона = 40% от расстояния между уровнями вокруг середины
        mid = (self._level_a + self._level_b) / 2.0
        dead_zone = level_gap * 0.2

        if abs(value - mid) < dead_zone and level_gap > 1e-6:
            return None, 0.0

        if dist_a < dist_b:
            return "a", dist_a
        return "b", dist_b

    def _add_point_to_level(self, level: str, time_ms: int, value: float) -> None:
        """Добавить точку в историю соответствующего уровня."""
        if level == "a":
            self._level_a_points.append((time_ms, value))
        else:
            self._level_b_points.append((time_ms, value))

    def _update_level_stats(self, level: str) -> None:
        """Обновить медиану и MAD для указанного уровня."""
        try:
            if level == "a":
                points = self._level_a_points
            else:
                points = self._level_b_points

            if len(points) < 3:
                return

            values = np.array([v for _, v in points], dtype=np.float64)
            median = float(np.median(values))
            mad = float(np.median(np.abs(values - median)))

            # Обновляем уровень (скользящая медиана)
            if level == "a":
                self._level_a = median
                self._mad_a = max(1e-3, 1.4826 * mad)
            else:
                self._level_b = median
                self._mad_b = max(1e-3, 1.4826 * mad)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обновления статистики уровня {level}: {e}")

    def _check_trend_bimodal(self, time_ms: int, level: str) -> list[DetectionResult]:
        """Проверка тренда по точкам одного уровня (линейная регрессия)."""
        results: list[DetectionResult] = []
        try:
            points = self._level_a_points if level == "a" else self._level_b_points
            if len(points) < 5:
                return results

            # Берём последние N точек уровня для регрессии
            recent = list(points)[-20:]
            times = np.array([t for t, _ in recent], dtype=np.float64)
            values = np.array([v for _, v in recent], dtype=np.float64)

            # Нормализуем время в секунды относительно первой точки
            t0 = times[0]
            t_sec = (times - t0) / 1000.0

            # Линейная регрессия: value = slope * t + intercept
            if len(t_sec) < 2:
                return results

            # Метод наименьших квадратов
            t_mean = np.mean(t_sec)
            v_mean = np.mean(values)
            numerator = np.sum((t_sec - t_mean) * (values - v_mean))
            denominator = np.sum((t_sec - t_mean) ** 2)

            if abs(denominator) < 1e-9:
                return results

            slope = float(numerator / denominator)

            # Динамический порог значимости наклона
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

            # Проверка, нужно ли сообщать о тренде
            should_report = False
            if (self._last_bimodal_trend_level != level or
                self._last_bimodal_trend_direction != direction or
                (self._last_bimodal_trend_slope is not None and
                 abs(slope) > abs(self._last_bimodal_trend_slope) + min_significant_slope)):
                should_report = True

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
                    metadata={
                        "direction": direction,
                        "level": level,
                        "time_to_breach_sec": time_to_breach_sec
                    }
                ))
                self._last_bimodal_trend_level = level
                self._last_bimodal_trend_direction = direction
                self._last_bimodal_trend_slope = slope
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обнаружения тренда (бимодальная модель): {e}")
        return results
