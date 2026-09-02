"""
ui/panels/plots_panel.py

Панель управления графиками симуляции.
Содержит список активных графиков и кнопки для добавления, открытия,
настройки и удаления графиков.

Эмитирует сигналы с идентификатором выбранного графика для координатора.
"""

import logging

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

logger = logging.getLogger(__name__)


class PlotsPanel(QWidget):
    """
    Панель управления графиками.

    Signals:
        add_requested: Запрос на создание нового графика.
        open_requested: Запрос на открытие окна выбранного графика (plot_id).
        settings_requested: Запрос на изменение настроек выбранного графика (plot_id).
        remove_requested: Запрос на удаление выбранного графика (plot_id).
    """

    add_requested = pyqtSignal()
    open_requested = pyqtSignal(str)
    settings_requested = pyqtSignal(str)
    remove_requested = pyqtSignal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Инициализация панели управления графиками.

        Args:
            parent: Родительский виджет.
        """
        super().__init__(parent)

        try:
            self._init_ui()
            self._connect_signals()
            logger.debug("Панель управления графиками инициализирована.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка инициализации панели управления графиками: {e}")
            raise

    def _init_ui(self) -> None:
        """Создание интерфейса панели управления графиками."""
        layout = QVBoxLayout(self)
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

        # Кнопки действий неактивны, пока не выбран график
        self._btn_open_plot.setEnabled(False)
        self._btn_settings_plot.setEnabled(False)
        self._btn_remove_plot.setEnabled(False)

        buttons_layout.addWidget(self._btn_add_plot)
        buttons_layout.addWidget(self._btn_open_plot)
        buttons_layout.addWidget(self._btn_settings_plot)
        buttons_layout.addWidget(self._btn_remove_plot)
        layout.addLayout(buttons_layout)

    def _connect_signals(self) -> None:
        """Подключение внутренних сигналов панели."""
        self._btn_add_plot.clicked.connect(self.add_requested.emit)
        self._btn_open_plot.clicked.connect(self._on_open_plot)
        self._btn_settings_plot.clicked.connect(self._on_settings_plot)
        self._btn_remove_plot.clicked.connect(self._on_remove_plot)
        self._plots_list.currentItemChanged.connect(self._on_selection_changed)

    def add_item(self, plot_id: str, name: str) -> None:
        """
        Добавить график в список на панели.

        Args:
            plot_id: Идентификатор графика.
            name: Отображаемое название графика.
        """
        try:
            item = QListWidgetItem(f"{name} [{plot_id}]")
            item.setData(Qt.ItemDataRole.UserRole, plot_id)
            self._plots_list.addItem(item)
            logger.info(f"График '{name}' добавлен в список панели.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка добавления графика в список панели: {e}")

    def remove_item(self, plot_id: str) -> None:
        """
        Удалить график из списка на панели.

        Args:
            plot_id: Идентификатор графика.
        """
        try:
            for i in range(self._plots_list.count()):
                item = self._plots_list.item(i)
                if item is not None and item.data(Qt.ItemDataRole.UserRole) == plot_id:
                    self._plots_list.takeItem(i)
                    logger.info(f"График '{plot_id}' удалён из списка панели.")
                    return
            logger.warning(f"График '{plot_id}' не найден в списке панели для удаления.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка удаления графика из списка панели: {e}")

    def get_selected_plot_id(self) -> str | None:
        """
        Получить идентификатор выбранного графика.

        Returns:
            str | None: Идентификатор выбранного графика или None, если ничего не выбрано.
        """
        item = self._plots_list.currentItem()
        if item is not None:
            return item.data(Qt.ItemDataRole.UserRole)
        return None

    def _on_open_plot(self) -> None:
        """Обработка нажатия кнопки 'Открыть'."""
        plot_id = self.get_selected_plot_id()
        if plot_id:
            self.open_requested.emit(plot_id)
        else:
            logger.warning("Не выбран график для открытия.")

    def _on_settings_plot(self) -> None:
        """Обработка нажатия кнопки 'Настройки'."""
        plot_id = self.get_selected_plot_id()
        if plot_id:
            self.settings_requested.emit(plot_id)
        else:
            logger.warning("Не выбран график для изменения настроек.")

    def _on_remove_plot(self) -> None:
        """Обработка нажатия кнопки 'Удалить'."""
        plot_id = self.get_selected_plot_id()
        if plot_id:
            self.remove_requested.emit(plot_id)
        else:
            logger.warning("Не выбран график для удаления.")

    def _on_selection_changed(self, current: QListWidgetItem | None, previous: QListWidgetItem | None) -> None:
        """Обработка изменения выбора в списке графиков."""
        has_selection = current is not None
        self._btn_open_plot.setEnabled(has_selection)
        self._btn_settings_plot.setEnabled(has_selection)
        self._btn_remove_plot.setEnabled(has_selection)
