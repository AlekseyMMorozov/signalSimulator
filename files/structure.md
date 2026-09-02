# Структура и метаданные проекта

## Метаданные проекта
- **Название:** signalSimulator
- **Версия:** не указана
- **Описание:** нет
- **Зависимости:** PyQt6==6.11.0, pyqtgraph==0.14.0, numpy==2.5.2
- **Точки входа:** compact_code.py, generate_structure.py, main.py, .venv\Lib\site-packages\flake8\__main__.py, .venv\Lib\site-packages\numpy\_configtool.py, .venv\Lib\site-packages\pip\__main__.py, .venv\Lib\site-packages\ruff\__main__.py, .venv\Lib\site-packages\numpy\f2py\crackfortran.py, .venv\Lib\site-packages\numpy\f2py\diagnose.py, .venv\Lib\site-packages\numpy\typing\tests\data\pass\lib_user_array.py, .venv\Lib\site-packages\numpy\_core\tests\test_cpu_features.py, .venv\Lib\site-packages\pip\_vendor\cachecontrol\_cmd.py, .venv\Lib\site-packages\pip\_vendor\distro\distro.py, .venv\Lib\site-packages\pip\_vendor\distro\__main__.py, .venv\Lib\site-packages\pip\_vendor\idna\cli.py, .venv\Lib\site-packages\pip\_vendor\idna\__main__.py, .venv\Lib\site-packages\pip\_vendor\packaging\_musllinux.py, .venv\Lib\site-packages\pip\_vendor\platformdirs\__main__.py, .venv\Lib\site-packages\pip\_vendor\requests\certs.py, .venv\Lib\site-packages\pip\_vendor\requests\help.py, .venv\Lib\site-packages\pip\_vendor\rich\abc.py, .venv\Lib\site-packages\pip\_vendor\rich\align.py, .venv\Lib\site-packages\pip\_vendor\rich\box.py, .venv\Lib\site-packages\pip\_vendor\rich\cells.py, .venv\Lib\site-packages\pip\_vendor\rich\color.py, .venv\Lib\site-packages\pip\_vendor\rich\columns.py, .venv\Lib\site-packages\pip\_vendor\rich\console.py, .venv\Lib\site-packages\pip\_vendor\rich\control.py, .venv\Lib\site-packages\pip\_vendor\rich\default_styles.py, .venv\Lib\site-packages\pip\_vendor\rich\diagnose.py, .venv\Lib\site-packages\pip\_vendor\rich\emoji.py, .venv\Lib\site-packages\pip\_vendor\rich\highlighter.py, .venv\Lib\site-packages\pip\_vendor\rich\json.py, .venv\Lib\site-packages\pip\_vendor\rich\layout.py, .venv\Lib\site-packages\pip\_vendor\rich\live.py, .venv\Lib\site-packages\pip\_vendor\rich\logging.py, .venv\Lib\site-packages\pip\_vendor\rich\markup.py, .venv\Lib\site-packages\pip\_vendor\rich\padding.py, .venv\Lib\site-packages\pip\_vendor\rich\pager.py, .venv\Lib\site-packages\pip\_vendor\rich\palette.py, .venv\Lib\site-packages\pip\_vendor\rich\panel.py, .venv\Lib\site-packages\pip\_vendor\rich\pretty.py, .venv\Lib\site-packages\pip\_vendor\rich\progress.py, .venv\Lib\site-packages\pip\_vendor\rich\progress_bar.py, .venv\Lib\site-packages\pip\_vendor\rich\prompt.py, .venv\Lib\site-packages\pip\_vendor\rich\repr.py, .venv\Lib\site-packages\pip\_vendor\rich\rule.py, .venv\Lib\site-packages\pip\_vendor\rich\scope.py, .venv\Lib\site-packages\pip\_vendor\rich\segment.py, .venv\Lib\site-packages\pip\_vendor\rich\spinner.py, .venv\Lib\site-packages\pip\_vendor\rich\status.py, .venv\Lib\site-packages\pip\_vendor\rich\styled.py, .venv\Lib\site-packages\pip\_vendor\rich\syntax.py, .venv\Lib\site-packages\pip\_vendor\rich\table.py, .venv\Lib\site-packages\pip\_vendor\rich\text.py, .venv\Lib\site-packages\pip\_vendor\rich\theme.py, .venv\Lib\site-packages\pip\_vendor\rich\traceback.py, .venv\Lib\site-packages\pip\_vendor\rich\tree.py, .venv\Lib\site-packages\pip\_vendor\rich\_log_render.py, .venv\Lib\site-packages\pip\_vendor\rich\_ratio.py, .venv\Lib\site-packages\pip\_vendor\rich\_win32_console.py, .venv\Lib\site-packages\pip\_vendor\rich\_windows.py, .venv\Lib\site-packages\pip\_vendor\rich\_wrap.py, .venv\Lib\site-packages\pip\_vendor\rich\__init__.py, .venv\Lib\site-packages\pip\_vendor\rich\__main__.py, .venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\_in_process.py, .venv\Lib\site-packages\PyQt6\uic\compile_ui.py, .venv\Lib\site-packages\pyqtgraph\examples\GLGradientLegendItem.py, .venv\Lib\site-packages\pyqtgraph\examples\GLGraphItem.py, .venv\Lib\site-packages\pyqtgraph\examples\InteractiveParameter.py, .venv\Lib\site-packages\pyqtgraph\examples\jupyter_console_example.py, .venv\Lib\site-packages\pyqtgraph\examples\MultiDataPlot.py, .venv\Lib\site-packages\pyqtgraph\examples\RunExampleApp.py, .venv\Lib\site-packages\pyqtgraph\examples\ScatterPlotSpeedTest.py, .venv\Lib\site-packages\pyqtgraph\examples\test_examples.py, .venv\Lib\site-packages\pyqtgraph\util\get_resolution.py

## Статистика проекта
- Папок: 7
- Python-файлов: 34
- Всего файлов: 34
- Классов: 60
- Функций: 2

## Дерево проекта
```
signalSimulator/
  analytics/
    __init__.py
    anomaly_detector.py
    detector.py
    detector_models.py
    detector_types.py
    deviation_detector.py
    metrics.py
    signal_preprocessor.py
    trend_detector.py
  configs/
  core/
    __init__.py
    clock.py
    config.py
    event_log.py
  simulation/
    __init__.py
    faults.py
    scheduler.py
    signals.py
    simulator.py
  ui/
    panels/
      __init__.py
      options_panel.py
      plots_panel.py
      time_panel.py
    __init__.py
    detector_settings_tab.py
    fault_rule_dialog.py
    fault_template_dialog.py
    fault_window.py
    log_window.py
    main_window.py
    period_widget.py
    plot_creation_dialog.py
    plot_window.py
    signal_params_form.py
  main.py
```

## Содержимое файлов (сигнатуры с docstring)

### Файл: `__init__.py`
> analytics/__init__.py
Инициализация пакета `analytics` — аналитика и обнаружение аномалий.
Содержит модули детектирования и подсчёта метрик.
#### Импорты
- **Сторонние библиотеки:**
  - `from analytics.detector import AnomalyDetector, DetectionResult, DetectionType, DetectorConfig`
  - `from analytics.metrics import FaultAnalysisRecord, MetricsCalculator, MetricsSummary`

### Файл: `anomaly_detector.py`
> analytics/anomaly_detector.py

Детектор точечных аномалий (резких выбросов и провалов) на основе анализа
остатков прогнозирующего фильтра с подтверждением временем (time-to-live).

Математическая основа:
    Прогноз:  x̂_t = l_{t-1} + b_{t-1} · dt  (модель Хольта)
    Остаток:  r_t = x_t - x̂_t
    Шум:      σ_noise = 1.4826 · MAD(остатков)
    Критерий: |r_t| > K · σ_noise, где K = sigma_factor (обычно 3–4)

Поддерживает:
- Робастную оценку шума через MAD по остаткам (не по сырому сигналу)
- Подтверждение временем (time-to-live) для подавления ложных срабатываний
- Адаптацию доверительного интервала при дефиците данных
- Дедупликацию обнаружений (не повторяем одну и ту же аномалию)

Важно: детектор работает с информативным параметром от препроцессора,
а не с сырым сигналом. Для меандра/ступенек фронты уже отфильтрованы,
для синуса/треугольника анализируется амплитуда, для пилы — наклон.
#### Импорты
- **Стандартная библиотека:**
  - `from collections import deque`
  - `import logging`
- **Сторонние библиотеки:**
  - `from analytics.detector import DetectionResult, DetectionType, DetectorConfig`
  - `import numpy as np`
#### Классы
##### `class SpikeDetector`
> Детектор точечных аномалий (резких выбросов и провалов).

Использует адаптивный прогнозирующий фильтр на основе модели Хольта
для вычисления остатка (ошибки прогноза). Аномалия фиксируется,
когда остаток превышает порог, подтверждённый несколькими
последовательными точками (time-to-live).

Attributes:
    min_allowed: Минимально допустимое значение сигнала.
    max_allowed: Максимально допустимое значение сигнала.
Методы:
- `def __init__(self, min_allowed: float, max_allowed: float, config: DetectorConfig | None) -> None`
  - Инициализация детектора точечных аномалий.

Args:
    min_allowed: Минимально допустимое значение сигнала.
    max_allowed: Максимально допустимое значение сигнала.
    config: Конфигурация детектора. Если None — используется по умолчанию.
- `def set_config(self, config: DetectorConfig) -> None`
  - Обновить конфигурацию детектора.

Args:
    config: Новая конфигурация.
- `def get_config(self) -> DetectorConfig`
  - Возвращает текущую конфигурацию детектора.
- `def process(self, time_ms: int, value: float) -> list[DetectionResult]`
  - Обработать новую точку и проверить наличие аномалии.

Args:
    time_ms: Логическое время в миллисекундах.
    value: Значение сигнала (или информативный параметр от препроцессора).

Returns:
    Список обнаружений (обычно 0 или 1 элемент).
- `def _get_forecast(self, dt_sec: float) -> float`
  - Вычислить прогноз значения на текущий момент.

Использует модель Хольта (уровень + наклон) для прогноза.

Args:
    dt_sec: Время с предыдущей точки в секундах.

Returns:
    Прогнозируемое значение.
- `def _update_filter(self, value: float, forecast: float, dt_sec: float) -> None`
  - Обновить состояние прогнозирующего фильтра (модель Хольта).

Args:
    value: Текущее значение сигнала.
    forecast: Прогноз на текущий момент.
    dt_sec: Время с предыдущей точки в секундах.
- `def _update_sigma_residual(self) -> None`
  - Обновить робастную оценку шума по остаткам через MAD.
- `def _get_anomaly_threshold(self, dt_sec: float) -> float`
  - Вычислить порог аномалии с учётом дефицита данных.

При дефиците данных доверительный интервал расширяется:
σ_прогноза = σ_noise · √(1 + dt / τ_корр)

Args:
    dt_sec: Время с предыдущей точки в секундах.

Returns:
    Порог аномалии.
- `def _check_anomaly(self, time_ms: int, value: float, residual: float, threshold: float) -> list[DetectionResult]`
  - Проверить аномалию с подтверждением временем (time-to-live).

Args:
    time_ms: Текущее логическое время.
    value: Текущее значение сигнала.
    residual: Остаток прогноза.
    threshold: Порог аномалии.

Returns:
    Список обнаружений аномалий.
- `def reset(self) -> None`
  - Сброс состояния детектора.
- `def get_state(self) -> dict`
  - Получить текущее состояние детектора для отладки и визуализации.

Returns:
    Словарь с текущими параметрами.

### Файл: `detector.py`
> analytics/detector.py

Главный фасад модуля обнаружения аномалий.
Координирует работу препроцессора и трёх специализированных детекторов:
- TrendDetector (модель Хольта) — обнаружение медленных трендов.
- SpikeDetector (остатки прогноза) — обнаружение резких аномалий.
- DeviationDetector (CUSUM) — обнаружение устойчивых смещений уровня.

Для обратной совместимости реэкспортирует типы данных из `detector_types`:
`DetectionType`, `DetectionResult`, `DetectorConfig`.

Пороговые проверки (выход за `min_allowed`/`max_allowed`) выполняются
в фасаде по сырому значению сигнала, тогда как статистические детекторы
работают с информативным параметром, извлечённым препроцессором.
#### Импорты
- **Стандартная библиотека:**
  - `from typing import Any`
  - `import logging`
- **Сторонние библиотеки:**
  - `from analytics.anomaly_detector import SpikeDetector`
  - `from analytics.detector_types import DetectionResult, DetectionType, DetectorConfig, DetectorKind`
  - `from analytics.deviation_detector import DeviationDetector`
  - `from analytics.signal_preprocessor import SignalPreprocessor`
  - `from analytics.trend_detector import TrendDetector`
#### Классы
##### `class AnomalyDetector`
> Главный фасад детектора аномалий.

Координирует работу препроцессора (извлечение информативного параметра)
и трёх специализированных детекторов (тренд, аномалия, отклонение).
Пороговые проверки выполняются по сырому значению сигнала.

Интерфейс полностью совместим со старой версией:
`__init__(min_allowed, max_allowed, config)`, `process(time_ms, value)`,
`set_config(config)`, `get_config()`, `reset()`.

Attributes:
    min_allowed: Минимально допустимое значение сигнала.
    max_allowed: Максимально допустимое значение сигнала.
Методы:
- `def __init__(self, min_allowed: float, max_allowed: float, config: DetectorConfig | None) -> None`
  - Инициализация фасада детектора аномалий.

Args:
    min_allowed: Минимально допустимое значение сигнала.
    max_allowed: Максимально допустимое значение сигнала.
    config: Конфигурация детектора. Если None — используется по умолчанию.
