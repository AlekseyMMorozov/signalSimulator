"""
ui/fault_template_dialog.py
Модальный диалог создания и редактирования шаблона неисправности.
Позволяет настроить название, тип неисправности, динамические параметры
и характер действия (постоянная, разовая, периодическая).
"""

import logging

from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QRadioButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from simulation.faults import FaultFactory
from simulation.scheduler import FaultTemplate

logger = logging.getLogger(__name__)

# Доступные типы неисправностей
FAULT_TYPES = FaultFactory.available_types()


class FaultTemplateDialog(QDialog):
    """
    Модальный диалог создания/редактирования шаблона неисправности.

    Позволяет настроить:
    - Название шаблона
    - Тип неисправности (dropout, spike, noise, degradation)
    - Динамические поля параметров (аналогично настройке сигналов)
    - Характер: постоянная / разовая / периодическая
    - Для разовой и периодической: длительность и период
    """

    def __init__(
        self,
        template: FaultTemplate | None = None,
        parent: QWidget | None = None
    ) -> None:
        """
        Инициализация диалога шаблона.

        Args:
            template: Существующий шаблон для редактирования (опционально).
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setWindowTitle("Создание шаблона неисправности" if template is None else "Редактирование шаблона")
        self.setMinimumWidth(500)

        self._template = template
        self._result_template: FaultTemplate | None = None

        try:
            self._init_ui()
            if template is not None:
                self._load_template(template)
            logger.info("Диалог шаблона неисправности инициализирован.")
        except Exception as e:
            logger.error(f"Ошибка инициализации диалога шаблона: {e}")
            raise

    def _init_ui(self) -> None:
        """Создание интерфейса диалога."""
        main_layout = QVBoxLayout(self)

        # Название шаблона
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Название шаблона:"))
        self._name_edit = QLineEdit()
        self._name_edit.setPlaceholderText("Например: Деградация АКБ")
        name_layout.addWidget(self._name_edit)
        main_layout.addLayout(name_layout)

        # Выбор типа неисправности
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Тип неисправности:"))
        self._fault_type_combo = QComboBox()
        for fault_type in FAULT_TYPES:
            self._fault_type_combo.addItem(fault_type)
        self._fault_type_combo.currentIndexChanged.connect(self._update_fault_params_fields)
        type_layout.addWidget(self._fault_type_combo)
        main_layout.addLayout(type_layout)

        # Динамические поля параметров
        params_group = QGroupBox("Параметры неисправности")
        self._params_layout = QFormLayout()
        params_group.setLayout(self._params_layout)
        main_layout.addWidget(params_group)

        # Характер неисправности
        character_group = QGroupBox("Характер неисправности")
        character_layout = QVBoxLayout()

        self._radio_permanent = QRadioButton("Постоянная (активна всё время)")
        self._radio_permanent.setChecked(True)
        character_layout.addWidget(self._radio_permanent)

        self._radio_once = QRadioButton("Разовая")
        character_layout.addWidget(self._radio_once)

        self._radio_periodic = QRadioButton("Периодическая")
        character_layout.addWidget(self._radio_periodic)

        # Длительность и период
        duration_layout = QHBoxLayout()
        duration_layout.addWidget(QLabel("Длительность (мс):"))
        self._duration_spin = QSpinBox()
        self._duration_spin.setRange(1, 1000000000)
        self._duration_spin.setValue(1000)
        self._duration_spin.setEnabled(False)
        duration_layout.addWidget(self._duration_spin)
        character_layout.addLayout(duration_layout)

        period_layout = QHBoxLayout()
        period_layout.addWidget(QLabel("Период (мс):"))
        self._period_spin = QSpinBox()
        self._period_spin.setRange(1, 1000000000)
        self._period_spin.setValue(10000)
        self._period_spin.setEnabled(False)
        period_layout.addWidget(self._period_spin)
        character_layout.addLayout(period_layout)

        character_group.setLayout(character_layout)
        main_layout.addWidget(character_group)

        # Подключение сигналов для управления доступностью полей
        self._radio_permanent.toggled.connect(self._on_character_changed)
        self._radio_once.toggled.connect(self._on_character_changed)
        self._radio_periodic.toggled.connect(self._on_character_changed)

        # Кнопки ОК / Отмена
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._on_accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

        # Инициализация полей параметров
        self._update_fault_params_fields()
        logger.debug("Интерфейс диалога шаблона создан.")

    def _on_character_changed(self) -> None:
        """Обработчик изменения характера неисправности."""
        try:
            if self._radio_permanent.isChecked():
                self._duration_spin.setEnabled(False)
                self._period_spin.setEnabled(False)
            elif self._radio_once.isChecked():
                self._duration_spin.setEnabled(True)
                self._period_spin.setEnabled(False)
            elif self._radio_periodic.isChecked():
                self._duration_spin.setEnabled(True)
                self._period_spin.setEnabled(True)
        except Exception as e:
            logger.error(f"Ошибка обработки изменения характера: {e}")

    def _update_fault_params_fields(self) -> None:
        """Обновление полей параметров неисправности при смене типа."""
        try:
            # Очистка старых полей
            while self._params_layout.count():
                item = self._params_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

            fault_type = self._fault_type_combo.currentText()

            # Создание полей в зависимости от типа неисправности
            if fault_type == "dropout":
                self._add_param("dropout_value", "Значение при пропадании:", 0.0)

            elif fault_type == "spike":
                self._add_param("magnitude_percent", "Величина скачка (%):", 100.0)

            elif fault_type == "noise":
                self._add_param("mean", "Среднее:", 0.0)
                self._add_param("sigma", "Сигма (сила шума):", 1.0)

            elif fault_type == "degradation":
                self._add_param("rate_percent_per_sec", "Скорость (%/сек):", -0.001)

            logger.debug(f"Обновлены поля параметров для типа '{fault_type}'.")
        except Exception as e:
            logger.error(f"Ошибка обновления полей параметров: {e}")

    def _add_param(self, param_name: str, label: str, default_value: float) -> None:
        """Добавить поле параметра неисправности в форму."""
        try:
            spin = QDoubleSpinBox()
            spin.setRange(-1e9, 1e9)
            spin.setDecimals(6)
            spin.setValue(default_value)
            spin.setProperty("param_name", param_name)
            self._params_layout.addRow(label, spin)
        except Exception as e:
            logger.error(f"Ошибка добавления поля параметра '{param_name}': {e}")

    def _load_template(self, template: FaultTemplate) -> None:
        """Загрузить параметры существующего шаблона в форму."""
        try:
            self._name_edit.setText(template.template_id)
            self._fault_type_combo.setCurrentText(template.fault_type)

            # Загрузка параметров
            for i in range(self._params_layout.count()):
                item = self._params_layout.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    param_name = widget.property("param_name")
                    if param_name in template.fault_params:
                        widget.setValue(template.fault_params[param_name])

            # Загрузка характера
            if template.fault_params.get("duration_ms") is None:
                self._radio_permanent.setChecked(True)
            elif template.fault_params.get("period_ms") is None:
                self._radio_once.setChecked(True)
                self._duration_spin.setValue(template.fault_params["duration_ms"])
            else:
                self._radio_periodic.setChecked(True)
                self._duration_spin.setValue(template.fault_params["duration_ms"])
                self._period_spin.setValue(template.fault_params["period_ms"])

            self._on_character_changed()
            logger.debug(f"Загружен шаблон '{template.template_id}'.")
        except Exception as e:
            logger.error(f"Ошибка загрузки шаблона: {e}")

    def _on_accept(self) -> None:
        """Обработчик нажатия кнопки ОК."""
        try:
            name = self._name_edit.text().strip()
            if not name:
                QMessageBox.warning(self, "Ошибка", "Название шаблона не может быть пустым.")
                return

            fault_type = self._fault_type_combo.currentText()

            # Сбор параметров неисправности
            fault_params = {}
            for i in range(self._params_layout.count()):
                item = self._params_layout.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    param_name = widget.property("param_name")
                    if param_name:
                        fault_params[param_name] = float(widget.value())

            # Добавление характера
            if self._radio_permanent.isChecked():
                fault_params["duration_ms"] = None
                fault_params["period_ms"] = None
            elif self._radio_once.isChecked():
                fault_params["duration_ms"] = self._duration_spin.value()
                fault_params["period_ms"] = None
            elif self._radio_periodic.isChecked():
                fault_params["duration_ms"] = self._duration_spin.value()
                fault_params["period_ms"] = self._period_spin.value()

            # Создание шаблона
            self._result_template = FaultTemplate(
                template_id=name,
                fault_type=fault_type,
                fault_params=fault_params,
            )

            logger.info(f"Шаблон '{name}' создан/обновлён.")
            self.accept()
        except Exception as e:
            logger.error(f"Ошибка при подтверждении диалога: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить шаблон:\n{e}")

    def get_template(self) -> FaultTemplate | None:
        """Получить созданный/обновлённый шаблон."""
        return self._result_template
