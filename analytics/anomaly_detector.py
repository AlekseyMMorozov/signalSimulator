"""
analytics/anomaly_detector.py

Детектор точечных аномалий (резких выбросов и провалов) на основе анализа
остатков прогнозирующего фильтра с подтверждением временем (time-to-live).

Математическая основа:
    Прогноз:  x̂_t = l_{t-1} + b_{t-1} · dt  (модель Хольта)
    Остаток:  r_t = x_t - x̂_t
    Шум:      σ_noise = 1.4826 · MAD(остатков)
    Критерий: |r_t| > K · σ_noise, где K = sigma_factor (обычно 3–4)

Поддерживает:
- Робастную оценку шума через MAD по остаткам (не по сырому сигналу)
- Подтверждение временем (time-to-live) для подавления ложных срабатываний
- Адаптацию доверительного интервала при дефиците данных
- Дедупликацию обнаружений (не повторяем одну и ту же аномалию)

Важно: детектор работает с информативным параметром от препроцессора,
а не с сырым сигналом. Для меандра/ступенек фронты уже отфильтрованы,
для синуса/треугольника анализируется амплитуда, для пилы — наклон.
"""

import logging
from collections import deque

import numpy as np

from analytics.detector_types import DetectionResult, DetectionType, DetectorConfig

logger = logging.getLogger(__name__)


