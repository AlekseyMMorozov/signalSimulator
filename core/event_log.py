"""
core/event_log.py

Центральный журнал событий симуляции.
Фиксирует все значимые события с логическим временем и используется
как источник данных для отдельного окна логов и для аналитики.
"""

import logging
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any

from PyQt6.QtCore import QObject, pyqtSignal

logger = logging.getLogger(__name__)


class EventType(Enum):
    """Типы событий симуляции."""

    # Симуляция
    SIMULATION_START = auto()
    SIMULATION_STOP = auto()
    SIMULATION_RESET = auto()
    SPEED_CHANGE = auto()

    # Графики
    PLOT_CREATED = auto()
    PLOT_REMOVED = auto()

    # Неисправности
    FAULT_INJECTED = auto()
    FAULT_ACTIVATED = auto()
    FAULT_DEACTIVATED = auto()

    # Обнаружения
    OPERATOR_DETECTION = auto()
    DETECTOR_DETECTION = auto()

    # Контроль
    LIMIT_EXCEEDED = auto()

    # Конфигурация
    CONFIG_SAVED = auto()
    CONFIG_LOADED = auto()


@dataclass
class EventRecord:
    """
    Запись события в журнале.

    Содержит логическое время, тип события, связанный график,
    текстовое описание и произвольные метаданные для аналитики.
    """
    time_ms: int
    event_type: EventType
    description: str
    plot_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        """Строковое представление записи для отображения в логах."""
        plot_info = f" [{self.plot_id}]" if self.plot_id else ""
        return f"{self.time_ms} мс | {self.event_type.name}{plot_info} | {self.description}"


class EventLog(QObject):
    """
    Журнал событий симуляции.

    Хранит все записи за сессию и испускает сигнал `event_added`
    при добавлении новой записи. Окно логов подписывается на сигнал
    для автоматического обновления. Аналитика читает записи через
    методы фильтрации.
    """

    # Сигнал уведомления о новой записи в журнале
    event_added = pyqtSignal(object)

    def __init__(self, parent: QObject | None = None) -> None:
        """
        Инициализация журнала событий.

        Args:
            parent: Родительский QObject для управления временем жизни.
        """
        super().__init__(parent)
        self._records: list[EventRecord] = []
        logger.info("EventLog инициализирован.")

    def add(
        self,
        time_ms: int,
        event_type: EventType,
        description: str,
        plot_id: str | None = None,
        metadata: dict[str, Any] | None = None
    ) -> EventRecord:
        """
        Добавить запись события в журнал.

        Создаёт запись, сохраняет её и испускает сигнал `event_added`.

        Args:
            time_ms: Логическое время события в миллисекундах.
            event_type: Тип события.
            description: Текстовое описание события.
            plot_id: Идентификатор связанного графика (опционально).
            metadata: Дополнительные данные для аналитики (опционально).

        Returns:
            EventRecord: Созданная запись.
        """
        try:
            record = EventRecord(
                time_ms=time_ms,
                event_type=event_type,
                description=description,
                plot_id=plot_id,
                metadata=metadata if metadata is not None else {},
            )
            self._records.append(record)
            logger.debug(f"Событие добавлено: {record}")
            self.event_added.emit(record)
            return record
        except Exception as e:
            logger.error(f"Ошибка добавления события в журнал: {e}")
            # Возвращаем запись даже при ошибке сигнала, чтобы не терять данные
            fallback = EventRecord(
                time_ms=time_ms,
                event_type=event_type,
                description=description,
                plot_id=plot_id,
                metadata=metadata if metadata is not None else {},
            )
            return fallback

    def get_records(
        self,
        event_type: EventType | None = None,
        plot_id: str | None = None,
        start_ms: int | None = None,
        end_ms: int | None = None
    ) -> list[EventRecord]:
        """
        Получить записи журнала с фильтрацией.

        Все параметры опциональны. При отсутствии параметра фильтр
        по нему не применяется.

        Args:
            event_type: Тип события (опционально).
            plot_id: Идентификатор графика (опционально).
            start_ms: Нижняя граница времени в мс (опционально).
            end_ms: Верхняя граница времени в мс (опционально).

        Returns:
            Список подходящих записей.
        """
        try:
            result = self._records
            if event_type is not None:
                result = [r for r in result if r.event_type == event_type]
            if plot_id is not None:
                result = [r for r in result if r.plot_id == plot_id]
            if start_ms is not None:
                result = [r for r in result if r.time_ms >= start_ms]
            if end_ms is not None:
                result = [r for r in result if r.time_ms <= end_ms]
            logger.debug(f"Фильтрация записей: возвращено {len(result)} из {len(self._records)}.")
            return result
        except Exception as e:
            logger.error(f"Ошибка фильтрации записей журнала: {e}")
            return []

    def get_all(self) -> list[EventRecord]:
        """
        Получить все записи журнала.

        Returns:
            Список всех записей.
        """
        logger.debug(f"Запрошены все записи журнала: {len(self._records)}.")
        return list(self._records)

    def get_count(self) -> int:
        """
        Получить количество записей в журнале.

        Returns:
            Количество записей.
        """
        return len(self._records)

    def clear(self) -> None:
        """Очистить журнал событий."""
        try:
            count = len(self._records)
            self._records.clear()
            logger.info(f"Журнал событий очищен. Удалено записей: {count}.")
        except Exception as e:
            logger.error(f"Ошибка очистки журнала: {e}")
