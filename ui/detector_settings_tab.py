"""
ui/detector_settings_tab.py

Вкладка настроек детектора аномалий для диалога создания/редактирования графика.
Позволяет настроить параметры скользящего окна, пороги сигм, автокалибровку тренда
и уровень толерантности к шуму без отключения самих проверок.
"""

import logging

from PyQt6.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from analytics.detector import DetectorConfig

logger = logging.getLogger(__name__)


class DetectorSettingsTab(QWidget):
    """
    Виджет вкладки настроек детектора.

    Предоставляет элементы управления для конфигурации `DetectorConfig`,
    включая размер окна, множители сигмы, пороги тренда и толерантность к шуму.
    Все виды проверок (тренд, статистика, пороги) остаются активными,
    меняется только их чувствительность.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Инициализация вкладки настроек детектора.

        Args:
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        """Создание интерфейса вкладки настроек детектора."""
        layout = QVBoxLayout(self)

        group = QGroupBox("Параметры обнаружения аномалий")
        form_layout = QFormLayout()

        # Размер окна
        self._window_size_spin = QSpinBox()
        self._window_size_spin.setRange(10, 500)
        self._window_size_spin.setValue(50)
        self._window_size_spin.setToolTip(
            "Размер скользящего окна (в точках) для статистического анализа и оценки тренда."
        )
        form_layout.addRow("Размер окна (точек):", self._window_size_spin)

        # Множитель сигмы
        self._sigma_factor_spin = QDoubleSpinBox()
        self._sigma_factor_spin.setRange(1.0, 10.0)
        self._sigma_factor_spin.setSingleStep(0.1)
        self._sigma_factor_spin.setValue(3.0)
        self._sigma_factor_spin.setToolTip(
            "Множитель стандартного отклонения (K) для порога аномалии. "
            "Рекомендуется 3.0 для чистых сигналов, 4.0–5.0 для зашумленных."
        )
        form_layout.addRow("Множитель сигмы (K):", self._sigma_factor_spin)

        # Минимальное количество образцов
        self._min_samples_spin = QSpinBox()
        self._min_samples_spin.setRange(5, 100)
        self._min_samples_spin.setValue(20)
        self._min_samples_spin.setToolTip(
            "Минимальное количество точек, необходимое для начала анализа трендов и статистики. "
            "Защищает от ложных срабатываний на старте, когда данных мало."
        )
        form_layout.addRow("Мин. точек для анализа:", self._min_samples_spin)

        # Порог тренда (0.0 = авто)
        self._trend_threshold_spin = QDoubleSpinBox()
        self._trend_threshold_spin.setRange(0.0, 10.0)
        self._trend_threshold_spin.setSingleStep(0.01)
        self._trend_threshold_spin.setValue(0.0)
        self._trend_threshold_spin.setToolTip(
            "Фиксированный порог наклона тренда (ед/сек). "
            "Если установлено 0.0, используется автоматическая калибровка на основе шума (trend_auto_sigma)."
        )
        form_layout.addRow("Порог тренда (0.0 = авто):", self._trend_threshold_spin)

        # Авто-сигма для тренда
        self._trend_auto_sigma_spin = QDoubleSpinBox()
        self._trend_auto_sigma_spin.setRange(1.0, 10.0)
        self._trend_auto_sigma_spin.setSingleStep(0.1)
        self._trend_auto_sigma_spin.setValue(3.0)
        self._trend_auto_sigma_spin.setToolTip(
            "Множитель стандартной ошибки наклона для автоматического порога тренда. "
            "Используется, если 'Порог тренда' равен 0.0."
        )
        form_layout.addRow("Авто-сигма тренда:", self._trend_auto_sigma_spin)

        # Толерантность к шуму (подготовка для будущей логики в detector.py)
        self._noise_tolerance_spin = QDoubleSpinBox()
        self._noise_tolerance_spin.setRange(0.0, 1.0)
        self._noise_tolerance_spin.setSingleStep(0.1)
        self._noise_tolerance_spin.setValue(0.0)
        self._noise_tolerance_spin.setToolTip(
            "Уровень толерантности к высокочастотному шуму (0.0 - 1.0). "
            "Увеличение значения повышает устойчивость детектора к шумовым всплескам, "
            "но может незначительно увеличить задержку обнаружения резких аномалий."
        )
        form_layout.addRow("Толерантность к шуму:", self._noise_tolerance_spin)

        group.setLayout(form_layout)
        layout.addWidget(group)
        layout.addStretch(1)

        logger.debug("Интерфейс вкладки настроек детектора создан.")

    def get_config(self) -> DetectorConfig:
        """
        Считать текущие значения из интерфейса и вернуть объект DetectorConfig.

        Returns:
            DetectorConfig: Текущая конфигурация детектора.
        """
        try:
            trend_threshold = self._trend_threshold_spin.value()
            # Если 0.0, передаем None, чтобы детектор использовал авто-режим
            threshold_val = None if trend_threshold == 0.0 else trend_threshold

            return DetectorConfig(
                window_size=self._window_size_spin.value(),
                sigma_factor=self._sigma_factor_spin.value(),
                trend_threshold=threshold_val,
                trend_auto_sigma=self._trend_auto_sigma_spin.value(),
                min_samples=self._min_samples_spin.value(),
            )
        except Exception as e:
            logger.error(f"Ошибка считывания конфигурации детектора: {e}")
            return DetectorConfig()

    def set_config(self, config: DetectorConfig) -> None:
        """
        Заполнить интерфейс значениями из переданного объекта DetectorConfig.

        Args:
            config: Конфигурация детектора для загрузки.
        """
        try:
            self._window_size_spin.setValue(config.window_size)
            self._sigma_factor_spin.setValue(config.sigma_factor)
            self._min_samples_spin.setValue(config.min_samples)
            self._trend_auto_sigma_spin.setValue(config.trend_auto_sigma)

            # Обработка None для trend_threshold (возвращаем к 0.0 для UI)
            threshold = config.trend_threshold if config.trend_threshold is not None else 0.0
            self._trend_threshold_spin.setValue(threshold)

            # Примечание: поле noise_tolerance пока не сохранено в DetectorConfig,
            # оно будет добавлено в analytics/detector.py на следующих итерациях.

            logger.debug("Настройки детектора загружены в интерфейс.")
        except Exception as e:
            logger.error(f"Ошибка загрузки конфигурации детектора в интерфейс: {e}")
