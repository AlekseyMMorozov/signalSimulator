"""
ui/period_widget.py

Специализированный виджет для удобного ввода периода сигнала
с автоматическим выбором и конвертацией единиц измерения.
"""

import logging

from PyQt6.QtWidgets import QComboBox, QHBoxLayout, QSpinBox, QWidget

logger = logging.getLogger(__name__)


class PeriodWidget(QWidget):
    """
    Виджет для удобного ввода периода с выбором единицы измерения.
    Автоматически конвертирует выбранное значение и единицу в миллисекунды и обратно.
    """

    def __init__(self, default_ms: int, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._spin = QSpinBox()
        self._spin.setRange(1, 1000000000)
        self._spin.setToolTip("Числовое значение периода.")

        self._unit_combo = QComboBox()
        self._unit_combo.addItems(["мс", "с", "мин"])
        self._unit_combo.setToolTip("Единица измерения периода.")

        # Умный дефолт: если значение кратно 1000, показываем в секундах или минутах для удобства
        if default_ms >= 1000 and default_ms % 1000 == 0:
            secs = default_ms // 1000
            if secs % 60 == 0:
                self._spin.setValue(secs // 60)
                self._unit_combo.setCurrentText("мин")
            else:
                self._spin.setValue(secs)
                self._unit_combo.setCurrentText("с")
        else:
            self._spin.setValue(default_ms)
            self._unit_combo.setCurrentText("мс")

        layout.addWidget(self._spin)
        layout.addWidget(self._unit_combo)
        layout.addStretch(1)

        self.setToolTip("Время, за которое сигнал совершает один полный цикл.")

    def get_period_ms(self) -> int:
        """Возвращает период, пересчитанный в миллисекунды."""
        val = self._spin.value()
        unit = self._unit_combo.currentText()
        multipliers = {"мс": 1, "с": 1000, "мин": 60000}
        return val * multipliers[unit]

    def set_period_ms(self, ms: int) -> None:
        """
        Устанавливает период, автоматически выбирая удобную единицу измерения.

        Args:
            ms: Значение периода в миллисекундах.
        """
        try:
            if ms >= 60000 and ms % 60000 == 0:
                self._spin.setValue(ms // 60000)
                self._unit_combo.setCurrentText("мин")
            elif ms >= 1000 and ms % 1000 == 0:
                self._spin.setValue(ms // 1000)
                self._unit_combo.setCurrentText("с")
            else:
                self._spin.setValue(ms)
                self._unit_combo.setCurrentText("мс")
        except Exception as e:
            logger.error(f"Ошибка установки периода в виджете: {e}")