- `def set_config(self, config: DetectorConfig) -> None`
  - Обновить конфигурацию фасада и всех детекторов.

Пересоздаёт препроцессор с новым типом сигнала и обновляет
конфигурацию всех специализированных детекторов.

Args:
    config: Новая конфигурация детектора.
- `def get_config(self) -> DetectorConfig`
  - Возвращает текущую конфигурацию детектора.
- `def process(self, time_ms: int, value: float) -> list[DetectionResult]`
  - Обработать новую точку сигнала.

Выполняет пороговые проверки по сырому значению, затем
извлекает информативный параметр через препроцессор
и передаёт его активным детекторам.

Args:
    time_ms: Логическое время в миллисекундах.
    value: Сырое значение сигнала.

Returns:
    Список всех обнаружений от всех активных детекторов.
- `def _check_thresholds(self, time_ms: int, value: float) -> list[DetectionResult]`
  - Пороговые проверки по сырому значению сигнала.

Фиксирует выход за допустимые пределы с гистерезисом
(не повторяет обнаружение, пока сигнал не вернётся в норму).

Args:
    time_ms: Логическое время в миллисекундах.
    value: Сырое значение сигнала.

Returns:
    Список пороговых обнаружений (0 или 1 элемент).
- `def reset(self) -> None`
  - Сброс состояния фасада и всех детекторов.
- `def get_active_detectors_info(self) -> dict[str, Any]`
  - Получить информацию об активных детекторах для UI.

Возвращает отображаемые названия и описания всех активных
детекторов для текущего типа сигнала.

Returns:
    Словарь с ключами: "active", "display_names", "explanations", "state".

### Файл: `detector_models.py`
> analytics/detector_models.py

Реализация конкретных стратегий обнаружения аномалий.
Выделено из detector.py для соблюдения принципа единой ответственности.
#### Импорты
- **Стандартная библиотека:**
  - `from collections import deque`
  - `import logging`
- **Сторонние библиотеки:**
  - `from analytics.detector_types import DetectionResult, DetectionType, DetectorConfig`
  - `import numpy as np`
#### Классы
##### `class HoltDetector`
> Модель Хольта (двойное экспоненциальное сглаживание).
Для периодических сигналов (синус, пила, треугольник) автоматически
переключается на Rolling Z-Score (скользящую медиану), чтобы избежать
ложных срабатываний из-за фазового сдвига прогноза.
Методы:
- `def __init__(self, min_allowed: float, max_allowed: float, config: DetectorConfig) -> None`
- `def process(self, time_ms: int, value: float) -> list[DetectionResult]`
- `def _process_periodic(self, time_ms: int, value: float) -> list[DetectionResult]`
- `def _process_trend(self, time_ms: int, value: float, dt_sec: float) -> list[DetectionResult]`
- `def _update_sigma_noise(self) -> None`
- `def _holt_step(self, value: float, dt_sec: float) -> tuple[float, float, float]`
- `def _check_trend(self, time_ms: int) -> list[DetectionResult]`
- `def reset(self) -> None`
##### `class BimodalDetector`
> Бимодальная модель для сигналов с двумя устойчивыми уровнями (меандр, ступеньки).
Игнорирует фронты, анализируя отклонения от локальных уровней и тренды по каждому уровню отдельно.
Методы:
- `def __init__(self, min_allowed: float, max_allowed: float, config: DetectorConfig) -> None`
- `def process(self, time_ms: int, value: float) -> list[DetectionResult]`
- `def _initialize_bimodal_levels(self) -> None`
- `def _assign_to_level(self, value: float) -> tuple[str | None, float]`
- `def _add_point_to_level(self, level: str, time_ms: int, value: float) -> None`
- `def _update_level_stats(self, level: str) -> None`
- `def _check_trend(self, time_ms: int, level: str) -> list[DetectionResult]`
- `def reset(self) -> None`

### Файл: `detector_types.py`
> analytics/detector_types.py

Типы данных и конфигурация для модуля обнаружения аномалий.
Выделено из detector.py для соблюдения принципа единой ответственности.

Поддерживает новую архитектуру с разделением ответственности:
- Препроцессор (извлечение информативного параметра)
- Детектор тренда (модель Хольта)
- Детектор аномалий (анализ остатков прогноза)
- Детектор отклонений (CUSUM)
#### Импорты
- **Стандартная библиотека:**
  - `from dataclasses import dataclass`
  - `from enum import Enum, auto`
  - `from typing import Any`
  - `import logging`
#### Классы
##### `class DetectionType(Enum)`
> Типы обнаружений.
##### `class DetectorKind(Enum)`
> Типы детекторов в новой архитектуре.
##### `@dataclass class DetectionResult`
> Результат обнаружения.
Содержит время, тип обнаружения, описание, текущее значение
и произвольные метаданные (например, направление тренда).
Методы:
- `def __str__(self) -> str`
- `def __getitem__(self, key: str) -> Any`
  - Поддержка доступа как к словарю для обратной совместимости.
##### `@dataclass class DetectorConfig`
> Конфигурация детектора, сериализуемая в словарь.

Поддерживает как старую архитектуру (одна модель), так и новую
(три независимых детектора). Для обратной совместимости старые
поля сохранены, новые добавлены с дефолтными значениями.
Методы:
- `def to_dict(self) -> dict[str, Any]`
  - Сериализация конфигурации в словарь.
- `@classmethod def from_dict(cls, data: dict[str, Any]) -> 'DetectorConfig'`
  - Десериализация конфигурации из словаря с обратной совместимостью.
- `def get_active_detectors(self) -> list[str]`
  - Определить список активных детекторов для текущего типа сигнала.

Если поле `active_detectors` задано явно — используется оно.
Иначе применяется автоматическое определение по типу сигнала:
- Для линейного/экспоненты тренд отключён (тренд — нормальное поведение)
- Для шума тренд отключён (случайный сигнал)
- Для остальных типов активны все три детектора

Returns:
    Список названий активных детекторов: "trend", "anomaly", "deviation".
- `def get_model_explanations(self) -> dict[str, str]`
  - Возвращает описания всех активных детекторов для текущего типа сигнала.

Используется в UI для отображения информации о моделях
с пояснениями, почему они выбраны.

Returns:
    Словарь {название_детектора: описание}.
- `def get_model_explanation(self) -> str`
  - Возвращает сводное описание активных детекторов (для обратной совместимости).

Returns:
    Строка с описанием всех активных детекторов.
- `def get_detector_display_names(self) -> dict[str, str]`
  - Возвращает отображаемые названия детекторов для UI.

Returns:
    Словарь {ключ_детектора: отображаемое_название}.

### Файл: `deviation_detector.py`
> analytics/deviation_detector.py

CUSUM-детектор смещения уровня (разладки).
Обнаруживает устойчивое смещение сигнала на новый уровень,
когда тренд может быть нулевым, но среднее значение изменилось.

Математическая основа (кумулятивная сумма):
    Целевое значение: μ₀ (адаптивная базовая линия)
    Допустимое смещение: δ (чувствительность)
    Порог: H = K · σ_noise

    Накопленные статистики:
        S_high = max(0, S_high + (x_t - μ₀) - δ)
        S_low  = max(0, S_low  + (μ₀ - x_t) - δ)

    Отклонение фиксируется, когда S_high > H или S_low > H.

Преимущество метода:
    CUSUM накапливает слабые отклонения по крупицам,
    а не ждёт одного большого выброса. Одиночный шумовой выброс
    быстро «затухает» в max(0, ...), а реальное смещение уровня
    растёт линейно и быстро превышает порог.

Поддерживает:
- Робастную оценку шума через MAD
- Адаптивную базовую линию (скользящая медиана)
- Автоматический сброс после обнаружения
- Кулдаун для подавления повторных срабатываний
#### Импорты
- **Стандартная библиотека:**
  - `from collections import deque`
  - `import logging`
- **Сторонние библиотеки:**
  - `from analytics.detector import DetectionResult, DetectionType, DetectorConfig`
  - `import numpy as np`
#### Классы
##### `class DeviationDetector`
> CUSUM-детектор смещения уровня (разладки).

Обнаруживает устойчивое смещение сигнала на новый уровень,
накапливая малые отклонения от базовой линии. Одиночные
шумовые выбросы не приводят к срабатыванию, тогда как
реальное смещение уровня быстро превышает порог.

Attributes:
    min_allowed: Минимально допустимое значение сигнала.
    max_allowed: Максимально допустимое значение сигнала.
Методы:
- `def __init__(self, min_allowed: float, max_allowed: float, config: DetectorConfig | None) -> None`
  - Инициализация CUSUM-детектора смещения уровня.

Args:
    min_allowed: Минимально допустимое значение сигнала.
    max_allowed: Максимально допустимое значение сигнала.
    config: Конфигурация детектора. Если None — используется по умолчанию.
- `def set_config(self, config: DetectorConfig) -> None`
  - Обновить конфигурацию детектора.

Args:
    config: Новая конфигурация.
- `def get_config(self) -> DetectorConfig`
  - Возвращает текущую конфигурацию детектора.
- `def process(self, time_ms: int, value: float) -> list[DetectionResult]`
  - Обработать новую точку и проверить наличие смещения уровня.

Args:
    time_ms: Логическое время в миллисекундах.
    value: Значение сигнала (или информативный параметр от препроцессора).

Returns:
    Список обнаружений (обычно 0 или 1 элемент).
- `def _update_sigma_noise(self) -> None`
  - Обновить робастную оценку шума через MAD по базовой линии.
- `def _cusum_step(self, time_ms: int, value: float) -> list[DetectionResult]`
  - Один шаг алгоритма CUSUM.

Обновляет накопленные статистики S_high и S_low
и проверяет превышение порога.

Args:
    time_ms: Текущее логическое время.
    value: Текущее значение сигнала.

Returns:
    Список обнаружений смещения уровня.
- `def _report_deviation(self, time_ms: int, value: float, direction: str, statistic: float, threshold: float) -> list[DetectionResult]`
  - Зафиксировать обнаруженное смещение уровня.

Args:
    time_ms: Текущее логическое время.
    value: Текущее значение сигнала.
    direction: Направление смещения ("повышение" или "понижение").
    statistic: Текущее значение накопленной статистики.
    threshold: Порог срабатывания.

Returns:
    Список обнаружений.
- `def _adapt_baseline(self, value: float) -> None`
  - Адаптация базовой линии при стабильном сигнале.

Если отклонение не активно, обновляем базовую линию
с использованием экспоненциального сглаживания.

Args:
    value: Текущее значение сигнала.
- `def reset(self) -> None`
  - Сброс состояния детектора.
- `def get_state(self) -> dict`
  - Получить текущее состояние детектора для отладки и визуализации.

Returns:
    Словарь с текущими параметрами.

### Файл: `metrics.py`
> analytics/metrics.py

Подсчёт метрик сравнения эффективности обнаружения неисправностей оператором
и детектором. Строится на основе событий из журнала. Позволяет оценить,
на сколько процентов детектор быстрее оператора, а также число ложных
срабатываний и пропусков.
#### Импорты
- **Стандартная библиотека:**
  - `from dataclasses import dataclass`
  - `import logging`
- **Сторонние библиотеки:**
  - `from core.event_log import EventRecord, EventType`
#### Классы
##### `@dataclass class FaultAnalysisRecord`
> Результат анализа одной неисправности.
##### `@dataclass class MetricsSummary`
> Агрегированные метрики сравнения оператора и детектора.
Методы:
- `def to_dict(self) -> dict[str, float]`
  - Сериализация метрик в словарь.
##### `class MetricsCalculator`
> Калькулятор метрик сравнения оператора и детектора.

Анализирует события из журнала и вычисляет:
- количество обнаруженных неисправностей (оператором, детектором, обоими);
- средние задержки обнаружения;
- ложные срабатывания;
- пропущенные неисправности;
- процентное соотношение, на сколько детектор быстрее оператора.

Логика пропуска:
- Для трендовых неисправностей (деградация): пропуск, если не обнаружена
  до выхода графика за пороговые значения.
- Для остальных неисправностей: пропуск, если не обнаружена до внедрения
  следующей неисправности на том же графике.
Методы:
- `def __init__(self, trend_fault_types: set[str] | None) -> None`
  - Инициализация калькулятора метрик.

Args:
    trend_fault_types: Множество типов неисправностей, для которых
        выход за порог считается индикатором пропуска.
        По умолчанию — {"degradation"}.
- `def calculate(self, events: list[EventRecord]) -> MetricsSummary`
  - Вычислить метрики по списку событий журнала.

Args:
    events: Список записей журнала событий.

Returns:
    MetricsSummary: Агрегированные метрики.
- `def _extract_events(self, events: list[EventRecord], event_type: EventType) -> dict[str, list[EventRecord]]`
  - Группировка событий по идентификатору графика.
- `def _analyze_plot(self, plot_id: str, faults: list[EventRecord], operator_detections: list[EventRecord], detector_detections: list[EventRecord], limit_exceeded: list[EventRecord]) -> tuple`
  - Анализ неисправностей для одного графика.

Возвращает кортеж (список записей анализа, ложные оператора, ложные детектора).
- `def _find_first_detection(self, detections: list[EventRecord], start_ms: int, end_ms: float) -> EventRecord | None`
  - Поиск первого обнаружения в временном окне [start_ms, end_ms).
- `def _has_preceding_fault(self, faults: list[EventRecord], time_ms: int) -> bool`
  - Проверка, была ли неисправность до указанного времени.
- `def _is_missed(self, fault_type: str, record: FaultAnalysisRecord, next_injection_time: float, limit_exceeded: list[EventRecord]) -> bool`
  - Определение, является ли неисправность пропущенной.

