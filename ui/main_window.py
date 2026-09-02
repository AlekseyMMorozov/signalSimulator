"""
ui/main_window.py

Главное окно приложения — центральная панель управления симуляцией.
Является оркестратором трёх специализированных панелей:
- TimePanel — управление временем (старт/стоп/сброс/скорость).
- PlotsPanel — управление списком графиков и действиями с ними.
- OptionsPanel — дополнительные настройки (скрытые метки, журнал).

Содержит меню, управляет сохранением/восстановлением геометрии окна
и уведомляет координатора о закрытии приложения.
"""

import logging

from PyQt6.QtCore import QSettings, pyqtSignal
from PyQt6.QtGui import QCloseEvent, QGuiApplication
from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from core.clock import GlobalClock
from ui.panels.options_panel import OptionsPanel
from ui.panels.plots_panel import PlotsPanel
from ui.panels.time_panel import TimePanel

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Главное окно приложения.

    Обеспечивает управление временем симуляции, списком графиков,
    открытие/закрытие журнала событий и запрос на изменение настроек
    существующих графиков. Логика сохранения/загрузки конфигурации
    делегирована координатору через сигналы.

    Signals:
        plot_open_requested: Запрос на открытие окна графика (plot_id).
        plot_add_requested: Запрос на создание нового графика.
        plot_remove_requested: Запрос на удаление графика (plot_id).
        plot_settings_requested: Запрос на изменение настроек графика (plot_id).
        reset_requested: Запрос на полный сброс симуляции (для очистки графиков).
        journal_toggled: Журнал открыт (True) или закрыт (False).
        hidden_markers_toggled: Режим скрытых меток включён (True) или выключён (False).
        save_config_requested: Запрос на сохранение конфигурации по указанному пути.
        load_config_requested: Запрос на загрузку конфигурации по указанному пути.
        window_closed: Сигнал о закрытии главного окна (для завершения работы приложения).
    """

    plot_open_requested = pyqtSignal(str)
    plot_add_requested = pyqtSignal()
    plot_remove_requested = pyqtSignal(str)
    plot_settings_requested = pyqtSignal(str)
    reset_requested = pyqtSignal()
    journal_toggled = pyqtSignal(bool)
    hidden_markers_toggled = pyqtSignal(bool)
    save_config_requested = pyqtSignal(str)
    load_config_requested = pyqtSignal(str)
    window_closed = pyqtSignal()

    def __init__(self, clock: GlobalClock, parent: QWidget | None = None) -> None:
        """
        Инициализация главного окна.

        Args:
            clock: Глобальные часы симуляции.
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setWindowTitle("signalSimulator")

        # Инициализация QSettings для сохранения состояния интерфейса
        self._settings = QSettings("signalSimulator", "signalSimulatorApp")

        self._clock = clock
        self._journal_visible = False

        # Создание специализированных панелей
        self._time_panel = TimePanel(clock)
        self._plots_panel = PlotsPanel()
        self._options_panel = OptionsPanel()

        try:
            self._init_menu()
            self._init_ui()
            self._connect_signals()
            self._restore_geometry()
            logger.info("Главное окно инициализировано (компактный режим).")
        except Exception as e:
            logger.error(f"Ошибка инициализации главного окна: {e}")
            raise

    def _restore_geometry(self) -> None:
        """Восстановление размера и положения окна из настроек."""
        try:
            geometry = self._settings.value("MainWindow/geometry")
            if geometry:
                self.restoreGeometry(geometry)
            else:
                # Fallback: если настроек нет, используем дефолтный компактный размер
                screen = QGuiApplication.primaryScreen().availableGeometry()
                target_width = max(600, screen.width() // 2)
                target_height = max(450, screen.height() // 2)
                self.resize(target_width, target_height)
                self.setMinimumSize(600, 450)

            is_maximized = self._settings.value("MainWindow/maximized", False, type=bool)
            if is_maximized:
                self.showMaximized()

            logger.debug("Геометрия главного окна восстановлена.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка восстановления геометрии главного окна: {e}")

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Обработка события закрытия окна.
        Сохраняет геометрию и уведомляет координатора о завершении работы.
        """
        try:
            self._settings.setValue("MainWindow/geometry", self.saveGeometry())
            self._settings.setValue("MainWindow/maximized", self.isMaximized())
            logger.info("Геометрия главного окна сохранена.")

            # Уведомляем координатора, чтобы он закрыл остальные окна
            self.window_closed.emit()

            super().closeEvent(event)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка при закрытии главного окна: {e}")
            super().closeEvent(event)

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
        """Создание основного интерфейса с использованием делегированных панелей."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        # Блок 1: Панель управления временем
        main_layout.addWidget(self._time_panel)

        # Разделитель
        main_layout.addWidget(self._create_separator())

        # Блок 2: Панель графиков (занимает всё доступное пространство)
        main_layout.addWidget(self._plots_panel, stretch=1)

        # Разделитель
        main_layout.addWidget(self._create_separator())

        # Блок 3: Панель дополнительных настроек
        main_layout.addWidget(self._options_panel)

        logger.debug("Интерфейс главного окна создан.")

    def _create_separator(self) -> QFrame:
        """Создание горизонтального разделителя для визуального структурирования."""
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        return line

    def _connect_signals(self) -> None:
        """Подключение сигналов панелей к сигналам главного окна."""
        # TimePanel -> MainWindow
        self._time_panel.start_requested.connect(self._on_start)
        self._time_panel.stop_requested.connect(self._on_stop)
        self._time_panel.reset_requested.connect(self._on_reset)
        # speed_changed(int) от TimePanel не требует промежуточной обработки,
        # так как TimePanel сам управляет часами через переданный clock.

        # PlotsPanel -> MainWindow
        self._plots_panel.add_requested.connect(self.plot_add_requested.emit)
        self._plots_panel.open_requested.connect(self.plot_open_requested.emit)
        self._plots_panel.settings_requested.connect(self.plot_settings_requested.emit)
        self._plots_panel.remove_requested.connect(self.plot_remove_requested.emit)

        # OptionsPanel -> MainWindow
        self._options_panel.hidden_markers_toggled.connect(self.hidden_markers_toggled.emit)
        self._options_panel.journal_toggled.connect(self._on_toggle_journal)

        logger.debug("Сигналы панелей подключены к главному окну.")

    # ------------------------------------------------------------------
    # Публичные методы (делегирование к PlotsPanel)
    # ------------------------------------------------------------------

    def add_plot_to_list(self, plot_id: str, name: str) -> None:
        """
        Добавить график в список на главном окне.

        Args:
            plot_id: Идентификатор графика.
            name: Отображаемое название графика.
        """
        self._plots_panel.add_item(plot_id, name)

    def remove_plot_from_list(self, plot_id: str) -> None:
        """
        Удалить график из списка на главном окне.

        Args:
            plot_id: Идентификатор графика.
        """
        self._plots_panel.remove_item(plot_id)

    def get_selected_plot_id(self) -> str | None:
        """Получить идентификатор выбранного графика."""
        return self._plots_panel.get_selected_plot_id()

    # ------------------------------------------------------------------
    # Обработчики управления временем (делегирование к TimePanel)
    # ------------------------------------------------------------------

    def _on_start(self) -> None:
        """Запуск симуляции."""
        try:
            self._clock.start()
            self._time_panel.set_running_state(True)
            logger.info("Симуляция запущена.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка запуска симуляции: {e}")

    def _on_stop(self) -> None:
        """Остановка симуляции."""
        try:
            self._clock.stop()
            self._time_panel.set_running_state(False)
            logger.info("Симуляция остановлена.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка остановки симуляции: {e}")

    def _on_reset(self) -> None:
        """Сброс симуляции."""
        try:
            self._clock.reset()
            self._clock.stop()
            self._time_panel.set_running_state(False)
            self._time_panel.reset_time_display(self._clock.get_formatted_time())

            # Уведомляем координатора о необходимости очистки данных графиков
            self.reset_requested.emit()

            logger.info("Симуляция сброшена.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка сброса симуляции: {e}")

    # ------------------------------------------------------------------
    # Обработчики меню и опций
    # ------------------------------------------------------------------

    def _on_toggle_journal(self, checked: bool) -> None:
        """Переключение видимости журнала событий (синхронизирует меню и чекбокс)."""
        try:
            self._journal_visible = checked
            self._journal_action.setChecked(checked)
            # Программно синхронизируем чекбокс без повторной эмиссии сигнала
            self._options_panel.set_journal_state(checked)
            self.journal_toggled.emit(self._journal_visible)
            state = "открыт" if self._journal_visible else "закрыт"
            logger.info(f"Журнал событий {state}.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка переключения журнала: {e}")

    def _on_save_config(self) -> None:
        """Запрос на сохранение текущей конфигурации в файл."""
        try:
            filepath, _ = QFileDialog.getSaveFileName(
                self, "Сохранить конфигурацию", "",
                "Конфигурация (*.json)"
            )
            if filepath:
                self.save_config_requested.emit(filepath)
            else:
                logger.debug("Сохранение конфигурации отменено пользователем.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Непредвиденная ошибка при запросе сохранения: {e}")
            QMessageBox.critical(self, "Ошибка", f"Непредвиденная ошибка:\n{e}")

    def _on_load_config(self) -> None:
        """Запрос на загрузку конфигурации из файла."""
        try:
            filepath, _ = QFileDialog.getOpenFileName(
                self, "Загрузить конфигурацию", "",
                "Конфигурация (*.json)"
            )
            if filepath:
                self.load_config_requested.emit(filepath)
            else:
                logger.debug("Загрузка конфигурации отменено пользователем.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Непредвиденная ошибка при запросе загрузки: {e}")
            QMessageBox.critical(self, "Ошибка", f"Непредвиденная ошибка:\n{e}")
