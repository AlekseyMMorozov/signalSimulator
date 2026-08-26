"""
simulation/simulator.py

Движок симуляции — центральный связующий компонент.
Объединяет часы, генераторы сигналов, неисправности, планировщик и журнал
событий. Вычисляет значения графиков на каждом тике времени с шагом
1 симуляционная секунда и обрабатывает события внедрения неисправностей.
"""

import logging
from typing import Any

import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal

from core.clock import GlobalClock
from core.event_log import EventLog, EventType
from simulation.faults import Fault, FaultChain, FaultFactory
from simulation.scheduler import FaultInjectionEvent, FaultScheduler
from simulation.signals import SignalGenerator

logger = logging.getLogger(__name__)

# Шаг генерации данных: 1 симуляционная секунда
GENERATION_STEP_MS = 1000

# Размер блока для эффективного хранения истории
HISTORY_CHUNK_SIZE = 100000


class HistoryBuffer:
    """
    Эффективный буфер истории значений сигнала.

    Хранит данные в виде блоков (чанков) `numpy` массивов, что позволяет
    работать с большими объёмами данных (например, телеметрия за несколько
    симуляционных лет) без чрезмерного потребления памяти.
    """

    def __init__(self) -> None:
        self._time_chunks: list[np.ndarray] = []
        self._value_chunks: list[np.ndarray] = []
        self._pending_times: list[int] = []
        self._pending_values: list[float] = []
        self._total_count: int = 0

    def append(self, time_ms: int, value: float) -> None:
        """Добавить точку (время, значение) в буфер."""
        self._pending_times.append(time_ms)
        self._pending_values.append(value)
        self._total_count += 1
        if len(self._pending_times) >= HISTORY_CHUNK_SIZE:
            self._flush_pending()

    def _flush_pending(self) -> None:
        """Сбросить накопленные точки в чанки `numpy`."""
        if self._pending_times:
            self._time_chunks.append(
                np.array(self._pending_times, dtype=np.int64)
            )
            self._value_chunks.append(
                np.array(self._pending_values, dtype=np.float64)
            )
            self._pending_times = []
            self._pending_values = []

    def get_all_times(self) -> np.ndarray:
        """Получить все времена как единый массив."""
        self._flush_pending()
        if not self._time_chunks:
            return np.array([], dtype=np.int64)
        return np.concatenate(self._time_chunks)

    def get_all_values(self) -> np.ndarray:
        """Получить все значения как единый массив."""
        self._flush_pending()
        if not self._value_chunks:
            return np.array([], dtype=np.float64)
        return np.concatenate(self._value_chunks)

    def get_last(self, n: int) -> tuple[np.ndarray, np.ndarray]:
        """Получить последние `n` точек (для отображения)."""
        times = self.get_all_times()
        values = self.get_all_values()
        if len(times) <= n:
            return times, values
        return times[-n:], values[-n:]

    def get_count(self) -> int:
        """Получить общее количество точек."""
        return self._total_count

    def clear(self) -> None:
        """Очистить буфер."""
        self._time_chunks.clear()
        self._value_chunks.clear()
        self._pending_times.clear()
        self._pending_values.clear()
        self._total_count = 0


class PlotState:
    """Состояние одного графика симуляции."""

    def __init__(
        self,
        plot_id: str,
        name: str,
        unit: str,
        max_unit_value: float,
        signal: SignalGenerator,
        min_allowed: float,
        max_allowed: float,
        observation_interval_ms: int
    ) -> None:
        self.plot_id = plot_id
        self.name = name
        self.unit = unit
        self.max_unit_value = max_unit_value
        self.signal = signal
        self.min_allowed = min_allowed
        self.max_allowed = max_allowed
        self.observation_interval_ms = observation_interval_ms
        self.fault_chain = FaultChain()
        self.history = HistoryBuffer()
        # Метки: время внедрения неисправностей (скрытые)
        self.fault_markers: list[dict[str, Any]] = []
        # Метки: обнаружения оператором
        self.operator_markers: list[int] = []
        # Метки: обнаружения детектором
        self.detector_markers: list[int] = []
        # Время последней сгенерированной точки
        self.last_generated_time_ms: int = -GENERATION_STEP_MS