Для трендовых неисправностей: пропуск, если не обнаружена до выхода за порог.
Для остальных: пропуск, если не обнаружена до следующей неисправности.
- `def _aggregate(self, records: list[FaultAnalysisRecord], operator_fp: int, detector_fp: int) -> MetricsSummary`
  - Агрегация результатов анализа в итоговые метрики.

### Файл: `signal_preprocessor.py`
> analytics/signal_preprocessor.py

Препроцессор сигналов — извлечение информативных параметров из сырых данных.
Работает O(1) по памяти на точку, адаптирован для реального времени.

Для каждого типа сигнала извлекает свой информативный параметр:
- Синус, Треугольник → амплитуда (скользящая огибающая)
- Меандр, Ступеньки → значения на плато (бимодальная фильтрация)
- Пила → наклон линейного участка
- Постоянный, Линейный, Экспонента, Шум → сырое значение
#### Импорты
- **Стандартная библиотека:**
  - `from collections import deque`
  - `from typing import Any`
  - `import logging`
- **Сторонние библиотеки:**
  - `import numpy as np`
#### Классы
##### `class SignalPreprocessor`
> Препроцессор сигналов для извлечения информативных параметров.
Применяет сигнал-специфичную фильтрацию перед детекцией аномалий.
Методы:
- `def __init__(self, signal_type: str, window_size: int) -> None`
  - Инициализация препроцессора.

Args:
    signal_type: Тип сигнала (sine, square, sawtooth и т.д.).
    window_size: Размер скользящего окна для анализа.
- `def process(self, time_ms: int, value: float) -> float | None`
  - Обработать точку и вернуть информативный параметр.

Args:
    time_ms: Логическое время в миллисекундах.
    value: Сырое значение сигнала.

Returns:
    Информативный параметр (амплитуда, наклон, уровень и т.д.)
    или None, если недостаточно данных для анализа.
- `def _process_bimodal(self, value: float) -> float | None`
  - Бимодальная фильтрация для меандра/ступенек.
Игнорирует фронты, возвращает значение на устойчивом уровне.
- `def _initialize_bimodal_levels(self) -> None`
  - Инициализация двух уровней по квантилям.
- `def _update_level(self, level: str, value: float) -> None`
  - Обновить скользящее среднее уровня.
- `def _process_envelope(self, value: float) -> float | None`
  - Анализ огибающей для синуса/треугольника.
Возвращает амплитуду (размах) сигнала.
- `def _process_slope(self, value: float) -> float | None`
  - Анализ наклона для пилы.
Возвращает скорость изменения на линейном участке.
- `def reset(self) -> None`
  - Сброс состояния препроцессора.
- `def get_state(self) -> dict[str, Any]`
  - Получить текущее состояние для отладки.

### Файл: `trend_detector.py`
> analytics/trend_detector.py

Детектор тренда на основе модели Хольта (двойное экспоненциальное сглаживание).
Обнаруживает медленный дрейф (низкочастотную составляющую) сигнала,
оценивая уровень и наклон в реальном времени.

Математическая основа:
    Уровень:  l_t = α·x_t + (1-α)·(l_{t-1} + b_{t-1}·dt)
    Наклон:   b_t = β·(l_t - l_{t-1})/dt + (1-β)·b_{t-1}

Критерий значимости тренда:
    Фиксированный: |b_t| > trend_threshold
    Автоматический: |b_t| > trend_auto_sigma · σ_noise / √N_eff

Поддерживает:
- Робастную оценку шума через MAD
- Прогноз времени выхода за допустимые пределы
- Подтверждение временем (time-to-live) для подавления ложных срабатываний
- Адаптацию коэффициентов под тип сигнала
#### Импорты
- **Стандартная библиотека:**
  - `from collections import deque`
  - `import logging`
- **Сторонние библиотеки:**
  - `from analytics.detector import DetectionResult, DetectionType, DetectorConfig`
  - `import numpy as np`
#### Классы
##### `class TrendDetector`
> Детектор тренда на основе модели Хольта.

Оценивает уровень и наклон сигнала в реальном времени (O(1) по памяти).
Фиксирует тренд, когда наклон статистически значимо отличается от нуля
и подтверждён несколькими последовательными точками (time-to-live).

Attributes:
    min_allowed: Минимально допустимое значение сигнала.
    max_allowed: Максимально допустимое значение сигнала.
Методы:
- `def __init__(self, min_allowed: float, max_allowed: float, config: DetectorConfig | None) -> None`
  - Инициализация детектора тренда.

Args:
    min_allowed: Минимально допустимое значение сигнала.
    max_allowed: Максимально допустимое значение сигнала.
    config: Конфигурация детектора. Если None — используется по умолчанию.
- `def set_config(self, config: DetectorConfig) -> None`
  - Обновить конфигурацию детектора.

Args:
    config: Новая конфигурация.
- `def get_config(self) -> DetectorConfig`
  - Возвращает текущую конфигурацию детектора.
- `def process(self, time_ms: int, value: float) -> list[DetectionResult]`
  - Обработать новую точку и проверить наличие тренда.

Args:
    time_ms: Логическое время в миллисекундах.
    value: Значение сигнала (или информативный параметр от препроцессора).

Returns:
    Список обнаружений (обычно 0 или 1 элемент).
- `def _holt_step(self, value: float, dt_sec: float) -> None`
  - Один шаг двойного экспоненциального сглаживания Хольта.

Обновляет уровень и наклон на основе нового значения.

Args:
    value: Текущее значение сигнала.
    dt_sec: Время с предыдущей точки в секундах.
- `def _update_sigma_noise(self) -> None`
  - Обновить робастную оценку шума через MAD.
- `def _check_trend(self, time_ms: int, current_value: float) -> list[DetectionResult]`
  - Проверить статистическую значимость тренда с подтверждением временем.

Args:
    time_ms: Текущее логическое время.
    current_value: Текущее значение сигнала.

Returns:
    Список обнаружений тренда.
- `def _get_significance_threshold(self) -> float`
  - Вычислить порог значимости наклона.

Если задан фиксированный порог — используется он.
Иначе — автоматический расчёт на основе шума и размера окна.

Returns:
    Порог значимости наклона (ед/сек).
- `@staticmethod def _format_time(seconds: float) -> str`
  - Форматировать время в человекочитаемую строку.
- `def reset(self) -> None`
  - Сброс состояния детектора.
- `def get_state(self) -> dict`
  - Получить текущее состояние детектора для отладки и визуализации.

Returns:
    Словарь с текущими параметрами.

### Файл: `__init__.py`
> core/__init__.py

Инициализация пакета `core` — ядро системы симуляции.
Содержит модули управления временем, конфигурациями и журналом событий.
#### Импорты
- **Сторонние библиотеки:**
  - `from core.clock import GlobalClock`
  - `from core.config import ConfigError, ConfigManager`
  - `from core.event_log import EventLog, EventRecord, EventType`

### Файл: `clock.py`
> core/clock.py
Модуль управления глобальным логическим временем симуляции.
Обеспечивает единый источник времени для всех компонентов системы.
#### Импорты
- **Стандартная библиотека:**
  - `from typing import ClassVar`
  - `import logging`
- **Сторонние библиотеки:**
  - `from PyQt6.QtCore import QObject, QTimer, pyqtSignal`
#### Классы
##### `class GlobalClock(QObject)`
> Глобальные часы симуляции с поддержкой ускорения времени.

Генерирует периодические сигналы обновления времени.

Attributes:
    time_updated (pyqtSignal): Сигнал, испускаемый при каждом обновлении времени.
        Передает текущее логическое время в миллисекундах.
Методы:
- `def __init__(self, parent: QObject | None) -> None`
  - Инициализация глобальных часов.

Args:
    parent: Родительский QObject для управления временем жизни.
- `def start(self) -> None`
  - Запуск симуляции времени.
- `def stop(self) -> None`
  - Остановка симуляции времени.
- `def reset(self) -> None`
  - Сброс времени в 0 миллисекунд.
- `def set_speed_multiplier(self, multiplier: int) -> None`
  - Установка множителя ускорения времени.

Args:
    multiplier: Множитель ускорения (должен быть в ALLOWED_MULTIPLIERS).

Raises:
    ValueError: Если множитель не входит в список допустимых.
- `def get_current_time_ms(self) -> int`
  - Получение текущего логического времени.

Returns:
    int: Текущее время в миллисекундах.
- `def get_speed_multiplier(self) -> int`
  - Получение текущего множителя ускорения.

Returns:
    int: Текущий множитель ускорения.
- `def is_running(self) -> bool`
  - Проверка состояния симуляции.

Returns:
    bool: True если симуляция запущена, False иначе.
- `def get_formatted_time(self) -> str`
  - Получение времени в формате ЧЧ:ММ:СС.мс.

Returns:
    str: Отформатированное время (например, "00:05:23.456").
- `def _on_tick(self) -> None`
  - Обработка тика таймера - обновление логического времени.

### Файл: `config.py`
> signalSimulator/core/config.py

Менеджер конфигураций: загрузка, сохранение и валидация настроек
графиков и неисправностей в формате JSON.
#### Импорты
- **Стандартная библиотека:**
  - `from datetime import datetime, timezone`
  - `from pathlib import Path`
  - `from typing import Any`
  - `import json`
  - `import logging`
#### Классы
##### `class ConfigError(Exception)`
> Кастомное исключение для ошибок конфигурации.
##### `class ConfigManager`
> Менеджер конфигураций симулятора.

Отвечает за сохранение и загрузку конфигураций в формате JSON,
а также за мягкую валидацию структуры данных.
Методы:
- `def __init__(self, configs_dir: Path | None) -> None`
  - Инициализация менеджера конфигураций.

Args:
    configs_dir: Путь к директории конфигураций.
                 По умолчанию используется папка 'configs/' проекта.
- `def save_config(self, config_data: dict) -> str`
  - Сохранение конфигурации в JSON-файл с автогенерацией имени.

Args:
    config_data: Словарь конфигурации для сохранения.

Returns:
    str: Путь к сохранённому файлу.

Raises:
    ConfigError: При ошибке записи файла.
- `def load_config(self, filepath: str) -> dict`
  - Загрузка конфигурации из JSON-файла.

Args:
    filepath: Путь к файлу конфигурации.

Returns:
    dict: Словарь загруженной конфигурации (после мягкой валидации).

Raises:
    ConfigError: При ошибке чтения или парсинга файла.
- `def validate_config(self, config_data: dict) -> dict`
  - Мягкая валидация конфигурации.
Дополняет отсутствующие поля значениями по умолчанию.

Args:
    config_data: Исходный словарь конфигурации.

Returns:
    dict: Валидированная конфигурация с заполненными полями.
- `def list_configs(self) -> list[str]`
  - Получение списка сохранённых конфигураций.

Returns:
    list[str]: Список имён файлов конфигураций.
- `def get_default_config(self) -> dict`
  - Получение пустой конфигурации-шаблона.

Returns:
    dict: Шаблон конфигурации со значениями по умолчанию.
- `def _validate_plot(self, plot: Any, index: int) -> dict`
  - Мягкая валидация одного графика.

Args:
    plot: Исходные данные графика.
    index: Индекс графика в списке (для генерации ID).

Returns:
    dict: Валидированный график.
- `def _validate_fault(self, fault: Any) -> dict`
  - Мягкая валидация одной неисправности.

Args:
    fault: Исходные данные неисправности.

Returns:
    dict: Валидированная неисправность.
- `def _generate_filename(self) -> str`
  - Автогенерация имени файла конфигурации.

Returns:
    str: Имя файла в формате 'config_YYYYMMDD_HHMMSS.json'.

### Файл: `event_log.py`
> core/event_log.py

Центральный журнал событий симуляции.
Фиксирует все значимые события с логическим временем и используется
как источник данных для отдельного окна логов и для аналитики.
#### Импорты
- **Стандартная библиотека:**
  - `from dataclasses import dataclass, field`
  - `from enum import Enum, auto`
  - `from typing import Any`
  - `import logging`
- **Сторонние библиотеки:**
  - `from PyQt6.QtCore import QObject, pyqtSignal`
#### Классы
##### `class EventType(Enum)`
> Типы событий симуляции.
##### `@dataclass class EventRecord`
> Запись события в журнале.

Содержит логическое время, тип события, связанный график,
текстовое описание и произвольные метаданные для аналитики.
Методы:
- `def __str__(self) -> str`
  - Строковое представление записи для отображения в логах.
##### `class EventLog(QObject)`
> Журнал событий симуляции.

Хранит все записи за сессию и испускает сигнал `event_added`
при добавлении новой записи. Окно логов подписывается на сигнал
для автоматического обновления. Аналитика читает записи через
методы фильтрации.
Методы:
- `def __init__(self, parent: QObject | None) -> None`
  - Инициализация журнала событий.

Args:
    parent: Родительский QObject для управления временем жизни.
- `def add(self, time_ms: int, event_type: EventType, description: str, plot_id: str | None, metadata: dict[str, Any] | None) -> EventRecord`
  - Добавить запись события в журнал.

Создаёт запись, сохраняет её и испускает сигнал `event_added`.

Args:
    time_ms: Логическое время события в миллисекундах.
    event_type: Тип события.
    description: Текстовое описание события.
    plot_id: Идентификатор связанного графика (опционально).
    metadata: Дополнительные данные для аналитики (опционально).

Returns:
    EventRecord: Созданная запись.
- `def get_records(self, event_type: EventType | None, plot_id: str | None, start_ms: int | None, end_ms: int | None) -> list[EventRecord]`
  - Получить записи журнала с фильтрацией.

Все параметры опциональны. При отсутствии параметра фильтр
по нему не применяется.

Args:
    event_type: Тип события (опционально).
    plot_id: Идентификатор графика (опционально).
    start_ms: Нижняя граница времени в мс (опционально).
    end_ms: Верхняя граница времени в мс (опционально).

Returns:
    Список подходящих записей.
