"""
analytics/detector.py

Главный фасад модуля обнаружения аномалий.
Координирует работу препроцессора и трёх специализированных детекторов:
- TrendDetector (модель Хольта) — обнаружение медленных трендов.
- SpikeDetector (остатки прогноза) — обнаружение резких аномалий.
- DeviationDetector (CUSUM) — обнаружение устойчивых смещений уровня.

Для обратной совместимости реэкспортирует типы данных из `detector_types`:
`DetectionType`, `DetectionResult`, `DetectorConfig`.

Пороговые проверки (выход за `min_allowed`/`max_allowed`) выполняются
в фасаде по сырому значению сигнала, тогда как статистические детекторы
работают с информативным параметром, извлечённым препроцессором.
"""

import logging
from typing import Any

from analytics.anomaly_detector import SpikeDetector
from analytics.detector_types import (
    DetectionResult,
    DetectionType,
    DetectorConfig,
    DetectorKind,
)
from analytics.deviation_detector import DeviationDetector
from analytics.signal_preprocessor import SignalPreprocessor
from analytics.trend_detector import TrendDetector

logger = logging.getLogger(__name__)

# Реэкспорт для обратной совместимости
__all__ = [
    "AnomalyDetector",
    "DetectionResult",
    "DetectionType",
    "DetectorConfig",
    "DetectorKind",
]


