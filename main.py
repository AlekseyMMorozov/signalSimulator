"""
main.py
Точка входа в приложение signalSimulator.
Инициализирует все компоненты системы (часы, журнал, движок, планировщик, окна)
и координирует их взаимодействие через паттерн Coordinator.

Детектор аномалий теперь полностью управляется движком симуляции (SimulationEngine),
координатор только подписывается на события журнала для визуализации меток на графиках.
"""

import json
import logging
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMessageBox

from core.clock import GlobalClock
from core.config import ConfigManager
from core.event_log import EventLog, EventRecord, EventType
from analytics.detector import DetectorConfig
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

    Детектор аномалий живёт внутри PlotState (в движке симуляции).
    Координатор не хранит отдельные экземпляры детекторов и не прогоняет
    через них данные — это делает движок при генерации точек.
    Координатор только подписывается на события журнала для визуализации
    меток обнаружений на графиках.
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
            self.main_window.plot_settings_requested.connect(self._on_plot_settings)
            self.main_window.reset_requested.connect(self._on_reset)
            self.main_window.journal_toggled.connect(self._on_toggle_journal)
            self.main_window.hidden_markers_toggled.connect(self._on_toggle_hidden_markers)
            self.main_window.window_closed.connect(self._on_main_window_closed)

            # Сигналы сохранения и загрузки конфигурации
            self.main_window.save_config_requested.connect(self._on_save_config_requested)
            self.main_window.load_config_requested.connect(self._on_load_config_requested)

            # Движок симуляции (только данные для UI)
            self.engine.plot_data_updated.connect(self._on_plot_data_updated)

            # Журнал событий — для визуализации меток детектора на графиках
            self.event_log.event_added.connect(self._on_event_added)

            # Окно неисправностей
            self.fault_window.fault_injected.connect(self._on_fault_injected)

            logger.debug("Сигналы координатора подключены.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка подключения сигналов: {e}")

    def _on_main_window_closed(self) -> None:
        """
        Обработка закрытия главного окна.
        Закрывает все остальные окна (что сохраняет их геометрию) и завершает приложение.
        """
        try:
            logger.info("Главное окно закрыто. Завершение работы приложения.")
            self.log_window.close()
            self.fault_window.close()
            for pw in list(self.plot_windows.values()):
                pw.close()
            QApplication.instance().quit()
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка при закрытии приложения: {e}")

    def _on_add_plot(self) -> None:
        """Обработка запроса на создание нового графика."""
        try:
            dialog = PlotCreationDialog(self.main_window)
            if dialog.exec() == dialog.DialogCode.Accepted:
                params = dialog.get_plot_params()
                if params:
                    plot_id = f"plot_{len(self.engine.get_all_plot_ids()) + 1}"
                    signal = SignalFactory.create(params["signal_type"], params["signal_params"])

                    # Парсим конфигурацию детектора и гарантируем, что signal_type установлен
                    detector_config_dict = params.get("detector_config", {})
                    detector_config = DetectorConfig.from_dict(detector_config_dict)
                    detector_config.signal_type = params["signal_type"]

                    # Добавляем в движок (детектор создаётся внутри PlotState)
                    self.engine.add_plot(
                        plot_id=plot_id,
                        name=params["name"],
                        unit=params["unit"],
                        max_unit_value=params["max_unit_value"],
                        signal=signal,
                        min_allowed=params["min_allowed"],
                        max_allowed=params["max_allowed"],
                        observation_interval_ms=params["observation_interval_ms"],
                        detector_config=detector_config,
                    )

                    # Обновляем главное окно
                    self.main_window.add_plot_to_list(plot_id, params["name"])

                    # Создаем и настраиваем окно графика
                    plot_window = PlotWindow(
                        plot_id=plot_id,
                        name=params["name"],
                        unit=params["unit"],
                        min_allowed=params["min_allowed"],
                        max_allowed=params["max_allowed"],
                        observation_interval_ms=params["observation_interval_ms"]
                    )

                    # Предотвращаем физическое уничтожение виджета при нажатии на крестик,
                    # чтобы окно можно было повторно открыть через кнопку "Просмотр".
                    plot_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)

                    plot_window.detection_requested.connect(self._on_operator_detection)
                    plot_window.window_closed.connect(self._on_plot_window_closed)
                    plot_window.set_hidden_markers_visible(self._hidden_markers_visible)

                    self.plot_windows[plot_id] = plot_window
                    plot_window.show()

                    logger.info(f"График '{plot_id}' успешно создан и открыт.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка при создании графика: {e}")

    def _on_open_plot(self, plot_id: str) -> None:
        """Показать существующее окно графика."""
        try:
            if plot_id in self.plot_windows:
                self.plot_windows[plot_id].show()
                self.plot_windows[plot_id].raise_()
                self.plot_windows[plot_id].activateWindow()
                logger.debug(f"Окно графика '{plot_id}' отображено.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка при открытии графика '{plot_id}': {e}")

    def _on_plot_settings(self, plot_id: str) -> None:
        """Обработка запроса на изменение настроек существующего графика."""
        try:
            plot_state = self.engine.get_plot(plot_id)
            if not plot_state:
                logger.warning(f"График '{plot_id}' не найден в движке.")
                return

            # Определяем тип сигнала по имени класса (например, 'SineSignal' -> 'sine')
            signal_class_name = type(plot_state.signal).__name__
            signal_type = signal_class_name.replace("Signal", "").lower()

            initial_params = {
                "name": plot_state.name,
                "unit": plot_state.unit,
                "max_unit_value": plot_state.max_unit_value,
                "min_allowed": plot_state.min_allowed,
                "max_allowed": plot_state.max_allowed,
                "observation_interval_ms": plot_state.observation_interval_ms,
                "signal_type": signal_type,
                "signal_params": plot_state.signal.get_params(),
                "detector_config": plot_state.detector_config.to_dict(),
            }

            dialog = PlotCreationDialog(self.main_window, initial_params=initial_params)
            if dialog.exec() == dialog.DialogCode.Accepted:
                params = dialog.get_plot_params()
                if params:
                    # 1. Обновляем состояние в движке
                    plot_state.name = params["name"]
                    plot_state.unit = params["unit"]
                    plot_state.max_unit_value = params["max_unit_value"]
                    plot_state.min_allowed = params["min_allowed"]
                    plot_state.max_allowed = params["max_allowed"]
                    plot_state.observation_interval_ms = params["observation_interval_ms"]
                    plot_state.signal = SignalFactory.create(params["signal_type"], params["signal_params"])

                    # 2. Обновляем конфигурацию детектора через движок
                    #    (пересоздаёт детектор с новыми параметрами и типом сигнала)
                    detector_config_dict = params.get("detector_config", {})
                    new_detector_config = DetectorConfig.from_dict(detector_config_dict)
                    new_detector_config.signal_type = params["signal_type"]
                    self.engine.update_plot_detector_config(plot_id, new_detector_config)

                    # 3. Обновляем список в главном окне
                    self.main_window.remove_plot_from_list(plot_id)
                    self.main_window.add_plot_to_list(plot_id, params["name"])

                    # 4. Обновляем открытое окно графика (если оно есть) через публичный метод
                    if plot_id in self.plot_windows:
                        self.plot_windows[plot_id].update_settings(
                            name=params["name"],
                            unit=params["unit"],
                            min_allowed=params["min_allowed"],
                            max_allowed=params["max_allowed"],
                            observation_interval_ms=params["observation_interval_ms"]
                        )
                        # Очищаем старые данные и метки графика после смены настроек
                        self.plot_windows[plot_id].clear_data()

                    logger.info(f"Настройки графика '{plot_id}' успешно обновлены.")
                    QMessageBox.information(
                        self.main_window,
                        "Успех",
                        f"Настройки графика '{params['name']}' успешно обновлены."
                    )
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка при обработке запроса настроек графика '{plot_id}': {e}")
            QMessageBox.critical(self.main_window, "Ошибка", f"Не удалось обновить настройки:\n{e}")

    def _on_reset(self) -> None:
        """Обработка запроса на сброс симуляции: очистка данных графиков и детекторов."""
        try:
            # Сброс движка симуляции (очищает историю, метки и детекторы на уровне движка)
            self.engine.reset()

            # Сброс всех окон графиков
            for pw in self.plot_windows.values():
                pw.clear_data()

            logger.info("Симуляция и все графики сброшены.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка при сбросе симуляции: {e}")

    def _on_remove_plot(self, plot_id: str) -> None:
        """Удаление графика из симуляции и корректное уничтожение его окна."""
        try:
            self.engine.remove_plot(plot_id)
            self.main_window.remove_plot_from_list(plot_id)

            if plot_id in self.plot_windows:
                # deleteLater гарантирует безопасное и полное уничтожение виджета Qt
                self.plot_windows[plot_id].deleteLater()
                del self.plot_windows[plot_id]

            logger.info(f"График '{plot_id}' полностью удален.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка при удалении графика '{plot_id}': {e}")

    def _on_toggle_journal(self, visible: bool) -> None:
        """Показать или скрыть окно журнала событий."""
        try:
            if visible:
                self.log_window.show()
            else:
                self.log_window.hide()
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка переключения журнала: {e}")

    def _on_toggle_hidden_markers(self, visible: bool) -> None:
        """Обновить видимость скрытых меток во всех открытых окнах графиков."""
        try:
            self._hidden_markers_visible = visible
            for pw in self.plot_windows.values():
                pw.set_hidden_markers_visible(visible)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка переключения скрытых меток: {e}")

    def _on_plot_data_updated(self, plot_id: str, data: tuple) -> None:
        """
        Обработка новых данных графика.
        Только обновляет окно графика. Детектор работает внутри движка
        при генерации точек, его результаты приходят через сигнал event_added.
        """
        try:
            times, values = data

            # Обновление UI
            if plot_id in self.plot_windows:
                self.plot_windows[plot_id].update_data(list(times), list(values))

        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обработки данных графика '{plot_id}': {e}")

    def _on_event_added(self, record: EventRecord) -> None:
        """
        Обработчик новых событий журнала.
        При обнаружении детектором аномалии добавляет визуальную метку на график.
        """
        try:
            if record.event_type != EventType.DETECTOR_DETECTION:
                return

            plot_id = record.plot_id
            if not plot_id or plot_id not in self.plot_windows:
                return

            # Добавляем визуальную метку детектора на график
            self.plot_windows[plot_id].add_detector_marker(record.time_ms)
            logger.debug(
                f"Добавлена метка детектора на график '{plot_id}' "
                f"в {record.time_ms} мс: {record.description}"
            )
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обработки события журнала: {e}")

    def _on_fault_injected(self, plot_id: str, fault_type: str, fault_params: dict) -> None:
        """Добавление скрытой метки неисправности в окно графика при ручном внедрении."""
        try:
            if plot_id in self.plot_windows:
                current_time = self.clock.get_current_time_ms()
                self.plot_windows[plot_id].add_fault_marker(current_time, fault_type)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка добавления метки неисправности: {e}")

    def _on_operator_detection(self, plot_id: str) -> None:
        """Фиксация обнаружения оператором и добавление метки."""
        try:
            self.engine.record_operator_detection(plot_id)
            if plot_id in self.plot_windows:
                current_time = self.clock.get_current_time_ms()
                self.plot_windows[plot_id].add_operator_marker(current_time)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка фиксации обнаружения оператором: {e}")

    def _on_plot_window_closed(self, plot_id: str) -> None:
        """Обработка закрытия окна графика пользователем (окно скрывается, но остается в памяти)."""
        try:
            # Окно намеренно не удаляется из словаря self.plot_windows,
            # чтобы кнопка "Просмотр" на главном окне могла его снова отобразить.
            logger.debug(f"Окно графика '{plot_id}' скрыто и доступно для повторного открытия.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка при обработке скрытия окна '{plot_id}': {e}")

    def _collect_current_config(self) -> dict:
        """
        Собрать текущую конфигурацию всех графиков и их детекторов для сохранения.

        Returns:
            dict: Словарь с данными конфигурации.
        """
        config = {"plots": []}
        for plot_id in self.engine.get_all_plot_ids():
            plot_state = self.engine.get_plot(plot_id)
            if plot_state:
                signal_class_name = type(plot_state.signal).__name__
                signal_type = signal_class_name.replace("Signal", "").lower()

                plot_data = {
                    "plot_id": plot_id,
                    "name": plot_state.name,
                    "unit": plot_state.unit,
                    "max_unit_value": plot_state.max_unit_value,
                    "min_allowed": plot_state.min_allowed,
                    "max_allowed": plot_state.max_allowed,
                    "observation_interval_ms": plot_state.observation_interval_ms,
                    "signal_type": signal_type,
                    "signal_params": plot_state.signal.get_params(),
                    "detector_config": plot_state.detector_config.to_dict(),
                }
                config["plots"].append(plot_data)
        return config

    def _on_save_config_requested(self, filepath: str) -> None:
        """
        Обработка запроса на сохранение конфигурации в указанный файл.

        Args:
            filepath: Путь к файлу для сохранения.
        """
        try:
            config_data = self._collect_current_config()
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
            logger.info(f"Конфигурация успешно сохранена в {filepath}")
            QMessageBox.information(
                self.main_window, "Успех", f"Конфигурация сохранена:\n{filepath}"
            )
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка сохранения конфигурации: {e}")
            QMessageBox.critical(self.main_window, "Ошибка", f"Не удалось сохранить конфигурацию:\n{e}")

    def _on_load_config_requested(self, filepath: str) -> None:
        """
        Обработка запроса на загрузку конфигурации из файла и применение её к симуляции.

        Args:
            filepath: Путь к файлу конфигурации.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                config_data = json.load(f)

            # Очищаем текущие графики перед загрузкой новых
            for plot_id in list(self.engine.get_all_plot_ids()):
                self._on_remove_plot(plot_id)

            plots = config_data.get("plots", [])
            for plot_data in plots:
                plot_id = plot_data.get("plot_id", f"plot_{len(self.engine.get_all_plot_ids()) + 1}")

                # Гарантируем уникальность plot_id при загрузке во избежание коллизий
                while plot_id in self.engine.get_all_plot_ids():
                    plot_id = f"{plot_id}_copy"

                signal = SignalFactory.create(plot_data["signal_type"], plot_data.get("signal_params", {}))

                # Парсим конфигурацию детектора
                detector_cfg_dict = plot_data.get("detector_config", {})
                detector_cfg = DetectorConfig.from_dict(detector_cfg_dict)
                detector_cfg.signal_type = plot_data["signal_type"]

                self.engine.add_plot(
                    plot_id=plot_id,
                    name=plot_data["name"],
                    unit=plot_data["unit"],
                    max_unit_value=plot_data["max_unit_value"],
                    signal=signal,
                    min_allowed=plot_data["min_allowed"],
                    max_allowed=plot_data["max_allowed"],
                    observation_interval_ms=plot_data["observation_interval_ms"],
                    detector_config=detector_cfg,
                )

                self.main_window.add_plot_to_list(plot_id, plot_data["name"])

                plot_window = PlotWindow(
                    plot_id=plot_id,
                    name=plot_data["name"],
                    unit=plot_data["unit"],
                    min_allowed=plot_data["min_allowed"],
                    max_allowed=plot_data["max_allowed"],
                    observation_interval_ms=plot_data["observation_interval_ms"]
                )
                plot_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)
                plot_window.detection_requested.connect(self._on_operator_detection)
                plot_window.window_closed.connect(self._on_plot_window_closed)
                plot_window.set_hidden_markers_visible(self._hidden_markers_visible)
                self.plot_windows[plot_id] = plot_window

            logger.info(f"Загружено и применено {len(plots)} графиков из конфигурации.")
            QMessageBox.information(
                self.main_window, "Успех", f"Конфигурация успешно загружена:\n{filepath}"
            )
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка загрузки конфигурации: {e}")
            QMessageBox.critical(self.main_window, "Ошибка", f"Не удалось загрузить конфигурацию:\n{e}")


def main() -> None:
    """Точка входа в приложение."""
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("signalSimulator")

        coordinator = Coordinator()
        coordinator.main_window.show()

        logger.info("Приложение signalSimulator запущено.")
        sys.exit(app.exec())
    except Exception as e:  # noqa: BLE001
        logger.critical(f"Критическая ошибка при запуске приложения: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
