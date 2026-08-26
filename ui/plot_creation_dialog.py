"""
ui/plot_creation_dialog.py

Модальный диалог создания нового графика телеметрии.
Позволяет настроить все параметры графика: название, единицу измерения,
тип сигнала с его параметрами, допустимые пределы и интервал наблюдения.
Вызывается из главного окна по сигналу plot_add_requested.
"""

import logging
from typing import Any, Dict, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from simulation.signals import SignalFactory


logger = logging.getLogger(__name__)

# Пресеты интервалов наблюдения (название, значение в секундах)
INTERVAL_PRESETS = [
    ("1 минута", 60),
    ("5 минут", 300),
    ("10 минут", 600),
    ("30 минут", 1800),
    ("1 час", 3600),
    ("6 часов", 21600),
    ("12 часов", 43200),
    ("1 сутки", 86400),
    ("1 неделя", 604800),
    ("1 месяц (30 дней)", 2592000),
    ("6 месяцев", 15552000),
    ("1 год", 31536000),
    ("2 года", 63072000),
    ("Ручной ввод", 0),
]

# Доступные типы сигналов
SIGNAL_TYPES = SignalFactory.available_types()


class PlotCreationDialog(QDialog):
    """
    Модальный диалог создания нового графика телеметрии.

    Позволяет настроить:
    - Основные параметры (название, единица, макс. значение)
    - Интервал наблюдения (через пресеты или ручной ввод в секундах)
    - Допустимые пределы (min_allowed, max_allowed)
    - Тип сигнала и его параметры (динамически меняются)

    После подтверждения результат доступен через метод get_plot_params().
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Инициализация диалога создания графика.

        Args:
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setWindowTitle("Создание графика")
        self.setMinimumWidth(500)

        self._plot_params: Optional[Dict[str, Any]] = None

        try:
            self._init_ui()
            self._update_signal_params_fields()
            logger.info("Диалог создания графика инициализирован.")
        except Exception as e:
            logger.error(f"Ошибка инициализации диалога создания графика: {e}")
            raise

    def _init_ui(self) -> None:
        """Создание интерфейса диалога."""
        main_layout = QVBoxLayout(self)

        # === Группа основных параметров ===
        basic_group = QGroupBox("Основные параметры")
        basic_layout = QFormLayout()

        # Название графика
        self._name_edit = QLineEdit()
        self._name_edit.setPlaceholderText("Например: Сила тока Батарея солнечная 1")
        basic_layout.addRow("Название:", self._name_edit)

        # Единица измерения
        self._unit_edit = QLineEdit()
        self._unit_edit.setPlaceholderText("Например: А")
        basic_layout.addRow("Единица измерения:", self._unit_edit)

        # Максимальное значение единицы
        self._max_unit_spin = QDoubleSpinBox()
        self._max_unit_spin.setRange(0.0, 1e9)
        self._max_unit_spin.setDecimals(4)
        self._max_unit_spin.setValue(10.0)
        basic_layout.addRow("Макс. значение единицы:", self._max_unit_spin)

        basic_group.setLayout(basic_layout)
        main_layout.addWidget(basic_group)

        # === Группа интервала наблюдения ===
        interval_group = QGroupBox("Интервал наблюдения")
        interval_layout = QVBoxLayout()

        # Пресеты
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("Пресет:"))
        self._interval_preset_combo = QComboBox()
        for name, _ in INTERVAL_PRESETS:
            self._interval_preset_combo.addItem(name)
        self._interval_preset_combo.setCurrentIndex(len(INTERVAL_PRESETS) - 1)  # "Ручной ввод"
        self._interval_preset_combo.currentIndexChanged.connect(self._on_preset_changed)
        preset_layout.addWidget(self._interval_preset_combo)
        interval_layout.addLayout(preset_layout)

        # Ручной ввод в секундах
        manual_layout = QHBoxLayout()
        manual_layout.addWidget(QLabel("Вручную (секунды):"))
        self._interval_spin = QSpinBox()
        self._interval_spin.setRange(1, 1000000000)
        self._interval_spin.setValue(60)
        manual_layout.addWidget(self._interval_spin)
        interval_layout.addLayout(manual_layout)

        interval_group.setLayout(interval_layout)
        main_layout.addWidget(interval_group)

        # === Группа допустимых пределов ===
        limits_group = QGroupBox("Допустимые пределы")
        limits_layout = QFormLayout()

        self._min_allowed_spin = QDoubleSpinBox()
        self._min_allowed_spin.setRange(-1e9, 1e9)
        self._min_allowed_spin.setDecimals(4)
        self._min_allowed_spin.setValue(0.0)
        limits_layout.addRow("Минимум:", self._min_allowed_spin)

        self._max_allowed_spin = QDoubleSpinBox()
        self._max_allowed_spin.setRange(-1e9, 1e9)
        self._max_allowed_spin.setDecimals(4)
        self._max_allowed_spin.setValue(10.0)
        limits_layout.addRow("Максимум:", self._max_allowed_spin)

        limits_group.setLayout(limits_layout)
        main_layout.addWidget(limits_group)

        # === Группа параметров сигнала ===
        signal_group = QGroupBox("Параметры сигнала")
        signal_layout = QVBoxLayout()

        # Выбор типа сигнала
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Тип сигнала:"))
        self._signal_type_combo = QComboBox()
        for sig_type in SIGNAL_TYPES:
            self._signal_type_combo.addItem(sig_type)
        self._signal_type_combo.currentIndexChanged.connect(self._update_signal_params_fields)
        type_layout.addWidget(self._signal_type_combo)
        signal_layout.addLayout(type_layout)

        # Контейнер для динамических полей параметров
        self._signal_params_widget = QWidget()
        self._signal_params_layout = QFormLayout(self._signal_params_widget)
        signal_layout.addWidget(self._signal_params_widget)

        signal_group.setLayout(signal_layout)
        main_layout.addWidget(signal_group)

        # === Кнопки ОК / Отмена ===
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._on_accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

        logger.debug("Интерфейс диалога создания графика создан.")

    def _on_preset_changed(self, index: int) -> None:
        """
        Обработчик изменения пресета интервала.

        При выборе пресета подставляет значение в поле ручного ввода.

        Args:
            index: Индекс выбранного пресета.
        """
        try:
            if 0 <= index < len(INTERVAL_PRESETS):
                _, value_sec = INTERVAL_PRESETS[index]
                if value_sec > 0:
                    self._interval_spin.setValue(value_sec)
                    logger.debug(f"Выбран пресет интервала: {value_sec} сек.")
        except Exception as e:
            logger.error(f"Ошибка обработки изменения пресета: {e}")

    def _update_signal_params_fields(self) -> None:
        """
        Обновление полей параметров сигнала при смене типа.

        Удаляет старые поля и создаёт новые в соответствии с выбранным типом сигнала.
        """
        try:
            # Очистка старых полей
            while self._signal_params_layout.count():
                item = self._signal_params_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

            signal_type = self._signal_type_combo.currentText()

            # Создание полей в зависимости от типа сигнала
            if signal_type in ["sawtooth", "triangle", "step"]:
                self._add_signal_param("min_val", "Минимум:", 0.0)
                self._add_signal_param("max_val", "Максимум:", 10.0)
                self._add_signal_param("period_ms", "Период (мс):", 10000, is_int=True)
                self._add_signal_param("offset", "Смещение:", 0.0)

            elif signal_type == "sine":
                self._add_signal_param("amplitude", "Амплитуда:", 1.0)
                self._add_signal_param("period_ms", "Период (мс):", 10000, is_int=True)
                self._add_signal_param("phase", "Фаза (рад):", 0.0)
                self._add_signal_param("offset", "Смещение:", 0.0)

            elif signal_type == "linear":
                self._add_signal_param("start_val", "Начальное значение:", 0.0)
                self._add_signal_param("rate_per_sec", "Скорость (ед/сек):", 0.01)
                self._add_signal_param("offset", "Смещение:", 0.0)

            elif signal_type == "square":
                self._add_signal_param("min_val", "Минимум:", 0.0)
                self._add_signal_param("max_val", "Максимум:", 10.0)
                self._add_signal_param("period_ms", "Период (мс):", 10000, is_int=True)
                self._add_signal_param("duty_cycle", "Коэфф. заполнения:", 0.5)
                self._add_signal_param("offset", "Смещение:", 0.0)

            elif signal_type == "exponential":
                self._add_signal_param("amplitude", "Амплитуда:", 1.0)
                self._add_signal_param("rate_per_sec", "Скорость (1/сек):", 0.01)
                self._add_signal_param("offset", "Смещение:", 0.0)

            elif signal_type == "noise":
                self._add_signal_param("mean", "Среднее:", 0.0)
                self._add_signal_param("sigma", "Сигма:", 1.0)

            elif signal_type == "constant":
                self._add_signal_param("value", "Значение:", 5.0)

            logger.debug(f"Обновлены поля параметров сигнала для типа '{signal_type}'.")
        except Exception as e:
            logger.error(f"Ошибка обновления полей параметров сигнала: {e}")

    def _add_signal_param(
        self,
        param_name: str,
        label: str,
        default_value: float,
        is_int: bool = False
    ) -> None:
        """
        Добавить поле параметра сигнала в форму.

        Args:
            param_name: Имя параметра (используется как ключ в словаре).
            label: Отображаемая метка.
            default_value: Значение по умолчанию.
            is_int: Если True, используется QSpinBox (целое), иначе QDoubleSpinBox.
        """
        try:
            if is_int:
                spin = QSpinBox()
                spin.setRange(1, 1000000000)
                spin.setValue(int(default_value))
                spin.setProperty("param_name", param_name)
                spin.setProperty("is_int", True)
                self._signal_params_layout.addRow(label, spin)
            else:
                spin = QDoubleSpinBox()
                spin.setRange(-1e9, 1e9)
                spin.setDecimals(6)
                spin.setValue(default_value)
                spin.setProperty("param_name", param_name)
                spin.setProperty("is_int", False)
                self._signal_params_layout.addRow(label, spin)
        except Exception as e:
            logger.error(f"Ошибка добавления поля параметра '{param_name}': {e}")

    def _on_accept(self) -> None:
        """
        Обработчик нажатия кнопки ОК.

        Выполняет валидацию и при успехе сохраняет параметры и закрывает диалог.
        """
        try:
            if not self._validate():
                return

            # Сбор основных параметров
            name = self._name_edit.text().strip()
            unit = self._unit_edit.text().strip()
            max_unit_value = self._max_unit_spin.value()
            interval_sec = self._interval_spin.value()
            interval_ms = interval_sec * 1000
            min_allowed = self._min_allowed_spin.value()
            max_allowed = self._max_allowed_spin.value()

            # Сбор параметров сигнала
            signal_type = self._signal_type_combo.currentText()
            signal_params = {}
            for i in range(self._signal_params_layout.count()):
                item = self._signal_params_layout.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    param_name = widget.property("param_name")
                    is_int = widget.property("is_int")
                    if param_name:
                        value = widget.value()
                        if is_int:
                            signal_params[param_name] = int(value)
                        else:
                            signal_params[param_name] = float(value)

            # Сохранение параметров
            self._plot_params = {
                "name": name,
                "unit": unit,
                "max_unit_value": max_unit_value,
                "observation_interval_ms": interval_ms,
                "min_allowed": min_allowed,
                "max_allowed": max_allowed,
                "signal_type": signal_type,
                "signal_params": signal_params,
            }

            logger.info(f"Диалог создания графика подтверждён: {name}.")
            self.accept()
        except Exception as e:
            logger.error(f"Ошибка при подтверждении диалога: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить параметры:\n{e}")

    def _validate(self) -> bool:
        """
        Валидация введённых данных.

        Returns:
            bool: True, если данные корректны, False иначе.
        """
        try:
            name = self._name_edit.text().strip()
            if not name:
                QMessageBox.warning(self, "Ошибка валидации", "Название графика не может быть пустым.")
                return False

            min_allowed = self._min_allowed_spin.value()
            max_allowed = self._max_allowed_spin.value()
            if min_allowed >= max_allowed:
                QMessageBox.warning(
                    self, "Ошибка валидации",
                    "Минимальный предел должен быть меньше максимального."
                )
                return False

            interval_sec = self._interval_spin.value()
            if interval_sec <= 0:
                QMessageBox.warning(
                    self, "Ошибка валидации",
                    "Интервал наблюдения должен быть больше нуля."
                )
                return False

            # Проверка периода для сигналов, у которых он есть
            signal_type = self._signal_type_combo.currentText()
            if signal_type in ["sawtooth", "triangle", "step", "sine", "square"]:
                for i in range(self._signal_params_layout.count()):
                    item = self._signal_params_layout.itemAt(i)
                    if item and item.widget():
                        widget = item.widget()
                        param_name = widget.property("param_name")
                        if param_name == "period_ms":
                            period = widget.value()
                            if period <= 0:
                                QMessageBox.warning(
                                    self, "Ошибка валидации",
                                    "Период сигнала должен быть больше нуля."
                                )
                                return False

            return True
        except Exception as e:
            logger.error(f"Ошибка валидации: {e}")
            return False

    def get_plot_params(self) -> Optional[Dict[str, Any]]:
        """
        Получить параметры графика после подтверждения диалога.

        Returns:
            dict: Словарь параметров графика, или None если диалог был отменён.
                  Структура:
                  {
                      "name": str,
                      "unit": str,
                      "max_unit_value": float,
                      "observation_interval_ms": int,
                      "min_allowed": float,
                      "max_allowed": float,
                      "signal_type": str,
                      "signal_params": dict
                  }
        """
        return self._plot_params
