"""
core/__init__.py

Инициализация пакета `core` — ядро системы симуляции.
Содержит модули управления временем, конфигурациями и журналом событий.
"""

from core.clock import GlobalClock
from core.config import ConfigManager, ConfigError
from core.event_log import EventLog, EventRecord, EventType


__all__ = [
    "GlobalClock",
    "ConfigManager",
    "ConfigError",
    "EventLog",
    "EventRecord",
    "EventType",
]
