"""
ui/main_window.py
Главное окно приложения — центральная панель управления симуляцией.
Содержит панель управления временем, список графиков, меню и кнопки
для открытия вспомогательных окон.
"""

import logging
from typing import Optional

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QListWidgetItem,
    QMenuBar, QMenu, QMessageBox, QFileDialog,
)
from PyQt6.QtCore import pyqtSignal, Qt

from core.clock import GlobalClock
from core.config import ConfigManager, ConfigError


logger = logging.getLogger(__name__)

# Допустимые множители ускорения времени
ALLOWED_MULTIPLIERS = [1, 10, 100, 1000, 10000]


class MainWindow(QMainWindow):
    """
    Главное окно приложения.

    Обеспечивает управление временем симуляции, списком графиков,
    открытие/закрытие журнала событий и сохранение/загрузку конфигураций.

    Signals:
        plot_open_requested: Запрос на открытие окна графика (plot_id).
        plot_add_requested: Запрос на создание нового графика.
        plot_remove_requested: Запрос на удаление графика (plot_id).
        journal_toggled: Журнал открыт (True) или закрыт (False).
        hidden_markers_toggled: Режим скрытых меток включён (True) или выключен (False).
    """

    plot_open_requested = pyqtSignal(str)
    plot_add_requested = pyqtSignal()
    plot_remove_requested = pyqtSignal(str)
    journal_toggled = pyqtSignal(bool)
    hidden_markers_toggled = pyqtSignal(bool)

    def __init__(self, clock: GlobalClock, parent: Optional[QWidget] = None) -> None:
        """
        Инициализация главного окна.

        Args:
            clock: Глобальные часы симуляции.
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setWindowTitle("signalSimulator")
        self.setMinimumSize(800, 600)

        self._clock = clock
        self._config_manager = ConfigManager()
        self._journal_visible = False
        self._hidden_markers_visible = False

        try:
            self._init_menu()
            self._init_ui()
            self._connect_signals()
            logger.info("Главное окно инициализировано.")
        except Exception as e:
            logger.error(f"Ошибка инициализации главного окна: {e}")
            raise

    def _init_menu(self) -> None:
        """Создание строки меню."""
        menubar = self.menuBar()

        # Меню "Файл"
        file_menu = menubar.addMenu("&Файл")
        save_action = file_menu.addAction("Сохранить конфигурацию")
        save_action.triggered.connect(self._on_save_config)
        load_action = file_menu.addAction("Загрузить конфигурацию")
        load_action.triggered.connect(self._on_load_config)
        file_menu.addSeparator()
        exit_action = file_menu.addAction("Выход")
        exit_action.triggered.connect(self.close)

        # Меню "Окна"
        windows_menu = menubar.addMenu("&Окна")
        self._journal_action = windows_menu.addAction("Журнал событий")
        self._journal_action.setCheckable(True)
        self._journal_action.setChecked(False)
        self._journal_action.triggered.connect(self._on_toggle_journal)

        logger.debug("Меню главного окна создано.")

    def _init_ui(self) -> None:
        """Создание основного интерфейса."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # --- Панель управления временем ---
        time_panel = self._create_time_panel()
        main_layout.addWidget(time_panel)

        # --- Панель графиков ---
        plots_panel = self._create_plots_panel()
        main_layout.addWidget(plots_panel, stretch=1)

        logger.debug("Интерфейс главного окна создан.")

    def _create_time_panel(self) -> QWidget:
        """Создание панели управления временем."""
        panel = QWidget()
        layout = QHBoxLayout(panel)

        # Кнопки управления симуляцией
        self._btn_start = QPushButton("▶ Старт")
        self._btn_stop = QPushButton("⏸ Стоп")
        self._btn_stop.setEnabled(False)
        self._btn_reset = QPushButton("⏹ Сброс")

        layout.addWidget(self._btn_start)
        layout.addWidget(self._btn_stop)
        layout.addWidget(self._btn_reset)

        layout.addSpacing(20)

        # Кнопки множителей ускорения
        layout.addWidget(QLabel("Скорость:"))
        self._speed_buttons: list[QPushButton] = []
        for mult in ALLOWED_MULTIPLIERS:
            btn = QPushButton(f"×{mult}")
            btn.setCheckable(True)
            btn.setChecked(mult == self._clock.get_speed_multiplier())
            btn.clicked.connect(lambda checked, m=mult: self._on_speed_change(m))
            self._speed_buttons.append(btn)
            layout.addWidget(btn)

        layout.addSpacing(20)

        # Отображение текущего времени
        self._time_label = QLabel("00:00:00.000")
        self._time_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self._time_label)

        layout.addSpacing(20)

        # Кнопка скрытых меток
        self._btn_hidden_markers = QPushButton("Скрытые метки")
        self._btn_hidden_markers.setCheckable(True)
        self._btn_hidden_markers.setChecked(False)
        layout.addWidget(self._btn_hidden_markers)

        return panel

    def _create_plots_panel(self) -> QWidget:
        """Создание панели управления графиками."""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        layout.addWidget(QLabel("Графики телеметрии:"))

        # Список графиков
        self._plots_list = QListWidget()
        self._plots_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        layout.addWidget(self._plots_list, stretch=1)

        # Кнопки управления графиками
        buttons_layout = QHBoxLayout()
        self._btn_add_plot = QPushButton("➕ Добавить график")
        self._btn_open_plot = QPushButton("📈 Открыть график")
        self._btn_remove_plot = QPushButton("🗑 Удалить график")
        self._btn_open_plot.setEnabled(False)
        self._btn_remove_plot.setEnabled(False)

        buttons_layout.addWidget(self._btn_add_plot)
        buttons_layout.addWidget(self._btn_open_plot)
        buttons_layout.addWidget(self._btn_remove_plot)
        layout.addLayout(buttons_layout)

        return panel

    def _connect_signals(self) -> None:
        """Подключение внутренних сигналов."""
        # Управление временем
        self._btn_start.clicked.connect(self._on_start)
        self._btn_stop.clicked.connect(self._on_stop)
        self._btn_reset.clicked.connect(self._on_reset)

        # Скрытые метки
        self._btn_hidden_markers.clicked.connect(self._on_toggle_hidden_markers)

        # Управление графиками
        self._btn_add_plot.clicked.connect(self._on_add_plot)
        self._btn_open_plot.clicked.connect(self._on_open_plot)
        self._btn_remove_plot.clicked.connect(self._on_remove_plot)
        self._plots_list.currentItemChanged.connect(self._on_plot_selection_changed)

        # Обновление времени от часов
        self._clock.time_updated.connect(self._on_time_updated)

        logger.debug("Сигналы главного окна подключены.")

    # --- Публичные методы ---

    def add_plot_to_list(self, plot_id: str, name: str) -> None:
        """
        Добавить график в список на главном окне.

        Args:
            plot_id: Идентификатор графика.
            name: Отображаемое название графика.
        """
        try:
            item = QListWidgetItem(f"{name} [{plot_id}]")
            item.setData(Qt.ItemDataRole.UserRole, plot_id)
            self._plots_list.addItem(item)
            logger.info(f"График '{name}' добавлен в список.")
        except Exception as e:
            logger.error(f"Ошибка добавления графика в список: {e}")

    def remove_plot_from_list(self, plot_id: str) -> None:
        """
        Удалить график из списка на главном окне.

        Args:
            plot_id: Идентификатор графика.
        """
        try:
            for i in range(self._plots_list.count()):
                item = self._plots_list.item(i)
                if item.data(Qt.ItemDataRole.UserRole) == plot_id:
                    self._plots_list.takeItem(i)
                    logger.info(f"График '{plot_id}' удалён из списка.")
                    return
            logger.warning(f"График '{plot_id}' не найден в списке для удаления.")
        except Exception as e:
            logger.error(f"Ошибка удаления графика из списка: {e}")

    def get_selected_plot_id(self) -> Optional[str]:
        """Получить идентификатор выбранного графика."""
        item = self._plots_list.currentItem()
        if item is not None:
            return item.data(Qt.ItemDataRole.UserRole)
        return None

    # --- Обработчики управления временем ---

    def _on_start(self) -> None:
        """Запуск симуляции."""
        try:
            self._clock.start()
            self._btn_start.setEnabled(False)
            self._btn_stop.setEnabled(True)
            logger.info("Симуляция запущена.")
        except Exception as e:
            logger.error(f"Ошибка запуска симуляции: {e}")

    def _on_stop(self) -> None:
        """Остановка симуляции."""
        try:
            self._clock.stop()
            self._btn_start.setEnabled(True)
            self._btn_stop.setEnabled(False)
            logger.info("Симуляция остановлена.")
        except Exception as e:
            logger.error(f"Ошибка остановки симуляции: {e}")

    def _on_reset(self) -> None:
        """Сброс симуляции."""
        try:
            self._clock.reset()
            self._clock.stop()
            self._btn_start.setEnabled(True)
            self._btn_stop.setEnabled(False)
            self._time_label.setText(self._clock.get_formatted_time())
            logger.info("Симуляция сброшена.")
        except Exception as e:
            logger.error(f"Ошибка сброса симуляции: {e}")

    def _on_speed_change(self, multiplier: int) -> None:
        """Изменение множителя ускорения времени."""
        try:
            self._clock.set_speed_multiplier(multiplier)
            for btn in self._speed_buttons:
                btn.setChecked(btn.text() == f"×{multiplier}")
            logger.info(f"Множитель ускорения изменён на ×{multiplier}.")
        except ValueError as e:
            logger.warning(f"Недопустимый множитель ускорения: {e}")
        except Exception as e:
            logger.error(f"Ошибка изменения множителя: {e}")

    def _on_time_updated(self, time_ms: int) -> None:
        """Обновление отображения времени."""
        try:
            self._time_label.setText(self._clock.get_formatted_time())
        except Exception as e:
            logger.error(f"Ошибка обновления времени: {e}")

    # --- Обработчики скрытых меток ---

    def _on_toggle_hidden_markers(self) -> None:
        """Переключение режима скрытых меток."""
        try:
            self._hidden_markers_visible = self._btn_hidden_markers.isChecked()
            self.hidden_markers_toggled.emit(self._hidden_markers_visible)
            state = "включён" if self._hidden_markers_visible else "выключен"
            logger.info(f"Режим скрытых меток {state}.")
        except Exception as e:
            logger.error(f"Ошибка переключения скрытых меток: {e}")

    # --- Обработчики графиков ---

    def _on_add_plot(self) -> None:
        """Запрос на создание нового графика."""
        logger.debug("Запрос на добавление графика.")
        self.plot_add_requested.emit()

    def _on_open_plot(self) -> None:
        """Запрос на открытие окна выбранного графика."""
        plot_id = self.get_selected_plot_id()
        if plot_id:
            logger.debug(f"Запрос на открытие графика '{plot_id}'.")
            self.plot_open_requested.emit(plot_id)
        else:
            logger.warning("Не выбран график для открытия.")

    def _on_remove_plot(self) -> None:
        """Запрос на удаление выбранного графика."""
        plot_id = self.get_selected_plot_id()
        if plot_id:
            logger.debug(f"Запрос на удаление графика '{plot_id}'.")
            self.plot_remove_requested.emit(plot_id)
        else:
            logger.warning("Не выбран график для удаления.")

    def _on_plot_selection_changed(self, current: Optional[QListWidgetItem], previous) -> None:
        """Обработка изменения выбора в списке графиков."""
        has_selection = current is not None
        self._btn_open_plot.setEnabled(has_selection)
        self._btn_remove_plot.setEnabled(has_selection)

    # --- Обработчики меню ---

    def _on_toggle_journal(self) -> None:
        """Переключение видимости журнала событий."""
        try:
            self._journal_visible = self._journal_action.isChecked()
            self.journal_toggled.emit(self._journal_visible)
            state = "открыт" if self._journal_visible else "закрыт"
            logger.info(f"Журнал событий {state}.")
        except Exception as e:
            logger.error(f"Ошибка переключения журнала: {e}")

    def _on_save_config(self) -> None:
        """Сохранение текущей конфигурации в файл."""
        try:
            filepath, _ = QFileDialog.getSaveFileName(
                self, "Сохранить конфигурацию", "",
                "Конфигурация (*.json)"
            )
            if filepath:
                config_data = self._collect_current_config()
                self._config_manager.save_config(config_data)
                logger.info(f"Конфигурация сохранена: {filepath}")
            else:
                logger.debug("Сохранение конфигурации отменено пользователем.")
        except ConfigError as e:
            logger.error(f"Ошибка сохранения конфигурации: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить конфигурацию:\n{e}")
        except Exception as e:
            logger.error(f"Непредвиденная ошибка при сохранении: {e}")
            QMessageBox.critical(self, "Ошибка", f"Непредвиденная ошибка:\n{e}")

    def _on_load_config(self) -> None:
        """Загрузка конфигурации из файла."""
        try:
            filepath, _ = QFileDialog.getOpenFileName(
                self, "Загрузить конфигурацию", "",
                "Конфигурация (*.json)"
            )
            if filepath:
                config_data = self._config_manager.load_config(filepath)
                self._apply_loaded_config(config_data)
                logger.info(f"Конфигурация загружена: {filepath}")
            else:
                logger.debug("Загрузка конфигурации отменена пользователем.")
        except ConfigError as e:
            logger.error(f"Ошибка загрузки конфигурации: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить конфигурацию:\n{e}")
        except Exception as e:
            logger.error(f"Непредвиденная ошибка при загрузке: {e}")
            QMessageBox.critical(self, "Ошибка", f"Непредвиденная ошибка:\n{e}")

    def _collect_current_config(self) -> dict:
        """Собрать текущую конфигурацию для сохранения."""
        config = self._config_manager.get_default_config()
        # TODO: Собрать данные графиков из движка симуляции
        return config

    def _apply_loaded_config(self, config_data: dict) -> None:
        """Применить загруженную конфигурацию."""
        try:
            plots = config_data.get("plots", [])
            logger.info(f"Загружено графиков из конфигурации: {len(plots)}")
            # TODO: Создать графики через движок симуляции
        except Exception as e:
            logger.error(f"Ошибка применения загруженной конфигурации: {e}")
