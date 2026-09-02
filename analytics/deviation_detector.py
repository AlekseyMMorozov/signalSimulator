"""
analytics/deviation_detector.py

CUSUM-детектор смещения уровня (разладки).
Обнаруживает устойчивое смещение сигнала на новый уровень,
когда тренд может быть нулевым, но среднее значение изменилось.

Математическая основа (кумулятивная сумма):
    Целевое значение: μ₀ (адаптивная базовая линия)
    Допустимое смещение: δ (чувствительность)
    Порог: H = K · σ_noise

    Накопленные статистики:
        S_high = max(0, S_high + (x_t - μ₀) - δ)
        S_low  = max(0, S_low  + (μ₀ - x_t) - δ)

    Отклонение фиксируется, когда S_high > H или S_low > H.

Преимущество метода:
    CUSUM накапливает слабые отклонения по крупицам,
    а не ждёт одного большого выброса. Одиночный шумовой выброс
    быстро «затухает» в max(0, ...), а реальное смещение уровня
    растёт линейно и быстро превышает порог.

Поддерживает:
- Робастную оценку шума через MAD
- Адаптивную базовую линию (скользящая медиана)
- Автоматический сброс после обнаружения
- Кулдаун для подавления повторных срабатываний
"""

import logging
from collections import deque

import numpy as np

from analytics.detector_types import DetectionResult, DetectionType, DetectorConfig

logger = logging.getLogger(__name__)


