"""
analytics/detector_types.py

Типы данных и конфигурация для модуля обнаружения аномалий.
Выделено из detector.py для соблюдения принципа единой ответственности.

Поддерживает новую архитектуру с разделением ответственности:
- Препроцессор (извлечение информативного параметра)
- Детектор тренда (модель Хольта)
- Детектор аномалий (анализ остатков прогноза)
- Детектор отклонений (CUSUM)
"""

import logging
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

logger = logging.getLogger(__name__)


class DetectionType(Enum):
    """Типы обнаружений."""
    THRESHOLD = auto()
    STATISTICAL = auto()
    TREND = auto()


class DetectorKind(Enum):
    """Типы детекторов в новой архитектуре."""
    TREND = "trend"
    ANOMALY = "anomaly"
    DEVIATION = "deviation"


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
        return (
            f"[{self.detection_type.name}] {self.time_ms} мс: "
            f"{self.description} (значение: {self.value}){meta_str}"
        )

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
    """
    Конфигурация детектора, сериализуемая в словарь.

    Поддерживает как старую архитектуру (одна модель), так и новую
    (три независимых детектора). Для обратной совместимости старые
    поля сохранены, новые добавлены с дефолтными значениями.
    """

    # === Общие параметры ===
    window_size: int = 50
    sigma_factor: float = 3.0
    min_samples: int = 20
    signal_type: str = "unknown"
    signal_model: str = "auto"
    noise_tolerance: float = 0.0
    tau_corr: float = 10.0

    # === Параметры детектора тренда ===
    trend_threshold: float | None = None
    trend_auto_sigma: float = 3.0
    trend_ttl: int = 5

    # === Параметры детектора аномалий ===
    anomaly_ttl: int = 3

    # === Параметры детектора отклонений (CUSUM) ===
    cusum_drift_factor: float = 0.5
    cusum_threshold_factor: float = 4.0
    cusum_baseline_alpha: float = 0.05

    # === Параметры препроцессора ===
    preprocessor_window: int = 100

    # === Активные детекторы (None = автоопределение) ===
    active_detectors: list[str] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Сериализация конфигурации в словарь."""
        return {
            "window_size": self.window_size,
            "sigma_factor": self.sigma_factor,
            "trend_threshold": self.trend_threshold,
            "trend_auto_sigma": self.trend_auto_sigma,
            "trend_ttl": self.trend_ttl,
            "anomaly_ttl": self.anomaly_ttl,
            "cusum_drift_factor": self.cusum_drift_factor,
            "cusum_threshold_factor": self.cusum_threshold_factor,
            "cusum_baseline_alpha": self.cusum_baseline_alpha,
            "min_samples": self.min_samples,
            "signal_type": self.signal_type,
            "signal_model": self.signal_model,
            "noise_tolerance": self.noise_tolerance,
            "tau_corr": self.tau_corr,
            "preprocessor_window": self.preprocessor_window,
            "active_detectors": self.active_detectors,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DetectorConfig":
        """Десериализация конфигурации из словаря с обратной совместимостью."""
        try:
            defaults = cls()
            active_detectors = data.get("active_detectors", defaults.active_detectors)
            if active_detectors is not None and not isinstance(active_detectors, list):
                active_detectors = defaults.active_detectors

            return cls(
                window_size=int(data.get("window_size", defaults.window_size)),
                sigma_factor=float(data.get("sigma_factor", defaults.sigma_factor)),
                trend_threshold=data.get("trend_threshold", defaults.trend_threshold),
                trend_auto_sigma=float(data.get("trend_auto_sigma", defaults.trend_auto_sigma)),
                trend_ttl=int(data.get("trend_ttl", defaults.trend_ttl)),
                anomaly_ttl=int(data.get("anomaly_ttl", defaults.anomaly_ttl)),
                cusum_drift_factor=float(data.get("cusum_drift_factor", defaults.cusum_drift_factor)),
                cusum_threshold_factor=float(data.get("cusum_threshold_factor", defaults.cusum_threshold_factor)),
                cusum_baseline_alpha=float(data.get("cusum_baseline_alpha", defaults.cusum_baseline_alpha)),
                min_samples=int(data.get("min_samples", defaults.min_samples)),
                signal_type=str(data.get("signal_type", defaults.signal_type)),
                signal_model=str(data.get("signal_model", defaults.signal_model)),
                noise_tolerance=float(data.get("noise_tolerance", defaults.noise_tolerance)),
                tau_corr=float(data.get("tau_corr", defaults.tau_corr)),
                preprocessor_window=int(data.get("preprocessor_window", defaults.preprocessor_window)),
                active_detectors=active_detectors,
            )
        except (ValueError, TypeError) as e:
            logger.error(
                f"Ошибка парсинга конфигурации детектора: {e}. "
                f"Используются значения по умолчанию."
            )
            return cls()

    def get_active_detectors(self) -> list[str]:
        """
        Определить список активных детекторов для текущего типа сигнала.

        Если поле `active_detectors` задано явно — используется оно.
        Иначе применяется автоматическое определение по типу сигнала:
        - Для линейного/экспоненты тренд отключён (тренд — нормальное поведение)
        - Для шума тренд отключён (случайный сигнал)
        - Для остальных типов активны все три детектора

        Returns:
            Список названий активных детекторов: "trend", "anomaly", "deviation".
        """
        if self.active_detectors is not None:
            return list(self.active_detectors)

        stype = self.signal_type.lower()

        # Типы сигналов, для которых тренд — нормальное поведение
        no_trend_signals = {"linear", "exponential", "noise"}

        if stype in no_trend_signals:
            return ["anomaly", "deviation"]

        return ["trend", "anomaly", "deviation"]

    def get_model_explanations(self) -> dict[str, str]:
        """
        Возвращает описания всех активных детекторов для текущего типа сигнала.

        Используется в UI для отображения информации о моделях
        с пояснениями, почему они выбраны.

        Returns:
            Словарь {название_детектора: описание}.
        """
        active = self.get_active_detectors()
        stype = self.signal_type.lower()
        result: dict[str, str] = {}

        # === Описание детектора тренда ===
        if "trend" in active:
            trend_explanations = {
                "sine": (
                    "Детектор тренда (модель Хольта): анализирует изменение "
                    "амплитуды синусоиды через препроцессор. Обнаруживает "
                    "медленную деградацию или дрейф амплитуды."
                ),
                "sawtooth": (
                    "Детектор тренда (модель Хольта): анализирует изменение "
                    "наклона линейных участков пилы через препроцессор. "
                    "Обнаруживает деградацию скорости нарастания."
                ),
                "triangle": (
                    "Детектор тренда (модель Хольта): анализирует изменение "
                    "амплитуды треугольного сигнала через препроцессор."
                ),
                "square": (
                    "Детектор тренда (модель Хольта): анализирует дрейф "
                    "уровней плато меандра через препроцессор. Игнорирует фронты."
                ),
                "step": (
                    "Детектор тренда (модель Хольта): анализирует дрейф "
                    "уровней ступенек через препроцессор. Игнорирует переходы."
                ),
                "constant": (
                    "Детектор тренда (модель Хольта): обнаруживает медленный "
                    "дрейф постоянного значения — признак деградации источника."
                ),
                "composite": (
                    "Детектор тренда (модель Хольта): обнаруживает медленный "
                    "дрейф композитного сигнала."
                ),
                "default": (
                    "Детектор тренда (модель Хольта): двойное экспоненциальное "
                    "сглаживание для оценки уровня и наклона сигнала."
                ),
            }
            result["trend"] = trend_explanations.get(
                stype, trend_explanations["default"]
            )

        # === Описание детектора аномалий ===
        if "anomaly" in active:
            anomaly_explanations = {
                "sine": (
                    "Детектор аномалий (остатки прогноза): анализирует отклонение "
                    "амплитуды от прогнозируемого значения. Подтверждение временем "
                    "подавляет ложные срабатывания на шумовых всплесках."
                ),
                "sawtooth": (
                    "Детектор аномалий (остатки прогноза): анализирует отклонение "
                    "наклона пилы от прогноза. Игнорирует плановые сбросы."
                ),
                "triangle": (
                    "Детектор аномалий (остатки прогноза): анализирует отклонение "
                    "амплитуды треугольного сигнала от прогноза."
                ),
                "square": (
                    "Детектор аномалий (остатки прогноза): анализирует отклонение "
                    "значений на плато меандра от прогноза. Фронты игнорируются "
                    "препроцессором."
                ),
                "step": (
                    "Детектор аномалий (остатки прогноза): анализирует отклонение "
                    "значений на плато ступенек от прогноза. Переходы игнорируются."
                ),
                "linear": (
                    "Детектор аномалий (остатки прогноза): анализирует отклонение "
                    "линейного сигнала от ожидаемого тренда. Обнаруживает скачки."
                ),
                "exponential": (
                    "Детектор аномалий (остатки прогноза): анализирует отклонение "
                    "экспоненциального сигнала от ожидаемой кривой."
                ),
                "noise": (
                    "Детектор аномалий (остатки прогноза): обнаруживает аномальные "
                    "выбросы, превышающие естественный уровень шума."
                ),
                "constant": (
                    "Детектор аномалий (остатки прогноза): обнаруживает резкие "
                    "выбросы и провалы относительно постоянного уровня."
                ),
                "default": (
                    "Детектор аномалий (остатки прогноза): анализирует ошибку "
                    "прогнозирующего фильтра с подтверждением временем."
                ),
            }
            result["anomaly"] = anomaly_explanations.get(
                stype, anomaly_explanations["default"]
            )

        # === Описание детектора отклонений ===
        if "deviation" in active:
            deviation_explanations = {
                "sine": (
                    "Детектор отклонений (CUSUM): обнаруживает устойчивое "
                    "смещение амплитуды синусоиды. Накопление малых отклонений "
                    "позволяет выявить дрейф до того, как он станет критическим."
                ),
                "sawtooth": (
                    "Детектор отклонений (CUSUM): обнаруживает устойчивое "
                    "смещение наклона пилы относительно базового уровня."
                ),
                "triangle": (
                    "Детектор отклонений (CUSUM): обнаруживает устойчивое "
                    "смещение амплитуды треугольного сигнала."
                ),
                "square": (
                    "Детектор отклонений (CUSUM): обнаруживает смещение уровней "
                    "плато меандра. Идеален для выявления деградации источника "
                    "питания до выхода за допустимые пределы."
                ),
                "step": (
                    "Детектор отклонений (CUSUM): обнаруживает смещение уровней "
                    "ступенек. Накопление малых отклонений выявляет разладку."
                ),
                "linear": (
                    "Детектор отклонений (CUSUM): обнаруживает смещение уровня "
                    "линейного сигнала относительно ожидаемого тренда."
                ),
                "exponential": (
                    "Детектор отклонений (CUSUM): обнаруживает смещение уровня "
                    "экспоненциального сигнала относительно ожидаемой кривой."
                ),
                "noise": (
                    "Детектор отклонений (CUSUM): обнаруживает смещение среднего "
                    "уровня шума (например, из-за дрейфа смещения датчика)."
                ),
                "constant": (
                    "Детектор отклонений (CUSUM): обнаруживает устойчивое "
                    "смещение постоянного уровня — классический случай разладки."
                ),
                "default": (
                    "Детектор отклонений (CUSUM): кумулятивная сумма для "
                    "обнаружения устойчивого смещения уровня сигнала."
                ),
            }
            result["deviation"] = deviation_explanations.get(
                stype, deviation_explanations["default"]
            )

        return result

    def get_model_explanation(self) -> str:
        """
        Возвращает сводное описание активных детекторов (для обратной совместимости).

        Returns:
            Строка с описанием всех активных детекторов.
        """
        explanations = self.get_model_explanations()
        if not explanations:
            return "Детекторы не активны для данного типа сигнала."
        return "\n\n".join(explanations.values())

    def get_detector_display_names(self) -> dict[str, str]:
        """
        Возвращает отображаемые названия детекторов для UI.

        Returns:
            Словарь {ключ_детектора: отображаемое_название}.
        """
        return {
            "trend": "📈 Детектор тренда (модель Хольта)",
            "anomaly": "⚡ Детектор аномалий (остатки прогноза)",
            "deviation": "📊 Детектор отклонений (CUSUM)",
        }
