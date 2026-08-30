# Структура и метаданные проекта

## Метаданные проекта
- **Название:** signalSimulator
- **Версия:** не указана
- **Описание:** нет
- **Зависимости:** PyQt6==6.11.0, pyqtgraph==0.14.0, numpy==2.5.2
- **Точки входа:** compact_code.py, generate_structure.py, main.py, .venv\Lib\site-packages\flake8\__main__.py, .venv\Lib\site-packages\numpy\_configtool.py, .venv\Lib\site-packages\pip\__main__.py, .venv\Lib\site-packages\ruff\__main__.py, .venv\Lib\site-packages\numpy\f2py\crackfortran.py, .venv\Lib\site-packages\numpy\f2py\diagnose.py, .venv\Lib\site-packages\numpy\typing\tests\data\pass\lib_user_array.py, .venv\Lib\site-packages\numpy\_core\tests\test_cpu_features.py, .venv\Lib\site-packages\pip\_vendor\cachecontrol\_cmd.py, .venv\Lib\site-packages\pip\_vendor\distro\distro.py, .venv\Lib\site-packages\pip\_vendor\distro\__main__.py, .venv\Lib\site-packages\pip\_vendor\idna\cli.py, .venv\Lib\site-packages\pip\_vendor\idna\__main__.py, .venv\Lib\site-packages\pip\_vendor\packaging\_musllinux.py, .venv\Lib\site-packages\pip\_vendor\platformdirs\__main__.py, .venv\Lib\site-packages\pip\_vendor\requests\certs.py, .venv\Lib\site-packages\pip\_vendor\requests\help.py, .venv\Lib\site-packages\pip\_vendor\rich\abc.py, .venv\Lib\site-packages\pip\_vendor\rich\align.py, .venv\Lib\site-packages\pip\_vendor\rich\box.py, .venv\Lib\site-packages\pip\_vendor\rich\cells.py, .venv\Lib\site-packages\pip\_vendor\rich\color.py, .venv\Lib\site-packages\pip\_vendor\rich\columns.py, .venv\Lib\site-packages\pip\_vendor\rich\console.py, .venv\Lib\site-packages\pip\_vendor\rich\control.py, .venv\Lib\site-packages\pip\_vendor\rich\default_styles.py, .venv\Lib\site-packages\pip\_vendor\rich\diagnose.py, .venv\Lib\site-packages\pip\_vendor\rich\emoji.py, .venv\Lib\site-packages\pip\_vendor\rich\highlighter.py, .venv\Lib\site-packages\pip\_vendor\rich\json.py, .venv\Lib\site-packages\pip\_vendor\rich\layout.py, .venv\Lib\site-packages\pip\_vendor\rich\live.py, .venv\Lib\site-packages\pip\_vendor\rich\logging.py, .venv\Lib\site-packages\pip\_vendor\rich\markup.py, .venv\Lib\site-packages\pip\_vendor\rich\padding.py, .venv\Lib\site-packages\pip\_vendor\rich\pager.py, .venv\Lib\site-packages\pip\_vendor\rich\palette.py, .venv\Lib\site-packages\pip\_vendor\rich\panel.py, .venv\Lib\site-packages\pip\_vendor\rich\pretty.py, .venv\Lib\site-packages\pip\_vendor\rich\progress.py, .venv\Lib\site-packages\pip\_vendor\rich\progress_bar.py, .venv\Lib\site-packages\pip\_vendor\rich\prompt.py, .venv\Lib\site-packages\pip\_vendor\rich\repr.py, .venv\Lib\site-packages\pip\_vendor\rich\rule.py, .venv\Lib\site-packages\pip\_vendor\rich\scope.py, .venv\Lib\site-packages\pip\_vendor\rich\segment.py, .venv\Lib\site-packages\pip\_vendor\rich\spinner.py, .venv\Lib\site-packages\pip\_vendor\rich\status.py, .venv\Lib\site-packages\pip\_vendor\rich\styled.py, .venv\Lib\site-packages\pip\_vendor\rich\syntax.py, .venv\Lib\site-packages\pip\_vendor\rich\table.py, .venv\Lib\site-packages\pip\_vendor\rich\text.py, .venv\Lib\site-packages\pip\_vendor\rich\theme.py, .venv\Lib\site-packages\pip\_vendor\rich\traceback.py, .venv\Lib\site-packages\pip\_vendor\rich\tree.py, .venv\Lib\site-packages\pip\_vendor\rich\_log_render.py, .venv\Lib\site-packages\pip\_vendor\rich\_ratio.py, .venv\Lib\site-packages\pip\_vendor\rich\_win32_console.py, .venv\Lib\site-packages\pip\_vendor\rich\_windows.py, .venv\Lib\site-packages\pip\_vendor\rich\_wrap.py, .venv\Lib\site-packages\pip\_vendor\rich\__init__.py, .venv\Lib\site-packages\pip\_vendor\rich\__main__.py, .venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\_in_process.py, .venv\Lib\site-packages\PyQt6\uic\compile_ui.py, .venv\Lib\site-packages\pyqtgraph\examples\GLGradientLegendItem.py, .venv\Lib\site-packages\pyqtgraph\examples\GLGraphItem.py, .venv\Lib\site-packages\pyqtgraph\examples\InteractiveParameter.py, .venv\Lib\site-packages\pyqtgraph\examples\jupyter_console_example.py, .venv\Lib\site-packages\pyqtgraph\examples\MultiDataPlot.py, .venv\Lib\site-packages\pyqtgraph\examples\RunExampleApp.py, .venv\Lib\site-packages\pyqtgraph\examples\ScatterPlotSpeedTest.py, .venv\Lib\site-packages\pyqtgraph\examples\test_examples.py, .venv\Lib\site-packages\pyqtgraph\util\get_resolution.py