- `def get_all(self) -> list[EventRecord]`
  - Получить все записи журнала.

Returns:
    Список всех записей.
- `def get_count(self) -> int`
  - Получить количество записей в журнале.

Returns:
    Количество записей.
- `def clear(self) -> None`
  - Очистить журнал событий.

### Файл: `__init__.py`
> simulation/__init__.py
Инициализация пакета `simulation` — слой симуляции сигналов и неисправностей.
Содержит генераторы сигналов, типы неисправностей и планировщик случайного внедрения.
#### Импорты
- **Сторонние библиотеки:**
  - `from simulation.faults import DegradationFault, DropoutFault, Fault, FaultChain, FaultFactory, NoiseFault, SpikeFault`
  - `from simulation.scheduler import FaultInjectionEvent, FaultScheduler, FaultTemplate, RandomFaultRule`
  - `from simulation.signals import CompositeSignal, ConstantSignal, ExponentialSignal, LinearSignal, NoiseSignal, SawtoothSignal, SignalFactory, SignalGenerator, SineSignal, SquareSignal, StepSignal, TriangleSignal`

### Файл: `faults.py`
> simulation/faults.py

Типы неисправностей для симуляции аномалий в телеметрических сигналах.
Каждая неисправность модифицирует базовое значение сигнала в заданный момент
логического времени. Поддерживаются активация/деактивация, периодичность
и композиция (последовательное применение нескольких неисправностей).
#### Импорты
- **Стандартная библиотека:**
  - `from abc import ABC, abstractmethod`
  - `from typing import Any, ClassVar`
  - `import logging`
  - `import random`
#### Классы
##### `class Fault(ABC)`
> Абстрактный базовый класс для всех неисправностей.

Неисправность активируется в определённый момент времени и может быть
однократной или периодической. Логика периодичности реализована в `is_active`.
Конкретные неисправности реализуют `_apply_effect`.

Attributes:
    duration_ms: Длительность активности в мс. `None` означает бесконечность.
    period_ms: Период повторения в мс. `None` или `0` — однократная неисправность.
    activation_time_ms: Время активации (для скрытых меток на графике).
Методы:
- `def __init__(self, duration_ms: int | None, period_ms: int | None) -> None`
- `def activate(self, time_ms: int) -> None`
  - Активировать неисправность в заданный момент времени.
- `def deactivate(self) -> None`
  - Деактивировать неисправность.
- `def is_active(self, time_ms: int) -> bool`
  - Проверить, активна ли неисправность в заданный момент времени.

Для периодической неисправности активна в окнах
`[activation + k*period, activation + k*period + duration]`.
Для однократной активна в `[activation, activation + duration]`.

Args:
    time_ms: Логическое время в миллисекундах.

Returns:
    bool: Активна ли неисправность.
- `def _effective_duration(self) -> int`
  - Эффективная длительность для проверки окна (при периодичности).
- `def apply(self, time_ms: int, base_value: float) -> float`
  - Применить неисправность к базовому значению.

Если неисправность не активна в данный момент, возвращает исходное значение.

Args:
    time_ms: Логическое время в миллисекундах.
    base_value: Базовое значение сигнала.

Returns:
    float: Модифицированное значение.
- `@abstractmethod def _apply_effect(self, time_ms: int, base_value: float) -> float`
  - Внутренний метод применения эффекта неисправности.

Вызывается только когда неисправность активна.

Args:
    time_ms: Логическое время в миллисекундах.
    base_value: Базовое значение сигнала.

Returns:
    float: Модифицированное значение.
- `@abstractmethod def get_params(self) -> dict[str, Any]`
  - Получить параметры неисправности для сериализации.

Returns:
    dict: Словарь параметров.
##### `class DropoutFault(Fault)`
> Пропадание сигнала.

Во время активности сигнал заменяется на заданное значение
(по умолчанию 0.0). Может быть однократным или периодическим.
Методы:
- `def __init__(self, duration_ms: int | None, period_ms: int | None, dropout_value: float) -> None`
- `def _apply_effect(self, time_ms: int, base_value: float) -> float`
- `def get_params(self) -> dict[str, Any]`
##### `class SpikeFault(Fault)`
> Скачок (импульс).

Величина скачка задаётся в процентах от базового значения.
Например, `magnitude_percent=100` удваивает значение.
Для имитации короткого замыкания задайте большой процент
и `duration_ms=None` (бесконечная длительность).
Методы:
- `def __init__(self, magnitude_percent: float, duration_ms: int | None, period_ms: int | None) -> None`
- `def _apply_effect(self, time_ms: int, base_value: float) -> float`
- `def get_params(self) -> dict[str, Any]`
##### `class NoiseFault(Fault)`
> Шум (гауссовский).

Добавляет случайное значение с нормальным распределением к базовому сигналу.
Сила шума задаётся параметром `sigma`. Неисправность активна всё время
после активации (по умолчанию длительность бесконечная).
Методы:
- `def __init__(self, mean: float, sigma: float, duration_ms: int | None, period_ms: int | None) -> None`
- `def _apply_effect(self, time_ms: int, base_value: float) -> float`
- `def get_params(self) -> dict[str, Any]`
##### `class DegradationFault(Fault)`
> Деградация (линейный тренд).

Скорость деградации задаётся в процентах в секунду от базового значения,
зафиксированного в момент активации. Знак `rate_percent_per_sec` определяет
направление: положительный — рост, отрицательный — убывание.

Пример: `rate_percent_per_sec=-0.001` означает уменьшение на 0.001% в секунду.
Методы:
- `def __init__(self, rate_percent_per_sec: float, duration_ms: int | None) -> None`
- `def activate(self, time_ms: int) -> None`
  - Активация с сбросом зафиксированного базового значения.
- `def _apply_effect(self, time_ms: int, base_value: float) -> float`
- `def get_params(self) -> dict[str, Any]`
##### `class FaultChain`
> Цепочка неисправностей для последовательного применения к сигналу.

Позволяет комбинировать несколько неисправностей на одном графике,
например: базовый сигнал + шум + деградация.
Методы:
- `def __init__(self, faults: list[Fault] | None) -> None`
- `def add_fault(self, fault: Fault) -> None`
  - Добавить неисправность в цепочку.
- `def remove_fault(self, fault: Fault) -> None`
  - Удалить неисправность из цепочки.
- `def clear(self) -> None`
  - Очистить цепочку.
- `def get_faults(self) -> list[Fault]`
  - Получить список неисправностей в цепочке.
- `def apply_all(self, time_ms: int, base_value: float) -> float`
  - Применить все активные неисправности последовательно.

Args:
    time_ms: Логическое время в миллисекундах.
    base_value: Базовое значение сигнала.

Returns:
    float: Значение после применения всех неисправностей.
- `def deactivate_all(self) -> None`
  - Деактивировать все неисправности в цепочке.
##### `class FaultFactory`
> Фабрика для создания неисправностей по строковому типу.
Методы:
- `@classmethod def register(cls, name: str, fault_class: type) -> None`
  - Зарегистрировать новый тип неисправности.
- `@classmethod def create(cls, fault_type: str, params: dict[str, Any] | None) -> Fault | None`
  - Создать неисправность по типу и параметрам.

Args:
    fault_type: Строковый тип неисправности.
    params: Словарь параметров.

Returns:
    Fault: Экземпляр неисправности. При ошибке — `None`.
- `@classmethod def available_types(cls) -> list[str]`
  - Вернуть список доступных типов неисправностей.

### Файл: `scheduler.py`
> simulation/scheduler.py

Механизм случайного внедрения неисправностей. Каждые N секунд проверяется
генератор случайных чисел, и с вероятностью X активируется неисправность
на целевых графиках. Параметры N и X задаёт оператор. Поддерживается
несколько независимых правил и реестр заготовленных шаблонов неисправностей.
#### Импорты
- **Стандартная библиотека:**
  - `from dataclasses import dataclass, field`
  - `from typing import Any`
  - `import logging`
  - `import random`
#### Классы
##### `@dataclass class FaultInjectionEvent`
> Событие внедрения неисправности.

Генерируется планировщиком при срабатывании правила и обрабатывается
внешним менеджером симуляции (создание экземпляра неисправности,
добавление в цепочку графика, активация, запись в журнал).
##### `@dataclass class FaultTemplate`
> Шаблон неисправности (заготовка).

Создаётся оператором и хранится в реестре планировщика. При срабатывании
правила планировщик использует шаблон для генерации события внедрения.

Режимы внедрения (target_mode):
    - "one": один случайный график из списка
    - "all": все графики из списка
    - "random_subset": случайное подмножество размера subset_count
Методы:
- `def select_target_plot_ids(self, available_plot_ids: list[str]) -> list[str]`
  - Определить целевые графики согласно режиму внедрения.

Если `target_plot_ids` пуст, используются все доступные графики
из `available_plot_ids`.

Args:
    available_plot_ids: Список всех доступных графиков.

Returns:
    Список целевых графиков.
##### `@dataclass class RandomFaultRule`
> Правило случайного внедрения неисправностей.

Каждые `check_interval_ms` миллисекунд проверяется генератор случайных
чисел. Если случайное число меньше `probability`, правило срабатывает
и выбирает один из шаблонов для внедрения.

Вероятность задаётся в долях: 0.0 — никогда, 1.0 — всегда.
##### `class FaultScheduler`
> Планировщик случайного внедрения неисправностей.

Хранит реестр шаблонов неисправностей и список правил. На каждом тике
времени (`tick`) проверяет правила и генерирует события внедрения.
Планировщик не знает о графиках и экземплярах неисправностей — он только
генерирует события, которые обрабатываются внешним менеджером.
Методы:
- `def __init__(self) -> None`
  - Инициализация планировщика с пустыми реестрами.
- `def add_template(self, template: FaultTemplate) -> None`
  - Добавить шаблон неисправности в реестр.
- `def remove_template(self, template_id: str) -> None`
  - Удалить шаблон неисправности из реестра.
- `def get_template(self, template_id: str) -> FaultTemplate | None`
  - Получить шаблон по ID.
- `def list_templates(self) -> list[FaultTemplate]`
  - Получить список всех шаблонов.
- `def add_rule(self, rule: RandomFaultRule) -> None`
  - Добавить правило случайного внедрения.
- `def remove_rule(self, rule_id: str) -> None`
  - Удалить правило случайного внедрения.
- `def get_rule(self, rule_id: str) -> RandomFaultRule | None`
  - Получить правило по ID.
- `def list_rules(self) -> list[RandomFaultRule]`
  - Получить список всех правил.
- `def tick(self, current_time_ms: int, available_plot_ids: list[str]) -> list[FaultInjectionEvent]`
  - Обработка одного тика времени.

Для каждого активного правила проверяет, наступило ли время проверки.
Если да — генерирует случайное число и при срабатывании создаёт
события внедрения. Корректно обрабатывает ускорение времени:
все пропущенные интервалы проверяются последовательно.

Args:
    current_time_ms: Текущее логическое время в миллисекундах.
    available_plot_ids: Список всех доступных графиков.

Returns:
    Список событий внедрения неисправностей.
- `def _inject_from_rule(self, rule: RandomFaultRule, time_ms: int, available_plot_ids: list[str]) -> list[FaultInjectionEvent]`
  - Внутренний метод генерации событий при срабатывании правила.

Выбирает случайный шаблон из списка правила, определяет целевые
графики и создаёт события внедрения для каждого целевого графика.

Args:
    rule: Сработавшее правило.
    time_ms: Время срабатывания.
    available_plot_ids: Список всех доступных графиков.

Returns:
    Список событий внедрения.
- `def reset(self) -> None`
  - Сброс состояния всех правил (при сбросе симуляции).
- `def clear(self) -> None`
  - Очистка реестров шаблонов и правил.

### Файл: `signals.py`
> signalSimulator/simulation/signals.py

Генераторы базовых сигналов для симуляции телеметрических данных.
Каждый генератор возвращает значение сигнала в заданный момент логического времени.
#### Импорты
- **Стандартная библиотека:**
  - `from abc import ABC, abstractmethod`
  - `from typing import Any, ClassVar`
  - `import logging`
  - `import math`
  - `import random`
#### Классы
##### `class SignalGenerator(ABC)`
> Абстрактный базовый класс для всех генераторов сигналов.

Определяет контракт: метод `get_value(time_ms)` возвращает
значение сигнала в момент времени `time_ms` (в миллисекундах).
Методы:
- `@abstractmethod def get_value(self, time_ms: int) -> float`
  - Получить значение сигнала в заданный момент времени.

Args:
    time_ms: Логическое время в миллисекундах.

Returns:
    float: Значение сигнала.
- `@abstractmethod def get_params(self) -> dict[str, Any]`
  - Получить параметры сигнала в виде словаря (для сериализации).

Returns:
    dict: Словарь параметров.
##### `class CompositeSignal(SignalGenerator)`
> Композитный сигнал — сумма нескольких сигналов.

Позволяет комбинировать базовый сигнал с трендами, шумами
и другими компонентами. Используется для построения
сложных сигналов, включая неисправности.
Методы:
- `def __init__(self, signals: list[SignalGenerator] | None) -> None`
  - Args:
    signals: Список вложенных сигналов для суммирования.
- `def add_signal(self, signal: SignalGenerator) -> None`
  - Добавить сигнал в композицию.
- `def remove_signal(self, signal: SignalGenerator) -> None`
  - Удалить сигнал из композиции.
- `def get_value(self, time_ms: int) -> float`
  - Сумма значений всех вложенных сигналов.
- `def get_params(self) -> dict[str, Any]`
  - Параметры всех вложенных сигналов.
