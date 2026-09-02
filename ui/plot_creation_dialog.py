"""
ui/plot_creation_dialog.py

Модальный диалог создания и редактирования графика телеметрии.
Позволяет настроить все параметры графика: название, единицу измерения,
тип сигнала, допустимые пределы, интервал наблюдения и настройки детектора.
Использует делегирование для динамических полей параметров сигнала.
"""

import logging
from typing import Any

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
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from analytics.detector import DetectorConfig
from ui.detector_settings_tab import DetectorSettingsTab
from ui.signal_params_form import SIGNAL_TYPE_DISPLAY, SignalParamsForm

logger = logging.getLogger(__name__)


class PlotCreationDialog(QDialog):
    """
    Модальный диалог создания и редактирования графика телеметрии.
    Делегирует управление динамическими полями сигнала классу SignalParamsForm.
    """

    def __init__(self, parent: QWidget | None = None, initial_params: dict[str, Any] | None = None) -> None:
        """
        Инициализация диалога создания/редактирования графика.

        Args:
            parent: Родительский виджет.
            initial_params: Словарь существующих параметров (режим редактирования).
        """
        super().__init__(parent)
        self.setWindowTitle("Редактирование графика" if initial_params else "Создание графика")
        self.setMinimumWidth(600)

        self._plot_params: dict[str, Any] | None = None

        try:
            self._init_ui()
            if initial_params:
                self._populate_fields(initial_params)
            else:
                # Инициализация полей сигнала для типа по умолчанию
                self._on_signal_type_changed()
            logger.info("Диалог графика инициализирован.")
        except Exception as e:
            logger.error(f"Ошибка инициализации диалога графика: {e}")
            raise

    def _init_ui(self) -> None:
        """Создание интерфейса диалога с использованием делегированных виджетов."""
        main_layout = QVBoxLayout(self)

        self._tab_widget = QTabWidget()
        main_layout.addWidget(self._tab_widget)

        # --- Вкладка 1: Параметры сигнала ---
        signal_tab = QWidget()
        signal_tab_layout = QVBoxLayout(signal_tab)
        signal_tab_layout.setContentsMargins(4, 4, 4, 4)
        signal_tab_layout.setSpacing(8)

        # Основные параметры
        basic_group = QGroupBox("Основные параметры")
        basic_layout = QFormLayout()
        self._name_edit = QLineEdit()
        self._name_edit.setPlaceholderText("Например: Сила тока БС1")
        self._unit_edit = QLineEdit()
        self._unit_edit.setPlaceholderText("Например: А")
        self._max_unit_spin = QDoubleSpinBox()
        self._max_unit_spin.setRange(0.0, 1e9)
        self._max_unit_spin.setDecimals(4)
        self._max_unit_spin.setValue(10.0)

        basic_layout.addRow("Название:", self._name_edit)
        basic_layout.addRow("Единица измерения:", self._unit_edit)
        basic_layout.addRow("Макс. значение единицы:", self._max_unit_spin)
        basic_group.setLayout(basic_layout)
        signal_tab_layout.addWidget(basic_group)

        # Интервал наблюдения
        interval_group = QGroupBox("Интервал наблюдения")
        interval_layout = QVBoxLayout()
        preset_layout = QHBoxLayout()
        self._interval_preset_combo = QComboBox()
        presets = [
            ("1 минута", 60), ("5 минут", 300), ("10 минут", 600), ("30 минут", 1800),
            ("1 час", 3600), ("6 часов", 21600), ("12 часов", 43200), ("1 сутки", 86400),
            ("1 неделя", 604800), ("1 месяц (30 дней)", 2592000), ("6 месяцев", 15552000),
            ("1 год", 31536000), ("2 года", 63072000), ("Ручной ввод", 0),
        ]
        for name, _ in presets:
            self._interval_preset_combo.addItem(name)
        self._interval_preset_combo.setCurrentIndex(len(presets) - 1)
        self._interval_preset_combo.currentIndexChanged.connect(self._on_preset_changed)
        preset_layout.addWidget(QLabel("Пресет:"))
        preset_layout.addWidget(self._interval_preset_combo)

        manual_layout = QHBoxLayout()
        self._interval_spin = QSpinBox()
        self._interval_spin.setRange(1, 1000000000)
        self._interval_spin.setValue(60)
        manual_layout.addWidget(QLabel("Вручную (секунды):"))
        manual_layout.addWidget(self._interval_spin)

        interval_layout.addLayout(preset_layout)
        interval_layout.addLayout(manual_layout)
        interval_group.setLayout(interval_layout)
        signal_tab_layout.addWidget(interval_group)

        # Допустимые пределы
        limits_group = QGroupBox("Допустимые пределы")
        limits_layout = QFormLayout()
        self._min_allowed_spin = QDoubleSpinBox()
        self._min_allowed_spin.setRange(-1e9, 1e9)
        self._min_allowed_spin.setDecimals(4)
        self._max_allowed_spin = QDoubleSpinBox()
        self._max_allowed_spin.setRange(-1e9, 1e9)
        self._max_allowed_spin.setDecimals(4)
        self._max_allowed_spin.setValue(10.0)
        limits_layout.addRow("Минимум:", self._min_allowed_spin)
        limits_layout.addRow("Максимум:", self._max_allowed_spin)
        limits_group.setLayout(limits_layout)
        signal_tab_layout.addWidget(limits_group)

        # Параметры сигнала (делегировано)
        signal_group = QGroupBox("Параметры сигнала")
        signal_layout = QVBoxLayout()
        type_layout = QHBoxLayout()
        self._signal_type_combo = QComboBox()
        for internal_key, display_name in SIGNAL_TYPE_DISPLAY.items():
            self._signal_type_combo.addItem(display_name, internal_key)
        self._signal_type_combo.currentIndexChanged.connect(self._on_signal_type_changed)
        type_layout.addWidget(QLabel("Тип сигнала:"))
        type_layout.addWidget(self._signal_type_combo)

        self._signal_params_form = SignalParamsForm()
        signal_layout.addLayout(type_layout)
        signal_layout.addWidget(self._signal_params_form)
        signal_group.setLayout(signal_layout)
        signal_tab_layout.addWidget(signal_group)

        signal_tab_layout.addStretch(1)
        self._tab_widget.addTab(signal_tab, "📊 Сигнал")

        # --- Вкладка 2: Настройки детектора ---
        self._detector_settings_tab = DetectorSettingsTab()
        self._tab_widget.addTab(self._detector_settings_tab, "🔍 Детектор")

        # Кнопки
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._on_accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

        logger.debug("Интерфейс диалога графика создан.")

    def _populate_fields(self, params: dict[str, Any]) -> None:
        """Предзаполняет поля диалога переданными параметрами."""
        try:
            self._name_edit.setText(params.get("name", ""))
            self._unit_edit.setText(params.get("unit", ""))
            self._max_unit_spin.setValue(params.get("max_unit_value", 10.0))
            self._min_allowed_spin.setValue(params.get("min_allowed", 0.0))
            self._max_allowed_spin.setValue(params.get("max_allowed", 10.0))

            interval_sec = params.get("observation_interval_ms", 60000) // 1000
            self._interval_spin.setValue(max(1, interval_sec))

            signal_type = params.get("signal_type", "sine")
            index = self._signal_type_combo.findData(signal_type)
            if index != -1:
                self._signal_type_combo.setCurrentIndex(index)

            # Делегируем заполнение параметров сигнала
            self._signal_params_form.update_fields(signal_type)
            self._signal_params_form.set_signal_params(params.get("signal_params", {}))

            # Настройки детектора
            detector_config_dict = params.get("detector_config")
            if detector_config_dict:
                try:
                    config = DetectorConfig.from_dict(detector_config_dict)
                    self._detector_settings_tab.set_config(config)
                except Exception as e:
                    logger.error(f"Ошибка загрузки конфигурации детектора: {e}")

            logger.debug("Поля диалога предзаполнены параметрами.")
        except Exception as e:
            logger.error(f"Ошибка предзаполнения полей: {e}")

    def _on_preset_changed(self, index: int) -> None:
        """Обработчик изменения пресета интервала."""
        try:
            presets = [
                ("1 минута", 60), ("5 минут", 300), ("10 минут", 600), ("30 минут", 1800),
                ("1 час", 3600), ("6 часов", 21600), ("12 часов", 43200), ("1 сутки", 86400),
                ("1 неделя", 604800), ("1 месяц (30 дней)", 2592000), ("6 месяцев", 15552000),
                ("1 год", 31536000), ("2 года", 63072000), ("Ручной ввод", 0),
            ]
            if 0 <= index < len(presets):
                _, value_sec = presets[index]
                if value_sec > 0:
                    self._interval_spin.setValue(value_sec)
        except Exception as e:
            logger.error(f"Ошибка обработки изменения пресета: {e}")

    def _on_signal_type_changed(self) -> None:
        """Обновление полей параметров сигнала при смене типа (делегирование)."""
        try:
            signal_type = self._signal_type_combo.currentData()
            self._signal_params_form.update_fields(signal_type)
        except Exception as e:
            logger.error(f"Ошибка обновления полей параметров сигнала: {e}")

    def _on_accept(self) -> None:
        """Обработчик нажатия кнопки ОК с валидацией и сбором данных."""
        try:
            if not self._validate():
                return

            signal_type = self._signal_type_combo.currentData()

            # Получаем конфигурацию детектора и устанавливаем signal_type
            detector_config = self._detector_settings_tab.get_config()
            detector_config.signal_type = signal_type

            self._plot_params = {
                "name": self._name_edit.text().strip(),
                "unit": self._unit_edit.text().strip(),
                "max_unit_value": self._max_unit_spin.value(),
                "observation_interval_ms": self._interval_spin.value() * 1000,
                "min_allowed": self._min_allowed_spin.value(),
                "max_allowed": self._max_allowed_spin.value(),
                "signal_type": signal_type,
                "signal_params": self._signal_params_form.get_signal_params(),
                "detector_config": detector_config.to_dict(),
            }

            logger.info(f"Параметры графика подтверждены: {self._plot_params['name']}.")
            self.accept()
        except Exception as e:
            logger.error(f"Ошибка при подтверждении диалога: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить параметры:\n{e}")

    def _validate(self) -> bool:
        """Валидация введённых данных."""
        try:
            if not self._name_edit.text().strip():
                QMessageBox.warning(self, "Ошибка валидации", "Название графика не может быть пустым.")
                return False

            if self._min_allowed_spin.value() >= self._max_allowed_spin.value():
                QMessageBox.warning(self, "Ошибка валидации", "Минимальный предел должен быть строго меньше максимального.")
                return False

            if self._interval_spin.value() <= 0:
                QMessageBox.warning(self, "Ошибка валидации", "Интервал наблюдения должен быть больше нуля.")
                return False

            return True
        except Exception as e:
            logger.error(f"Ошибка валидации: {e}")
            return False

    def get_plot_params(self) -> dict[str, Any] | None:
        """Получить параметры графика после подтверждения диалога."""
        return self._plot_params

