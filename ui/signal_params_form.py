"""
ui/signal_params_form.py

Виджет для динамического построения полей параметров сигнала.
Поддерживает различные типы сигналов (синус, пила, меандр и т.д.)
и автоматически создает соответствующие поля ввода для каждого типа.
"""

import logging
from typing import Any

from PyQt6.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QSpinBox,
    QWidget,
)

from ui.period_widget import PeriodWidget

logger = logging.getLogger(__name__)

# Сопоставление внутренних ключей сигналов с русскими названиями для интерфейса
SIGNAL_TYPE_DISPLAY = {
    "sine": "Синусоида",
    "sawtooth": "Пилообразный",
    "triangle": "Треугольный",
    "step": "Ступенчатый",
    "linear": "Линейный (тренд)",
    "square": "Прямоугольный (меандр)",
    "exponential": "Экспоненциальный",
    "noise": "Случайный шум",
    "constant": "Постоянный",
}


class SignalParamsForm(QWidget):
    """
    Виджет для динамического построения полей параметров сигнала.

    Автоматически создает поля ввода в зависимости от выбранного типа сигнала.
    Поддерживает получение и установку значений параметров.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Инициализация формы параметров сигнала.

        Args:
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self._form_layout = QFormLayout(self)
        self._form_layout.setContentsMargins(0, 0, 0, 0)

    def update_fields(self, signal_type: str) -> None:
        """
        Обновление полей параметров сигнала при смене типа.
        Удаляет старые поля и создаёт новые в соответствии с выбранным типом сигнала.

        Args:
            signal_type: Внутренний ключ типа сигнала.
        """
        try:
            # Удаляем все существующие поля
            while self._form_layout.count():
                item = self._form_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

            # Создаем поля для нового типа сигнала
            if signal_type in ["sawtooth", "triangle", "step"]:
                self._add_param("min_val", "Минимум:", 0.0,
                                tooltip="Нижнее значение сигнала (состояние '0' или 'выключено').")
                self._add_param("max_val", "Максимум:", 10.0,
                                tooltip="Верхнее значение сигнала (состояние '1' или 'включено').")
                self._add_param("period_ms", "Период:", 10000, is_int=True)
                self._add_param("offset", "Смещение:", 0.0,
                                tooltip="Постоянная величина, добавляемая ко всему сигналу. Сдвигает весь график вверх или вниз.")

            elif signal_type == "sine":
                self._add_param("amplitude", "Амплитуда:", 1.0,
                                tooltip="Максимальное отклонение сигнала от центра. Пиковое значение синусоиды.")
                self._add_param("period_ms", "Период:", 10000, is_int=True)
                self._add_param("phase", "Фаза (рад):", 0.0,
                                tooltip="Начальный сдвиг синусоиды в радианах. 0 — начало с нуля, 1.57 (π/2) — начало с максимума.")
                self._add_param("offset", "Смещение:", 0.0,
                                tooltip="Постоянная величина, добавляемая ко всему сигналу. Сдвигает весь график вверх или вниз.")

            elif signal_type == "linear":
                self._add_param("start_val", "Начальное значение:", 0.0,
                                tooltip="Значение сигнала в момент времени 0.")
                self._add_param("rate_per_sec", "Скорость (ед/сек):", 0.01,
                                tooltip="На сколько единиц изменяется значение сигнала за одну секунду. Положительное — рост, отрицательное — падение.")
                self._add_param("offset", "Смещение:", 0.0,
                                tooltip="Постоянная величина, добавляемая ко всему сигналу. Сдвигает весь график вверх или вниз.")

            elif signal_type == "square":
                self._add_param("min_val", "Минимум:", 0.0,
                                tooltip="Нижнее значение сигнала (состояние '0' или 'выключено').")
                self._add_param("max_val", "Максимум:", 10.0,
                                tooltip="Верхнее значение сигнала (состояние '1' или 'включено').")
                self._add_param("period_ms", "Период:", 10000, is_int=True)
                self._add_param("duty_cycle", "Коэфф. заполнения:", 0.5,
                                tooltip="Доля периода, в течение которой сигнал находится на уровне максимума. 0.5 означает классический меандр (50% времени на максимуме). Диапазон: 0.0 - 1.0.")
                self._add_param("offset", "Смещение:", 0.0,
                                tooltip="Постоянная величина, добавляемая ко всему сигналу. Сдвигает весь график вверх или вниз.")

            elif signal_type == "exponential":
                self._add_param("amplitude", "Амплитуда:", 1.0,
                                tooltip="Множитель экспоненты. Начальная величина отклонения.")
                self._add_param("rate_per_sec", "Скорость (1/сек):", 0.01,
                                tooltip="Скорость роста или затухания. Положительное — экспоненциальный рост, отрицательное — затухание.")
                self._add_param("offset", "Смещение:", 0.0,
                                tooltip="Постоянная величина, добавляемая ко всему сигналу. Сдвигает весь график вверх или вниз.")

            elif signal_type == "noise":
                self._add_param("mean", "Среднее:", 0.0,
                                tooltip="Центр распределения случайного шума (среднее значение).")
                self._add_param("sigma", "Сигма:", 1.0,
                                tooltip="Сила шума (стандартное отклонение). Чем больше, тем сильнее разброс значений.")

            elif signal_type == "constant":
                self._add_param("value", "Значение:", 5.0,
                                tooltip="Постоянное значение сигнала, которое не меняется со временем.")

            logger.debug(f"Обновлены поля параметров сигнала для типа '{signal_type}'.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обновления полей параметров сигнала: {e}")

    def _add_param(
            self,
            param_name: str,
            label: str,
            default_value: float,
            is_int: bool = False,
            tooltip: str = ""
    ) -> None:
        """
        Добавить поле параметра сигнала в форму.
        Для периода используется специализированный виджет с выбором единицы измерения.

        Args:
            param_name: Внутреннее имя параметра.
            label: Отображаемая метка поля.
            default_value: Значение по умолчанию.
            is_int: True если параметр целочисленный.
            tooltip: Всплывающая подсказка.
        """
        try:
            if param_name == "period_ms":
                widget = PeriodWidget(int(default_value))
                widget.setProperty("param_name", param_name)
                widget.setProperty("is_period", True)
                self._form_layout.addRow(label, widget)
            elif is_int:
                spin = QSpinBox()
                spin.setRange(1, 1000000000)
                spin.setValue(int(default_value))
                spin.setProperty("param_name", param_name)
                spin.setProperty("is_int", True)
                if tooltip:
                    spin.setToolTip(tooltip)
                self._form_layout.addRow(label, spin)
            else:
                spin = QDoubleSpinBox()
                spin.setRange(-1e9, 1e9)
                spin.setDecimals(6)
                spin.setValue(default_value)
                spin.setProperty("param_name", param_name)
                spin.setProperty("is_int", False)
                if tooltip:
                    spin.setToolTip(tooltip)
                self._form_layout.addRow(label, spin)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка добавления поля параметра '{param_name}': {e}")

    def get_signal_params(self) -> dict[str, Any]:
        """
        Получить текущие значения всех параметров сигнала.

        Returns:
            dict: Словарь параметров {param_name: value}.
        """
        params = {}
        try:
            for i in range(self._form_layout.count()):
                item = self._form_layout.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    param_name = widget.property("param_name")
                    if not param_name:
                        continue

                    if widget.property("is_period"):
                        params[param_name] = widget.get_period_ms()
                    else:
                        is_int = widget.property("is_int")
                        value = widget.value()
                        params[param_name] = int(value) if is_int else float(value)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка получения параметров сигнала: {e}")
        return params

    def set_signal_params(self, params: dict[str, Any]) -> None:
        """
        Установить значения параметров сигнала (для режима редактирования).

        Args:
            params: Словарь параметров {param_name: value}.
        """
        try:
            for i in range(self._form_layout.count()):
                item = self._form_layout.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    param_name = widget.property("param_name")
                    if param_name in params:
                        val = params[param_name]
                        if widget.property("is_period"):
                            widget.set_period_ms(int(val))
                        else:
                            widget.setValue(val)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка установки параметров сигнала: {e}")