##### `class SawtoothSignal(SignalGenerator)`
> Пилообразный сигнал: линейный рост от min_val до max_val за период,
затем резкий сброс к min_val.
Методы:
- `def __init__(self, min_val: float, max_val: float, period_ms: int, offset: float) -> None`
- `def get_value(self, time_ms: int) -> float`
- `def get_params(self) -> dict[str, Any]`
##### `class TriangleSignal(SignalGenerator)`
> Треугольный сигнал (симметричная пила): линейный рост от min_val до max_val,
затем линейное падение обратно к min_val.
Методы:
- `def __init__(self, min_val: float, max_val: float, period_ms: int, offset: float) -> None`
- `def get_value(self, time_ms: int) -> float`
- `def get_params(self) -> dict[str, Any]`
##### `class SineSignal(SignalGenerator)`
> Синусоидальный сигнал.
Методы:
- `def __init__(self, amplitude: float, period_ms: int, phase: float, offset: float) -> None`
- `def get_value(self, time_ms: int) -> float`
- `def get_params(self) -> dict[str, Any]`
##### `class StepSignal(SignalGenerator)`
> Ступенчатый сигнал: первая половина периода — min_val,
вторая половина — max_val.
Методы:
- `def __init__(self, min_val: float, max_val: float, period_ms: int, offset: float) -> None`
- `def get_value(self, time_ms: int) -> float`
- `def get_params(self) -> dict[str, Any]`
##### `class LinearSignal(SignalGenerator)`
> Линейный сигнал (тренд).

Параметр rate_per_sec — скорость изменения значения за секунду.
Например, rate_per_sec = 0.01 означает, что за 1 секунду значение
увеличивается на 0.01.
Методы:
- `def __init__(self, start_val: float, rate_per_sec: float, offset: float) -> None`
- `def get_value(self, time_ms: int) -> float`
- `def get_params(self) -> dict[str, Any]`
##### `class SquareSignal(SignalGenerator)`
> Прямоугольный сигнал (меандр) с настраиваемым коэффициентом заполнения.

duty_cycle — доля периода, в течение которой сигнал находится в max_val.
Методы:
- `def __init__(self, min_val: float, max_val: float, period_ms: int, duty_cycle: float, offset: float) -> None`
- `def get_value(self, time_ms: int) -> float`
- `def get_params(self) -> dict[str, Any]`
##### `class ExponentialSignal(SignalGenerator)`
> Экспоненциальный сигнал.

Значение: offset + amplitude * exp(rate_per_sec * t_sec).
При отрицательном rate_per_sec получаем затухающую экспоненту.
Методы:
- `def __init__(self, amplitude: float, rate_per_sec: float, offset: float) -> None`
- `def get_value(self, time_ms: int) -> float`
- `def get_params(self) -> dict[str, Any]`
##### `class NoiseSignal(SignalGenerator)`
> Случайный шум (гауссовский).

Каждый вызов `get_value` возвращает новое случайное значение
с нормальным распределением. Параметр sigma задаёт силу шума.
Методы:
- `def __init__(self, mean: float, sigma: float) -> None`
- `def get_value(self, time_ms: int) -> float`
- `def get_params(self) -> dict[str, Any]`
##### `class ConstantSignal(SignalGenerator)`
> Постоянное значение.
Методы:
- `def __init__(self, value: float) -> None`
- `def get_value(self, time_ms: int) -> float`
- `def get_params(self) -> dict[str, Any]`
##### `class SignalFactory`
> Фабрика для создания генераторов сигналов по типу.

Поддерживает все зарегистрированные типы сигналов.
Методы:
- `@classmethod def register(cls, name: str, signal_class: type) -> None`
  - Зарегистрировать новый тип сигнала.
- `@classmethod def create(cls, signal_type: str, params: dict[str, Any] | None) -> SignalGenerator`
  - Создать генератор сигнала по типу и параметрам.

Args:
    signal_type: Строковый тип сигнала.
    params: Словарь параметров для инициализации.

Returns:
    SignalGenerator: Экземпляр сигнала. При ошибке — ConstantSignal(0).
- `@classmethod def available_types(cls) -> list[str]`
  - Вернуть список доступных типов сигналов.

### Файл: `simulator.py`
> simulation/simulator.py

Движок симуляции — центральный связующий компонент.
Объединяет часы, генераторы сигналов, неисправности, планировщик, детектор
аномалий и журнал событий. Вычисляет значения графиков на каждом тике времени
с шагом 1 симуляционная секунда, обрабатывает события внедрения неисправностей
и прогоняет данные через трёхкомпонентный детектор аномалий.
#### Импорты
- **Стандартная библиотека:**
  - `from typing import Any`
  - `import logging`
- **Сторонние библиотеки:**
  - `from PyQt6.QtCore import QObject, pyqtSignal`
  - `from analytics.detector import AnomalyDetector, DetectorConfig`
  - `from core.clock import GlobalClock`
  - `from core.event_log import EventLog, EventType`
  - `from simulation.faults import Fault, FaultChain, FaultFactory`
  - `from simulation.scheduler import FaultInjectionEvent, FaultScheduler`
  - `from simulation.signals import SignalGenerator`
  - `import numpy as np`
#### Классы
##### `class HistoryBuffer`
> Эффективный буфер истории значений сигнала.

Хранит данные в виде блоков (чанков) `numpy` массивов, что позволяет
работать с большими объёмами данных (например, телеметрия за несколько
симуляционных лет) без чрезмерного потребления памяти.
Методы:
- `def __init__(self) -> None`
- `def append(self, time_ms: int, value: float) -> None`
  - Добавить точку (время, значение) в буфер.
- `def _flush_pending(self) -> None`
  - Сбросить накопленные точки в чанки `numpy`.
- `def get_all_times(self) -> np.ndarray`
  - Получить все времена как единый массив.
- `def get_all_values(self) -> np.ndarray`
  - Получить все значения как единый массив.
- `def get_last(self, n: int) -> tuple[np.ndarray, np.ndarray]`
  - Получить последние `n` точек (для отображения).
- `def get_count(self) -> int`
  - Получить общее количество точек.
- `def clear(self) -> None`
  - Очистить буфер.
##### `class PlotState`
> Состояние одного графика симуляции.
Методы:
- `def __init__(self, plot_id: str, name: str, unit: str, max_unit_value: float, signal: SignalGenerator, min_allowed: float, max_allowed: float, observation_interval_ms: int, detector_config: DetectorConfig | None) -> None`
- `def init_detector(self) -> None`
  - Инициализировать детектор аномалий с текущей конфигурацией.
- `def update_detector_config(self, config: DetectorConfig) -> None`
  - Обновить конфигурацию детектора. Пересоздаёт детектор с новыми параметрами.

Args:
    config: Новая конфигурация детектора.
##### `class SimulationEngine(QObject)`
> Движок симуляции.

Подписывается на сигнал `time_updated` глобальных часов, генерирует
данные графиков с шагом 1 симуляционная секунда, обрабатывает события
планировщика неисправностей, прогоняет данные через детектор аномалий
и ведёт журнал событий.
Методы:
- `def __init__(self, clock: GlobalClock, event_log: EventLog, scheduler: FaultScheduler | None, parent: QObject | None) -> None`
  - Инициализация движка симуляции.

Args:
    clock: Глобальные часы симуляции.
    event_log: Журнал событий.
    scheduler: Планировщик случайных неисправностей (опционально).
    parent: Родительский QObject.
- `def add_plot(self, plot_id: str, name: str, unit: str, max_unit_value: float, signal: SignalGenerator, min_allowed: float, max_allowed: float, observation_interval_ms: int, detector_config: DetectorConfig | None) -> PlotState`
  - Добавить график в симуляцию и инициализировать для него детектор аномалий.

Args:
    plot_id: Уникальный идентификатор графика.
    name: Название графика.
    unit: Единица измерения.
    max_unit_value: Максимальное значение единицы измерения.
    signal: Генератор сигнала.
    min_allowed: Минимально допустимое значение.
    max_allowed: Максимально допустимое значение.
    observation_interval_ms: Интервал наблюдения.
    detector_config: Конфигурация детектора (опционально).

Returns:
    PlotState: Состояние созданного графика.
- `def remove_plot(self, plot_id: str) -> None`
  - Удалить график из симуляции.
- `def get_plot(self, plot_id: str) -> PlotState | None`
  - Получить состояние графика по ID.
- `def get_all_plot_ids(self) -> list[str]`
  - Получить список всех идентификаторов графиков.
- `def update_plot_detector_config(self, plot_id: str, detector_config: DetectorConfig) -> None`
  - Обновить конфигурацию детектора для существующего графика.

Args:
    plot_id: Идентификатор графика.
    detector_config: Новая конфигурация детектора.
- `def _on_time_updated(self, time_ms: int) -> None`
  - Обработка тика часов: генерация данных и обработка событий.
- `def _generate_points(self, plot: PlotState, current_time_ms: int) -> None`
  - Генерация точек для графика до текущего времени с шагом 1 секунда.
Каждая точка пропускается через детектор аномалий.
- `def inject_fault(self, plot_id: str, fault_type: str, fault_params: dict[str, Any]) -> Fault | None`
  - Ручное внедрение неисправности на график.

Создаёт неисправность через фабрику, добавляет в цепочку,
активирует и фиксирует скрытую метку.

Args:
    plot_id: Идентификатор графика.
    fault_type: Тип неисправности.
    fault_params: Параметры неисправности.

Returns:
    Созданная неисправность или `None` при ошибке.
- `def process_injection_events(self, events: list[FaultInjectionEvent]) -> None`
  - Обработка событий внедрения от планировщика.

Для каждого события создаёт неисправность, добавляет в цепочку
графика, активирует и фиксирует скрытую метку.

Args:
    events: Список событий внедрения.
- `def record_operator_detection(self, plot_id: str) -> None`
  - Фиксация обнаружения неисправности оператором.
- `def record_detector_detection(self, plot_id: str, description: str) -> None`
  - Фиксация обнаружения неисправности детектором.

Args:
    plot_id: Идентификатор графика.
    description: Детальное описание причины обнаружения
                 (для журнала событий).
- `def reset(self) -> None`
  - Сброс состояния движка (очистка историй, меток и детекторов).

### Файл: `__init__.py`

### Файл: `options_panel.py`
> ui/panels/options_panel.py

Панель дополнительных настроек главного окна.
Содержит два чекбокса:
- Показывать скрытые метки неисправностей (управляет видимостью меток на графиках).
- Показать журнал событий (дублирует действие из меню для удобства).

Эмитирует сигналы для координатора при изменении состояния пользователем.
Программное изменение состояния (для синхронизации с меню) не вызывает
повторной эмиссии сигналов, что предотвращает циклические обновления.
#### Импорты
- **Стандартная библиотека:**
  - `import logging`
- **Сторонние библиотеки:**
  - `from PyQt6.QtCore import pyqtSignal`
  - `from PyQt6.QtWidgets import QCheckBox, QHBoxLayout, QWidget`
#### Классы
##### `class OptionsPanel(QWidget)`
> Панель дополнительных настроек главного окна.

Signals:
    hidden_markers_toggled(bool): Режим скрытых меток включён/выключен.
    journal_toggled(bool): Журнал событий открыт/закрыт.
Методы:
- `def __init__(self, parent: QWidget | None) -> None`
  - Инициализация панели дополнительных настроек.

Args:
    parent: Родительский виджет.
- `def _init_ui(self) -> None`
  - Создание интерфейса панели дополнительных настроек.
- `def _connect_signals(self) -> None`
  - Подключение внутренних сигналов панели.
- `def set_hidden_markers_state(self, checked: bool) -> None`
  - Программно установить состояние чекбокса скрытых меток.

Не вызывает эмиссию сигнала `hidden_markers_toggled`,
чтобы избежать циклических обновлений при синхронизации.

Args:
    checked: True — включить, False — выключить.
- `def set_journal_state(self, checked: bool) -> None`
  - Программно установить состояние чекбокса журнала событий.

Не вызывает эмиссию сигнала `journal_toggled`,
чтобы избежать циклических обновлений при синхронизации с меню.

Args:
    checked: True — открыть журнал, False — закрыть.
- `def _on_hidden_markers_changed(self, state: int) -> None`
  - Обработка изменения состояния чекбокса скрытых меток пользователем.
- `def _on_journal_changed(self, checked: bool) -> None`
  - Обработка изменения состояния чекбокса журнала пользователем.

### Файл: `plots_panel.py`
> ui/panels/plots_panel.py

Панель управления графиками симуляции.
Содержит список активных графиков и кнопки для добавления, открытия,
настройки и удаления графиков.

Эмитирует сигналы с идентификатором выбранного графика для координатора.
#### Импорты
- **Стандартная библиотека:**
  - `import logging`
- **Сторонние библиотеки:**
  - `from PyQt6.QtCore import Qt, pyqtSignal`
  - `from PyQt6.QtWidgets import QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QWidget`
#### Классы
##### `class PlotsPanel(QWidget)`
> Панель управления графиками.

Signals:
    add_requested: Запрос на создание нового графика.
    open_requested: Запрос на открытие окна выбранного графика (plot_id).
    settings_requested: Запрос на изменение настроек выбранного графика (plot_id).
    remove_requested: Запрос на удаление выбранного графика (plot_id).
Методы:
- `def __init__(self, parent: QWidget | None) -> None`
  - Инициализация панели управления графиками.

Args:
    parent: Родительский виджет.
- `def _init_ui(self) -> None`
  - Создание интерфейса панели управления графиками.
- `def _connect_signals(self) -> None`
  - Подключение внутренних сигналов панели.
- `def add_item(self, plot_id: str, name: str) -> None`
  - Добавить график в список на панели.

Args:
    plot_id: Идентификатор графика.
    name: Отображаемое название графика.
- `def remove_item(self, plot_id: str) -> None`
  - Удалить график из списка на панели.

Args:
    plot_id: Идентификатор графика.
