"""
ui/main_window.py
Главное окно приложения — центральная панель управления симуляцией.
Содержит панель управления временем, список графиков, меню и кнопки
для открытия вспомогательных окон и изменения настроек графиков.
"""

import logging

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.clock import GlobalClock

logger = logging.getLogger(__name__)

# Допустимые множители ускорения времени
ALLOWED_MULTIPLIERS = [1, 10, 100, 1000, 10000]


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

    def __init__(self, clock: GlobalClock, parent: QWidget | None = None) -> None:
        """
        Инициализация главного окна.

        Args:
            clock: Глобальные часы симуляции.
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setWindowTitle("signalSimulator")

        # Компактный размер по умолчанию, занимающий не более четверти экрана
        self.resize(600, 450)
        self.setMinimumSize(500, 350)

        self._clock = clock
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

        # Чекбокс скрытых меток (замена кнопки)
        self._chk_hidden_markers = QCheckBox("Показывать скрытые метки")
        self._chk_hidden_markers.setChecked(self._hidden_markers_visible)
        self._chk_hidden_markers.setToolTip("Включите для отображения скрытых меток неисправностей на графиках.")
        layout.addWidget(self._chk_hidden_markers)

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
        self._btn_settings_plot = QPushButton("⚙️ Настройки графика")
        self._btn_remove_plot = QPushButton("🗑 Удалить график")

        self._btn_open_plot.setEnabled(False)
        self._btn_settings_plot.setEnabled(False)
        self._btn_remove_plot.setEnabled(False)

        buttons_layout.addWidget(self._btn_add_plot)
        buttons_layout.addWidget(self._btn_open_plot)
        buttons_layout.addWidget(self._btn_settings_plot)
        buttons_layout.addWidget(self._btn_remove_plot)
        layout.addLayout(buttons_layout)

        return panel

    def _connect_signals(self) -> None:
        """Подключение внутренних сигналов."""
        # Управление временем
        self._btn_start.clicked.connect(self._on_start)
        self._btn_stop.clicked.connect(self._on_stop)
        self._btn_reset.clicked.connect(self._on_reset)

        # Скрытые метки (используем stateChanged для чекбокса)
        self._chk_hidden_markers.stateChanged.connect(self._on_toggle_hidden_markers)

        # Управление графиками
        self._btn_add_plot.clicked.connect(self._on_add_plot)
        self._btn_open_plot.clicked.connect(self._on_open_plot)
        self._btn_settings_plot.clicked.connect(self._on_plot_settings)
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

    def get_selected_plot_id(self) -> str | None:
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

            # Уведомляем координатора о необходимости очистки данных графиков
            self.reset_requested.emit()

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
            self._hidden_markers_visible = self._chk_hidden_markers.isChecked()
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

    def _on_plot_settings(self) -> None:
        """Запрос на изменение настроек выбранного графика."""
        plot_id = self.get_selected_plot_id()
        if plot_id:
            logger.debug(f"Запрос на изменение настроек графика '{plot_id}'.")
            self.plot_settings_requested.emit(plot_id)
        else:
            logger.warning("Не выбран график для изменения настроек.")

    def _on_remove_plot(self) -> None:
        """Запрос на удаление выбранного графика."""
        plot_id = self.get_selected_plot_id()
        if plot_id:
            logger.debug(f"Запрос на удаление графика '{plot_id}'.")
            self.plot_remove_requested.emit(plot_id)
        else:
            logger.warning("Не выбран график для удаления.")

    def _on_plot_selection_changed(self, current: QListWidgetItem | None, previous) -> None:
        """Обработка изменения выбора в списке графиков."""
        has_selection = current is not None
        self._btn_open_plot.setEnabled(has_selection)
        self._btn_settings_plot.setEnabled(has_selection)
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
        """Запрос на сохранение текущей конфигурации в файл."""
        try:
            filepath, _ = QFileDialog.getSaveFileName(
                self, "Сохранить конфигурацию", "",
                "Конфигурация (*.json)"
            )
            if filepath:
                # Делегируем сохранение координатору
                self.save_config_requested.emit(filepath)
            else:
                logger.debug("Сохранение конфигурации отменено пользователем.")
        except Exception as e:
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
                # Делегируем загрузку координатору
                self.load_config_requested.emit(filepath)
            else:
                logger.debug("Загрузка конфигурации отменена пользователем.")
        except Exception as e:
            logger.error(f"Непредвиденная ошибка при запросе загрузки: {e}")
            QMessageBox.critical(self, "Ошибка", f"Непредвиденная ошибка:\n{e}")
