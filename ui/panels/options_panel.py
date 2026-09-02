"""
ui/panels/options_panel.py

Панель дополнительных настроек главного окна.
Содержит два чекбокса:
- Показывать скрытые метки неисправностей (управляет видимостью меток на графиках).
- Показать журнал событий (дублирует действие из меню для удобства).

Эмитирует сигналы для координатора при изменении состояния пользователем.
Программное изменение состояния (для синхронизации с меню) не вызывает
повторной эмиссии сигналов, что предотвращает циклические обновления.
"""

import logging

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QWidget,
)

logger = logging.getLogger(__name__)


class OptionsPanel(QWidget):
    """
    Панель дополнительных настроек главного окна.

    Signals:
        hidden_markers_toggled(bool): Режим скрытых меток включён/выключен.
        journal_toggled(bool): Журнал событий открыт/закрыт.
    """

    hidden_markers_toggled = pyqtSignal(bool)
    journal_toggled = pyqtSignal(bool)

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Инициализация панели дополнительных настроек.

        Args:
            parent: Родительский виджет.
        """
        super().__init__(parent)

        try:
            self._init_ui()
            self._connect_signals()
            logger.debug("Панель дополнительных настроек инициализирована.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка инициализации панели дополнительных настроек: {e}")
            raise

    def _init_ui(self) -> None:
        """Создание интерфейса панели дополнительных настроек."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 5)
        layout.setSpacing(15)

        # Чекбокс скрытых меток
        self._chk_hidden_markers = QCheckBox("Показывать скрытые метки неисправностей")
        self._chk_hidden_markers.setChecked(False)
        self._chk_hidden_markers.setToolTip(
            "Включите для отображения скрытых меток неисправностей на графиках."
        )
        layout.addWidget(self._chk_hidden_markers)

        layout.addStretch(1)

        # Чекбокс журнала событий (дублирует действие из меню для удобства)
        self._chk_journal = QCheckBox("Показать журнал событий")
        self._chk_journal.setChecked(False)
        self._chk_journal.setToolTip("Открыть или скрыть окно журнала событий.")
        layout.addWidget(self._chk_journal)

    def _connect_signals(self) -> None:
        """Подключение внутренних сигналов панели."""
        self._chk_hidden_markers.stateChanged.connect(self._on_hidden_markers_changed)
        self._chk_journal.toggled.connect(self._on_journal_changed)

    def set_hidden_markers_state(self, checked: bool) -> None:
        """
        Программно установить состояние чекбокса скрытых меток.

        Не вызывает эмиссию сигнала `hidden_markers_toggled`,
        чтобы избежать циклических обновлений при синхронизации.

        Args:
            checked: True — включить, False — выключить.
        """
        try:
            self._chk_hidden_markers.blockSignals(True)
            self._chk_hidden_markers.setChecked(checked)
            self._chk_hidden_markers.blockSignals(False)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка программной установки состояния скрытых меток: {e}")
            self._chk_hidden_markers.blockSignals(False)

    def set_journal_state(self, checked: bool) -> None:
        """
        Программно установить состояние чекбокса журнала событий.

        Не вызывает эмиссию сигнала `journal_toggled`,
        чтобы избежать циклических обновлений при синхронизации с меню.

        Args:
            checked: True — открыть журнал, False — закрыть.
        """
        try:
            self._chk_journal.blockSignals(True)
            self._chk_journal.setChecked(checked)
            self._chk_journal.blockSignals(False)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка программной установки состояния журнала: {e}")
            self._chk_journal.blockSignals(False)

    def _on_hidden_markers_changed(self, state: int) -> None:
        """Обработка изменения состояния чекбокса скрытых меток пользователем."""
        try:
            checked = bool(state)
            self.hidden_markers_toggled.emit(checked)
            state_str = "включён" if checked else "выключен"
            logger.info(f"Режим скрытых меток {state_str} (пользовательское действие).")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обработки изменения скрытых меток: {e}")

    def _on_journal_changed(self, checked: bool) -> None:
        """Обработка изменения состояния чекбокса журнала пользователем."""
        try:
            self.journal_toggled.emit(checked)
            state_str = "открыт" if checked else "закрыт"
            logger.info(f"Журнал событий {state_str} (пользовательское действие).")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обработки изменения состояния журнала: {e}")