- `def get_selected_plot_id(self) -> str | None`
  - Получить идентификатор выбранного графика.

Returns:
    str | None: Идентификатор выбранного графика или None, если ничего не выбрано.
- `def _on_open_plot(self) -> None`
  - Обработка нажатия кнопки 'Открыть'.
- `def _on_settings_plot(self) -> None`
  - Обработка нажатия кнопки 'Настройки'.
- `def _on_remove_plot(self) -> None`
  - Обработка нажатия кнопки 'Удалить'.
- `def _on_selection_changed(self, current: QListWidgetItem | None, previous: QListWidgetItem | None) -> None`
  - Обработка изменения выбора в списке графиков.

### Файл: `time_panel.py`
> ui/panels/time_panel.py

Панель управления временем симуляции.
Содержит кнопки запуска/остановки/сброса, выпадающий список скорости
и крупную метку текущего логического времени.

Подписывается на сигнал `time_updated` глобальных часов для обновления
отображения времени и эмитирует сигналы для координатора.
#### Импорты
- **Стандартная библиотека:**
  - `import logging`
- **Сторонние библиотеки:**
  - `from PyQt6.QtCore import pyqtSignal`
  - `from PyQt6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QPushButton, QWidget`
  - `from core.clock import GlobalClock`
#### Классы
##### `class TimePanel(QWidget)`
> Панель управления временем симуляции.

Signals:
    start_requested: Запрос на запуск симуляции.
    stop_requested: Запрос на остановку симуляции.
    reset_requested: Запрос на полный сброс симуляции.
    speed_changed(int): Изменение множителя ускорения времени.
Методы:
- `def __init__(self, clock: GlobalClock, parent: QWidget | None) -> None`
  - Инициализация панели управления временем.

Args:
    clock: Глобальные часы симуляции (источник времени и сигналов).
    parent: Родительский виджет.
- `def _init_ui(self) -> None`
  - Создание интерфейса панели управления временем.
- `def _connect_signals(self) -> None`
  - Подключение внутренних сигналов панели.
- `def set_running_state(self, is_running: bool) -> None`
  - Обновить состояние кнопок Старт/Стоп в зависимости от состояния симуляции.

Args:
    is_running: True, если симуляция запущена, False — если остановлена.
- `def reset_time_display(self, formatted_time: str) -> None`
  - Сбросить отображение времени к указанному значению.

Args:
    formatted_time: Отформатированная строка времени (например, "00:00:00.000").
- `def _on_speed_changed(self, index: int) -> None`
  - Обработка изменения выбранного множителя ускорения.
- `def _on_time_updated(self, time_ms: int) -> None`
  - Обновление отображения текущего времени.

### Файл: `__init__.py`
> ui/__init__.py

Инициализация пакета `ui` — графический интерфейс приложения.
Содержит модули главного окна, окон графиков, неисправностей,
журнала событий и диалогов создания/настройки.
#### Импорты
- **Сторонние библиотеки:**
  - `from ui.fault_rule_dialog import FaultRuleDialog`
  - `from ui.fault_template_dialog import FaultTemplateDialog`
  - `from ui.fault_window import FaultWindow`
  - `from ui.log_window import LogWindow`
  - `from ui.main_window import MainWindow`
  - `from ui.plot_creation_dialog import PlotCreationDialog`
  - `from ui.plot_window import PlotWindow`

### Файл: `detector_settings_tab.py`
> ui/detector_settings_tab.py

Вкладка настроек детектора аномалий для диалога создания/редактирования графика.
Отображает информацию об активных детекторах (тренд, аномалия, отклонение)
с пояснениями, почему они выбраны для текущего типа сигнала, и предоставляет
элементы настройки параметров каждого детектора с подробными подсказками.

Поддерживает новую архитектуру с разделением ответственности:
- Детектор тренда (модель Хольта)
- Детектор аномалий (остатки прогноза)
- Детектор отклонений (CUSUM)
#### Импорты
- **Стандартная библиотека:**
  - `import logging`
- **Сторонние библиотеки:**
  - `from PyQt6.QtWidgets import QDoubleSpinBox, QFormLayout, QGroupBox, QLabel, QSpinBox, QVBoxLayout, QWidget`
  - `from analytics.detector import DetectorConfig`
#### Классы
##### `class DetectorSettingsTab(QWidget)`
> Виджет вкладки настроек детектора.

Отображает активные детекторы для выбранного типа сигнала
и предоставляет элементы управления для конфигурации каждого:
- Общие параметры (окно, мин. точек, толерантность к шуму)
- Детектор тренда (порог, авто-сигма, подтверждение временем)
- Детектор аномалий (множитель сигмы, подтверждение временем)
- Детектор отклонений CUSUM (дрейф, порог, адаптация базовой линии)
Методы:
- `def __init__(self, parent: QWidget | None) -> None`
  - Инициализация вкладки настроек детектора.

Args:
    parent: Родительский виджет.
- `def _init_ui(self) -> None`
  - Создание интерфейса вкладки настроек детектора.
- `def _create_common_params_group(self) -> QGroupBox`
  - Создание группы общих параметров детекторов.
- `def _create_trend_params_group(self) -> QGroupBox`
  - Создание группы параметров детектора тренда.
- `def _create_anomaly_params_group(self) -> QGroupBox`
  - Создание группы параметров детектора аномалий.
- `def _create_deviation_params_group(self) -> QGroupBox`
  - Создание группы параметров детектора отклонений (CUSUM).
- `def update_model_info(self, signal_type: str, config: DetectorConfig) -> None`
  - Обновить отображение активных детекторов и пояснений к ним.

Очищает блок информации и создаёт новые метки для каждого
активного детектора с его названием и описанием.

Args:
    signal_type: Тип сигнала (например, 'sine', 'square').
    config: Текущая конфигурация детектора.
- `def get_config(self) -> DetectorConfig`
  - Считать текущие значения из интерфейса и вернуть объект DetectorConfig.

Returns:
    DetectorConfig: Текущая конфигурация детектора.
- `def set_config(self, config: DetectorConfig) -> None`
  - Заполнить интерфейс значениями из переданного объекта DetectorConfig.

Args:
    config: Конфигурация детектора для загрузки.

### Файл: `fault_rule_dialog.py`
> ui/fault_rule_dialog.py
Модальный диалог создания правила автоматического внедрения неисправностей.
Позволяет настроить название правила, выбрать шаблон неисправности,
задать период проверки, вероятность срабатывания и режим внедрения.
#### Импорты
- **Стандартная библиотека:**
  - `import logging`
- **Сторонние библиотеки:**
  - `from PyQt6.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QDoubleSpinBox, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QRadioButton, QSpinBox, QVBoxLayout, QWidget`
  - `from simulation.scheduler import FaultTemplate, RandomFaultRule`
#### Классы
##### `class FaultRuleDialog(QDialog)`
> Модальный диалог создания правила автоматического внедрения неисправностей.

Позволяет настроить:
- Название правила
- Выбор шаблона (из списка)
- Период проверки (N мс)
- Вероятность срабатывания (X в долях 0.0–1.0)
- Режим внедрения: один / все / случайное подмножество
Методы:
- `def __init__(self, available_templates: list[FaultTemplate], parent: QWidget | None) -> None`
  - Инициализация диалога правила.

Args:
    available_templates: Список доступных шаблонов для выбора.
    parent: Родительский виджет.
- `def _init_ui(self) -> None`
  - Создание интерфейса диалога.
- `def _on_accept(self) -> None`
  - Обработчик нажатия кнопки ОК.
- `def get_rule(self) -> RandomFaultRule | None`
  - Получить созданное правило.

### Файл: `fault_template_dialog.py`
> ui/fault_template_dialog.py
Модальный диалог создания и редактирования шаблона неисправности.
Позволяет настроить название, тип неисправности, динамические параметры
и характер действия (постоянная, разовая, периодическая).
#### Импорты
- **Стандартная библиотека:**
  - `import logging`
- **Сторонние библиотеки:**
  - `from PyQt6.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QDoubleSpinBox, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QRadioButton, QSpinBox, QVBoxLayout, QWidget`
  - `from simulation.faults import FaultFactory`
  - `from simulation.scheduler import FaultTemplate`
#### Классы
##### `class FaultTemplateDialog(QDialog)`
> Модальный диалог создания/редактирования шаблона неисправности.

Позволяет настроить:
- Название шаблона
- Тип неисправности (dropout, spike, noise, degradation)
- Динамические поля параметров (аналогично настройке сигналов)
- Характер: постоянная / разовая / периодическая
- Для разовой и периодической: длительность и период
Методы:
- `def __init__(self, template: FaultTemplate | None, parent: QWidget | None) -> None`
  - Инициализация диалога шаблона.

Args:
    template: Существующий шаблон для редактирования (опционально).
    parent: Родительский виджет.
- `def _init_ui(self) -> None`
  - Создание интерфейса диалога.
- `def _on_character_changed(self) -> None`
  - Обработчик изменения характера неисправности.
- `def _update_fault_params_fields(self) -> None`
  - Обновление полей параметров неисправности при смене типа.
- `def _add_param(self, param_name: str, label: str, default_value: float) -> None`
  - Добавить поле параметра неисправности в форму.
- `def _load_template(self, template: FaultTemplate) -> None`
  - Загрузить параметры существующего шаблона в форму.
- `def _on_accept(self) -> None`
  - Обработчик нажатия кнопки ОК.
- `def get_template(self) -> FaultTemplate | None`
  - Получить созданный/обновлённый шаблон.

### Файл: `fault_window.py`
> ui/fault_window.py

Окно управления неисправностями с тремя вкладками: Шаблоны, Ручное внедрение, Правила.
Позволяет создавать заготовки неисправностей, внедрять их вручную на выбранные графики
и настраивать автоматическое внедрение через правила с параметрами периода и вероятности.
Диалоги создания шаблонов и правил вынесены в отдельные модули.
#### Импорты
- **Стандартная библиотека:**
  - `import logging`
- **Сторонние библиотеки:**
  - `from PyQt6.QtCore import QSettings, pyqtSignal`
  - `from PyQt6.QtGui import QCloseEvent`
  - `from PyQt6.QtWidgets import QComboBox`
  - `from PyQt6.QtWidgets import QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QMainWindow, QMessageBox, QPushButton, QTabWidget, QVBoxLayout, QWidget`
  - `from simulation.scheduler import FaultScheduler, FaultTemplate`
  - `from simulation.simulator import SimulationEngine`
  - `from ui.fault_rule_dialog import FaultRuleDialog`
  - `from ui.fault_template_dialog import FaultTemplateDialog`
#### Классы
##### `class FaultWindow(QMainWindow)`
> Окно управления неисправностями с тремя вкладками.

Вкладка "Шаблоны": создание, редактирование и удаление заготовок неисправностей.
Вкладка "Ручное внедрение": внедрение шаблона на выбранный график.
Вкладка "Правила": настройка автоматического внедрения с периодом и вероятностью.

Signals:
    fault_injected: Неисправность внедрена вручную (plot_id, fault_type, fault_params).
Методы:
- `def __init__(self, scheduler: FaultScheduler, engine: SimulationEngine, parent: QWidget | None) -> None`
  - Инициализация окна управления неисправностями.

Args:
    scheduler: Планировщик случайных неисправностей.
    engine: Движок симуляции.
    parent: Родительский виджет.
- `def _restore_geometry(self) -> None`
  - Восстановление размера и положения окна из настроек.
- `def _init_ui(self) -> None`
  - Создание интерфейса окна.
- `def _create_templates_tab(self) -> QWidget`
  - Создание вкладки 'Шаблоны'.
- `def _create_manual_tab(self) -> QWidget`
  - Создание вкладки 'Ручное внедрение'.
- `def _create_rules_tab(self) -> QWidget`
  - Создание вкладки 'Правила'.
- `def _refresh_templates_list(self) -> None`
  - Обновить список шаблонов на вкладке 'Шаблоны'.
- `def _refresh_plots_combo(self) -> None`
  - Обновить выпадающий список графиков на вкладке 'Ручное внедрение'.
- `def _refresh_manual_templates_list(self) -> None`
  - Обновить список шаблонов с кнопками 'Внедрить' на вкладке 'Ручное внедрение'.
- `def _refresh_rules_list(self) -> None`
  - Обновить список правил на вкладке 'Правила'.
- `def _on_create_template(self) -> None`
  - Создание нового шаблона.
- `def _on_edit_template(self) -> None`
  - Редактирование выбранного шаблона.
- `def _on_delete_template(self) -> None`
  - Удаление выбранного шаблона.
- `def _on_inject_fault(self, template: FaultTemplate) -> None`
  - Внедрение неисправности из шаблона на выбранный график.
- `def _on_create_rule(self) -> None`
  - Создание нового правила.
- `def _on_toggle_rule(self) -> None`
  - Включение/выключение выбранного правила.
- `def _on_delete_rule(self) -> None`
  - Удаление выбранного правила.
- `def closeEvent(self, event: QCloseEvent) -> None`
  - Обработка закрытия окна.
Сохраняет геометрию перед закрытием.

### Файл: `log_window.py`
> ui/log_window.py

Отдельное окно журнала событий симуляции.
Отображает записи журнала в виде текстового лога в реальном времени,
поддерживает фильтрацию по типу события, графику и времени,
а также автоматическую прокрутку к последним записям.
Окно открывается и закрывается из главного окна через координатор.
#### Импорты
- **Стандартная библиотека:**
  - `import logging`
- **Сторонние библиотеки:**
  - `from PyQt6.QtCore import QSettings`
  - `from PyQt6.QtGui import QCloseEvent`
  - `from PyQt6.QtWidgets import QCheckBox, QComboBox, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget`
  - `from core.event_log import EventLog, EventRecord, EventType`
