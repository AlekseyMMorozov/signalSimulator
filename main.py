"""
main.py
Точка входа в приложение signalSimulator.
Инициализирует все компоненты системы (часы, журнал, движок, планировщик, окна)
и координирует их взаимодействие через паттерн Coordinator.
"""

import logging
import sys

from PyQt6.QtWidgets import QApplication

from analytics.detector import AnomalyDetector
from core.clock import GlobalClock
from core.config import ConfigManager
from core.event_log import EventLog
from simulation.scheduler import FaultScheduler
from simulation.signals import SignalFactory
from simulation.simulator import SimulationEngine
from ui.fault_window import FaultWindow
from ui.log_window import LogWindow
from ui.main_window import MainWindow
from ui.plot_creation_dialog import PlotCreationDialog
from ui.plot_window import PlotWindow

# Настройка базового логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


class Coordinator:
    """
    Координатор приложения.

    Связывает компоненты бизнес-логики (движок, часы, планировщик)
    с компонентами пользовательского интерфейса, обрабатывая сигналы
    и перенаправляя данные между ними.
    """

    def __init__(self) -> None:
        """Инициализация всех компонентов и подключение сигналов."""
        # Ядро
        self.clock = GlobalClock()
        self.event_log = EventLog()
        self.config_manager = ConfigManager()

        # Симуляция
        self.scheduler = FaultScheduler()
        self.engine = SimulationEngine(self.clock, self.event_log, self.scheduler)

        # Интерфейс
        self.main_window = MainWindow(self.clock)
        self.log_window = LogWindow(self.event_log)
        self.fault_window = FaultWindow(self.scheduler, self.engine)

        # Состояние
        self.plot_windows: dict[str, PlotWindow] = {}
        self.detectors: dict[str, AnomalyDetector] = {}
        self._hidden_markers_visible = False

        self._connect_signals()
        logger.info("Координатор инициализирован.")

    def _connect_signals(self) -> None:
        """Подключение всех сигналов и слотов."""
        try:
            # Главное окно
            self.main_window.plot_add_requested.connect(self._on_add_plot)
            self.main_window.plot_open_requested.connect(self._on_open_plot)
            self.main_window.plot_remove_requested.connect(self._on_remove_plot)
            self.main_window.journal_toggled.connect(self._on_toggle_journal)
            self.main_window.hidden_markers_toggled.connect(self._on_toggle_hidden_markers)

            # Движок симуляции
            self.engine.plot_data_updated.connect(self._on_plot_data_updated)

            # Окно неисправностей
            self.fault_window.fault_injected.connect(self._on_fault_injected)

            logger.debug("Сигналы координатора подключены.")
        except Exception as e:
            logger.error(f"Ошибка подключения сигналов: {e}")

    def _on_add_plot(self) -> None:
        """Обработка запроса на создание нового графика."""
        try:
            dialog = PlotCreationDialog(self.main_window)
            if dialog.exec() == dialog.DialogCode.Accepted:
                params = dialog.get_plot_params()
                if params:
                    plot_id = f"plot_{len(self.engine.get_all_plot_ids()) + 1}"
                    signal = SignalFactory.create(params["signal_type"], params["signal_params"])

                    # Добавляем в движок
                    self.engine.add_plot(
                        plot_id=plot_id,
                        name=params["name"],
                        unit=params["unit"],
                        max_unit_value=params["max_unit_value"],
                        signal=signal,
                        min_allowed=params["min_allowed"],
                        max_allowed=params["max_allowed"],
                        observation_interval_ms=params["observation_interval_ms"]
                    )

                    # Обновляем главное окно
                    self.main_window.add_plot_to_list(plot_id, params["name"])

                    # Создаем детектор для графика
                    self.detectors[plot_id] = AnomalyDetector(
                        min_allowed=params["min_allowed"],
                        max_allowed=params["max_allowed"]
                    )

                    # Создаем и настраиваем окно графика
                    plot_window = PlotWindow(
                        plot_id=plot_id,
                        name=params["name"],
                        unit=params["unit"],
                        min_allowed=params["min_allowed"],
                        max_allowed=params["max_allowed"],
                        observation_interval_ms=params["observation_interval_ms"]
                    )
                    plot_window.detection_requested.connect(self._on_operator_detection)
                    plot_window.window_closed.connect(self._on_plot_window_closed)
                    plot_window.set_hidden_markers_visible(self._hidden_markers_visible)

                    self.plot_windows[plot_id] = plot_window
                    plot_window.show()

                    logger.info(f"График '{plot_id}' успешно создан.")
        except Exception as e:
            logger.error(f"Ошибка при создании графика: {e}")

    def _on_open_plot(self, plot_id: str) -> None:
        """Показать существующее окно графика."""
        try:
            if plot_id in self.plot_windows:
                self.plot_windows[plot_id].show()
                self.plot_windows[plot_id].raise_()
                self.plot_windows[plot_id].activateWindow()
        except Exception as e:
            logger.error(f"Ошибка при открытии графика '{plot_id}': {e}")

    def _on_remove_plot(self, plot_id: str) -> None:
        """Удаление графика из симуляции и закрытие его окна."""
        try:
            self.engine.remove_plot(plot_id)
            self.main_window.remove_plot_from_list(plot_id)

            if plot_id in self.plot_windows:
                self.plot_windows[plot_id].close()
                del self.plot_windows[plot_id]
            if plot_id in self.detectors:
                del self.detectors[plot_id]

            logger.info(f"График '{plot_id}' удален.")
        except Exception as e:
            logger.error(f"Ошибка при удалении графика '{plot_id}': {e}")

    def _on_toggle_journal(self, visible: bool) -> None:
        """Показать или скрыть окно журнала событий."""
        try:
            if visible:
                self.log_window.show()
            else:
                self.log_window.hide()
        except Exception as e:
            logger.error(f"Ошибка переключения журнала: {e}")

    def _on_toggle_hidden_markers(self, visible: bool) -> None:
        """Обновить видимость скрытых меток во всех открытых окнах графиков."""
        try:
            self._hidden_markers_visible = visible
            for pw in self.plot_windows.values():
                pw.set_hidden_markers_visible(visible)
        except Exception as e:
            logger.error(f"Ошибка переключения скрытых меток: {e}")

    def _on_plot_data_updated(self, plot_id: str, data: tuple) -> None:
        """
        Обработка новых данных графика.
        Обновляет окно графика и прогоняет данные через детектор аномалий.
        """
        try:
            times, values = data

            # Обновление UI
            if plot_id in self.plot_windows:
                self.plot_windows[plot_id].update_data(list(times), list(values))

            # Анализ детектором
            if plot_id in self.detectors:
                detector = self.detectors[plot_id]
                detected_in_batch = False

                for t, v in zip(times, values):
                    detections = detector.process(t, v)
                    if detections and not detected_in_batch:
                        self.engine.record_detector_detection(plot_id)
                        if plot_id in self.plot_windows:
                            self.plot_windows[plot_id].add_detector_marker(t)
                        detected_in_batch = True  # Избегаем множественных маркеров за один пакет
        except Exception as e:
            logger.error(f"Ошибка обработки данных графика '{plot_id}': {e}")

    def _on_fault_injected(self, plot_id: str, fault_type: str, fault_params: dict) -> None:
        """Добавление скрытой метки неисправности в окно графика при ручном внедрении."""
        try:
            if plot_id in self.plot_windows:
                current_time = self.clock.get_current_time_ms()
                self.plot_windows[plot_id].add_fault_marker(current_time, fault_type)
        except Exception as e:
            logger.error(f"Ошибка добавления метки неисправности: {e}")

    def _on_operator_detection(self, plot_id: str) -> None:
        """Фиксация обнаружения оператором и добавление метки."""
        try:
            self.engine.record_operator_detection(plot_id)
            if plot_id in self.plot_windows:
                current_time = self.clock.get_current_time_ms()
                self.plot_windows[plot_id].add_operator_marker(current_time)
        except Exception as e:
            logger.error(f"Ошибка фиксации обнаружения оператором: {e}")

    def _on_plot_window_closed(self, plot_id: str) -> None:
        """Обработка закрытия окна графика пользователем (удаление из словаря)."""
        try:
            if plot_id in self.plot_windows:
                del self.plot_windows[plot_id]
                logger.debug(f"Окно графика '{plot_id}' закрыто и удалено из координатора.")
        except Exception as e:
            logger.error(f"Ошибка при обработке закрытия окна '{plot_id}': {e}")


def main() -> None:
    """Точка входа в приложение."""
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("signalSimulator")

        coordinator = Coordinator()
        coordinator.main_window.show()

        logger.info("Приложение signalSimulator запущено.")
        sys.exit(app.exec())
    except Exception as e:
        logger.critical(f"Критическая ошибка при запуске приложения: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