class SimulationEngine(QObject):
    """
    Движок симуляции.

    Подписывается на сигнал `time_updated` глобальных часов, генерирует
    данные графиков с шагом 1 симуляционная секунда, обрабатывает события
    планировщика неисправностей и ведёт журнал событий.
    """

    # Сигнал обновления данных графика: (plot_id, (times, values))
    plot_data_updated = pyqtSignal(str, object)
    # Сигнал выхода за пределы: (plot_id, time_ms)
    limit_exceeded = pyqtSignal(str, int)

    def __init__(
        self,
        clock: GlobalClock,
        event_log: EventLog,
        scheduler: FaultScheduler | None = None,
        parent: QObject | None = None
    ) -> None:
        """
        Инициализация движка симуляции.

        Args:
            clock: Глобальные часы симуляции.
            event_log: Журнал событий.
            scheduler: Планировщик случайных неисправностей (опционально).
            parent: Родительский QObject.
        """
        super().__init__(parent)
        self._clock = clock
        self._event_log = event_log
        self._scheduler = scheduler
        self._plots: dict[str, PlotState] = {}
        try:
            self._clock.time_updated.connect(self._on_time_updated)
            logger.info("SimulationEngine инициализирован и подключён к часам.")
        except Exception as e:
            logger.error(f"Ошибка подключения к часам: {e}")

    def add_plot(
        self,
        plot_id: str,
        name: str,
        unit: str,
        max_unit_value: float,
        signal: SignalGenerator,
        min_allowed: float,
        max_allowed: float,
        observation_interval_ms: int
    ) -> PlotState:
        """Добавить график в симуляцию."""
        try:
            plot = PlotState(
                plot_id=plot_id,
                name=name,
                unit=unit,
                max_unit_value=max_unit_value,
                signal=signal,
                min_allowed=min_allowed,
                max_allowed=max_allowed,
                observation_interval_ms=observation_interval_ms,
            )
            self._plots[plot_id] = plot
            self._event_log.add(
                time_ms=self._clock.get_current_time_ms(),
                event_type=EventType.PLOT_CREATED,
                description=f"Создан график: {name}",
                plot_id=plot_id,
                metadata={"unit": unit, "min_allowed": min_allowed, "max_allowed": max_allowed},
            )
            logger.info(f"Добавлен график '{plot_id}' ({name}).")
            return plot
        except Exception as e:
            logger.error(f"Ошибка добавления графика '{plot_id}': {e}")
            raise

    def remove_plot(self, plot_id: str) -> None:
        """Удалить график из симуляции."""
        try:
            if plot_id in self._plots:
                del self._plots[plot_id]
                self._event_log.add(
                    time_ms=self._clock.get_current_time_ms(),
                    event_type=EventType.PLOT_REMOVED,
                    description=f"Удалён график: {plot_id}",
                    plot_id=plot_id,
                )
                logger.info(f"Удалён график '{plot_id}'.")
            else:
                logger.warning(f"Попытка удалить несуществующий график '{plot_id}'.")
        except Exception as e:
            logger.error(f"Ошибка удаления графика '{plot_id}': {e}")

    def get_plot(self, plot_id: str) -> PlotState | None:
        """Получить состояние графика по ID."""
        return self._plots.get(plot_id)

    def get_all_plot_ids(self) -> list[str]:
        """Получить список всех идентификаторов графиков."""
        return list(self._plots.keys())

    def _on_time_updated(self, time_ms: int) -> None:
        """Обработка тика часов: генерация данных и обработка событий."""
        try:
            # Генерация данных для каждого графика
            for plot in self._plots.values():
                self._generate_points(plot, time_ms)

            # Обработка планировщика неисправностей
            if self._scheduler is not None and self._plots:
                events = self._scheduler.tick(time_ms, self.get_all_plot_ids())
                if events:
                    self.process_injection_events(events)
        except Exception as e:
            logger.error(f"Ошибка обработки тика времени {time_ms}: {e}")

    def _generate_points(self, plot: PlotState, current_time_ms: int) -> None:
        """Генерация точек для графика до текущего времени с шагом 1 секунда."""
        new_times: list[int] = []
        new_values: list[float] = []
        try:
            t = plot.last_generated_time_ms + GENERATION_STEP_MS
            while t <= current_time_ms:
                base_value = plot.signal.get_value(t)
                final_value = plot.fault_chain.apply_all(t, base_value)
                plot.history.append(t, final_value)
                new_times.append(t)
                new_values.append(final_value)

                # Проверка выхода за допустимые пределы
                if final_value < plot.min_allowed or final_value > plot.max_allowed:
                    self._event_log.add(
                        time_ms=t,
                        event_type=EventType.LIMIT_EXCEEDED,
                        description=f"Выход за пределы: {final_value:.4f} {plot.unit}",
                        plot_id=plot.plot_id,
                        metadata={"value": final_value, "min": plot.min_allowed, "max": plot.max_allowed},
                    )
                    self.limit_exceeded.emit(plot.plot_id, t)

                t += GENERATION_STEP_MS

            plot.last_generated_time_ms = current_time_ms - (current_time_ms % GENERATION_STEP_MS)

            # Испускаем сигнал с новыми данными (списком для эффективности)
            if new_times:
                self.plot_data_updated.emit(plot.plot_id, (new_times, new_values))
        except Exception as e:
            logger.error(f"Ошибка генерации точек для графика '{plot.plot_id}': {e}")

    def inject_fault(self, plot_id: str, fault_type: str, fault_params: dict[str, Any]) -> Fault | None:
        """
        Ручное внедрение неисправности на график.

        Создаёт неисправность через фабрику, добавляет в цепочку,
        активирует и фиксирует скрытую метку.

        Args:
            plot_id: Идентификатор графика.
            fault_type: Тип неисправности.
            fault_params: Параметры неисправности.

        Returns:
            Созданная неисправность или `None` при ошибке.
        """
        try:
            plot = self._plots.get(plot_id)
            if plot is None:
                logger.warning(f"Не удалось внедрить неисправность: график '{plot_id}' не найден.")
                return None

            fault = FaultFactory.create(fault_type, fault_params)
            if fault is None:
                logger.warning(f"Не удалось создать неисправность типа '{fault_type}'.")
                return None

            current_time = self._clock.get_current_time_ms()
            plot.fault_chain.add_fault(fault)
            fault.activate(current_time)

            # Фиксируем скрытую метку
            plot.fault_markers.append({
                "time_ms": current_time,
                "fault_type": fault_type,
                "fault_params": fault_params,
            })

            self._event_log.add(
                time_ms=current_time,
                event_type=EventType.FAULT_INJECTED,
                description=f"Внедрена неисправность: {fault_type}",
                plot_id=plot_id,
                metadata={"fault_type": fault_type, "fault_params": fault_params},
            )
            logger.info(f"Внедрена неисправность '{fault_type}' на график '{plot_id}' в {current_time} мс.")
            return fault
        except Exception as e:
            logger.error(f"Ошибка внедрения неисправности на график '{plot_id}': {e}")
            return None

    def process_injection_events(self, events: list[FaultInjectionEvent]) -> None:
        """
        Обработка событий внедрения от планировщика.

        Для каждого события создаёт неисправность, добавляет в цепочку
        графика, активирует и фиксирует скрытую метку.

        Args:
            events: Список событий внедрения.
        """
        for event in events:
            try:
                self.inject_fault(event.plot_id, event.fault_type, event.fault_params)
            except Exception as e:
                logger.error(f"Ошибка обработки события внедрения {event}: {e}")

    def record_operator_detection(self, plot_id: str) -> None:
        """Фиксация обнаружения неисправности оператором."""
        try:
            plot = self._plots.get(plot_id)
            if plot is None:
                logger.warning(f"Обнаружение оператора: график '{plot_id}' не найден.")
                return
            current_time = self._clock.get_current_time_ms()
            plot.operator_markers.append(current_time)
            self._event_log.add(
                time_ms=current_time,
                event_type=EventType.OPERATOR_DETECTION,
                description="Оператор обнаружил неисправность",
                plot_id=plot_id,
            )
            logger.info(f"Оператор обнаружил неисправность на графике '{plot_id}' в {current_time} мс.")
        except Exception as e:
            logger.error(f"Ошибка фиксации обнаружения оператора на '{plot_id}': {e}")

    def record_detector_detection(self, plot_id: str) -> None:
        """Фиксация обнаружения неисправности детектором."""
        try:
            plot = self._plots.get(plot_id)
            if plot is None:
                logger.warning(f"Обнаружение детектора: график '{plot_id}' не найден.")
                return
            current_time = self._clock.get_current_time_ms()
            plot.detector_markers.append(current_time)
            self._event_log.add(
                time_ms=current_time,
                event_type=EventType.DETECTOR_DETECTION,
                description="Детектор обнаружил неисправность",
                plot_id=plot_id,
            )
            logger.info(f"Детектор обнаружил неисправность на графике '{plot_id}' в {current_time} мс.")
        except Exception as e:
            logger.error(f"Ошибка фиксации обнаружения детектора на '{plot_id}': {e}")

    def reset(self) -> None:
        """Сброс состояния движка (очистка историй и меток)."""
        try:
            for plot in self._plots.values():
                plot.history.clear()
                plot.fault_markers.clear()
                plot.operator_markers.clear()
                plot.detector_markers.clear()
                plot.fault_chain.clear()
                plot.last_generated_time_ms = -GENERATION_STEP_MS
            if self._scheduler is not None:
                self._scheduler.reset()
            logger.info("Состояние движка симуляции сброшено.")
        except Exception as e:
            logger.error(f"Ошибка сброса состояния движка: {e}")