#### Классы
##### `class LogWindow(QMainWindow)`
> Окно журнала событий симуляции.

Отображает записи журнала в виде текстового лога (по одной строке на запись).
Подписывается на сигнал `EventLog.event_added` для автоматического
отображения новых записей. Поддерживает фильтрацию по типу события,
графику и диапазону времени, а также автопрокрутку.

Формат строки лога: `ЧЧ:ММ:СС.мс | ТИП_СОБЫТИЯ | график | Описание`
Методы:
- `def __init__(self, event_log: EventLog, parent: QWidget | None) -> None`
  - Инициализация окна журнала.

Args:
    event_log: Журнал событий (источник записей).
    parent: Родительский виджет.
- `def _restore_geometry(self) -> None`
  - Восстановление размера и положения окна из настроек.
- `def _init_ui(self) -> None`
  - Создание интерфейса окна журнала.
- `def _on_event_added(self, record: EventRecord) -> None`
  - Обработчик новой записи журнала (сигнал `event_added`).

Добавляет запись в список и отображает, если она подходит под фильтр.

Args:
    record: Новая запись журнала.
- `def _apply_filter(self) -> None`
  - Применить текущий фильтр и перерисовать лог.
- `def _get_filter_params(self) -> tuple[str, str, int | None, int | None]`
  - Получить текущие параметры фильтра из элементов интерфейса.

Returns:
    Кортеж (тип события или "Все типы", подстрока графика, время от, время до).
- `def _parse_time_ms(self, text: str) -> int | None`
  - Разобрать текст поля времени в миллисекунды.

Пустая строка означает отсутствие ограничения.

Args:
    text: Текст из поля ввода.

Returns:
    int или None, если пусто или некорректно.
- `def _matches_filter(self, record: EventRecord, type_filter: str, plot_filter: str, start_ms: int | None, end_ms: int | None) -> bool`
  - Проверить, подходит ли запись под текущий фильтр.

Args:
    record: Запись журнала.
    type_filter: Тип события или "Все типы".
    plot_filter: Подстрока для фильтрации по графику.
    start_ms: Нижняя граница времени (или None).
    end_ms: Верхняя граница времени (или None).

Returns:
    bool: Подходит ли запись под фильтр.
- `def _append_record_to_view(self, record: EventRecord) -> None`
  - Добавить запись в текстовый лог.

Формат: `ЧЧ:ММ:СС.мс | ТИП_СОБЫТИЯ | график | Описание`

Args:
    record: Запись журнала.
- `def _update_count(self) -> None`
  - Обновить счётчик записей с учётом фильтра.
- `def _scroll_to_bottom(self) -> None`
  - Прокрутить лог к последней записи.
- `def closeEvent(self, event: QCloseEvent) -> None`
  - Обработка закрытия окна.
Сохраняет геометрию перед закрытием.
#### Функции
- `def format_time_ms(time_ms: int) -> str`
  - Форматировать время в миллисекундах в строку ЧЧ:ММ:СС.мс.

Args:
    time_ms: Время в миллисекундах.

Returns:
    str: Отформатированное время (например, "00:05:23.456").

### Файл: `main_window.py`
> ui/main_window.py

Главное окно приложения — центральная панель управления симуляцией.
Является оркестратором трёх специализированных панелей:
- TimePanel — управление временем (старт/стоп/сброс/скорость).
- PlotsPanel — управление списком графиков и действиями с ними.
- OptionsPanel — дополнительные настройки (скрытые метки, журнал).

Содержит меню, управляет сохранением/восстановлением геометрии окна
и уведомляет координатора о закрытии приложения.
#### Импорты
- **Стандартная библиотека:**
  - `import logging`
- **Сторонние библиотеки:**
  - `from PyQt6.QtCore import QSettings, pyqtSignal`
  - `from PyQt6.QtGui import QCloseEvent, QGuiApplication`
  - `from PyQt6.QtWidgets import QFileDialog, QFrame, QMainWindow, QMessageBox, QVBoxLayout, QWidget`
  - `from core.clock import GlobalClock`
  - `from ui.panels.options_panel import OptionsPanel`
  - `from ui.panels.plots_panel import PlotsPanel`
  - `from ui.panels.time_panel import TimePanel`
#### Классы
##### `class MainWindow(QMainWindow)`
> Главное окно приложения.

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
    window_closed: Сигнал о закрытии главного окна (для завершения работы приложения).
Методы:
- `def __init__(self, clock: GlobalClock, parent: QWidget | None) -> None`
  - Инициализация главного окна.

Args:
    clock: Глобальные часы симуляции.
    parent: Родительский виджет.
- `def _restore_geometry(self) -> None`
  - Восстановление размера и положения окна из настроек.
- `def closeEvent(self, event: QCloseEvent) -> None`
  - Обработка события закрытия окна.
Сохраняет геометрию и уведомляет координатора о завершении работы.
- `def _init_menu(self) -> None`
  - Создание строки меню.
- `def _init_ui(self) -> None`
  - Создание основного интерфейса с использованием делегированных панелей.
- `def _create_separator(self) -> QFrame`
  - Создание горизонтального разделителя для визуального структурирования.
- `def _connect_signals(self) -> None`
  - Подключение сигналов панелей к сигналам главного окна.
- `def add_plot_to_list(self, plot_id: str, name: str) -> None`
  - Добавить график в список на главном окне.

Args:
    plot_id: Идентификатор графика.
    name: Отображаемое название графика.
- `def remove_plot_from_list(self, plot_id: str) -> None`
  - Удалить график из списка на главном окне.

Args:
    plot_id: Идентификатор графика.
- `def get_selected_plot_id(self) -> str | None`
  - Получить идентификатор выбранного графика.
- `def _on_start(self) -> None`
  - Запуск симуляции.
- `def _on_stop(self) -> None`
  - Остановка симуляции.
- `def _on_reset(self) -> None`
  - Сброс симуляции.
- `def _on_toggle_journal(self, checked: bool) -> None`
  - Переключение видимости журнала событий (синхронизирует меню и чекбокс).
- `def _on_save_config(self) -> None`
  - Запрос на сохранение текущей конфигурации в файл.
- `def _on_load_config(self) -> None`
  - Запрос на загрузку конфигурации из файла.

### Файл: `period_widget.py`
> ui/period_widget.py

Специализированный виджет для удобного ввода периода сигнала
с автоматическим выбором и конвертацией единиц измерения.
#### Импорты
- **Стандартная библиотека:**
  - `import logging`
- **Сторонние библиотеки:**
  - `from PyQt6.QtWidgets import QComboBox, QHBoxLayout, QSpinBox, QWidget`
#### Классы
##### `class PeriodWidget(QWidget)`
> Виджет для удобного ввода периода с выбором единицы измерения.
Автоматически конвертирует выбранное значение и единицу в миллисекунды и обратно.
Методы:
- `def __init__(self, default_ms: int, parent: QWidget | None) -> None`
- `def get_period_ms(self) -> int`
  - Возвращает период, пересчитанный в миллисекунды.
- `def set_period_ms(self, ms: int) -> None`
  - Устанавливает период, автоматически выбирая удобную единицу измерения.

Args:
    ms: Значение периода в миллисекундах.

### Файл: `plot_creation_dialog.py`
> ui/plot_creation_dialog.py

Модальный диалог создания и редактирования графика телеметрии.
Позволяет настроить все параметры графика: название, единицу измерения,
тип сигнала, допустимые пределы, интервал наблюдения и настройки детектора.
Использует делегирование для динамических полей параметров сигнала.
#### Импорты
- **Стандартная библиотека:**
  - `from typing import Any`
  - `import logging`
- **Сторонние библиотеки:**
  - `from PyQt6.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QDoubleSpinBox, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QSpinBox, QTabWidget, QVBoxLayout, QWidget`
  - `from analytics.detector import DetectorConfig`
  - `from ui.detector_settings_tab import DetectorSettingsTab`
  - `from ui.signal_params_form import SIGNAL_TYPE_DISPLAY, SignalParamsForm`
#### Классы
##### `class PlotCreationDialog(QDialog)`
> Модальный диалог создания и редактирования графика телеметрии.
Делегирует управление динамическими полями сигнала классу SignalParamsForm,
а настройку детекторов — классу DetectorSettingsTab.
Методы:
- `def __init__(self, parent: QWidget | None, initial_params: dict[str, Any] | None) -> None`
  - Инициализация диалога создания/редактирования графика.

Args:
    parent: Родительский виджет.
    initial_params: Словарь существующих параметров (режим редактирования).
- `def _init_ui(self) -> None`
  - Создание интерфейса диалога с использованием делегированных виджетов.
- `def _populate_fields(self, params: dict[str, Any]) -> None`
  - Предзаполняет поля диалога переданными параметрами.
- `def _on_preset_changed(self, index: int) -> None`
  - Обработчик изменения пресета интервала.
- `def _on_signal_type_changed(self) -> None`
  - Обновление полей параметров сигнала и информации об активных детекторах при смене типа.
- `def _on_accept(self) -> None`
  - Обработчик нажатия кнопки ОК с валидацией и сбором данных.
- `def _validate(self) -> bool`
  - Валидация введённых данных.
- `def get_plot_params(self) -> dict[str, Any] | None`
  - Получить параметры графика после подтверждения диалога.

### Файл: `plot_window.py`
> ui/plot_window.py

Отдельное окно графика телеметрии с отрисовкой сигнала в реальном времени.
Содержит кривую сигнала, пределы допустимых значений, метки неисправностей
и обнаружений, а также кнопку фиксации обнаружения оператором.
Окно не зависит от движка симуляции: данные поступают через публичный
метод `update_data`, а подписку выполняет координатор (главное окно).
#### Импорты
- **Стандартная библиотека:**
  - `import logging`
- **Сторонние библиотеки:**
  - `from PyQt6.QtCore import QSettings, Qt, pyqtSignal`
  - `from PyQt6.QtGui import QCloseEvent`
  - `from PyQt6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget`
  - `import numpy as np`
  - `import pyqtgraph as pg`
#### Классы
##### `class PlotWindow(QMainWindow)`
> Окно графика телеметрии.

Отображает сигнал в реальном времени с пределами допустимых значений,
скрытыми метками неисправностей и метками обнаружений. Данные поступают
через публичный метод `update_data` (слабая связанность с движком).

Signals:
    detection_requested: Оператор нажал кнопку обнаружения (передаёт `plot_id`).
    window_closed: Окно закрыто (передаёт `plot_id`).
Методы:
- `def __init__(self, plot_id: str, name: str, unit: str, min_allowed: float, max_allowed: float, observation_interval_ms: int, parent: QWidget | None) -> None`
  - Инициализация окна графика.

Args:
    plot_id: Уникальный идентификатор графика.
    name: Название графика.
    unit: Единица измерения.
    min_allowed: Минимально допустимое значение.
    max_allowed: Максимально допустимое значение.
    observation_interval_ms: Интервал наблюдения (длительность по оси X).
    parent: Родительский виджет.
- `def _restore_geometry(self) -> None`
  - Восстановление размера и положения окна из настроек.
- `def _init_ui(self) -> None`
  - Создание интерфейса окна.
- `def clear_data(self) -> None`
  - Очистить накопленные данные графика и все метки (кроме линий пределов).
Вызывается при сбросе симуляции или изменении настроек графика.
- `def update_settings(self, name: str, unit: str, min_allowed: float, max_allowed: float, observation_interval_ms: int) -> None`
  - Обновить настройки графика (название, единицы, пределы, интервал) без пересоздания окна.

Args:
    name: Новое название графика.
    unit: Новая единица измерения.
    min_allowed: Новое минимально допустимое значение.
    max_allowed: Новое максимально допустимое значение.
    observation_interval_ms: Новый интервал наблюдения (длительность по оси X).
- `def update_data(self, times: list[int], values: list[float]) -> None`
  - Обновить данные графика (публичный метод для координатора).

Новые точки добавляются к накопленной истории, после чего
применяется децимация и выполняется перерисовка.

Args:
    times: Список времён в миллисекундах.
    values: Список значений сигнала.
- `def add_fault_marker(self, time_ms: int, fault_type: str) -> None`
  - Добавить скрытую метку неисправности (вертикальная линия + подпись типа).

Метка видима только при включённом режиме скрытых меток.

Args:
    time_ms: Время внедрения неисправности.
    fault_type: Тип неисправности (отображается в подписи).
- `def add_operator_marker(self, time_ms: int) -> None`
  - Добавить метку обнаружения оператором (вертикальная линия).
- `def add_detector_marker(self, time_ms: int) -> None`
  - Добавить метку обнаружения детектором (вертикальная линия).
- `def set_hidden_markers_visible(self, visible: bool) -> None`
  - Переключить видимость скрытых меток неисправностей.
- `def _on_always_on_top_changed(self, state: int) -> None`
  - Обработка изменения состояния чекбокса 'Поверх других окон'.

Args:
    state: Состояние чекбокса (Qt.CheckState.Checked или Qt.CheckState.Unchecked).
- `def _decimate(self, times: list[int], values: list[float]) -> tuple[list[int], list[float]]`
  - Децимация данных для отрисовки.

Если точек не больше `MAX_DISPLAY_POINTS` — возвращает как есть.
Иначе применяет min-max децимацию по блокам, сохраняя пики и впадины.

Args:
    times: Полная история времён.
    values: Полная история значений.

Returns:
    Кортеж (прореженные времена, прореженные значения).
- `def _on_detect_clicked(self) -> None`
  - Обработчик нажатия кнопки обнаружения.
- `def closeEvent(self, event: QCloseEvent) -> None`
  - Обработка закрытия окна.
Сохраняет геометрию и уведомляет координатора о закрытии.

### Файл: `signal_params_form.py`
> ui/signal_params_form.py

