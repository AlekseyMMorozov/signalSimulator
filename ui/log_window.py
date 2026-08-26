"""
ui/log_window.py

Отдельное окно журнала событий симуляции.
Отображает записи журнала в виде текстового лога в реальном времени,
поддерживает фильтрацию по типу события, графику и времени,
а также автоматическую прокрутку к последним записям.
Окно открывается и закрывается из главного окна через координатор.
"""

import logging
from typing import List, Optional, Tuple

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.event_log import EventLog, EventRecord, EventType


logger = logging.getLogger(__name__)


def format_time_ms(time_ms: int) -> str:
    """
    Форматировать время в миллисекундах в строку ЧЧ:ММ:СС.мс.

    Args:
        time_ms: Время в миллисекундах.

    Returns:
        str: Отформатированное время (например, "00:05:23.456").
    """
    try:
        total_seconds = time_ms // 1000
        ms = time_ms % 1000
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{ms:03d}"
    except Exception as e:
        logger.error(f"Ошибка форматирования времени {time_ms}: {e}")
        return "00:00:00.000"


class LogWindow(QMainWindow):
    """
    Окно журнала событий симуляции.

    Отображает записи журнала в виде текстового лога (по одной строке на запись).
    Подписывается на сигнал `EventLog.event_added` для автоматического
    отображения новых записей. Поддерживает фильтрацию по типу события,
    графику и диапазону времени, а также автопрокрутку.

    Формат строки лога: `ЧЧ:ММ:СС.мс | ТИП_СОБЫТИЯ | график | Описание`
    """

    def __init__(self, event_log: EventLog, parent: Optional[QWidget] = None) -> None:
        """
        Инициализация окна журнала.

        Args:
            event_log: Журнал событий (источник записей).
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setWindowTitle("Журнал событий")
        self.setMinimumSize(600, 400)

        self._event_log = event_log
        self._records: List[EventRecord] = []

        try:
            # Загрузка существующих записей журнала
            self._records = self._event_log.get_all()
            # Подписка на новые записи
            self._event_log.event_added.connect(self._on_event_added)

            self._init_ui()
            self._apply_filter()
            logger.info(f"Окно журнала инициализировано. Записей: {len(self._records)}.")
        except Exception as e:
            logger.error(f"Ошибка инициализации окна журнала: {e}")
            raise

    def _init_ui(self) -> None:
        """Создание интерфейса окна журнала."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        # --- Панель фильтрации ---
        filter_layout = QHBoxLayout()

        # Фильтр по типу события
        filter_layout.addWidget(QLabel("Тип:"))
        self._type_combo = QComboBox()
        self._type_combo.addItem("Все типы")
        for event_type in EventType:
            self._type_combo.addItem(event_type.name)
        filter_layout.addWidget(self._type_combo)

        # Фильтр по графику
        filter_layout.addWidget(QLabel("График:"))
        self._plot_edit = QLineEdit()
        self._plot_edit.setPlaceholderText("Фильтр по графику")
        filter_layout.addWidget(self._plot_edit)

        # Фильтр по времени: от
        filter_layout.addWidget(QLabel("От (мс):"))
        self._start_edit = QLineEdit()
        self._start_edit.setPlaceholderText("0")
        self._start_edit.setMaximumWidth(100)
        filter_layout.addWidget(self._start_edit)

        # Фильтр по времени: до
        filter_layout.addWidget(QLabel("До (мс):"))
        self._end_edit = QLineEdit()
        self._end_edit.setPlaceholderText("∞")
        self._end_edit.setMaximumWidth(100)
        filter_layout.addWidget(self._end_edit)

        layout.addLayout(filter_layout)

        # --- Область текстового лога ---
        self._log_view = QPlainTextEdit()
        self._log_view.setReadOnly(True)
        self._log_view.setStyleSheet("font-family: Consolas, monospace; font-size: 12px;")
        layout.addWidget(self._log_view, stretch=1)

        # --- Нижняя панель: автопрокрутка и счётчик ---
        bottom_layout = QHBoxLayout()

        self._autoscroll_check = QCheckBox("Автопрокрутка")
        self._autoscroll_check.setChecked(True)
        bottom_layout.addWidget(self._autoscroll_check)

        bottom_layout.addStretch(1)

        self._count_label = QLabel("Записей: 0")
        bottom_layout.addWidget(self._count_label)

        layout.addLayout(bottom_layout)

        # --- Подключение сигналов фильтрации ---
        self._type_combo.currentIndexChanged.connect(self._apply_filter)
        self._plot_edit.textChanged.connect(self._apply_filter)
        self._start_edit.editingFinished.connect(self._apply_filter)
        self._end_edit.editingFinished.connect(self._apply_filter)

        logger.debug("Интерфейс окна журнала создан.")

    # ------------------------------------------------------------------
    # Внутренние методы
    # ------------------------------------------------------------------

    def _on_event_added(self, record: EventRecord) -> None:
        """
        Обработчик новой записи журнала (сигнал `event_added`).

        Добавляет запись в список и отображает, если она подходит под фильтр.

        Args:
            record: Новая запись журнала.
        """
        try:
            self._records.append(record)
            type_filter, plot_filter, start_ms, end_ms = self._get_filter_params()
            if self._matches_filter(record, type_filter, plot_filter, start_ms, end_ms):
                self._append_record_to_view(record)
                self._update_count()
                if self._autoscroll_check.isChecked():
                    self._scroll_to_bottom()
        except Exception as e:
            logger.error(f"Ошибка обработки новой записи журнала: {e}")

    def _apply_filter(self) -> None:
        """Применить текущий фильтр и перерисовать лог."""
        try:
            type_filter, plot_filter, start_ms, end_ms = self._get_filter_params()

            # Очищаем лог и добавляем подходящие записи
            self._log_view.clear()
            for record in self._records:
                if self._matches_filter(record, type_filter, plot_filter, start_ms, end_ms):
                    self._append_record_to_view(record)

            self._update_count()
            if self._autoscroll_check.isChecked():
                self._scroll_to_bottom()
            logger.debug("Фильтр журнала применён.")
        except Exception as e:
            logger.error(f"Ошибка применения фильтра журнала: {e}")

    def _get_filter_params(self) -> Tuple[str, str, Optional[int], Optional[int]]:
        """
        Получить текущие параметры фильтра из элементов интерфейса.

        Returns:
            Кортеж (тип события или "Все типы", подстрока графика, время от, время до).
        """
        try:
            type_filter = self._type_combo.currentText()
            plot_filter = self._plot_edit.text().strip()
            start_ms = self._parse_time_ms(self._start_edit.text())
            end_ms = self._parse_time_ms(self._end_edit.text())
            return type_filter, plot_filter, start_ms, end_ms
        except Exception as e:
            logger.error(f"Ошибка получения параметров фильтра: {e}")
            return "Все типы", "", None, None

    def _parse_time_ms(self, text: str) -> Optional[int]:
        """
        Разобрать текст поля времени в миллисекунды.

        Пустая строка означает отсутствие ограничения.

        Args:
            text: Текст из поля ввода.

        Returns:
            int или None, если пусто или некорректно.
        """
        text = text.strip()
        if not text:
            return None
        try:
            return int(text)
        except ValueError:
            logger.warning(f"Некорректное значение времени: '{text}'. Игнорируется.")
            return None

    def _matches_filter(
        self,
        record: EventRecord,
        type_filter: str,
        plot_filter: str,
        start_ms: Optional[int],
        end_ms: Optional[int]
    ) -> bool:
        """
        Проверить, подходит ли запись под текущий фильтр.

        Args:
            record: Запись журнала.
            type_filter: Тип события или "Все типы".
            plot_filter: Подстрока для фильтрации по графику.
            start_ms: Нижняя граница времени (или None).
            end_ms: Верхняя граница времени (или None).

        Returns:
            bool: Подходит ли запись под фильтр.
        """
        try:
            # Фильтр по типу события
            if type_filter != "Все типы" and record.event_type.name != type_filter:
                return False
            # Фильтр по графику (подстрока)
            if plot_filter:
                plot_id = record.plot_id if record.plot_id else ""
                if plot_filter.lower() not in plot_id.lower():
                    return False
            # Фильтр по времени
            if start_ms is not None and record.time_ms < start_ms:
                return False
            if end_ms is not None and record.time_ms > end_ms:
                return False
            return True
        except Exception as e:
            logger.error(f"Ошибка проверки фильтра для записи: {e}")
            return True

    def _append_record_to_view(self, record: EventRecord) -> None:
        """
        Добавить запись в текстовый лог.

        Формат: `ЧЧ:ММ:СС.мс | ТИП_СОБЫТИЯ | график | Описание`

        Args:
            record: Запись журнала.
        """
        try:
            time_str = format_time_ms(record.time_ms)
            plot_str = record.plot_id if record.plot_id else "—"
            line = f"{time_str} | {record.event_type.name} | {plot_str} | {record.description}"
            self._log_view.appendPlainText(line)
        except Exception as e:
            logger.error(f"Ошибка добавления записи в лог: {e}")

    def _update_count(self) -> None:
        """Обновить счётчик записей с учётом фильтра."""
        try:
            total = len(self._records)
            visible = self._log_view.blockCount()
            self._count_label.setText(f"Записей: {visible} из {total}")
        except Exception as e:
            logger.error(f"Ошибка обновления счётчика записей: {e}")

    def _scroll_to_bottom(self) -> None:
        """Прокрутить лог к последней записи."""
        try:
            scrollbar = self._log_view.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
        except Exception as e:
            logger.error(f"Ошибка автопрокрутки лога: {e}")

    def closeEvent(self, event) -> None:
        """Обработка закрытия окна журнала."""
        try:
            logger.info("Окно журнала закрывается.")
        except Exception as e:
            logger.error(f"Ошибка при закрытии окна журнала: {e}")
        super().closeEvent(event)

