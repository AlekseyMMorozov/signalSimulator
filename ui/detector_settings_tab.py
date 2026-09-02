"""
ui/detector_settings_tab.py

Вкладка настроек детектора аномалий для диалога создания/редактирования графика.
Отображает информацию об активных детекторах (тренд, аномалия, отклонение)
с пояснениями, почему они выбраны для текущего типа сигнала, и предоставляет
элементы настройки параметров каждого детектора с подробными подсказками.

Поддерживает новую архитектуру с разделением ответственности:
- Детектор тренда (модель Хольта)
- Детектор аномалий (остатки прогноза)
- Детектор отклонений (CUSUM)
"""

import logging

from PyQt6.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from analytics.detector import DetectorConfig

logger = logging.getLogger(__name__)


class DetectorSettingsTab(QWidget):
    """
    Виджет вкладки настроек детектора.

    Отображает активные детекторы для выбранного типа сигнала
    и предоставляет элементы управления для конфигурации каждого:
    - Общие параметры (окно, мин. точек, толерантность к шуму)
    - Детектор тренда (порог, авто-сигма, подтверждение временем)
    - Детектор аномалий (множитель сигмы, подтверждение временем)
    - Детектор отклонений CUSUM (дрейф, порог, адаптация базовой линии)
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
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(6)

        # Блок информации об активных детекторах
        info_group = QGroupBox("Активные детекторы")
        self._detectors_info_layout = QVBoxLayout()
        self._detectors_info_layout.setSpacing(4)
        info_group.setLayout(self._detectors_info_layout)
        layout.addWidget(info_group)

        # Группы параметров
        layout.addWidget(self._create_common_params_group())
        layout.addWidget(self._create_trend_params_group())
        layout.addWidget(self._create_anomaly_params_group())
        layout.addWidget(self._create_deviation_params_group())
        layout.addStretch(1)

        logger.debug("Интерфейс вкладки настроек детектора создан.")

    def _create_common_params_group(self) -> QGroupBox:
        """Создание группы общих параметров детекторов."""
        group = QGroupBox("Общие параметры")
        form = QFormLayout()

        self._window_size_spin = QSpinBox()
        self._window_size_spin.setRange(10, 500)
        self._window_size_spin.setValue(50)
        self._window_size_spin.setToolTip(
            "<b>Размер скользящего окна (в точках).</b><br>"
            "Определяет глубину анализа для оценки статистики шума.<br>"
            "<i>Рекомендация:</i> 10-30 для быстрой реакции, 100-500 для "
            "сильно зашумлённых сигналов."
        )
        form.addRow("Размер окна (точек):", self._window_size_spin)

        self._min_samples_spin = QSpinBox()
        self._min_samples_spin.setRange(5, 100)
        self._min_samples_spin.setValue(20)
        self._min_samples_spin.setToolTip(
            "<b>Минимальное количество точек для старта анализа.</b><br>"
            "Защита от ложных срабатываний на «холодном старте».<br>"
            "<i>Рекомендация:</i> 20–30 для большинства сигналов."
        )
        form.addRow("Мин. точек для анализа:", self._min_samples_spin)

        self._noise_tolerance_spin = QDoubleSpinBox()
        self._noise_tolerance_spin.setRange(0.0, 1.0)
        self._noise_tolerance_spin.setSingleStep(0.1)
        self._noise_tolerance_spin.setValue(0.0)
        self._noise_tolerance_spin.setToolTip(
            "<b>Толерантность к высокочастотному шуму.</b><br>"
            "Дополнительно расширяет порог срабатывания.<br>"
            "0.0 — базовый порог, 1.0 — удвоенный порог."
        )
        form.addRow("Толерантность к шуму:", self._noise_tolerance_spin)

        self._tau_corr_spin = QDoubleSpinBox()
        self._tau_corr_spin.setRange(1.0, 300.0)
        self._tau_corr_spin.setSingleStep(1.0)
        self._tau_corr_spin.setValue(10.0)
        self._tau_corr_spin.setToolTip(
            "<b>Характерное время корреляции сигнала (сек).</b><br>"
            "Используется для расширения доверительного интервала "
            "при дефиците данных (пропадание телеметрии).<br>"
            "<i>Рекомендация:</i> 10 с для быстрых сигналов, "
            "60–300 с для медленных процессов."
        )
        form.addRow("τ корреляции (сек):", self._tau_corr_spin)

        self._preprocessor_window_spin = QSpinBox()
        self._preprocessor_window_spin.setRange(10, 500)
        self._preprocessor_window_spin.setValue(100)
        self._preprocessor_window_spin.setToolTip(
            "<b>Размер окна препроцессора (в точках).</b><br>"
            "Определяет глубину анализа для извлечения информативного "
            "параметра (амплитуда, уровень плато, наклон).<br>"
            "<i>Рекомендация:</i> 50–200 для периодических сигналов."
        )
        form.addRow("Окно препроцессора:", self._preprocessor_window_spin)

        group.setLayout(form)
        return group

    def _create_trend_params_group(self) -> QGroupBox:
        """Создание группы параметров детектора тренда."""
        group = QGroupBox("📈 Детектор тренда (модель Хольта)")
        form = QFormLayout()

        self._trend_threshold_spin = QDoubleSpinBox()
        self._trend_threshold_spin.setRange(0.0, 10.0)
        self._trend_threshold_spin.setSingleStep(0.01)
        self._trend_threshold_spin.setValue(0.0)
        self._trend_threshold_spin.setToolTip(
            "<b>Фиксированный порог наклона тренда (ед/сек).</b><br>"
            "Если 0.0 — используется автоматический режим.<br>"
            "<i>Рекомендация:</i> установите конкретное значение, "
            "если известна физическая скорость деградации."
        )
        form.addRow("Порог тренда (0.0 = авто):", self._trend_threshold_spin)

        self._trend_auto_sigma_spin = QDoubleSpinBox()
        self._trend_auto_sigma_spin.setRange(1.0, 10.0)
        self._trend_auto_sigma_spin.setSingleStep(0.1)
        self._trend_auto_sigma_spin.setValue(3.0)
        self._trend_auto_sigma_spin.setToolTip(
            "<b>Множитель сигмы для авто-режима.</b><br>"
            "Наклон значим, если |b| > K·σ/√N.<br>"
            "<i>Рекомендация:</i> 3.0 — баланс чувствительности "
            "и ложных срабатываний."
        )
        form.addRow("Авто-сигма тренда:", self._trend_auto_sigma_spin)

        self._trend_ttl_spin = QSpinBox()
        self._trend_ttl_spin.setRange(1, 20)
        self._trend_ttl_spin.setValue(5)
        self._trend_ttl_spin.setToolTip(
            "<b>Подтверждение временем (точек).</b><br>"
            "Тренд фиксируется, если наклон значим в течение "
            "указанного числа последовательных точек.<br>"
            "<i>Рекомендация:</i> 3–7 для подавления ложных срабатываний."
        )
        form.addRow("Подтверждение (точек):", self._trend_ttl_spin)

        group.setLayout(form)
        return group

    def _create_anomaly_params_group(self) -> QGroupBox:
        """Создание группы параметров детектора аномалий."""
        group = QGroupBox("⚡ Детектор аномалий (остатки прогноза)")
        form = QFormLayout()

        self._sigma_factor_spin = QDoubleSpinBox()
        self._sigma_factor_spin.setRange(1.0, 10.0)
        self._sigma_factor_spin.setSingleStep(0.1)
        self._sigma_factor_spin.setValue(3.0)
        self._sigma_factor_spin.setToolTip(
            "<b>Множитель сигмы для порога аномалии (K).</b><br>"
            "Аномалия фиксируется при |остаток| > K·σ.<br>"
            "<i>Рекомендация:</i> 3.0 — правило «трёх сигм», "
            "4.0–5.0 для сильно зашумлённых сигналов."
        )
        form.addRow("Множитель сигмы (K):", self._sigma_factor_spin)

        self._anomaly_ttl_spin = QSpinBox()
        self._anomaly_ttl_spin.setRange(1, 10)
        self._anomaly_ttl_spin.setValue(3)
        self._anomaly_ttl_spin.setToolTip(
            "<b>Подтверждение временем (точек).</b><br>"
            "Аномалия фиксируется, если остаток превышает порог "
            "в течение указанного числа последовательных точек.<br>"
            "<i>Рекомендация:</i> 2–4 для подавления одиночных "
            "шумовых всплесков."
        )
        form.addRow("Подтверждение (точек):", self._anomaly_ttl_spin)

        group.setLayout(form)
        return group

    def _create_deviation_params_group(self) -> QGroupBox:
        """Создание группы параметров детектора отклонений (CUSUM)."""
        group = QGroupBox("📊 Детектор отклонений (CUSUM)")
        form = QFormLayout()

        self._cusum_drift_spin = QDoubleSpinBox()
        self._cusum_drift_spin.setRange(0.1, 2.0)
        self._cusum_drift_spin.setSingleStep(0.1)
        self._cusum_drift_spin.setValue(0.5)
        self._cusum_drift_spin.setToolTip(
            "<b>Допустимое смещение δ = drift_factor · σ.</b><br>"
            "Чувствительность к малым отклонениям. Меньшие значения — "
            "выше чувствительность, но больше ложных срабатываний.<br>"
            "<i>Рекомендация:</i> 0.5 для большинства сигналов."
        )
        form.addRow("Фактор дрейфа (δ):", self._cusum_drift_spin)

        self._cusum_threshold_spin = QDoubleSpinBox()
        self._cusum_threshold_spin.setRange(2.0, 10.0)
        self._cusum_threshold_spin.setSingleStep(0.5)
        self._cusum_threshold_spin.setValue(4.0)
        self._cusum_threshold_spin.setToolTip(
            "<b>Порог срабатывания H = threshold_factor · σ.</b><br>"
            "Отклонение фиксируется, когда накопленная статистика "
            "превышает порог. Меньшие значения — быстрее обнаружение.<br>"
            "<i>Рекомендация:</i> 4.0 — классическое значение."
        )
        form.addRow("Фактор порога (H):", self._cusum_threshold_spin)

        self._cusum_alpha_spin = QDoubleSpinBox()
        self._cusum_alpha_spin.setRange(0.01, 0.5)
        self._cusum_alpha_spin.setSingleStep(0.01)
        self._cusum_alpha_spin.setValue(0.05)
        self._cusum_alpha_spin.setToolTip(
            "<b>Коэффициент адаптации базовой линии (α).</b><br>"
            "Скорость подстройки базовой линии под медленные изменения.<br>"
            "<i>Рекомендация:</i> 0.01–0.1. Меньшие значения — "
            "медленнее адаптация, но стабильнее базовая линия."
        )
        form.addRow("Адаптация базы (α):", self._cusum_alpha_spin)

        group.setLayout(form)
        return group

    def update_model_info(self, signal_type: str, config: DetectorConfig) -> None:
        """
        Обновить отображение активных детекторов и пояснений к ним.

        Очищает блок информации и создаёт новые метки для каждого
        активного детектора с его названием и описанием.

        Args:
            signal_type: Тип сигнала (например, 'sine', 'square').
            config: Текущая конфигурация детектора.
        """
        try:
            # Обновляем тип сигнала в конфиге
            config.signal_type = signal_type

            # Очищаем существующие метки
            while self._detectors_info_layout.count():
                item = self._detectors_info_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

            # Получаем информацию об активных детекторах
            active = config.get_active_detectors()
            display_names = config.get_detector_display_names()
            explanations = config.get_model_explanations()

            if not active:
                label = QLabel("<i>Детекторы не активны для данного типа сигнала.</i>")
                label.setWordWrap(True)
                self._detectors_info_layout.addWidget(label)
                return

            # Создаём метку для каждого активного детектора
            for detector_key in active:
                name = display_names.get(detector_key, detector_key)
                explanation = explanations.get(detector_key, "")

                label = QLabel(f"<b>{name}</b><br><i style='color:#555;'>{explanation}</i>")
                label.setWordWrap(True)
                label.setStyleSheet(
                    "QLabel { background-color: #f8f9fa; padding: 6px; "
                    "border-radius: 3px; border-left: 3px solid #4a90d9; }"
                )
                self._detectors_info_layout.addWidget(label)

            logger.debug(
                f"Обновлена информация о детекторах для типа '{signal_type}': "
                f"активны {active}."
            )
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка обновления информации о детекторах: {e}")

    def get_config(self) -> DetectorConfig:
        """
        Считать текущие значения из интерфейса и вернуть объект DetectorConfig.

        Returns:
            DetectorConfig: Текущая конфигурация детектора.
        """
        try:
            trend_threshold = self._trend_threshold_spin.value()
            threshold_val = None if trend_threshold == 0.0 else trend_threshold

            return DetectorConfig(
                window_size=self._window_size_spin.value(),
                sigma_factor=self._sigma_factor_spin.value(),
                trend_threshold=threshold_val,
                trend_auto_sigma=self._trend_auto_sigma_spin.value(),
                trend_ttl=self._trend_ttl_spin.value(),
                anomaly_ttl=self._anomaly_ttl_spin.value(),
                cusum_drift_factor=self._cusum_drift_spin.value(),
                cusum_threshold_factor=self._cusum_threshold_spin.value(),
                cusum_baseline_alpha=self._cusum_alpha_spin.value(),
                min_samples=self._min_samples_spin.value(),
                noise_tolerance=self._noise_tolerance_spin.value(),
                tau_corr=self._tau_corr_spin.value(),
                preprocessor_window=self._preprocessor_window_spin.value(),
            )
        except Exception as e:  # noqa: BLE001
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
            self._noise_tolerance_spin.setValue(config.noise_tolerance)
            self._tau_corr_spin.setValue(config.tau_corr)
            self._preprocessor_window_spin.setValue(config.preprocessor_window)

            # Детектор тренда
            threshold = config.trend_threshold if config.trend_threshold is not None else 0.0
            self._trend_threshold_spin.setValue(threshold)
            self._trend_auto_sigma_spin.setValue(config.trend_auto_sigma)
            self._trend_ttl_spin.setValue(config.trend_ttl)

            # Детектор аномалий
            self._anomaly_ttl_spin.setValue(config.anomaly_ttl)

            # Детектор отклонений
            self._cusum_drift_spin.setValue(config.cusum_drift_factor)
            self._cusum_threshold_spin.setValue(config.cusum_threshold_factor)
            self._cusum_alpha_spin.setValue(config.cusum_baseline_alpha)

            # Обновляем информацию о детекторах, если тип сигнала известен
            if hasattr(config, "signal_type") and config.signal_type:
                self.update_model_info(config.signal_type, config)

            logger.debug("Настройки детектора загружены в интерфейс.")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка загрузки конфигурации детектора в интерфейс: {e}")
