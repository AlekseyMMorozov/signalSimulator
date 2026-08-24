"""
ui/plot_window.py

Отдельное окно графика телеметрии с отрисовкой сигнала в реальном времени.
Содержит кривую сигнала, пределы допустимых значений, метки неисправностей
и обнаружений, а также кнопку фиксации обнаружения оператором.
Окно не зависит от движка симуляции: данные поступают через публичный
метод `update_data`, а подписку выполняет координатор (главное окно).
"""

import logging
from typing import List, Optional, Tuple

import numpy as np
import pyqtgraph as pg
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


logger = logging.getLogger(__name__)

# ============================================================================
# НАСТРАИВАЕМЫЕ ПАРАМЕТРЫ (подкрутить после первой проверки)
# ============================================================================
# Начальный размер окна: широкий и невысокий, чтобы размещать 6-8 окон
# в два столбца на экране.
DEFAULT_WIDTH = 900
DEFAULT_HEIGHT = 280
# Целевое число точек для отображения после децимации.
# Если точек меньше — отрисовываем все без прореживания.
MAX_DISPLAY_POINTS = 4000
# Цвета элементов графика
COLOR_SIGNAL = "b"          # кривая сигнала (синий)
COLOR_LIMIT = "r"           # пределы допустимых значений (красный)
COLOR_FAULT_MARKER = (255, 140, 0)    # скрытые метки неисправностей (оранжевый)
COLOR_OPERATOR_MARKER = (0, 200, 0)   # метки оператора (зелёный)
COLOR_DETECTOR_MARKER = (0, 180, 255) # метки детектора (голубой)


