"""
ui/fault_window.py
Окно управления неисправностями с тремя вкладками: Шаблоны, Ручное внедрение, Правила.
Позволяет создавать заготовки неисправностей, внедрять их вручную на выбранные графики
и настраивать автоматическое внедрение через правила с параметрами периода и вероятности.
Диалоги создания шаблонов и правил вынесены в отдельные модули.
"""

import logging
from typing import Optional

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from simulation.scheduler import FaultScheduler, FaultTemplate
from simulation.simulator import SimulationEngine
from ui.fault_template_dialog import FaultTemplateDialog
from ui.fault_rule_dialog import FaultRuleDialog


logger = logging.getLogger(__name__)


class FaultWindow(QMainWindow):
    """
    Окно управления неисправностями с тремя вкладками.

    Вкладка "Шаблоны": создание, редактирование и удаление заготовок неисправностей.
    Вкладка "Ручное внедрение": внедрение шаблона на выбранный график.
    Вкладка "Правила": настройка автоматического внедрения с периодом и вероятностью.

    Signals:
        fault_injected: Неисправность внедрена вручную (plot_id, fault_type, fault_params).
    """

    fault_injected = pyqtSignal(str, str, dict)

    def __init__(
        self,
        scheduler: FaultScheduler,
        engine: SimulationEngine,
        parent: Optional[QWidget] = None
    ) -> None:
        """
        Инициализация окна управления неисправностями.

        Args:
            scheduler: Планировщик случайных неисправностей.
            engine: Движок симуляции.
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setWindowTitle("Управление неисправностями")
        self.setMinimumSize(600, 500)

        self._scheduler = scheduler
        self._engine = engine

        try:
            self._init_ui()
            self._refresh_templates_list()
            self._refresh_rules_list()
            logger.info("Окно управления неисправностями инициализировано.")
        except Exception as e:
            logger.error(f"Ошибка инициализации окна неисправностей: {e}")
            raise

    def _init_ui(self) -> None:
        """Создание интерфейса окна."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Вкладки
        self._tabs = QTabWidget()

        # Вкладка "Шаблоны"
        templates_tab = self._create_templates_tab()
        self._tabs.addTab(templates_tab, "Шаблоны")

        # Вкладка "Ручное внедрение"
        manual_tab = self._create_manual_tab()
        self._tabs.addTab(manual_tab, "Ручное внедрение")

        # Вкладка "Правила"
        rules_tab = self._create_rules_tab()
        self._tabs.addTab(rules_tab, "Правила")

        main_layout.addWidget(self._tabs)
        logger.debug("Интерфейс окна неисправностей создан.")

    def _create_templates_tab(self) -> QWidget:
        """Создание вкладки 'Шаблоны'."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Список шаблонов
        self._templates_list = QListWidget()
        layout.addWidget(self._templates_list, stretch=1)

        # Кнопки управления
        buttons_layout = QHBoxLayout()
        self._btn_create_template = QPushButton("Создать шаблон")
        self._btn_create_template.clicked.connect(self._on_create_template)
        buttons_layout.addWidget(self._btn_create_template)

        self._btn_edit_template = QPushButton("Редактировать")
        self._btn_edit_template.clicked.connect(self._on_edit_template)
        buttons_layout.addWidget(self._btn_edit_template)

        self._btn_delete_template = QPushButton("Удалить")
        self._btn_delete_template.clicked.connect(self._on_delete_template)
        buttons_layout.addWidget(self._btn_delete_template)

        layout.addLayout(buttons_layout)
        return widget

    def _create_manual_tab(self) -> QWidget:
        """Создание вкладки 'Ручное внедрение'."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Выбор графика
        plot_layout = QHBoxLayout()
        plot_layout.addWidget(QLabel("Внедрить на график:"))
        self._plot_combo = QWidget()  # Будет заменен на QComboBox в refresh
        # Используем временный placeholder, реальный QComboBox создается в _refresh_plots_combo
        from PyQt6.QtWidgets import QComboBox
        self._plot_combo = QComboBox()
        plot_layout.addWidget(self._plot_combo)
        layout.addLayout(plot_layout)

        # Список шаблонов с кнопками "Внедрить"
        self._manual_templates_list = QListWidget()
        layout.addWidget(self._manual_templates_list, stretch=1)

        # Обновление списков
        self._refresh_plots_combo()
        self._refresh_manual_templates_list()

        return widget

    def _create_rules_tab(self) -> QWidget:
        """Создание вкладки 'Правила'."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Список правил
        self._rules_list = QListWidget()
        layout.addWidget(self._rules_list, stretch=1)

        # Кнопки управления
        buttons_layout = QHBoxLayout()
        self._btn_create_rule = QPushButton("Создать правило")
        self._btn_create_rule.clicked.connect(self._on_create_rule)
        buttons_layout.addWidget(self._btn_create_rule)

        self._btn_toggle_rule = QPushButton("Вкл/Выкл")
        self._btn_toggle_rule.clicked.connect(self._on_toggle_rule)
        buttons_layout.addWidget(self._btn_toggle_rule)

        self._btn_delete_rule = QPushButton("Удалить")
        self._btn_delete_rule.clicked.connect(self._on_delete_rule)
        buttons_layout.addWidget(self._btn_delete_rule)

        layout.addLayout(buttons_layout)
        return widget

    # ------------------------------------------------------------------
    # Обновление списков
    # ------------------------------------------------------------------

    def _refresh_templates_list(self) -> None:
        """Обновить список шаблонов на вкладке 'Шаблоны'."""
        try:
            self._templates_list.clear()
            for template in self._scheduler.list_templates():
                item_text = f"{template.template_id} ({template.fault_type})"
                item = QListWidgetItem(item_text)
                item.setData(1, template.template_id)
                self._templates_list.addItem(item)
            logger.debug(f"Список шаблонов обновлён: {len(self._scheduler.list_templates())} шт.")
        except Exception as e:
            logger.error(f"Ошибка обновления списка шаблонов: {e}")

    def _refresh_plots_combo(self) -> None:
        """Обновить выпадающий список графиков на вкладке 'Ручное внедрение'."""
        try:
            self._plot_combo.clear()
            for plot_id in self._engine.get_all_plot_ids():
                plot = self._engine.get_plot(plot_id)
                if plot:
                    display_text = f"{plot.name} [{plot_id}]"
                    self._plot_combo.addItem(display_text, plot_id)
            logger.debug(f"Список графиков обновлён: {len(self._engine.get_all_plot_ids())} шт.")
        except Exception as e:
            logger.error(f"Ошибка обновления списка графиков: {e}")

    def _refresh_manual_templates_list(self) -> None:
        """Обновить список шаблонов с кнопками 'Внедрить' на вкладке 'Ручное внедрение'."""
        try:
            self._manual_templates_list.clear()
            for template in self._scheduler.list_templates():
                item = QListWidgetItem(f"{template.template_id} ({template.fault_type})")
                item.setData(1, template.template_id)
                self._manual_templates_list.addItem(item)

                # Добавление кнопки "Внедрить"
                btn = QPushButton("Внедрить")
                btn.clicked.connect(lambda checked, t=template: self._on_inject_fault(t))
                self._manual_templates_list.setItemWidget(item, btn)

            logger.debug("Список шаблонов для ручного внедрения обновлён.")
        except Exception as e:
            logger.error(f"Ошибка обновления списка шаблонов для ручного внедрения: {e}")

    def _refresh_rules_list(self) -> None:
        """Обновить список правил на вкладке 'Правила'."""
        try:
            self._rules_list.clear()
            for rule in self._scheduler.list_rules():
                status = "ВКЛ" if rule.enabled else "ВЫКЛ"
                item_text = f"{rule.rule_id} [{status}] — Период: {rule.check_interval_ms} мс, Вероятность: {rule.probability}"
                item = QListWidgetItem(item_text)
                item.setData(1, rule.rule_id)
                self._rules_list.addItem(item)
            logger.debug(f"Список правил обновлён: {len(self._scheduler.list_rules())} шт.")
        except Exception as e:
            logger.error(f"Ошибка обновления списка правил: {e}")

    # ------------------------------------------------------------------
    # Обработчики вкладок
    # ------------------------------------------------------------------

    def _on_create_template(self) -> None:
        """Создание нового шаблона."""
        try:
            dialog = FaultTemplateDialog(parent=self)
            if dialog.exec() == dialog.DialogCode.Accepted:
                template = dialog.get_template()
                if template:
                    self._scheduler.add_template(template)
                    self._refresh_templates_list()
                    self._refresh_manual_templates_list()
                    logger.info(f"Создан шаблон '{template.template_id}'.")
        except Exception as e:
            logger.error(f"Ошибка создания шаблона: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать шаблон:\n{e}")

    def _on_edit_template(self) -> None:
        """Редактирование выбранного шаблона."""
        try:
            item = self._templates_list.currentItem()
            if item is None:
                QMessageBox.warning(self, "Ошибка", "Выберите шаблон для редактирования.")
                return

            template_id = item.data(1)
            template = self._scheduler.get_template(template_id)
            if template is None:
                QMessageBox.warning(self, "Ошибка", f"Шаблон '{template_id}' не найден.")
                return

            dialog = FaultTemplateDialog(template=template, parent=self)
            if dialog.exec() == dialog.DialogCode.Accepted:
                new_template = dialog.get_template()
                if new_template:
                    self._scheduler.remove_template(template_id)
                    self._scheduler.add_template(new_template)
                    self._refresh_templates_list()
                    self._refresh_manual_templates_list()
                    logger.info(f"Шаблон '{template_id}' обновлён.")
        except Exception as e:
            logger.error(f"Ошибка редактирования шаблона: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось отредактировать шаблон:\n{e}")

    def _on_delete_template(self) -> None:
        """Удаление выбранного шаблона."""
        try:
            item = self._templates_list.currentItem()
            if item is None:
                QMessageBox.warning(self, "Ошибка", "Выберите шаблон для удаления.")
                return

            template_id = item.data(1)
            reply = QMessageBox.question(
                self, "Подтверждение",
                f"Удалить шаблон '{template_id}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self._scheduler.remove_template(template_id)
                self._refresh_templates_list()
                self._refresh_manual_templates_list()
                logger.info(f"Шаблон '{template_id}' удалён.")
        except Exception as e:
            logger.error(f"Ошибка удаления шаблона: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить шаблон:\n{e}")

    def _on_inject_fault(self, template: FaultTemplate) -> None:
        """Внедрение неисправности из шаблона на выбранный график."""
        try:
            plot_id = self._plot_combo.currentData()
            if plot_id is None:
                QMessageBox.warning(self, "Ошибка", "Выберите график для внедрения.")
                return

            fault = self._engine.inject_fault(plot_id, template.fault_type, template.fault_params)
            if fault:
                self.fault_injected.emit(plot_id, template.fault_type, template.fault_params)
                QMessageBox.information(self, "Успех", f"Неисправность '{template.template_id}' внедрена на график '{plot_id}'.")
                logger.info(f"Неисправность '{template.template_id}' внедрена на график '{plot_id}'.")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось внедрить неисправность.")
        except Exception as e:
            logger.error(f"Ошибка внедрения неисправности: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось внедрить неисправность:\n{e}")

    def _on_create_rule(self) -> None:
        """Создание нового правила."""
        try:
            templates = self._scheduler.list_templates()
            if not templates:
                QMessageBox.warning(self, "Ошибка", "Нет доступных шаблонов. Создайте хотя бы один шаблон.")
                return

            dialog = FaultRuleDialog(available_templates=templates, parent=self)
            if dialog.exec() == dialog.DialogCode.Accepted:
                rule = dialog.get_rule()
                if rule:
                    self._scheduler.add_rule(rule)
                    self._refresh_rules_list()
                    logger.info(f"Создано правило '{rule.rule_id}'.")
        except Exception as e:
            logger.error(f"Ошибка создания правила: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать правило:\n{e}")

    def _on_toggle_rule(self) -> None:
        """Включение/выключение выбранного правила."""
        try:
            item = self._rules_list.currentItem()
            if item is None:
                QMessageBox.warning(self, "Ошибка", "Выберите правило для включения/выключения.")
                return

            rule_id = item.data(1)
            rule = self._scheduler.get_rule(rule_id)
            if rule:
                rule.enabled = not rule.enabled
                self._refresh_rules_list()
                state = "включено" if rule.enabled else "выключено"
                logger.info(f"Правило '{rule_id}' {state}.")
            else:
                QMessageBox.warning(self, "Ошибка", f"Правило '{rule_id}' не найдено.")
        except Exception as e:
            logger.error(f"Ошибка переключения правила: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось переключить правило:\n{e}")

    def _on_delete_rule(self) -> None:
        """Удаление выбранного правила."""
        try:
            item = self._rules_list.currentItem()
            if item is None:
                QMessageBox.warning(self, "Ошибка", "Выберите правило для удаления.")
                return

            rule_id = item.data(1)
            reply = QMessageBox.question(
                self, "Подтверждение",
                f"Удалить правило '{rule_id}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self._scheduler.remove_rule(rule_id)
                self._refresh_rules_list()
                logger.info(f"Правило '{rule_id}' удалено.")
        except Exception as e:
            logger.error(f"Ошибка удаления правила: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить правило:\n{e}")