class AnomalyDetector:
    """
    Главный фасад детектора аномалий.

    Координирует работу препроцессора (извлечение информативного параметра)
    и трёх специализированных детекторов (тренд, аномалия, отклонение).
    Пороговые проверки выполняются по сырому значению сигнала.

    Интерфейс полностью совместим со старой версией:
    `__init__(min_allowed, max_allowed, config)`, `process(time_ms, value)`,
    `set_config(config)`, `get_config()`, `reset()`.

    Attributes:
        min_allowed: Минимально допустимое значение сигнала.
        max_allowed: Максимально допустимое значение сигнала.
    """

    def __init__(self, min_allowed: float, max_allowed: float,
                 config: DetectorConfig | None = None) -> None:
        """
        Инициализация фасада детектора аномалий.

        Args:
            min_allowed: Минимально допустимое значение сигнала.
            max_allowed: Максимально допустимое значение сигнала.
            config: Конфигурация детектора. Если None — используется по умолчанию.
        """
        self.min_allowed = float(min_allowed)
        self.max_allowed = float(max_allowed)
        self._config = config if config is not None else DetectorConfig()

        # Состояние пороговых проверок
        self._threshold_state: str = "normal"

        # Препроцессор (извлечение информативного параметра)
        self._preprocessor = SignalPreprocessor(
            signal_type=self._config.signal_type,
            window_size=self._config.preprocessor_window,
        )

        # Специализированные детекторы
        self._trend_detector = TrendDetector(
            self.min_allowed, self.max_allowed, self._config
        )
        self._spike_detector = SpikeDetector(
            self.min_allowed, self.max_allowed, self._config
        )
        self._deviation_detector = DeviationDetector(
            self.min_allowed, self.max_allowed, self._config
        )

        active = self._config.get_active_detectors()
        logger.info(
            f"AnomalyDetector инициализирован. "
            f"Тип сигнала: {self._config.signal_type}, "
            f"активные детекторы: {active}, "
            f"окно препроцессора: {self._config.preprocessor_window}."
        )

    def set_config(self, config: DetectorConfig) -> None:
        """
        Обновить конфигурацию фасада и всех детекторов.

        Пересоздаёт препроцессор с новым типом сигнала и обновляет
        конфигурацию всех специализированных детекторов.

        Args:
            config: Новая конфигурация детектора.
        """
        try:
            self._config = config

            # Пересоздаём препроцессор с новым типом сигнала
            self._preprocessor = SignalPreprocessor(
                signal_type=config.signal_type,
                window_size=config.preprocessor_window,
            )

            # Обновляем конфигурацию детекторов
            self._trend_detector.set_config(config)
            self._spike_detector.set_config(config)
            self._deviation_detector.set_config(config)

            # Сбрасываем состояние
            self.reset()

            active = config.get_active_detectors()
            logger.info(
                f"Конфигурация AnomalyDetector обновлена. "
                f"Тип сигнала: {config.signal_type}, "
                f"активные детекторы: {active}."
            )
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обновления конфигурации AnomalyDetector: {e}")

    def get_config(self) -> DetectorConfig:
        """Возвращает текущую конфигурацию детектора."""
        return self._config

    def process(self, time_ms: int, value: float) -> list[DetectionResult]:
        """
        Обработать новую точку сигнала.

        Выполняет пороговые проверки по сырому значению, затем
        извлекает информативный параметр через препроцессор
        и передаёт его активным детекторам.

        Args:
            time_ms: Логическое время в миллисекундах.
            value: Сырое значение сигнала.

        Returns:
            Список всех обнаружений от всех активных детекторов.
        """
        results: list[DetectionResult] = []
        try:
            # Пороговые проверки по сырому значению
            results.extend(self._check_thresholds(time_ms, value))

            # Препроцессинг: извлечение информативного параметра
            informative_value = self._preprocessor.process(time_ms, value)
            if informative_value is None:
                # Недостаточно данных или точка на фронте — пропускаем детекторы
                return results

            # Определяем активные детекторы для текущего типа сигнала
            active = self._config.get_active_detectors()

            # Передаём информативный параметр активным детекторам
            if "trend" in active:
                results.extend(
                    self._trend_detector.process(time_ms, informative_value)
                )
            if "anomaly" in active:
                results.extend(
                    self._spike_detector.process(time_ms, informative_value)
                )
            if "deviation" in active:
                results.extend(
                    self._deviation_detector.process(time_ms, informative_value)
                )

        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обработки точки в {time_ms} мс: {e}")

        return results

    def _check_thresholds(self, time_ms: int, value: float) -> list[DetectionResult]:
        """
        Пороговые проверки по сырому значению сигнала.

        Фиксирует выход за допустимые пределы с гистерезисом
        (не повторяет обнаружение, пока сигнал не вернётся в норму).

        Args:
            time_ms: Логическое время в миллисекундах.
            value: Сырое значение сигнала.

        Returns:
            Список пороговых обнаружений (0 или 1 элемент).
        """
        results: list[DetectionResult] = []

        if value < self.min_allowed and self._threshold_state != "below_min":
            results.append(DetectionResult(
                time_ms=time_ms,
                detection_type=DetectionType.THRESHOLD,
                description=(
                    f"Ниже минимума: {value:.4f} < {self.min_allowed:.4f}"
                ),
                value=value,
            ))
            self._threshold_state = "below_min"
        elif value > self.max_allowed and self._threshold_state != "above_max":
            results.append(DetectionResult(
                time_ms=time_ms,
                detection_type=DetectionType.THRESHOLD,
                description=(
                    f"Выше максимума: {value:.4f} > {self.max_allowed:.4f}"
                ),
                value=value,
            ))
            self._threshold_state = "above_max"
        elif self.min_allowed <= value <= self.max_allowed:
            self._threshold_state = "normal"

        return results

    def reset(self) -> None:
        """Сброс состояния фасада и всех детекторов."""
        self._threshold_state = "normal"
        self._preprocessor.reset()
        self._trend_detector.reset()
        self._spike_detector.reset()
        self._deviation_detector.reset()
        logger.debug("AnomalyDetector сброшен.")

    def get_active_detectors_info(self) -> dict[str, Any]:
        """
        Получить информацию об активных детекторах для UI.

        Возвращает отображаемые названия и описания всех активных
        детекторов для текущего типа сигнала.

        Returns:
            Словарь с ключами: "active", "display_names", "explanations", "state".
        """
        try:
            active = self._config.get_active_detectors()
            display_names = self._config.get_detector_display_names()
            explanations = self._config.get_model_explanations()

            return {
                "active": active,
                "display_names": display_names,
                "explanations": explanations,
                "state": {
                    "trend": self._trend_detector.get_state(),
                    "anomaly": self._spike_detector.get_state(),
                    "deviation": self._deviation_detector.get_state(),
                    "preprocessor": self._preprocessor.get_state(),
                },
            }
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка получения информации о детекторах: {e}")
            return {
                "active": [],
                "display_names": {},
                "explanations": {},
                "state": {},
            }