class SpikeDetector:
    """
    Детектор точечных аномалий (резких выбросов и провалов).

    Использует адаптивный прогнозирующий фильтр на основе модели Хольта
    для вычисления остатка (ошибки прогноза). Аномалия фиксируется,
    когда остаток превышает порог, подтверждённый несколькими
    последовательными точками (time-to-live).

    Attributes:
        min_allowed: Минимально допустимое значение сигнала.
        max_allowed: Максимально допустимое значение сигнала.
    """

    # Количество последовательных точек для подтверждения аномалии
    ANOMALY_TTL_REQUIRED = 3

    # Максимальный размер буфера остатков для оценки шума
    RESIDUAL_BUFFER_SIZE = 100

    def __init__(self, min_allowed: float, max_allowed: float,
                 config: DetectorConfig | None = None) -> None:
        """
        Инициализация детектора точечных аномалий.

        Args:
            min_allowed: Минимально допустимое значение сигнала.
            max_allowed: Максимально допустимое значение сигнала.
            config: Конфигурация детектора. Если None — используется по умолчанию.
        """
        self.min_allowed = float(min_allowed)
        self.max_allowed = float(max_allowed)
        self._config = config if config is not None else DetectorConfig()

        # Буферы
        self._residuals: deque[float] = deque(maxlen=self.RESIDUAL_BUFFER_SIZE)
        self._last_time_ms: int | None = None

        # Состояние прогнозирующего фильтра (модель Хольта, только уровень)
        self._level: float | None = None
        self._slope: float = 0.0

        # Оценка шума по остаткам
        self._sigma_residual: float = 1.0

        # Time-to-live для подтверждения аномалии
        self._anomaly_ttl_counter: int = 0
        self._anomaly_active: bool = False

        # Дедупликация
        self._last_anomaly_time_ms: int | None = None
        self._anomaly_cooldown_points: int = 0

        logger.info(
            f"SpikeDetector инициализирован. "
            f"Диапазон: [{self.min_allowed:.4f}, {self.max_allowed:.4f}], "
            f"sigma_factor: {self._config.sigma_factor}."
        )

    def set_config(self, config: DetectorConfig) -> None:
        """
        Обновить конфигурацию детектора.

        Args:
            config: Новая конфигурация.
        """
        try:
            self._config = config
            self.reset()
            logger.info("Конфигурация SpikeDetector обновлена.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обновления конфигурации SpikeDetector: {e}")

    def get_config(self) -> DetectorConfig:
        """Возвращает текущую конфигурацию детектора."""
        return self._config

    def process(self, time_ms: int, value: float) -> list[DetectionResult]:
        """
        Обработать новую точку и проверить наличие аномалии.

        Args:
            time_ms: Логическое время в миллисекундах.
            value: Значение сигнала (или информативный параметр от препроцессора).

        Returns:
            Список обнаружений (обычно 0 или 1 элемент).
        """
        results: list[DetectionResult] = []
        try:
            # Первая точка — инициализация
            if self._last_time_ms is None:
                self._last_time_ms = time_ms
                self._level = value
                self._slope = 0.0
                return results

            dt_sec = (time_ms - self._last_time_ms) / 1000.0
            self._last_time_ms = time_ms

            if dt_sec <= 0:
                return results

            # Прогноз и остаток
            forecast = self._get_forecast(dt_sec)
            residual = value - forecast

            # Обновляем фильтр
            self._update_filter(value, forecast, dt_sec)

            # Сохраняем остаток для оценки шума
            self._residuals.append(residual)

            # Обновляем оценку шума по остаткам
            self._update_sigma_residual()

            # Вычисляем порог с учётом дефицита данных
            threshold = self._get_anomaly_threshold(dt_sec)

            # Проверяем аномалию с time-to-live
            results.extend(
                self._check_anomaly(time_ms, value, residual, threshold)
            )

            # Обработка кулдауна после обнаружения
            if self._anomaly_cooldown_points > 0:
                self._anomaly_cooldown_points -= 1

        except Exception as e:  # noqa: BLE001
            logger.error(
                f"Ошибка обработки точки в SpikeDetector ({time_ms} мс): {e}"
            )

        return results

    def _get_forecast(self, dt_sec: float) -> float:
        """
        Вычислить прогноз значения на текущий момент.

        Использует модель Хольта (уровень + наклон) для прогноза.

        Args:
            dt_sec: Время с предыдущей точки в секундах.

        Returns:
            Прогнозируемое значение.
        """
        if self._level is None:
            return 0.0
        return self._level + self._slope * dt_sec

    def _update_filter(self, value: float, forecast: float,
                       dt_sec: float) -> None:
        """
        Обновить состояние прогнозирующего фильтра (модель Хольта).

        Args:
            value: Текущее значение сигнала.
            forecast: Прогноз на текущий момент.
            dt_sec: Время с предыдущей точки в секундах.
        """
        # Адаптивные коэффициенты в зависимости от типа сигнала
        if self._config.signal_type in {"sine", "triangle", "sawtooth"}:
            alpha, beta = 0.3, 0.05
        elif self._config.signal_type in {"square", "step"}:
            alpha, beta = 0.4, 0.1
        else:
            alpha, beta = 0.2, 0.05

        level_prev = self._level if self._level is not None else value

        # Обновление уровня
        new_level = alpha * value + (1.0 - alpha) * forecast

        # Обновление наклона
        if dt_sec > 0:
            new_slope = beta * (new_level - level_prev) / dt_sec + \
                        (1.0 - beta) * self._slope
        else:
            new_slope = self._slope

        self._level = new_level
        self._slope = new_slope

    def _update_sigma_residual(self) -> None:
        """Обновить робастную оценку шума по остаткам через MAD."""
        try:
            if len(self._residuals) < 5:
                return

            arr = np.array(self._residuals, dtype=np.float64)
            median = float(np.median(arr))
            mad = float(np.median(np.abs(arr - median)))
            estimated_sigma = 1.4826 * mad

            # Минимальный порог шума — 1% от диапазона
            min_sigma = max(1e-4, (self.max_allowed - self.min_allowed) * 0.01)
            self._sigma_residual = max(estimated_sigma, min_sigma)
        except Exception:  # noqa: BLE001
            self._sigma_residual = 1.0

    def _get_anomaly_threshold(self, dt_sec: float) -> float:
        """
        Вычислить порог аномалии с учётом дефицита данных.

        При дефиците данных доверительный интервал расширяется:
        σ_прогноза = σ_noise · √(1 + dt / τ_корр)

        Args:
            dt_sec: Время с предыдущей точки в секундах.

        Returns:
            Порог аномалии.
        """
        # Базовый порог: K · σ_noise
        k = self._config.sigma_factor * (1.0 + self._config.noise_tolerance)

        # Расширение доверительного интервала при дефиците данных
        tau_corr = self._config.tau_corr
        expansion_factor = np.sqrt(1.0 + max(0.0, dt_sec) / tau_corr)

        threshold = k * self._sigma_residual * expansion_factor

        return threshold

    def _check_anomaly(self, time_ms: int, value: float,
                       residual: float, threshold: float) -> list[DetectionResult]:
        """
        Проверить аномалию с подтверждением временем (time-to-live).

        Args:
            time_ms: Текущее логическое время.
            value: Текущее значение сигнала.
            residual: Остаток прогноза.
            threshold: Порог аномалии.

        Returns:
            Список обнаружений аномалий.
        """
        results: list[DetectionResult] = []

        # Проверяем, превышает ли остаток порог
        is_exceeding = abs(residual) > threshold

        if is_exceeding:
            self._anomaly_ttl_counter += 1
        else:
            # Остаток в норме — сбрасываем счётчик и состояние
            self._anomaly_ttl_counter = 0
            self._anomaly_active = False
            return results

        # Проверяем кулдаун (не сообщаем повторно сразу после обнаружения)
        if self._anomaly_cooldown_points > 0:
            return results

        # Проверяем, что аномалия подтверждена достаточным числом точек
        if self._anomaly_ttl_counter < self.ANOMALY_TTL_REQUIRED:
            return results

        # Аномалия подтверждена — проверяем дедупликацию
        if self._anomaly_active:
            # Уже сообщали об этой аномалии — не повторяем
            return results

        # Фиксируем аномалию
        self._anomaly_active = True
        self._last_anomaly_time_ms = time_ms
        self._anomaly_cooldown_points = self.ANOMALY_TTL_REQUIRED * 2

        direction = "выброс" if residual > 0 else "провал"

        results.append(DetectionResult(
            time_ms=time_ms,
            detection_type=DetectionType.STATISTICAL,
            description=(
                f"Аномалия ({direction}): остаток {residual:+.4f} "
                f"превысил порог {threshold:.4f} "
                f"(K={self._config.sigma_factor:.1f}, "
                f"σ={self._sigma_residual:.4f}, "
                f"TTL={self._anomaly_ttl_counter})"
            ),
            value=value,
            metadata={
                "residual": residual,
                "threshold": threshold,
                "sigma_residual": self._sigma_residual,
                "ttl_confirmed": self._anomaly_ttl_counter,
                "direction": direction,
            }
        ))

        logger.debug(
            f"Аномалия обнаружена: остаток={residual:+.4f}, "
            f"порог={threshold:.4f}, TTL={self._anomaly_ttl_counter}."
        )

        return results

    def reset(self) -> None:
        """Сброс состояния детектора."""
        self._residuals.clear()
        self._last_time_ms = None
        self._level = None
        self._slope = 0.0
        self._sigma_residual = 1.0
        self._anomaly_ttl_counter = 0
        self._anomaly_active = False
        self._last_anomaly_time_ms = None
        self._anomaly_cooldown_points = 0
        logger.debug("SpikeDetector сброшен.")

    def get_state(self) -> dict:
        """
        Получить текущее состояние детектора для отладки и визуализации.

        Returns:
            Словарь с текущими параметрами.
        """
        return {
            "level": self._level,
            "slope": self._slope,
            "sigma_residual": self._sigma_residual,
            "anomaly_ttl_counter": self._anomaly_ttl_counter,
            "anomaly_active": self._anomaly_active,
            "residual_buffer_size": len(self._residuals),
        }
