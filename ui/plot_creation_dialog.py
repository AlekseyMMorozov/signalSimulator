"""
ui/plot_creation_dialog.py

Модальный диалог создания и редактирования графика телеметрии.
Позволяет настроить все параметры графика: название, единицу измерения,
тип сигнала с его параметрами, допустимые пределы, интервал наблюдения
и настройки детектора аномалий.
Вызывается из главного окна по сигналу plot_add_requested или plot_settings_requested.
"""

import logging
from typing import Any

from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from analytics.detector import DetectorConfig
from ui.detector_settings_tab import DetectorSettingsTab

logger = logging.getLogger(__name__)

# Сопоставление внутренних ключей сигналов с русскими названиями для интерфейса
SIGNAL_TYPE_DISPLAY = {
    "sine": "Синусоида",
    "sawtooth": "Пилообразный",
    "triangle": "Треугольный",
    "step": "Ступенчатый",
    "linear": "Линейный (тренд)",
    "square": "Прямоугольный (меандр)",
    "exponential": "Экспоненциальный",
    "noise": "Случайный шум",
    "constant": "Постоянный",
}


class PeriodWidget(QWidget):
    """
    Виджет для удобного ввода периода с выбором единицы измерения.
    Автоматически конвертирует выбранное значение и единицу в миллисекунды и обратно.
    """

    def __init__(self, default_ms: int, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._spin = QSpinBox()
        self._spin.setRange(1, 1000000000)
        self._spin.setToolTip("Числовое значение периода.")

        self._unit_combo = QComboBox()
        self._unit_combo.addItems(["мс", "с", "мин"])
        self._unit_combo.setToolTip("Единица измерения периода.")

        # Умный дефолт: если значение кратно 1000, показываем в секундах или минутах для удобства
        if default_ms >= 1000 and default_ms % 1000 == 0:
            secs = default_ms // 1000
            if secs % 60 == 0:
                self._spin.setValue(secs // 60)
                self._unit_combo.setCurrentText("мин")
            else:
                self._spin.setValue(secs)
                self._unit_combo.setCurrentText("с")
        else:
            self._spin.setValue(default_ms)
            self._unit_combo.setCurrentText("мс")

        layout.addWidget(self._spin)
        layout.addWidget(self._unit_combo)
        layout.addStretch(1)

        self.setToolTip("Время, за которое сигнал совершает один полный цикл.")

    def get_period_ms(self) -> int:
        """Возвращает период, пересчитанный в миллисекунды."""
        val = self._spin.value()
        unit = self._unit_combo.currentText()
        multipliers = {"мс": 1, "с": 1000, "мин": 60000}
        return val * multipliers[unit]

    def set_period_ms(self, ms: int) -> None:
        """
        Устанавливает период, автоматически выбирая удобную единицу измерения.

        Args:
            ms: Значение периода в миллисекундах.
        """
        try:
            if ms >= 60000 and ms % 60000 == 0:
                self._spin.setValue(ms // 60000)
                self._unit_combo.setCurrentText("мин")
            elif ms >= 1000 and ms % 1000 == 0:
                self._spin.setValue(ms // 1000)
                self._unit_combo.setCurrentText("с")
            else:
                self._spin.setValue(ms)
                self._unit_combo.setCurrentText("мс")
        except Exception as e:
            logger.error(f"Ошибка установки периода в виджете: {e}")


class PlotCreationDialog(QDialog):
    """
    Модальный диалог создания и редактирования графика телеметрии.

    Позволяет настроить:
    - Основные параметры (название, единица, макс. значение)
    - Интервал наблюдения (через пресеты или ручной ввод в секундах)
    - Допустимые пределы (min_allowed, max_allowed)
    - Тип сигнала и его параметры (динамически меняются)
    - Настройки детектора аномалий (размер окна, сигмы, пороги)

    Если передан initial_params, диалог переходит в режим редактирования и предзаполняет поля.
    После подтверждения результат доступен через метод get_plot_params().
    """

    def __init__(self, parent: QWidget | None = None, initial_params: dict[str, Any] | None = None) -> None:
        """
        Инициализация диалога создания/редактирования графика.

        Args:
            parent: Родительский виджет.
            initial_params: Словарь существующих параметров для предзаполнения (режим редактирования).
        """
        super().__init__(parent)
        self.setWindowTitle("Редактирование графика" if initial_params else "Создание графика")
        self.setMinimumWidth(600)

        self._plot_params: dict[str, Any] | None = None

        try:
            self._init_ui()
            self._update_signal_params_fields()

            if initial_params:
                self._populate_fields(initial_params)

            logger.info("Диалог графика инициализирован.")
        except Exception as e:
            logger.error(f"Ошибка инициализации диалога графика: {e}")
            raise

    def _init_ui(self) -> None:
        """Создание интерфейса диалога."""
        main_layout = QVBoxLayout(self)

        # === Вкладки ===
        self._tab_widget = QTabWidget()
        main_layout.addWidget(self._tab_widget)

        # --- Вкладка 1: Параметры сигнала ---
        signal_tab = QWidget()
        signal_tab_layout = QVBoxLayout(signal_tab)
        signal_tab_layout.setContentsMargins(4, 4, 4, 4)
        signal_tab_layout.setSpacing(8)

        # === Группа основных параметров ===
        basic_group = QGroupBox("Основные параметры")
        basic_layout = QFormLayout()

        self._name_edit = QLineEdit()
        self._name_edit.setPlaceholderText("Например: Сила тока Батарея солнечная 1")
        self._name_edit.setToolTip("Уникальное имя графика для отображения в списке и заголовке окна.")
        basic_layout.addRow("Название:", self._name_edit)

        self._unit_edit = QLineEdit()
        self._unit_edit.setPlaceholderText("Например: А")
        self._unit_edit.setToolTip("Единица измерения величины (например: 'А', 'В', 'Па', '°C').")
        basic_layout.addRow("Единица измерения:", self._unit_edit)

        self._max_unit_spin = QDoubleSpinBox()
        self._max_unit_spin.setRange(0.0, 1e9)
        self._max_unit_spin.setDecimals(4)
        self._max_unit_spin.setValue(10.0)
        self._max_unit_spin.setToolTip(
            "Верхняя граница шкалы графика по оси Y. Используется для корректного масштабирования. "
            "Например, если датчик измеряет до 100 А, укажите 100."
        )
        basic_layout.addRow("Макс. значение единицы:", self._max_unit_spin)

        basic_group.setLayout(basic_layout)
        signal_tab_layout.addWidget(basic_group)

        # === Группа интервала наблюдения ===
        interval_group = QGroupBox("Интервал наблюдения")
        interval_layout = QVBoxLayout()

        preset_layout = QHBoxLayout()
        lbl_preset = QLabel("Пресет:")
        lbl_preset.setToolTip("Быстрый выбор длительности отображения графика по оси X.")
        preset_layout.addWidget(lbl_preset)

        self._interval_preset_combo = QComboBox()
        self._interval_preset_combo.setToolTip("Выберите готовый шаблон длительности.")
        presets = [
            ("1 минута", 60), ("5 минут", 300), ("10 минут", 600), ("30 минут", 1800),
            ("1 час", 3600), ("6 часов", 21600), ("12 часов", 43200), ("1 сутки", 86400),
            ("1 неделя", 604800), ("1 месяц (30 дней)", 2592000), ("6 месяцев", 15552000),
            ("1 год", 31536000), ("2 года", 63072000), ("Ручной ввод", 0),
        ]
        for name, _ in presets:
            self._interval_preset_combo.addItem(name)
        self._interval_preset_combo.setCurrentIndex(len(presets) - 1)
        self._interval_preset_combo.currentIndexChanged.connect(self._on_preset_changed)
        preset_layout.addWidget(self._interval_preset_combo)
        interval_layout.addLayout(preset_layout)

        manual_layout = QHBoxLayout()
        lbl_manual = QLabel("Вручную (секунды):")
        lbl_manual.setToolTip(
            "Длительность отображения графика по оси X в секундах. "
            "Определяет, какой временной промежуток будет виден на экране целиком."
        )
        manual_layout.addWidget(lbl_manual)

        self._interval_spin = QSpinBox()
        self._interval_spin.setRange(1, 1000000000)
        self._interval_spin.setValue(60)
        self._interval_spin.setToolTip("Введите длительность в секундах.")
        manual_layout.addWidget(self._interval_spin)
        interval_layout.addLayout(manual_layout)

        interval_group.setLayout(interval_layout)
        signal_tab_layout.addWidget(interval_group)

        # === Группа допустимых пределов ===
        limits_group = QGroupBox("Допустимые пределы")
        limits_layout = QFormLayout()

        self._min_allowed_spin = QDoubleSpinBox()
        self._min_allowed_spin.setRange(-1e9, 1e9)
        self._min_allowed_spin.setDecimals(4)
        self._min_allowed_spin.setValue(0.0)
        self._min_allowed_spin.setToolTip(
            "Нижняя граница нормального режима работы. Выход сигнала ниже этого значения "
            "будет считаться аномалией и отмечаться на графике красной линией."
        )
        limits_layout.addRow("Минимум:", self._min_allowed_spin)

        self._max_allowed_spin = QDoubleSpinBox()
        self._max_allowed_spin.setRange(-1e9, 1e9)
        self._max_allowed_spin.setDecimals(4)
        self._max_allowed_spin.setValue(10.0)
        self._max_allowed_spin.setToolTip(
            "Верхняя граница нормального режима работы. Выход сигнала выше этого значения "
            "будет считаться аномалией и отмечаться на графике красной линией."
        )
        limits_layout.addRow("Максимум:", self._max_allowed_spin)

        limits_group.setLayout(limits_layout)
        signal_tab_layout.addWidget(limits_group)

        # === Группа параметров сигнала ===
        signal_group = QGroupBox("Параметры сигнала")
        signal_layout = QVBoxLayout()

        type_layout = QHBoxLayout()
        lbl_type = QLabel("Тип сигнала:")
        lbl_type.setToolTip("Форма базового сигнала, который будет генерироваться.")
        type_layout.addWidget(lbl_type)

        self._signal_type_combo = QComboBox()
        self._signal_type_combo.setToolTip("Выберите форму сигнала из списка.")
        for internal_key, display_name in SIGNAL_TYPE_DISPLAY.items():
            self._signal_type_combo.addItem(display_name, internal_key)
        self._signal_type_combo.currentIndexChanged.connect(self._update_signal_params_fields)
        type_layout.addWidget(self._signal_type_combo)
        signal_layout.addLayout(type_layout)

        self._signal_params_widget = QWidget()
        self._signal_params_layout = QFormLayout(self._signal_params_widget)
        signal_layout.addWidget(self._signal_params_widget)

        signal_group.setLayout(signal_layout)
        signal_tab_layout.addWidget(signal_group)

        signal_tab_layout.addStretch(1)
        self._tab_widget.addTab(signal_tab, "📊 Сигнал")

        # --- Вкладка 2: Настройки детектора ---
        self._detector_settings_tab = DetectorSettingsTab()
        self._tab_widget.addTab(self._detector_settings_tab, "🔍 Детектор")

        # === Кнопки ОК / Отмена ===
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._on_accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

        logger.debug("Интерфейс диалога графика создан.")

    def _populate_fields(self, params: dict[str, Any]) -> None:
        """
        Предзаполняет поля диалога переданными параметрами (для режима редактирования).

        Args:
            params: Словарь параметров графика.
        """
        try:
            self._name_edit.setText(params.get("name", ""))
            self._unit_edit.setText(params.get("unit", ""))
            self._max_unit_spin.setValue(params.get("max_unit_value", 10.0))
            self._min_allowed_spin.setValue(params.get("min_allowed", 0.0))
            self._max_allowed_spin.setValue(params.get("max_allowed", 10.0))

            interval_sec = params.get("observation_interval_ms", 60000) // 1000
            self._interval_spin.setValue(max(1, interval_sec))

            signal_type = params.get("signal_type", "sine")
            index = self._signal_type_combo.findData(signal_type)
            if index != -1:
                self._signal_type_combo.setCurrentIndex(index)

            signal_params = params.get("signal_params", {})
            for i in range(self._signal_params_layout.count()):
                item = self._signal_params_layout.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    param_name = widget.property("param_name")
                    if param_name in signal_params:
                        val = signal_params[param_name]
                        if widget.property("is_period"):
                            widget.set_period_ms(int(val))
                        else:
                            widget.setValue(val)

            # Предзаполнение настроек детектора
            detector_config_dict = params.get("detector_config")
            if detector_config_dict:
                try:
                    config = DetectorConfig.from_dict(detector_config_dict)
                    self._detector_settings_tab.set_config(config)
                except Exception as e:
                    logger.error(f"Ошибка загрузки конфигурации детектора: {e}")

            logger.debug("Поля диалога предзаполнены параметрами.")
        except Exception as e:
            logger.error(f"Ошибка предзаполнения полей: {e}")

    def _on_preset_changed(self, index: int) -> None:
        """
        Обработчик изменения пресета интервала.
        При выборе пресета подставляет значение в поле ручного ввода.
        """
        try:
            presets = [
                ("1 минута", 60), ("5 минут", 300), ("10 минут", 600), ("30 минут", 1800),
                ("1 час", 3600), ("6 часов", 21600), ("12 часов", 43200), ("1 сутки", 86400),
                ("1 неделя", 604800), ("1 месяц (30 дней)", 2592000), ("6 месяцев", 15552000),
                ("1 год", 31536000), ("2 года", 63072000), ("Ручной ввод", 0),
            ]
            if 0 <= index < len(presets):
                _, value_sec = presets[index]
                if value_sec > 0:
                    self._interval_spin.setValue(value_sec)
                    logger.debug(f"Выбран пресет интервала: {value_sec} сек.")
        except Exception as e:
            logger.error(f"Ошибка обработки изменения пресета: {e}")

    def _update_signal_params_fields(self) -> None:
        """
        Обновление полей параметров сигнала при смене типа.
        Удаляет старые поля и создаёт новые в соответствии с выбранным типом сигнала.
        """
        try:
            while self._signal_params_layout.count():
                item = self._signal_params_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

            signal_type = self._signal_type_combo.currentData()

            if signal_type in ["sawtooth", "triangle", "step"]:
                self._add_signal_param("min_val", "Минимум:", 0.0,
                                       tooltip="Нижнее значение сигнала (состояние '0' или 'выключено').")
                self._add_signal_param("max_val", "Максимум:", 10.0,
                                       tooltip="Верхнее значение сигнала (состояние '1' или 'включено').")
                self._add_signal_param("period_ms", "Период:", 10000, is_int=True)
                self._add_signal_param("offset", "Смещение:", 0.0,
                                       tooltip="Постоянная величина, добавляемая ко всему сигналу. Сдвигает весь график вверх или вниз.")

            elif signal_type == "sine":
                self._add_signal_param("amplitude", "Амплитуда:", 1.0,
                                       tooltip="Максимальное отклонение сигнала от центра. Пиковое значение синусоиды.")
                self._add_signal_param("period_ms", "Период:", 10000, is_int=True)
                self._add_signal_param("phase", "Фаза (рад):", 0.0,
                                       tooltip="Начальный сдвиг синусоиды в радианах. 0 — начало с нуля, 1.57 (π/2) — начало с максимума.")
                self._add_signal_param("offset", "Смещение:", 0.0,
                                       tooltip="Постоянная величина, добавляемая ко всему сигналу. Сдвигает весь график вверх или вниз.")

            elif signal_type == "linear":
                self._add_signal_param("start_val", "Начальное значение:", 0.0,
                                       tooltip="Значение сигнала в момент времени 0.")
                self._add_signal_param("rate_per_sec", "Скорость (ед/сек):", 0.01,
                                       tooltip="На сколько единиц изменяется значение сигнала за одну секунду. Положительное — рост, отрицательное — падение.")
                self._add_signal_param("offset", "Смещение:", 0.0,
                                       tooltip="Постоянная величина, добавляемая ко всему сигналу. Сдвигает весь график вверх или вниз.")

            elif signal_type == "square":
                self._add_signal_param("min_val", "Минимум:", 0.0,
                                       tooltip="Нижнее значение сигнала (состояние '0' или 'выключено').")
                self._add_signal_param("max_val", "Максимум:", 10.0,
                                       tooltip="Верхнее значение сигнала (состояние '1' или 'включено').")
                self._add_signal_param("period_ms", "Период:", 10000, is_int=True)
                self._add_signal_param("duty_cycle", "Коэфф. заполнения:", 0.5,
                                       tooltip="Доля периода, в течение которой сигнал находится на уровне максимума. 0.5 означает классический меандр (50% времени на максимуме). Диапазон: 0.0 - 1.0.")
                self._add_signal_param("offset", "Смещение:", 0.0,
                                       tooltip="Постоянная величина, добавляемая ко всему сигналу. Сдвигает весь график вверх или вниз.")

            elif signal_type == "exponential":
                self._add_signal_param("amplitude", "Амплитуда:", 1.0,
                                       tooltip="Множитель экспоненты. Начальная величина отклонения.")
                self._add_signal_param("rate_per_sec", "Скорость (1/сек):", 0.01,
                                       tooltip="Скорость роста или затухания. Положительное — экспоненциальный рост, отрицательное — затухание.")
                self._add_signal_param("offset", "Смещение:", 0.0,
                                       tooltip="Постоянная величина, добавляемая ко всему сигналу. Сдвигает весь график вверх или вниз.")

            elif signal_type == "noise":
                self._add_signal_param("mean", "Среднее:", 0.0,
                                       tooltip="Центр распределения случайного шума (среднее значение).")
                self._add_signal_param("sigma", "Сигма:", 1.0,
                                       tooltip="Сила шума (стандартное отклонение). Чем больше, тем сильнее разброс значений.")

            elif signal_type == "constant":
                self._add_signal_param("value", "Значение:", 5.0,
                                       tooltip="Постоянное значение сигнала, которое не меняется со временем.")

            logger.debug(f"Обновлены поля параметров сигнала для типа '{signal_type}'.")
        except Exception as e:
            logger.error(f"Ошибка обновления полей параметров сигнала: {e}")

    def _add_signal_param(
        self,
        param_name: str,
        label: str,
        default_value: float,
        is_int: bool = False,
        tooltip: str = ""
    ) -> None:
        """
        Добавить поле параметра сигнала в форму.
        Для периода используется специализированный виджет с выбором единицы измерения.
        """
        try:
            if param_name == "period_ms":
                widget = PeriodWidget(int(default_value))
                widget.setProperty("param_name", param_name)
                widget.setProperty("is_period", True)
                self._signal_params_layout.addRow(label, widget)
            elif is_int:
                spin = QSpinBox()
                spin.setRange(1, 1000000000)
                spin.setValue(int(default_value))
                spin.setProperty("param_name", param_name)
                spin.setProperty("is_int", True)
                if tooltip:
                    spin.setToolTip(tooltip)
                self._signal_params_layout.addRow(label, spin)
            else:
                spin = QDoubleSpinBox()
                spin.setRange(-1e9, 1e9)
                spin.setDecimals(6)
                spin.setValue(default_value)
                spin.setProperty("param_name", param_name)
                spin.setProperty("is_int", False)
                if tooltip:
                    spin.setToolTip(tooltip)
                self._signal_params_layout.addRow(label, spin)
        except Exception as e:
            logger.error(f"Ошибка добавления поля параметра '{param_name}': {e}")

    def _on_accept(self) -> None:
        """
        Обработчик нажатия кнопки ОК.
        Выполняет валидацию и при успехе сохраняет параметры и закрывает диалог.
        """
        try:
            if not self._validate():
                return

            name = self._name_edit.text().strip()
            unit = self._unit_edit.text().strip()
            max_unit_value = self._max_unit_spin.value()
            interval_sec = self._interval_spin.value()
            interval_ms = interval_sec * 1000
            min_allowed = self._min_allowed_spin.value()
            max_allowed = self._max_allowed_spin.value()

            signal_type = self._signal_type_combo.currentData()
            signal_params = {}

            for i in range(self._signal_params_layout.count()):
                item = self._signal_params_layout.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    param_name = widget.property("param_name")
                    if not param_name:
                        continue

                    if widget.property("is_period"):
                        signal_params[param_name] = widget.get_period_ms()
                    else:
                        is_int = widget.property("is_int")
                        value = widget.value()
                        signal_params[param_name] = int(value) if is_int else float(value)

            self._plot_params = {
                "name": name,
                "unit": unit,
                "max_unit_value": max_unit_value,
                "observation_interval_ms": interval_ms,
                "min_allowed": min_allowed,
                "max_allowed": max_allowed,
                "signal_type": signal_type,
                "signal_params": signal_params,
                "detector_config": self._detector_settings_tab.get_config().to_dict(),
            }

            logger.info(f"Параметры графика подтверждены: {name}.")
            self.accept()
        except Exception as e:
            logger.error(f"Ошибка при подтверждении диалога: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить параметры:\n{e}")

    def _validate(self) -> bool:
        """
        Валидация введённых данных.
        """
        try:
            name = self._name_edit.text().strip()
            if not name:
                QMessageBox.warning(self, "Ошибка валидации", "Название графика не может быть пустым.")
                return False

            min_allowed = self._min_allowed_spin.value()
            max_allowed = self._max_allowed_spin.value()
            if min_allowed >= max_allowed:
                QMessageBox.warning(
                    self, "Ошибка валидации",
                    "Минимальный предел должен быть строго меньше максимального."
                )
                return False

            interval_sec = self._interval_spin.value()
            if interval_sec <= 0:
                QMessageBox.warning(
                    self, "Ошибка валидации",
                    "Интервал наблюдения должен быть больше нуля."
                )
                return False

            return True
        except Exception as e:
            logger.error(f"Ошибка валидации: {e}")
            return False

    def get_plot_params(self) -> dict[str, Any] | None:
        """
        Получить параметры графика после подтверждения диалога.
        """
        return self._plot_params