class PlotWindow(QMainWindow):
    """
    Окно графика телеметрии.

    Отображает сигнал в реальном времени с пределами допустимых значений,
    скрытыми метками неисправностей и метками обнаружений. Данные поступают
    через публичный метод `update_data` (слабая связанность с движком).

    Signals:
        detection_requested: Оператор нажал кнопку обнаружения (передаёт `plot_id`).
        window_closed: Окно закрыто (передаёт `plot_id`).
    """

    detection_requested = pyqtSignal(str)
    window_closed = pyqtSignal(str)

    def __init__(
        self,
        plot_id: str,
        name: str,
        unit: str,
        min_allowed: float,
        max_allowed: float,
        observation_interval_ms: int,
        parent: Optional[QWidget] = None
    ) -> None:
        """
        Инициализация окна графика.

        Args:
            plot_id: Уникальный идентификатор графика.
            name: Название графика.
            unit: Единица измерения.
            min_allowed: Минимально допустимое значение.
            max_allowed: Максимально допустимое значение.
            observation_interval_ms: Интервал наблюдения (длительность по оси X).
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.plot_id = plot_id
        self._name = name
        self._unit = unit
        self._min_allowed = float(min_allowed)
        self._max_allowed = float(max_allowed)
        self._observation_interval_ms = int(observation_interval_ms)

        # Накопленные данные (полная история для децимации)
        self._times: List[int] = []
        self._values: List[float] = []

        # Скрытые метки неисправностей: (вертикальная линия, подпись)
        self._fault_marker_items: List[Tuple[pg.InfiniteLine, pg.TextItem]] = []
        self._hidden_markers_visible = False

        try:
            self._init_ui()
            logger.info(
                f"Окно графика '{plot_id}' инициализировано. "
                f"Пределы: [{self._min_allowed}, {self._max_allowed}] {self._unit}."
            )
        except Exception as e:
            logger.error(f"Ошибка инициализации окна графика '{plot_id}': {e}")
            raise

    def _init_ui(self) -> None:
        """Создание интерфейса окна."""
        self.setWindowTitle(f"{self._name} [{self.plot_id}]")
        self.resize(DEFAULT_WIDTH, DEFAULT_HEIGHT)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)

        # --- Область графика ---
        self._plot_widget = pg.PlotWidget()
        self._plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self._plot_widget.setLabel("bottom", "Время", units="мс")
        self._plot_widget.setLabel("left", self._name, units=self._unit)

        # Кривая сигнала
        self._curve = self._plot_widget.plot(
            [], [], pen=pg.mkPen(color=COLOR_SIGNAL, width=1)
        )

        # Горизонтальные линии пределов
        self._plot_widget.addItem(
            pg.InfiniteLine(pos=self._min_allowed, angle=0,
                            pen=pg.mkPen(color=COLOR_LIMIT, width=1, style=2))
        )
        self._plot_widget.addItem(
            pg.InfiniteLine(pos=self._max_allowed, angle=0,
                            pen=pg.mkPen(color=COLOR_LIMIT, width=1, style=2))
        )

        # Диапазон оси X на весь интервал наблюдения (график умещается целиком)
        self._plot_widget.setXRange(0, self._observation_interval_ms, padding=0)
        # Автодиапазон по оси Y
        self._plot_widget.enableAutoRange(axis="y")

        layout.addWidget(self._plot_widget, stretch=1)

        # --- Нижняя панель: текущее значение и кнопка обнаружения ---
        bottom_layout = QHBoxLayout()
        self._value_label = QLabel(f"Текущее значение: — {self._unit}")
        bottom_layout.addWidget(self._value_label)
        bottom_layout.addStretch(1)

        self._btn_detect = QPushButton("🚨 Обнаружил проблему")
        self._btn_detect.clicked.connect(self._on_detect_clicked)
        bottom_layout.addWidget(self._btn_detect)

        layout.addLayout(bottom_layout)
        logger.debug("Интерфейс окна графика создан.")

    # ------------------------------------------------------------------
    # Публичные методы (вызываются координатором)
    # ------------------------------------------------------------------

    def update_data(self, times: List[int], values: List[float]) -> None:
        """
        Обновить данные графика (публичный метод для координатора).

        Новые точки добавляются к накопленной истории, после чего
        применяется децимация и выполняется перерисовка.

        Args:
            times: Список времён в миллисекундах.
            values: Список значений сигнала.
        """
        try:
            if len(times) != len(values):
                logger.warning(
                    f"Несовпадение длин данных для графика '{self.plot_id}': "
                    f"times={len(times)}, values={len(values)}."
                )
                return
            self._times.extend(times)
            self._values.extend(values)

            # Децимация для отрисовки
            disp_times, disp_values = self._decimate(self._times, self._values)
            self._curve.setData(disp_times, disp_values)

            # Обновление текущего значения
            if values:
                last_value = values[-1]
                self._value_label.setText(
                    f"Текущее значение: {last_value:.4f} {self._unit}"
                )
        except Exception as e:
            logger.error(f"Ошибка обновления данных графика '{self.plot_id}': {e}")

    def add_fault_marker(self, time_ms: int, fault_type: str) -> None:
        """
        Добавить скрытую метку неисправности (вертикальная линия + подпись типа).

        Метка видима только при включённом режиме скрытых меток.

        Args:
            time_ms: Время внедрения неисправности.
            fault_type: Тип неисправности (отображается в подписи).
        """
        try:
            line = pg.InfiniteLine(
                pos=time_ms, angle=90,
                pen=pg.mkPen(color=COLOR_FAULT_MARKER, width=1, style=2)
            )
            label = pg.TextItem(fault_type, color=COLOR_FAULT_MARKER, anchor=(0, 1))
            label.setPos(time_ms, self._max_allowed)
            self._plot_widget.addItem(line)
            self._plot_widget.addItem(label)

            line.setVisible(self._hidden_markers_visible)
            label.setVisible(self._hidden_markers_visible)

            self._fault_marker_items.append((line, label))
            logger.debug(f"Добавлена скрытая метка неисправности '{fault_type}' в {time_ms} мс.")
        except Exception as e:
            logger.error(f"Ошибка добавления скрытой метки неисправности: {e}")

    def add_operator_marker(self, time_ms: int) -> None:
        """Добавить метку обнаружения оператором (вертикальная линия)."""
        try:
            line = pg.InfiniteLine(
                pos=time_ms, angle=90,
                pen=pg.mkPen(color=COLOR_OPERATOR_MARKER, width=2)
            )
            self._plot_widget.addItem(line)
            logger.debug(f"Добавлена метка оператора в {time_ms} мс.")
        except Exception as e:
            logger.error(f"Ошибка добавления метки оператора: {e}")

    def add_detector_marker(self, time_ms: int) -> None:
        """Добавить метку обнаружения детектором (вертикальная линия)."""
        try:
            line = pg.InfiniteLine(
                pos=time_ms, angle=90,
                pen=pg.mkPen(color=COLOR_DETECTOR_MARKER, width=2, style=2)
            )
            self._plot_widget.addItem(line)
            logger.debug(f"Добавлена метка детектора в {time_ms} мс.")
        except Exception as e:
            logger.error(f"Ошибка добавления метки детектора: {e}")

    def set_hidden_markers_visible(self, visible: bool) -> None:
        """Переключить видимость скрытых меток неисправностей."""
        try:
            self._hidden_markers_visible = visible
            for line, label in self._fault_marker_items:
                line.setVisible(visible)
                label.setVisible(visible)
            state = "включён" if visible else "выключен"
            logger.debug(f"Режим скрытых меток для графика '{self.plot_id}' {state}.")
        except Exception as e:
            logger.error(f"Ошибка переключения скрытых меток: {e}")

    # ------------------------------------------------------------------
    # Внутренние методы
    # ------------------------------------------------------------------

    def _decimate(self, times: List[int], values: List[float]) -> Tuple[List[int], List[float]]:
        """
        Децимация данных для отрисовки.

        Если точек не больше `MAX_DISPLAY_POINTS` — возвращает как есть.
        Иначе применяет min-max децимацию по блокам, сохраняя пики и впадины.

        Args:
            times: Полная история времён.
            values: Полная история значений.

        Returns:
            Кортеж (прореженные времена, прореженные значения).
        """
        n = len(times)
        if n <= MAX_DISPLAY_POINTS:
            return times, values

        try:
            num_blocks = MAX_DISPLAY_POINTS // 2
            block_size = n / num_blocks
            dec_times: List[int] = []
            dec_values: List[float] = []
            values_arr = np.asarray(values, dtype=np.float64)

            for i in range(num_blocks):
                start = int(i * block_size)
                end = min(int((i + 1) * block_size), n)
                if start >= n:
                    break
                block = values_arr[start:end]
                min_idx = start + int(np.argmin(block))
                max_idx = start + int(np.argmax(block))
                # Добавляем мин и макс в хронологическом порядке
                for idx in sorted({min_idx, max_idx}):
                    dec_times.append(times[idx])
                    dec_values.append(values[idx])
            return dec_times, dec_values
        except Exception as e:
            logger.error(f"Ошибка децимации данных: {e}")
            return times, values

    def _on_detect_clicked(self) -> None:
        """Обработчик нажатия кнопки обнаружения."""
        try:
            logger.info(f"Оператор нажал кнопку обнаружения на графике '{self.plot_id}'.")
            self.detection_requested.emit(self.plot_id)
        except Exception as e:
            logger.error(f"Ошибка обработки нажатия кнопки обнаружения: {e}")

    def closeEvent(self, event) -> None:
        """Обработка закрытия окна."""
        try:
            logger.info(f"Окно графика '{self.plot_id}' закрывается.")
            self.window_closed.emit(self.plot_id)
        except Exception as e:
            logger.error(f"Ошибка при закрытии окна графика: {e}")
        super().closeEvent(event)