class DeviationDetector:
    """
    CUSUM-детектор смещения уровня (разладки).

    Обнаруживает устойчивое смещение сигнала на новый уровень,
    накапливая малые отклонения от базовой линии. Одиночные
    шумовые выбросы не приводят к срабатыванию, тогда как
    реальное смещение уровня быстро превышает порог.

    Attributes:
        min_allowed: Минимально допустимое значение сигнала.
        max_allowed: Максимально допустимое значение сигнала.
    """

    # Размер окна для адаптивной базовой линии
    BASELINE_WINDOW_SIZE = 50

    # Коэффициент для допустимого смещения δ = DRIFT_FACTOR · σ
    DRIFT_FACTOR = 0.5

    # Коэффициент для порога H = THRESHOLD_FACTOR · σ
    THRESHOLD_FACTOR = 4.0

    # Кулдаун после обнаружения (в точках)
    COOLDOWN_POINTS = 10

    def __init__(self, min_allowed: float, max_allowed: float,
                 config: DetectorConfig | None = None) -> None:
        """
        Инициализация CUSUM-детектора смещения уровня.

        Args:
            min_allowed: Минимально допустимое значение сигнала.
            max_allowed: Максимально допустимое значение сигнала.
            config: Конфигурация детектора. Если None — используется по умолчанию.
        """
        self.min_allowed = float(min_allowed)
        self.max_allowed = float(max_allowed)
        self._config = config if config is not None else DetectorConfig()

        # Буферы для адаптивной базовой линии
        self._baseline_buffer: deque[float] = deque(
            maxlen=self.BASELINE_WINDOW_SIZE
        )

        # Базовая линия (целевое значение μ₀)
        self._baseline: float | None = None

        # Оценка шума через MAD
        self._sigma_noise: float = 1.0

        # Накопленные статистики CUSUM
        self._s_high: float = 0.0
        self._s_low: float = 0.0

        # Состояние обнаружения
        self._deviation_active: bool = False
        self._deviation_direction: str | None = None
        self._cooldown_counter: int = 0

        # Счётчик точек для инициализации
        self._points_processed: int = 0

        logger.info(
            f"DeviationDetector инициализирован. "
            f"Диапазон: [{self.min_allowed:.4f}, {self.max_allowed:.4f}], "
            f"дрейф: {self.DRIFT_FACTOR}, порог: {self.THRESHOLD_FACTOR}."
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
            logger.info("Конфигурация DeviationDetector обновлена.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обновления конфигурации DeviationDetector: {e}")

    def get_config(self) -> DetectorConfig:
        """Возвращает текущую конфигурацию детектора."""
        return self._config

    def process(self, time_ms: int, value: float) -> list[DetectionResult]:
        """
        Обработать новую точку и проверить наличие смещения уровня.

        Args:
            time_ms: Логическое время в миллисекундах.
            value: Значение сигнала (или информативный параметр от препроцессора).

        Returns:
            Список обнаружений (обычно 0 или 1 элемент).
        """
        results: list[DetectionResult] = []
        try:
            self._points_processed += 1

            # Инициализация базовой линии по первым точкам
            if self._baseline is None:
                self._baseline_buffer.append(value)
                if len(self._baseline_buffer) >= 10:
                    self._baseline = float(np.median(self._baseline_buffer))
                    self._update_sigma_noise()
                    logger.debug(
                        f"Базовая линия инициализирована: {self._baseline:.4f}"
                    )
                return results

            # Обновляем оценку шума
            self._update_sigma_noise()

            # Проверяем кулдаун
            if self._cooldown_counter > 0:
                self._cooldown_counter -= 1
                return results

            # Шаг CUSUM
            results.extend(self._cusum_step(time_ms, value))

            # Адаптация базовой линии, если отклонение не активно
            if not self._deviation_active:
                self._adapt_baseline(value)

        except Exception as e:  # noqa: BLE001
            logger.error(
                f"Ошибка обработки точки в DeviationDetector ({time_ms} мс): {e}"
            )

        return results

    def _update_sigma_noise(self) -> None:
        """Обновить робастную оценку шума через MAD по базовой линии."""
        try:
            if len(self._baseline_buffer) < 5:
                return

            arr = np.array(self._baseline_buffer, dtype=np.float64)
            median = float(np.median(arr))
            mad = float(np.median(np.abs(arr - median)))
            estimated_sigma = 1.4826 * mad

            # Минимальный порог шума — 1% от диапазона
            min_sigma = max(1e-4, (self.max_allowed - self.min_allowed) * 0.01)
            self._sigma_noise = max(estimated_sigma, min_sigma)
        except Exception:  # noqa: BLE001
            self._sigma_noise = 1.0

    def _cusum_step(self, time_ms: int, value: float) -> list[DetectionResult]:
        """
        Один шаг алгоритма CUSUM.

        Обновляет накопленные статистики S_high и S_low
        и проверяет превышение порога.

        Args:
            time_ms: Текущее логическое время.
            value: Текущее значение сигнала.

        Returns:
            Список обнаружений смещения уровня.
        """
        results: list[DetectionResult] = []

        if self._baseline is None:
            return results

        # Параметры CUSUM
        delta = self.DRIFT_FACTOR * self._sigma_noise
        threshold = self.THRESHOLD_FACTOR * self._sigma_noise

        # Обновляем накопленные статистики
        self._s_high = max(0.0, self._s_high + (value - self._baseline) - delta)
        self._s_low = max(0.0, self._s_low + (self._baseline - value) - delta)

        # Проверяем превышение порога
        if self._s_high > threshold:
            results.extend(
                self._report_deviation(
                    time_ms, value, "повышение", self._s_high, threshold
                )
            )
        elif self._s_low > threshold:
            results.extend(
                self._report_deviation(
                    time_ms, value, "понижение", self._s_low, threshold
                )
            )

        return results

    def _report_deviation(self, time_ms: int, value: float,
                          direction: str, statistic: float,
                          threshold: float) -> list[DetectionResult]:
        """
        Зафиксировать обнаруженное смещение уровня.

        Args:
            time_ms: Текущее логическое время.
            value: Текущее значение сигнала.
            direction: Направление смещения ("повышение" или "понижение").
            statistic: Текущее значение накопленной статистики.
            threshold: Порог срабатывания.

        Returns:
            Список обнаружений.
        """
        # Проверяем дедупликацию
        if self._deviation_active and self._deviation_direction == direction:
            return []

        # Фиксируем обнаружение
        self._deviation_active = True
        self._deviation_direction = direction
        self._cooldown_counter = self.COOLDOWN_POINTS

        # Сбрасываем накопленные статистики
        self._s_high = 0.0
        self._s_low = 0.0

        # Обновляем базовую линию на новый уровень
        self._baseline = value
        self._baseline_buffer.clear()
        self._baseline_buffer.append(value)

        dir_str = "повышение" if direction == "повышение" else "понижение"
        results = [DetectionResult(
            time_ms=time_ms,
            detection_type=DetectionType.STATISTICAL,
            description=(
                f"Смещение уровня ({dir_str}): сигнал устойчиво сместился "
                f"на новый уровень. Текущее значение: {value:.4f}, "
                f"статистика CUSUM: {statistic:.4f} > порог {threshold:.4f}."
            ),
            value=value,
            metadata={
                "direction": direction,
                "cusum_statistic": statistic,
                "threshold": threshold,
                "new_baseline": self._baseline,
                "sigma_noise": self._sigma_noise,
            }
        )]

        logger.info(
            f"Смещение уровня обнаружено ({dir_str}): "
            f"значение={value:.4f}, новая базовая линия={self._baseline:.4f}."
        )

        return results

    def _adapt_baseline(self, value: float) -> None:
        """
        Адаптация базовой линии при стабильном сигнале.

        Если отклонение не активно, обновляем базовую линию
        с использованием экспоненциального сглаживания.

        Args:
            value: Текущее значение сигнала.
        """
        if self._baseline is None:
            self._baseline = value
            return

        # Коэффициент сглаживания для адаптации базовой линии
        alpha = 0.05
        self._baseline = alpha * value + (1.0 - alpha) * self._baseline

        # Добавляем в буфер для оценки шума
        self._baseline_buffer.append(value)

    def reset(self) -> None:
        """Сброс состояния детектора."""
        self._baseline_buffer.clear()
        self._baseline = None
        self._sigma_noise = 1.0
        self._s_high = 0.0
        self._s_low = 0.0
        self._deviation_active = False
        self._deviation_direction = None
        self._cooldown_counter = 0
        self._points_processed = 0
        logger.debug("DeviationDetector сброшен.")

    def get_state(self) -> dict:
        """
        Получить текущее состояние детектора для отладки и визуализации.

        Returns:
            Словарь с текущими параметрами.
        """
        return {
            "baseline": self._baseline,
            "sigma_noise": self._sigma_noise,
            "s_high": self._s_high,
            "s_low": self._s_low,
            "deviation_active": self._deviation_active,
            "deviation_direction": self._deviation_direction,
            "cooldown_counter": self._cooldown_counter,
            "points_processed": self._points_processed,
            "baseline_buffer_size": len(self._baseline_buffer),
        }
