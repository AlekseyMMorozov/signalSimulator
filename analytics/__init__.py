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

__all__ = [
    "AnomalyDetector",
    "DetectorConfig",
    "DetectionResult",
    "DetectionType",
]