## Статистика проекта
- Папок: 6
- Python-файлов: 21
- Всего файлов: 21
- Классов: 48
- Функций: 2

## Дерево проекта
```
signalSimulator/
  analytics/
    __init__.py
    detector.py
    metrics.py
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
    __init__.py
    fault_rule_dialog.py
    fault_template_dialog.py
    fault_window.py
    log_window.py
    main_window.py
    plot_creation_dialog.py
    plot_window.py
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

### Файл: `detector.py`
> analytics/detector.py

Лёгкая статистическая модель обнаружения аномалий и трендов в реальном времени.
Реализует три уровня анализа: пороговый контроль, статистическая проверка
(отклонение от скользящего среднего) и обнаружение тренда (линейная регрессия).
Все параметры настраиваются через DetectorConfig для управления из интерфейса.
Реализует логику "срабатывания по фронту", отсечение шумовых микронаклонов
и прогноз времени пересечения допустимых границ.
#### Импорты
- **Стандартная библиотека:**
  - `from collections import deque`
  - `from dataclasses import dataclass, field`
  - `from enum import Enum, auto`
  - `from typing import Any`
  - `import logging`
- **Сторонние библиотеки:**
  - `import numpy as np`
#### Классы
##### `class DetectionType(Enum)`
> Типы обнаружений.
##### `@dataclass class DetectionResult`
> Результат обнаружения.

Содержит время, тип обнаружения, описание, текущее значение
и произвольные метаданные (например, направление тренда).
Методы:
- `def __str__(self) -> str`
  - Строковое представление результата.
##### `@dataclass class DetectorConfig`
> Конфигурация детектора.

Все параметры могут быть изменены из интерфейса настроек.
Сериализуется в словарь для сохранения в конфигурации.
Методы:
- `def to_dict(self) -> dict[str, Any]`
  - Сериализация конфигурации в словарь.
- `@classmethod def from_dict(cls, data: dict[str, Any]) -> 'DetectorConfig'`
  - Создание конфигурации из словаря (мягкая валидация).
##### `class AnomalyDetector`
> Лёгкая статистическая модель для обнаружения аномалий и трендов.

Создаётся отдельно для каждого графика. Метод `process(time_ms, value)`
вызывается на каждой новой точке и возвращает список обнаружений.
Параметры настраиваются через `DetectorConfig` и могут быть изменены
в любой момент через `set_config` (для интерфейса настроек).
Реализует логику "срабатывания по фронту", игнорирование микронаклонов
и расчет прогнозируемого времени выхода за допустимые пределы.
Методы:
- `def __init__(self, min_allowed: float, max_allowed: float, config: DetectorConfig | None) -> None`
  - Инициализация детектора.

Args:
    min_allowed: Минимально допустимое значение сигнала.
    max_allowed: Максимально допустимое значение сигнала.
    config: Конфигурация детектора. По умолчанию — стандартная.
- `def set_config(self, config: DetectorConfig) -> None`
  - Обновить конфигурацию детектора (вызывается из интерфейса настроек).
- `def get_config(self) -> DetectorConfig`
  - Получить текущую конфигурацию детектора.
- `def process(self, time_ms: int, value: float) -> list[DetectionResult]`
  - Обработать новую точку данных.

Добавляет точку в скользящее окно и выполняет все три уровня анализа.

Args:
    time_ms: Логическое время точки в миллисекундах.
    value: Значение сигнала.

Returns:
    Список обнаружений (может быть пустым).
- `def reset(self) -> None`
  - Сброс скользящего окна и состояния детектора.
- `def _trim_window(self) -> None`
  - Обрезать скользящее окно до размера из конфигурации.
- `def _check_threshold(self, time_ms: int, value: float) -> list[DetectionResult]`
  - Пороговый контроль: выход за допустимые пределы.
Реализует логику срабатывания по фронту (только при переходе границы).
- `def _check_statistical(self, time_ms: int, value: float) -> list[DetectionResult]`
  - Статистическая проверка: отклонение от скользящего среднего.
- `def _check_trend(self, time_ms: int) -> list[DetectionResult]`
  - Обнаружение тренда: линейная регрессия по скользящему окну.
Реализует отсечение шумовых микронаклонов, расчет времени до пересечения
границы и логику срабатывания по фронту / ухудшению тренда.

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
  - `from datetime import datetime`
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
  - `from typing import Any`
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
  - `from typing import Any`
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
Объединяет часы, генераторы сигналов, неисправности, планировщик и журнал
событий. Вычисляет значения графиков на каждом тике времени с шагом
1 симуляционная секунда и обрабатывает события внедрения неисправностей.
#### Импорты
- **Стандартная библиотека:**
  - `from typing import Any`
  - `import logging`
- **Сторонние библиотеки:**
  - `from PyQt6.QtCore import QObject, pyqtSignal`
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
- `def __init__(self, plot_id: str, name: str, unit: str, max_unit_value: float, signal: SignalGenerator, min_allowed: float, max_allowed: float, observation_interval_ms: int) -> None`
##### `class SimulationEngine(QObject)`
> Движок симуляции.

Подписывается на сигнал `time_updated` глобальных часов, генерирует
данные графиков с шагом 1 симуляционная секунда, обрабатывает события
планировщика неисправностей и ведёт журнал событий.
Методы:
- `def __init__(self, clock: GlobalClock, event_log: EventLog, scheduler: FaultScheduler | None, parent: QObject | None) -> None`
  - Инициализация движка симуляции.

Args:
    clock: Глобальные часы симуляции.
    event_log: Журнал событий.
    scheduler: Планировщик случайных неисправностей (опционально).
    parent: Родительский QObject.
- `def add_plot(self, plot_id: str, name: str, unit: str, max_unit_value: float, signal: SignalGenerator, min_allowed: float, max_allowed: float, observation_interval_ms: int) -> PlotState`
  - Добавить график в симуляцию.
- `def remove_plot(self, plot_id: str) -> None`
  - Удалить график из симуляции.
- `def get_plot(self, plot_id: str) -> PlotState | None`
  - Получить состояние графика по ID.
- `def get_all_plot_ids(self) -> list[str]`
  - Получить список всех идентификаторов графиков.
- `def _on_time_updated(self, time_ms: int) -> None`
  - Обработка тика часов: генерация данных и обработка событий.
- `def _generate_points(self, plot: PlotState, current_time_ms: int) -> None`
  - Генерация точек для графика до текущего времени с шагом 1 секунда.
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
    description: Детальное описание причины обнаружения (для журнала событий).
- `def reset(self) -> None`
  - Сброс состояния движка (очистка историй и меток).

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
  - `from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QDoubleSpinBox, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QRadioButton, QSpinBox, QVBoxLayout, QWidget`
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
  - `from PyQt6.QtCore import pyqtSignal`
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
- `def closeEvent(self, event) -> None`
  - Обработка закрытия окна журнала.
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
Содержит панель управления временем, список графиков, меню и кнопки
для открытия вспомогательных окон и изменения настроек графиков.
#### Импорты
- **Стандартная библиотека:**
  - `import logging`
- **Сторонние библиотеки:**
  - `from PyQt6.QtCore import Qt, pyqtSignal`
  - `from PyQt6.QtWidgets import QCheckBox, QFileDialog, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget`
  - `from core.clock import GlobalClock`
  - `from core.config import ConfigError, ConfigManager`
#### Классы
##### `class MainWindow(QMainWindow)`
> Главное окно приложения.

Обеспечивает управление временем симуляции, списком графиков,
открытие/закрытие журнала событий, сохранение/загрузку конфигураций
и запрос на изменение настроек существующих графиков.

Signals:
    plot_open_requested: Запрос на открытие окна графика (plot_id).
    plot_add_requested: Запрос на создание нового графика.
    plot_remove_requested: Запрос на удаление графика (plot_id).
    plot_settings_requested: Запрос на изменение настроек графика (plot_id).
    reset_requested: Запрос на полный сброс симуляции (для очистки графиков).
    journal_toggled: Журнал открыт (True) или закрыт (False).
    hidden_markers_toggled: Режим скрытых меток включён (True) или выключён (False).
Методы:
- `def __init__(self, clock: GlobalClock, parent: QWidget | None) -> None`
  - Инициализация главного окна.

Args:
    clock: Глобальные часы симуляции.
    parent: Родительский виджет.
- `def _init_menu(self) -> None`
  - Создание строки меню.
- `def _init_ui(self) -> None`
  - Создание основного интерфейса.
- `def _create_time_panel(self) -> QWidget`
  - Создание панели управления временем.
- `def _create_plots_panel(self) -> QWidget`
  - Создание панели управления графиками.
- `def _connect_signals(self) -> None`
  - Подключение внутренних сигналов.
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
- `def _on_speed_change(self, multiplier: int) -> None`
  - Изменение множителя ускорения времени.
- `def _on_time_updated(self, time_ms: int) -> None`
  - Обновление отображения времени.
- `def _on_toggle_hidden_markers(self) -> None`
  - Переключение режима скрытых меток.
- `def _on_add_plot(self) -> None`
  - Запрос на создание нового графика.
- `def _on_open_plot(self) -> None`
  - Запрос на открытие окна выбранного графика.
- `def _on_plot_settings(self) -> None`
  - Запрос на изменение настроек выбранного графика.
- `def _on_remove_plot(self) -> None`
  - Запрос на удаление выбранного графика.
- `def _on_plot_selection_changed(self, current: QListWidgetItem | None, previous) -> None`
  - Обработка изменения выбора в списке графиков.
- `def _on_toggle_journal(self) -> None`
  - Переключение видимости журнала событий.
- `def _on_save_config(self) -> None`
  - Сохранение текущей конфигурации в файл.
- `def _on_load_config(self) -> None`
  - Загрузка конфигурации из файла.
- `def _collect_current_config(self) -> dict`
  - Собрать текущую конфигурацию для сохранения.
- `def _apply_loaded_config(self, config_data: dict) -> None`
  - Применить загруженную конфигурацию.

### Файл: `plot_creation_dialog.py`
> ui/plot_creation_dialog.py

Модальный диалог создания и редактирования графика телеметрии.
Позволяет настроить все параметры графика: название, единицу измерения,
тип сигнала с его параметрами, допустимые пределы и интервал наблюдения.
Вызывается из главного окна по сигналу plot_add_requested или plot_settings_requested.
#### Импорты
- **Стандартная библиотека:**
  - `from typing import Any`
  - `import logging`
- **Сторонние библиотеки:**
  - `from PyQt6.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QDoubleSpinBox, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QSpinBox, QVBoxLayout, QWidget`
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
##### `class PlotCreationDialog(QDialog)`
> Модальный диалог создания и редактирования графика телеметрии.

Позволяет настроить:
- Основные параметры (название, единица, макс. значение)
- Интервал наблюдения (через пресеты или ручной ввод в секундах)
- Допустимые пределы (min_allowed, max_allowed)
- Тип сигнала и его параметры (динамически меняются, период вводится с выбором единицы)

Если передан initial_params, диалог переходит в режим редактирования и предзаполняет поля.
После подтверждения результат доступен через метод get_plot_params().
Методы:
- `def __init__(self, parent: QWidget | None, initial_params: dict[str, Any] | None) -> None`
  - Инициализация диалога создания/редактирования графика.

Args:
    parent: Родительский виджет.
    initial_params: Словарь существующих параметров для предзаполнения (режим редактирования).
- `def _init_ui(self) -> None`
  - Создание интерфейса диалога.
- `def _populate_fields(self, params: dict[str, Any]) -> None`
  - Предзаполняет поля диалога переданными параметрами (для режима редактирования).

Args:
    params: Словарь параметров графика.
- `def _on_preset_changed(self, index: int) -> None`
  - Обработчик изменения пресета интервала.
При выборе пресета подставляет значение в поле ручного ввода.
- `def _update_signal_params_fields(self) -> None`
  - Обновление полей параметров сигнала при смене типа.
Удаляет старые поля и создаёт новые в соответствии с выбранным типом сигнала.
- `def _add_signal_param(self, param_name: str, label: str, default_value: float, is_int: bool, tooltip: str) -> None`
  - Добавить поле параметра сигнала в форму.
Для периода используется специализированный виджет с выбором единицы измерения.
- `def _on_accept(self) -> None`
  - Обработчик нажатия кнопки ОК.
Выполняет валидацию и при успехе сохраняет параметры и закрывает диалог.
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
  - `from PyQt6.QtCore import Qt, pyqtSignal`
  - `from PyQt6.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget`
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
- `def closeEvent(self, event) -> None`
  - Обработка закрытия окна.

### Файл: `main.py`
> main.py
Точка входа в приложение signalSimulator.
Инициализирует все компоненты системы (часы, журнал, движок, планировщик, окна)
и координирует их взаимодействие через паттерн Coordinator.
#### Импорты
- **Стандартная библиотека:**
  - `import logging`
  - `import sys`
- **Сторонние библиотеки:**
  - `from PyQt6.QtCore import Qt`
  - `from PyQt6.QtWidgets import QApplication, QMessageBox`
  - `from analytics.detector import AnomalyDetector`
  - `from core.clock import GlobalClock`
  - `from core.config import ConfigManager`
  - `from core.event_log import EventLog`
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
Методы:
- `def __init__(self) -> None`
  - Инициализация всех компонентов и подключение сигналов.
- `def _connect_signals(self) -> None`
  - Подключение всех сигналов и слотов.
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
Обновляет окно графика и прогоняет данные через детектор аномалий.
- `def _on_fault_injected(self, plot_id: str, fault_type: str, fault_params: dict) -> None`
  - Добавление скрытой метки неисправности в окно графика при ручном внедрении.
- `def _on_operator_detection(self, plot_id: str) -> None`
  - Фиксация обнаружения оператором и добавление метки.
- `def _on_plot_window_closed(self, plot_id: str) -> None`
  - Обработка закрытия окна графика пользователем (окно скрывается, но остается в памяти).
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
- `clock.py` → `PyQt6.QtCore`
- `clock.py` → `logging`
- `config.py` → `datetime`
- `config.py` → `json`
- `config.py` → `logging`
- `config.py` → `pathlib`
- `config.py` → `typing`
- `detector.py` → `collections`
- `detector.py` → `dataclasses`
- `detector.py` → `enum`
- `detector.py` → `logging`
- `detector.py` → `numpy`
- `detector.py` → `typing`
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
- `log_window.py` → `PyQt6.QtWidgets`
- `log_window.py` → `core.event_log`
- `log_window.py` → `logging`
- `main.py` → `PyQt6.QtCore`
- `main.py` → `PyQt6.QtWidgets`
- `main.py` → `analytics.detector`
- `main.py` → `core.clock`
- `main.py` → `core.config`
- `main.py` → `core.event_log`
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
- `main_window.py` → `PyQt6.QtWidgets`
- `main_window.py` → `core.clock`
- `main_window.py` → `core.config`
- `main_window.py` → `logging`
- `metrics.py` → `core.event_log`
- `metrics.py` → `dataclasses`
- `metrics.py` → `logging`
- `plot_creation_dialog.py` → `PyQt6.QtWidgets`
- `plot_creation_dialog.py` → `logging`
- `plot_creation_dialog.py` → `typing`
- `plot_window.py` → `PyQt6.QtCore`
- `plot_window.py` → `PyQt6.QtWidgets`
- `plot_window.py` → `logging`
- `plot_window.py` → `numpy`
- `plot_window.py` → `pyqtgraph`
- `scheduler.py` → `dataclasses`
- `scheduler.py` → `logging`
- `scheduler.py` → `random`
- `scheduler.py` → `typing`
- `signals.py` → `abc`
- `signals.py` → `logging`
- `signals.py` → `math`
- `signals.py` → `random`
- `signals.py` → `typing`
- `simulator.py` → `PyQt6.QtCore`
- `simulator.py` → `core.clock`
- `simulator.py` → `core.event_log`
- `simulator.py` → `logging`
- `simulator.py` → `numpy`
- `simulator.py` → `simulation.faults`
- `simulator.py` → `simulation.scheduler`
- `simulator.py` → `simulation.signals`
- `simulator.py` → `typing`
