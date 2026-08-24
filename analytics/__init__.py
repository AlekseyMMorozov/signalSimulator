"""
analytics/__init__.py
Инициализация пакета `analytics` — аналитика и обнаружение аномалий.
Содержит модули детектирования и подсчёта метрик.
"""

from analytics.detector import (
    AnomalyDetector,
    DetectorConfig,
    DetectionResult,
    DetectionType,
)
from analytics.metrics import (
    FaultAnalysisRecord,
    MetricsCalculator,
    MetricsSummary,
)

__all__ = [
    "AnomalyDetector",
    "DetectorConfig",
    "DetectionResult",
    "DetectionType",
    "FaultAnalysisRecord",
    "MetricsCalculator",
    "MetricsSummary",
]
