"""
analytics/__init__.py
Инициализация пакета `analytics` — аналитика и обнаружение аномалий.
Содержит модули детектирования и подсчёта метрик.
"""

from analytics.detector import (
    AnomalyDetector,
    DetectionResult,
    DetectionType,
    DetectorConfig,
)
from analytics.metrics import (
    FaultAnalysisRecord,
    MetricsCalculator,
    MetricsSummary,
)

__all__ = [
    "AnomalyDetector",
    "DetectionResult",
    "DetectionType",
    "DetectorConfig",
    "FaultAnalysisRecord",
    "MetricsCalculator",
    "MetricsSummary",
]
