"""
ui/fault_rule_dialog.py
Модальный диалог создания правила автоматического внедрения неисправностей.
Позволяет настроить название правила, выбрать шаблон неисправности,
задать период проверки, вероятность срабатывания и режим внедрения.
"""

import logging
from typing import List, Optional

from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
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

from simulation.scheduler import FaultTemplate, RandomFaultRule

logger = logging.getLogger(__name__)


class FaultRuleDialog(QDialog):
    """
    Модальный диалог создания правила автоматического внедрения неисправностей.

    Позволяет настроить:
    - Название правила
    - Выбор шаблона (из списка)
    - Период проверки (N мс)
    - Вероятность срабатывания (X в долях 0.0–1.0)
    - Режим внедрения: один / все / случайное подмножество
    """

    def __init__(
            self,
            available_templates: List[FaultTemplate],
            parent: Optional[QWidget] = None
    ) -> None:
        """
        Инициализация диалога правила.

        Args:
            available_templates: Список доступных шаблонов для выбора.
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setWindowTitle("Создание правила автоматического внедрения")
        self.setMinimumWidth(500)

        self._available_templates = available_templates
        self._result_rule: Optional[RandomFaultRule] = None

        try:
            self._init_ui()
            logger.info("Диалог правила инициализирован.")
        except Exception as e:
            logger.error(f"Ошибка инициализации диалога правила: {e}")
            raise

    def _init_ui(self) -> None:
        """Создание интерфейса диалога."""
        main_layout = QVBoxLayout(self)

        # Название правила
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Название правила:"))
        self._name_edit = QLineEdit()
        self._name_edit.setPlaceholderText("Например: Случайный шум")
        name_layout.addWidget(self._name_edit)
        main_layout.addLayout(name_layout)

        # Выбор шаблона
        template_layout = QHBoxLayout()
        template_layout.addWidget(QLabel("Шаблон неисправности:"))
        self._template_combo = QComboBox()
        for template in self._available_templates:
            self._template_combo.addItem(template.template_id)
        template_layout.addWidget(self._template_combo)
        main_layout.addLayout(template_layout)

        # Период проверки
        period_layout = QHBoxLayout()
        period_layout.addWidget(QLabel("Период проверки (мс):"))
        self._period_spin = QSpinBox()
        self._period_spin.setRange(100, 1000000000)
        self._period_spin.setValue(20000)
        period_layout.addWidget(self._period_spin)
        main_layout.addLayout(period_layout)

        # Вероятность срабатывания
        prob_layout = QHBoxLayout()
        prob_layout.addWidget(QLabel("Вероятность срабатывания (0.0–1.0):"))
        self._prob_spin = QDoubleSpinBox()
        self._prob_spin.setRange(0.0, 1.0)
        self._prob_spin.setDecimals(2)
        self._prob_spin.setSingleStep(0.1)
        self._prob_spin.setValue(0.5)
        prob_layout.addWidget(self._prob_spin)
        main_layout.addLayout(prob_layout)

        # Режим внедрения
        mode_group = QGroupBox("Режим внедрения")
        mode_layout = QVBoxLayout()

        self._radio_one = QRadioButton("Один случайный график")
        self._radio_one.setChecked(True)
        mode_layout.addWidget(self._radio_one)

        self._radio_all = QRadioButton("Все графики")
        mode_layout.addWidget(self._radio_all)

        self._radio_subset = QRadioButton("Случайное подмножество")
        mode_layout.addWidget(self._radio_subset)

        subset_layout = QHBoxLayout()
        subset_layout.addWidget(QLabel("Размер подмножества:"))
        self._subset_spin = QSpinBox()
        self._subset_spin.setRange(1, 100)
        self._subset_spin.setValue(2)
        self._subset_spin.setEnabled(False)
        subset_layout.addWidget(self._subset_spin)
        mode_layout.addLayout(subset_layout)

        mode_group.setLayout(mode_layout)
        main_layout.addWidget(mode_group)

        # Подключение сигналов для управления доступностью
        self._radio_subset.toggled.connect(self._subset_spin.setEnabled)

        # Кнопки ОК / Отмена
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._on_accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

        logger.debug("Интерфейс диалога правила создан.")

    def _on_accept(self) -> None:
        """Обработчик нажатия кнопки ОК."""
        try:
            name = self._name_edit.text().strip()
            if not name:
                QMessageBox.warning(self, "Ошибка", "Название правила не может быть пустым.")
                return

            if not self._available_templates:
                QMessageBox.warning(self, "Ошибка", "Нет доступных шаблонов. Создайте хотя бы один шаблон.")
                return

            template_id = self._template_combo.currentText()
            period_ms = self._period_spin.value()
            probability = self._prob_spin.value()

            # Определение режима
            if self._radio_one.isChecked():
                target_mode = "one"
                subset_count = 1
            elif self._radio_all.isChecked():
                target_mode = "all"
                subset_count = 0
            else:
                target_mode = "random_subset"
                subset_count = self._subset_spin.value()

            # Создание правила
            self._result_rule = RandomFaultRule(
                rule_id=name,
                check_interval_ms=period_ms,
                probability=probability,
                template_ids=[template_id],
                enabled=True,
            )

            # Установка режима через шаблон (упрощение: правило использует один шаблон)
            template = next((t for t in self._available_templates if t.template_id == template_id), None)
            if template:
                template.target_mode = target_mode
                template.subset_count = subset_count

            logger.info(f"Правило '{name}' создано.")
            self.accept()
        except Exception as e:
            logger.error(f"Ошибка при подтверждении диалога: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить правило:\n{e}")

    def get_rule(self) -> Optional[RandomFaultRule]:
        """Получить созданное правило."""
        return self._result_rule
