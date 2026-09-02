"""
ui/panels/time_panel.py

Панель управления временем симуляции.
Содержит кнопки запуска/остановки/сброса, выпадающий список скорости
и крупную метку текущего логического времени.

Подписывается на сигнал `time_updated` глобальных часов для обновления
отображения времени и эмитирует сигналы для координатора.
"""

import logging

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)

from core.clock import GlobalClock

logger = logging.getLogger(__name__)

# Допустимые множители ускорения времени
ALLOWED_MULTIPLIERS = [1, 10, 100, 1000, 10000]


class TimePanel(QWidget):
    """
    Панель управления временем симуляции.

    Signals:
        start_requested: Запрос на запуск симуляции.
        stop_requested: Запрос на остановку симуляции.
        reset_requested: Запрос на полный сброс симуляции.
        speed_changed(int): Изменение множителя ускорения времени.
    """

    start_requested = pyqtSignal()
    stop_requested = pyqtSignal()
    reset_requested = pyqtSignal()
    speed_changed = pyqtSignal(int)

    def __init__(self, clock: GlobalClock, parent: QWidget | None = None) -> None:
        """
        Инициализация панели управления временем.

        Args:
            clock: Глобальные часы симуляции (источник времени и сигналов).
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self._clock = clock

        try:
            self._init_ui()
            self._connect_signals()
            logger.debug("Панель управления временем инициализирована.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка инициализации панели управления временем: {e}")
            raise

    def _init_ui(self) -> None:
        """Создание интерфейса панели управления временем."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        # Группа кнопок управления симуляцией
        self._btn_start = QPushButton("▶ Старт")
        self._btn_stop = QPushButton("⏸ Стоп")
        self._btn_stop.setEnabled(False)
        self._btn_reset = QPushButton("⏹ Сброс")

        layout.addWidget(self._btn_start)
        layout.addWidget(self._btn_stop)
        layout.addWidget(self._btn_reset)

        layout.addSpacing(15)
        layout.addWidget(QLabel("Скорость:"))

        # Выпадающий список множителей ускорения (вместо ряда кнопок)
        self._speed_combo = QComboBox()
        for mult in ALLOWED_MULTIPLIERS:
            self._speed_combo.addItem(f"×{mult}", mult)

        current_mult = self._clock.get_speed_multiplier()
        index = self._speed_combo.findData(current_mult)
        if index != -1:
            self._speed_combo.setCurrentIndex(index)

        self._speed_combo.setFixedWidth(80)  # Компактная ширина
        layout.addWidget(self._speed_combo)

        layout.addStretch(1)

        # Отображение текущего времени (немного уменьшен шрифт для экономии места)
        self._time_label = QLabel("00:00:00.000")
        self._time_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(self._time_label)

    def _connect_signals(self) -> None:
        """Подключение внутренних сигналов панели."""
        self._btn_start.clicked.connect(self.start_requested.emit)
        self._btn_stop.clicked.connect(self.stop_requested.emit)
        self._btn_reset.clicked.connect(self.reset_requested.emit)
        self._speed_combo.currentIndexChanged.connect(self._on_speed_changed)

        # Обновление времени от глобальных часов
        self._clock.time_updated.connect(self._on_time_updated)

    def set_running_state(self, is_running: bool) -> None:
        """
        Обновить состояние кнопок Старт/Стоп в зависимости от состояния симуляции.

        Args:
            is_running: True, если симуляция запущена, False — если остановлена.
        """
        self._btn_start.setEnabled(not is_running)
        self._btn_stop.setEnabled(is_running)

    def reset_time_display(self, formatted_time: str) -> None:
        """
        Сбросить отображение времени к указанному значению.

        Args:
            formatted_time: Отформатированная строка времени (например, "00:00:00.000").
        """
        self._time_label.setText(formatted_time)

    def _on_speed_changed(self, index: int) -> None:
        """Обработка изменения выбранного множителя ускорения."""
        try:
            multiplier = self._speed_combo.itemData(index)
            if multiplier is not None:
                self.speed_changed.emit(multiplier)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обработки изменения скорости: {e}")

    def _on_time_updated(self, time_ms: int) -> None:
        """Обновление отображения текущего времени."""
        try:
            self._time_label.setText(self._clock.get_formatted_time())
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обновления отображения времени: {e}")
