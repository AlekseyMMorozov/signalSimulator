"""
ui/main_window.py
Главное окно приложения — центральная панель управления симуляцией.
Содержит панель управления временем, список графиков, меню и кнопки
для открытия вспомогательных окон и изменения настроек графиков.
Интерфейс оптимизирован для компактного размещения (до 1/4 экрана)
без потери видимости элементов.
"""

import logging

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFrame,
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

        # Компактный размер: не более 1/4 площади экрана (1/2 ширины * 1/2 высоты)
        # но с гарантированным минимальным размером для вмещения всех элементов
        screen = QGuiApplication.primaryScreen().availableGeometry()
        target_width = max(600, screen.width() // 2)
        target_height = max(450, screen.height() // 2)

        self.resize(target_width, target_height)
        self.setMinimumSize(600, 450)

        self._clock = clock
        self._journal_visible = False
        self._hidden_markers_visible = False

        try:
            self._init_menu()
            self._init_ui()
            self._connect_signals()
            logger.info("Главное окно инициализировано (компактный режим).")
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
        """Создание основного интерфейса с разделением на логические блоки."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        # Блок 1: Панель управления временем
        main_layout.addWidget(self._create_time_panel())

        # Разделитель
        main_layout.addWidget(self._create_separator())

        # Блок 2: Панель графиков (занимает всё доступное пространство)
        main_layout.addWidget(self._create_plots_panel(), stretch=1)

        # Разделитель
        main_layout.addWidget(self._create_separator())

        # Блок 3: Панель дополнительных настроек
        main_layout.addWidget(self._create_options_panel())

        logger.debug("Интерфейс главного окна создан.")

    def _create_separator(self) -> QFrame:
        """Создание горизонтального разделителя для визуального структурирования."""
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        return line

    def _create_time_panel(self) -> QWidget:
        """Создание панели управления временем."""
        panel = QWidget()
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        # Группа кнопок управления симуляцией
        self._btn_start = QPushButton("▶ Старт")
        self._btn_stop = QPushButton("⏸ Стоп")
        self._btn_stop.setEnabled(False)
        self._btn_reset = QPushButton("⏹ Сброс")

        layout.addWidget(self._btn_start)
        layout.addWidget(self._btn_stop)
        layout.addWidget(self._btn_reset)

        layout.addSpacing(15)
        layout.addWidget(QLabel("Скорость:"))

        # Выпадающий список множителей ускорения (вместо ряда кнопок)
        self._speed_combo = QComboBox()
        for mult in ALLOWED_MULTIPLIERS:
            self._speed_combo.addItem(f"×{mult}", mult)

        current_mult = self._clock.get_speed_multiplier()
        index = self._speed_combo.findData(current_mult)
        if index != -1:
            self._speed_combo.setCurrentIndex(index)

        self._speed_combo.setFixedWidth(80)  # Компактная ширина
        self._speed_combo.currentIndexChanged.connect(self._on_speed_change)
        layout.addWidget(self._speed_combo)

        layout.addStretch(1)

        # Отображение текущего времени (немного уменьшен шрифт для экономии места)
        self._time_label = QLabel("00:00:00.000")
        self._time_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(self._time_label)

        return panel

    def _create_plots_panel(self) -> QWidget:
        """Создание панели управления графиками."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)

        layout.addWidget(QLabel("<b>Графики телеметрии:</b>"))

        # Список графиков
        self._plots_list = QListWidget()
        self._plots_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        # Высота подбирается автоматически layout-ом, но ограничиваем разумным максимумом
        self._plots_list.setMaximumHeight(250)
        layout.addWidget(self._plots_list, stretch=1)

        # Кнопки управления графиками в одну строку
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)

        self._btn_add_plot = QPushButton("➕ Добавить")
        self._btn_open_plot = QPushButton("📈 Открыть")
        self._btn_settings_plot = QPushButton("⚙️ Настройки")
        self._btn_remove_plot = QPushButton("🗑 Удалить")

        self._btn_open_plot.setEnabled(False)
        self._btn_settings_plot.setEnabled(False)
        self._btn_remove_plot.setEnabled(False)

        buttons_layout.addWidget(self._btn_add_plot)
        buttons_layout.addWidget(self._btn_open_plot)
        buttons_layout.addWidget(self._btn_settings_plot)
        buttons_layout.addWidget(self._btn_remove_plot)
        layout.addLayout(buttons_layout)

        return panel

    def _create_options_panel(self) -> QWidget:
        """Создание панели дополнительных настроек (чекбоксы)."""
        panel = QWidget()
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(5, 0, 5, 5)
        layout.setSpacing(15)

        # Чекбокс скрытых меток
        self._chk_hidden_markers = QCheckBox("Показывать скрытые метки неисправностей")
        self._chk_hidden_markers.setChecked(self._hidden_markers_visible)
        self._chk_hidden_markers.setToolTip("Включите для отображения скрытых меток неисправностей на графиках.")
        layout.addWidget(self._chk_hidden_markers)

        layout.addStretch(1)

        # Чекбокс журнала событий (дублирует действие из меню для удобства)
        self._chk_journal = QCheckBox("Показать журнал событий")
        self._chk_journal.setChecked(self._journal_visible)
        self._chk_journal.setToolTip("Открыть или скрыть окно журнала событий.")
        layout.addWidget(self._chk_journal)

        return panel

    def _connect_signals(self) -> None:
        """Подключение внутренних сигналов."""
        # Управление временем
        self._btn_start.clicked.connect(self._on_start)
        self._btn_stop.clicked.connect(self._on_stop)
        self._btn_reset.clicked.connect(self._on_reset)

        # Скрытые метки
        self._chk_hidden_markers.stateChanged.connect(
            lambda state: self._on_toggle_hidden_markers(bool(state))
        )

        # Журнал событий (синхронизация чекбокса и действия меню)
        self._chk_journal.toggled.connect(self._on_toggle_journal)

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
        except Exception as e:  # noqa: BLE001
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
        except Exception as e:  # noqa: BLE001
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
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка запуска симуляции: {e}")

    def _on_stop(self) -> None:
        """Остановка симуляции."""
        try:
            self._clock.stop()
            self._btn_start.setEnabled(True)
            self._btn_stop.setEnabled(False)
            logger.info("Симуляция остановлена.")
        except Exception as e:  # noqa: BLE001
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
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка сброса симуляции: {e}")

    def _on_speed_change(self, index: int) -> None:
        """Изменение множителя ускорения времени через выпадающий список."""
        try:
            multiplier = self._speed_combo.itemData(index)
            if multiplier is not None:
                self._clock.set_speed_multiplier(multiplier)
                logger.info(f"Множитель ускорения изменён на ×{multiplier}.")
        except ValueError as e:
            logger.warning(f"Недопустимый множитель ускорения: {e}")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка изменения множителя: {e}")

    def _on_time_updated(self, time_ms: int) -> None:
        """Обновление отображения времени."""
        try:
            self._time_label.setText(self._clock.get_formatted_time())
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обновления времени: {e}")

    # --- Обработчики скрытых меток ---

    def _on_toggle_hidden_markers(self, checked: bool) -> None:
        """Переключение режима скрытых меток."""
        try:
            self._hidden_markers_visible = checked
            self.hidden_markers_toggled.emit(self._hidden_markers_visible)
            state = "включён" if self._hidden_markers_visible else "выключен"
            logger.info(f"Режим скрытых меток {state}.")
        except Exception as e:  # noqa: BLE001
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

    # --- Обработчики меню и опций ---

    def _on_toggle_journal(self, checked: bool) -> None:
        """Переключение видимости журнала событий (синхронизирует меню и чекбокс)."""
        try:
            self._journal_visible = checked
            self._journal_action.setChecked(checked)
            self._chk_journal.setChecked(checked)
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
                # Делегируем сохранение координатору
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
                # Делегируем загрузку координатору
                self.load_config_requested.emit(filepath)
            else:
                logger.debug("Загрузка конфигурации отменено пользователем.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Непредвиденная ошибка при запросе загрузки: {e}")
            QMessageBox.critical(self, "Ошибка", f"Непредвиденная ошибка:\n{e}")