Виджет для динамического построения полей параметров сигнала.
Поддерживает различные типы сигналов (синус, пила, меандр и т.д.)
и автоматически создает соответствующие поля ввода для каждого типа.
#### Импорты
- **Стандартная библиотека:**
  - `from typing import Any`
  - `import logging`
- **Сторонние библиотеки:**
  - `from PyQt6.QtWidgets import QDoubleSpinBox, QFormLayout, QSpinBox, QWidget`
  - `from ui.period_widget import PeriodWidget`
#### Классы
##### `class SignalParamsForm(QWidget)`
> Виджет для динамического построения полей параметров сигнала.

Автоматически создает поля ввода в зависимости от выбранного типа сигнала.
Поддерживает получение и установку значений параметров.
Методы:
- `def __init__(self, parent: QWidget | None) -> None`
  - Инициализация формы параметров сигнала.

Args:
    parent: Родительский виджет.
- `def update_fields(self, signal_type: str) -> None`
  - Обновление полей параметров сигнала при смене типа.
Удаляет старые поля и создаёт новые в соответствии с выбранным типом сигнала.

Args:
    signal_type: Внутренний ключ типа сигнала.
- `def _add_param(self, param_name: str, label: str, default_value: float, is_int: bool, tooltip: str) -> None`
  - Добавить поле параметра сигнала в форму.
Для периода используется специализированный виджет с выбором единицы измерения.

Args:
    param_name: Внутреннее имя параметра.
    label: Отображаемая метка поля.
    default_value: Значение по умолчанию.
    is_int: True если параметр целочисленный.
    tooltip: Всплывающая подсказка.
- `def get_signal_params(self) -> dict[str, Any]`
  - Получить текущие значения всех параметров сигнала.

Returns:
    dict: Словарь параметров {param_name: value}.
- `def set_signal_params(self, params: dict[str, Any]) -> None`
  - Установить значения параметров сигнала (для режима редактирования).

Args:
    params: Словарь параметров {param_name: value}.

### Файл: `main.py`
> main.py
Точка входа в приложение signalSimulator.
Инициализирует все компоненты системы (часы, журнал, движок, планировщик, окна)
и координирует их взаимодействие через паттерн Coordinator.

Детектор аномалий теперь полностью управляется движком симуляции (SimulationEngine),
координатор только подписывается на события журнала для визуализации меток на графиках.
#### Импорты
- **Стандартная библиотека:**
  - `import json`
  - `import logging`
  - `import sys`
- **Сторонние библиотеки:**
  - `from PyQt6.QtCore import Qt`
  - `from PyQt6.QtWidgets import QApplication, QMessageBox`
  - `from analytics.detector import DetectorConfig`
  - `from core.clock import GlobalClock`
  - `from core.config import ConfigManager`
  - `from core.event_log import EventLog, EventRecord, EventType`
  - `from simulation.scheduler import FaultScheduler`
  - `from simulation.signals import SignalFactory`
  - `from simulation.simulator import SimulationEngine`
  - `from ui.fault_window import FaultWindow`
  - `from ui.log_window import LogWindow`
  - `from ui.main_window import MainWindow`
  - `from ui.plot_creation_dialog import PlotCreationDialog`
  - `from ui.plot_window import PlotWindow`
#### Классы
##### `class Coordinator`
> Координатор приложения.

Связывает компоненты бизнес-логики (движок, часы, планировщик)
с компонентами пользовательского интерфейса, обрабатывая сигналы
и перенаправляя данные между ними.

Детектор аномалий живёт внутри PlotState (в движке симуляции).
Координатор не хранит отдельные экземпляры детекторов и не прогоняет
через них данные — это делает движок при генерации точек.
Координатор только подписывается на события журнала для визуализации
меток обнаружений на графиках.
Методы:
- `def __init__(self) -> None`
  - Инициализация всех компонентов и подключение сигналов.
- `def _connect_signals(self) -> None`
  - Подключение всех сигналов и слотов.
- `def _on_main_window_closed(self) -> None`
  - Обработка закрытия главного окна.
Закрывает все остальные окна (что сохраняет их геометрию) и завершает приложение.
- `def _on_add_plot(self) -> None`
  - Обработка запроса на создание нового графика.
- `def _on_open_plot(self, plot_id: str) -> None`
  - Показать существующее окно графика.
- `def _on_plot_settings(self, plot_id: str) -> None`
  - Обработка запроса на изменение настроек существующего графика.
- `def _on_reset(self) -> None`
  - Обработка запроса на сброс симуляции: очистка данных графиков и детекторов.
- `def _on_remove_plot(self, plot_id: str) -> None`
  - Удаление графика из симуляции и корректное уничтожение его окна.
- `def _on_toggle_journal(self, visible: bool) -> None`
  - Показать или скрыть окно журнала событий.
- `def _on_toggle_hidden_markers(self, visible: bool) -> None`
  - Обновить видимость скрытых меток во всех открытых окнах графиков.
- `def _on_plot_data_updated(self, plot_id: str, data: tuple) -> None`
  - Обработка новых данных графика.
Только обновляет окно графика. Детектор работает внутри движка
при генерации точек, его результаты приходят через сигнал event_added.
- `def _on_event_added(self, record: EventRecord) -> None`
  - Обработчик новых событий журнала.
При обнаружении детектором аномалии добавляет визуальную метку на график.
- `def _on_fault_injected(self, plot_id: str, fault_type: str, fault_params: dict) -> None`
  - Добавление скрытой метки неисправности в окно графика при ручном внедрении.
- `def _on_operator_detection(self, plot_id: str) -> None`
  - Фиксация обнаружения оператором и добавление метки.
- `def _on_plot_window_closed(self, plot_id: str) -> None`
  - Обработка закрытия окна графика пользователем (окно скрывается, но остается в памяти).
- `def _collect_current_config(self) -> dict`
  - Собрать текущую конфигурацию всех графиков и их детекторов для сохранения.

Returns:
    dict: Словарь с данными конфигурации.
- `def _on_save_config_requested(self, filepath: str) -> None`
  - Обработка запроса на сохранение конфигурации в указанный файл.

Args:
    filepath: Путь к файлу для сохранения.
- `def _on_load_config_requested(self, filepath: str) -> None`
  - Обработка запроса на загрузку конфигурации из файла и применение её к симуляции.

Args:
    filepath: Путь к файлу конфигурации.
#### Функции
- `def main() -> None`
  - Точка входа в приложение.

## Граф зависимостей между файлами
(Файл -> импортируемый модуль)
- `__init__.py` → `analytics.detector`
- `__init__.py` → `analytics.metrics`
- `__init__.py` → `core.clock`
- `__init__.py` → `core.config`
- `__init__.py` → `core.event_log`
- `__init__.py` → `simulation.faults`
- `__init__.py` → `simulation.scheduler`
- `__init__.py` → `simulation.signals`
- `__init__.py` → `ui.fault_rule_dialog`
- `__init__.py` → `ui.fault_template_dialog`
- `__init__.py` → `ui.fault_window`
- `__init__.py` → `ui.log_window`
- `__init__.py` → `ui.main_window`
- `__init__.py` → `ui.plot_creation_dialog`
- `__init__.py` → `ui.plot_window`
- `anomaly_detector.py` → `analytics.detector`
- `anomaly_detector.py` → `collections`
- `anomaly_detector.py` → `logging`
- `anomaly_detector.py` → `numpy`
- `clock.py` → `PyQt6.QtCore`
- `clock.py` → `logging`
- `clock.py` → `typing`
- `config.py` → `datetime`
- `config.py` → `json`
- `config.py` → `logging`
- `config.py` → `pathlib`
- `config.py` → `typing`
- `detector.py` → `analytics.anomaly_detector`
- `detector.py` → `analytics.detector_types`
- `detector.py` → `analytics.deviation_detector`
- `detector.py` → `analytics.signal_preprocessor`
- `detector.py` → `analytics.trend_detector`
- `detector.py` → `logging`
- `detector.py` → `typing`
- `detector_models.py` → `analytics.detector_types`
- `detector_models.py` → `collections`
- `detector_models.py` → `logging`
- `detector_models.py` → `numpy`
- `detector_settings_tab.py` → `PyQt6.QtWidgets`
- `detector_settings_tab.py` → `analytics.detector`
- `detector_settings_tab.py` → `logging`
- `detector_types.py` → `dataclasses`
- `detector_types.py` → `enum`
- `detector_types.py` → `logging`
- `detector_types.py` → `typing`
- `deviation_detector.py` → `analytics.detector`
- `deviation_detector.py` → `collections`
- `deviation_detector.py` → `logging`
- `deviation_detector.py` → `numpy`
- `event_log.py` → `PyQt6.QtCore`
- `event_log.py` → `dataclasses`
- `event_log.py` → `enum`
- `event_log.py` → `logging`
- `event_log.py` → `typing`
- `fault_rule_dialog.py` → `PyQt6.QtWidgets`
- `fault_rule_dialog.py` → `logging`
- `fault_rule_dialog.py` → `simulation.scheduler`
- `fault_template_dialog.py` → `PyQt6.QtWidgets`
- `fault_template_dialog.py` → `logging`
- `fault_template_dialog.py` → `simulation.faults`
- `fault_template_dialog.py` → `simulation.scheduler`
- `fault_window.py` → `PyQt6.QtCore`
- `fault_window.py` → `PyQt6.QtGui`
- `fault_window.py` → `PyQt6.QtWidgets`
- `fault_window.py` → `PyQt6.QtWidgets`
- `fault_window.py` → `logging`
- `fault_window.py` → `simulation.scheduler`
- `fault_window.py` → `simulation.simulator`
- `fault_window.py` → `ui.fault_rule_dialog`
- `fault_window.py` → `ui.fault_template_dialog`
- `faults.py` → `abc`
- `faults.py` → `logging`
- `faults.py` → `random`
- `faults.py` → `typing`
- `log_window.py` → `PyQt6.QtCore`
- `log_window.py` → `PyQt6.QtGui`
- `log_window.py` → `PyQt6.QtWidgets`
- `log_window.py` → `core.event_log`
- `log_window.py` → `logging`
- `main.py` → `PyQt6.QtCore`
- `main.py` → `PyQt6.QtWidgets`
- `main.py` → `analytics.detector`
- `main.py` → `core.clock`
- `main.py` → `core.config`
- `main.py` → `core.event_log`
- `main.py` → `json`
- `main.py` → `logging`
- `main.py` → `simulation.scheduler`
- `main.py` → `simulation.signals`
- `main.py` → `simulation.simulator`
- `main.py` → `sys`
- `main.py` → `ui.fault_window`
- `main.py` → `ui.log_window`
- `main.py` → `ui.main_window`
- `main.py` → `ui.plot_creation_dialog`
- `main.py` → `ui.plot_window`
- `main_window.py` → `PyQt6.QtCore`
- `main_window.py` → `PyQt6.QtGui`
- `main_window.py` → `PyQt6.QtWidgets`
- `main_window.py` → `core.clock`
- `main_window.py` → `logging`
- `main_window.py` → `ui.panels.options_panel`
- `main_window.py` → `ui.panels.plots_panel`
- `main_window.py` → `ui.panels.time_panel`
- `metrics.py` → `core.event_log`
- `metrics.py` → `dataclasses`
- `metrics.py` → `logging`
- `options_panel.py` → `PyQt6.QtCore`
- `options_panel.py` → `PyQt6.QtWidgets`
- `options_panel.py` → `logging`
- `period_widget.py` → `PyQt6.QtWidgets`
- `period_widget.py` → `logging`
- `plot_creation_dialog.py` → `PyQt6.QtWidgets`
- `plot_creation_dialog.py` → `analytics.detector`
- `plot_creation_dialog.py` → `logging`
- `plot_creation_dialog.py` → `typing`
- `plot_creation_dialog.py` → `ui.detector_settings_tab`
- `plot_creation_dialog.py` → `ui.signal_params_form`
- `plot_window.py` → `PyQt6.QtCore`
- `plot_window.py` → `PyQt6.QtGui`
- `plot_window.py` → `PyQt6.QtWidgets`
- `plot_window.py` → `logging`
- `plot_window.py` → `numpy`
- `plot_window.py` → `pyqtgraph`
- `plots_panel.py` → `PyQt6.QtCore`
- `plots_panel.py` → `PyQt6.QtWidgets`
- `plots_panel.py` → `logging`
- `scheduler.py` → `dataclasses`
- `scheduler.py` → `logging`
- `scheduler.py` → `random`
- `scheduler.py` → `typing`
- `signal_params_form.py` → `PyQt6.QtWidgets`
- `signal_params_form.py` → `logging`
- `signal_params_form.py` → `typing`
- `signal_params_form.py` → `ui.period_widget`
- `signal_preprocessor.py` → `collections`
- `signal_preprocessor.py` → `logging`
- `signal_preprocessor.py` → `numpy`
- `signal_preprocessor.py` → `typing`
- `signals.py` → `abc`
- `signals.py` → `logging`
- `signals.py` → `math`
- `signals.py` → `random`
- `signals.py` → `typing`
- `simulator.py` → `PyQt6.QtCore`
- `simulator.py` → `analytics.detector`
- `simulator.py` → `core.clock`
- `simulator.py` → `core.event_log`
- `simulator.py` → `logging`
- `simulator.py` → `numpy`
- `simulator.py` → `simulation.faults`
- `simulator.py` → `simulation.scheduler`
- `simulator.py` → `simulation.signals`
- `simulator.py` → `typing`
- `time_panel.py` → `PyQt6.QtCore`
- `time_panel.py` → `PyQt6.QtWidgets`
- `time_panel.py` → `core.clock`
- `time_panel.py` → `logging`
- `trend_detector.py` → `analytics.detector`
- `trend_detector.py` → `collections`
- `trend_detector.py` → `logging`
- `trend_detector.py` → `numpy`
