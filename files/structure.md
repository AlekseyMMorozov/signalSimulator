# Структура и метаданные проекта

## Метаданные проекта
- **Название:** signalSimulator
- **Версия:** не указана
- **Описание:** нет
- **Зависимости:** не найдены
- **Точки входа:** compact_code.py, generate_structure.py, .venv\Lib\site-packages\pip\__main__.py, .venv\Lib\site-packages\pip\_vendor\cachecontrol\_cmd.py, .venv\Lib\site-packages\pip\_vendor\distro\distro.py, .venv\Lib\site-packages\pip\_vendor\distro\__main__.py, .venv\Lib\site-packages\pip\_vendor\packaging\_musllinux.py, .venv\Lib\site-packages\pip\_vendor\platformdirs\__main__.py, .venv\Lib\site-packages\pip\_vendor\requests\certs.py, .venv\Lib\site-packages\pip\_vendor\requests\help.py, .venv\Lib\site-packages\pip\_vendor\rich\abc.py, .venv\Lib\site-packages\pip\_vendor\rich\align.py, .venv\Lib\site-packages\pip\_vendor\rich\box.py, .venv\Lib\site-packages\pip\_vendor\rich\cells.py, .venv\Lib\site-packages\pip\_vendor\rich\color.py, .venv\Lib\site-packages\pip\_vendor\rich\columns.py, .venv\Lib\site-packages\pip\_vendor\rich\console.py, .venv\Lib\site-packages\pip\_vendor\rich\control.py, .venv\Lib\site-packages\pip\_vendor\rich\default_styles.py, .venv\Lib\site-packages\pip\_vendor\rich\diagnose.py, .venv\Lib\site-packages\pip\_vendor\rich\emoji.py, .venv\Lib\site-packages\pip\_vendor\rich\highlighter.py, .venv\Lib\site-packages\pip\_vendor\rich\json.py, .venv\Lib\site-packages\pip\_vendor\rich\layout.py, .venv\Lib\site-packages\pip\_vendor\rich\live.py, .venv\Lib\site-packages\pip\_vendor\rich\logging.py, .venv\Lib\site-packages\pip\_vendor\rich\markup.py, .venv\Lib\site-packages\pip\_vendor\rich\padding.py, .venv\Lib\site-packages\pip\_vendor\rich\pager.py, .venv\Lib\site-packages\pip\_vendor\rich\palette.py, .venv\Lib\site-packages\pip\_vendor\rich\panel.py, .venv\Lib\site-packages\pip\_vendor\rich\pretty.py, .venv\Lib\site-packages\pip\_vendor\rich\progress.py, .venv\Lib\site-packages\pip\_vendor\rich\progress_bar.py, .venv\Lib\site-packages\pip\_vendor\rich\prompt.py, .venv\Lib\site-packages\pip\_vendor\rich\repr.py, .venv\Lib\site-packages\pip\_vendor\rich\rule.py, .venv\Lib\site-packages\pip\_vendor\rich\scope.py, .venv\Lib\site-packages\pip\_vendor\rich\segment.py, .venv\Lib\site-packages\pip\_vendor\rich\spinner.py, .venv\Lib\site-packages\pip\_vendor\rich\status.py, .venv\Lib\site-packages\pip\_vendor\rich\styled.py, .venv\Lib\site-packages\pip\_vendor\rich\syntax.py, .venv\Lib\site-packages\pip\_vendor\rich\table.py, .venv\Lib\site-packages\pip\_vendor\rich\text.py, .venv\Lib\site-packages\pip\_vendor\rich\theme.py, .venv\Lib\site-packages\pip\_vendor\rich\traceback.py, .venv\Lib\site-packages\pip\_vendor\rich\tree.py, .venv\Lib\site-packages\pip\_vendor\rich\_log_render.py, .venv\Lib\site-packages\pip\_vendor\rich\_ratio.py, .venv\Lib\site-packages\pip\_vendor\rich\_win32_console.py, .venv\Lib\site-packages\pip\_vendor\rich\_windows.py, .venv\Lib\site-packages\pip\_vendor\rich\_wrap.py, .venv\Lib\site-packages\pip\_vendor\rich\__init__.py, .venv\Lib\site-packages\pip\_vendor\rich\__main__.py, .venv\Lib\site-packages\pip\_vendor\chardet\cli\chardetect.py

## Статистика проекта
- Папок: 3
- Python-файлов: 6
- Всего файлов: 6
- Классов: 26
- Функций: 0

## Дерево проекта
```
signalSimulator/
  core/
    clock.py
    config.py
  simulation/
    faults.py
    scheduler.py
    signals.py
  main.py
```

## Содержимое файлов (сигнатуры с docstring)

### Файл: `clock.py`
> signalSimulator/core/clock.py

Модуль управления глобальным логическим временем симуляции.
Обеспечивает единый источник времени для всех компонентов системы.
#### Импорты
- **Стандартная библиотека:**
  - `from typing import Optional`
  - `import logging`
- **Сторонние библиотеки:**
  - `from PyQt6.QtCore import QObject, QTimer, pyqtSignal`
#### Классы
##### `class GlobalClock(QObject)`
> Глобальные часы симуляции с поддержкой ускорения времени.

Реализует паттерн Singleton для обеспечения единого источника времени
во всем приложении. Генерирует периодические сигналы обновления времени.

Attributes:
    time_updated (pyqtSignal): Сигнал, испускаемый при каждом обновлении времени.
        Передает текущее логическое время в миллисекундах.
Методы:
- `def __new__(cls, *args, **kwargs) -> 'GlobalClock'`
  - Реализация паттерна Singleton.
- `def __init__(self, parent: Optional[QObject]) -> None`
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

### Файл: `faults.py`
> simulation/faults.py

Типы неисправностей для симуляции аномалий в телеметрических сигналах.
Каждая неисправность модифицирует базовое значение сигнала в заданный момент
логического времени. Поддерживаются активация/деактивация, периодичность
и композиция (последовательное применение нескольких неисправностей).
#### Импорты
- **Стандартная библиотека:**
  - `from abc import ABC, abstractmethod`
  - `from typing import Any, Dict, List, Optional`
  - `import logging`
  - `import math`
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
- `def __init__(self, duration_ms: Optional[int], period_ms: Optional[int]) -> None`
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
- `@abstractmethod def get_params(self) -> Dict[str, Any]`
  - Получить параметры неисправности для сериализации.

Returns:
    dict: Словарь параметров.
##### `class DropoutFault(Fault)`
> Пропадание сигнала.

Во время активности сигнал заменяется на заданное значение
(по умолчанию 0.0). Может быть однократным или периодическим.
Методы:
- `def __init__(self, duration_ms: Optional[int], period_ms: Optional[int], dropout_value: float) -> None`
- `def _apply_effect(self, time_ms: int, base_value: float) -> float`
- `def get_params(self) -> Dict[str, Any]`
##### `class SpikeFault(Fault)`
> Скачок (импульс).

Величина скачка задаётся в процентах от базового значения.
Например, `magnitude_percent=100` удваивает значение.
Для имитации короткого замыкания задайте большой процент
и `duration_ms=None` (бесконечная длительность).
Методы:
- `def __init__(self, magnitude_percent: float, duration_ms: Optional[int], period_ms: Optional[int]) -> None`
- `def _apply_effect(self, time_ms: int, base_value: float) -> float`
- `def get_params(self) -> Dict[str, Any]`
##### `class NoiseFault(Fault)`
> Шум (гауссовский).

Добавляет случайное значение с нормальным распределением к базовому сигналу.
Сила шума задаётся параметром `sigma`. Неисправность активна всё время
после активации (по умолчанию длительность бесконечная).
Методы:
- `def __init__(self, mean: float, sigma: float, duration_ms: Optional[int], period_ms: Optional[int]) -> None`
- `def _apply_effect(self, time_ms: int, base_value: float) -> float`
- `def get_params(self) -> Dict[str, Any]`
##### `class DegradationFault(Fault)`
> Деградация (линейный тренд).

Скорость деградации задаётся в процентах в секунду от базового значения,
зафиксированного в момент активации. Знак `rate_percent_per_sec` определяет
направление: положительный — рост, отрицательный — убывание.

Пример: `rate_percent_per_sec=-0.001` означает уменьшение на 0.001% в секунду.
Методы:
- `def __init__(self, rate_percent_per_sec: float, duration_ms: Optional[int]) -> None`
- `def activate(self, time_ms: int) -> None`
  - Активация с сбросом зафиксированного базового значения.
- `def _apply_effect(self, time_ms: int, base_value: float) -> float`
- `def get_params(self) -> Dict[str, Any]`
##### `class FaultChain`
> Цепочка неисправностей для последовательного применения к сигналу.

Позволяет комбинировать несколько неисправностей на одном графике,
например: базовый сигнал + шум + деградация.
Методы:
- `def __init__(self, faults: Optional[List[Fault]]) -> None`
- `def add_fault(self, fault: Fault) -> None`
  - Добавить неисправность в цепочку.
- `def remove_fault(self, fault: Fault) -> None`
  - Удалить неисправность из цепочки.
- `def clear(self) -> None`
  - Очистить цепочку.
- `def get_faults(self) -> List[Fault]`
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
- `@classmethod def create(cls, fault_type: str, params: Optional[Dict[str, Any]]) -> Optional[Fault]`
  - Создать неисправность по типу и параметрам.

Args:
    fault_type: Строковый тип неисправности.
    params: Словарь параметров.

Returns:
    Fault: Экземпляр неисправности. При ошибке — `None`.
- `@classmethod def available_types(cls) -> List[str]`
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
  - `from typing import Any, Dict, List, Optional`
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
- `def select_target_plot_ids(self, available_plot_ids: List[str]) -> List[str]`
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
- `def get_template(self, template_id: str) -> Optional[FaultTemplate]`
  - Получить шаблон по ID.
- `def list_templates(self) -> List[FaultTemplate]`
  - Получить список всех шаблонов.
- `def add_rule(self, rule: RandomFaultRule) -> None`
  - Добавить правило случайного внедрения.
- `def remove_rule(self, rule_id: str) -> None`
  - Удалить правило случайного внедрения.
- `def get_rule(self, rule_id: str) -> Optional[RandomFaultRule]`
  - Получить правило по ID.
- `def list_rules(self) -> List[RandomFaultRule]`
  - Получить список всех правил.
- `def tick(self, current_time_ms: int, available_plot_ids: List[str]) -> List[FaultInjectionEvent]`
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
- `def _inject_from_rule(self, rule: RandomFaultRule, time_ms: int, available_plot_ids: List[str]) -> List[FaultInjectionEvent]`
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
  - `from typing import Any, Dict, List, Optional`
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
- `@abstractmethod def get_params(self) -> Dict[str, Any]`
  - Получить параметры сигнала в виде словаря (для сериализации).

Returns:
    dict: Словарь параметров.
##### `class CompositeSignal(SignalGenerator)`
> Композитный сигнал — сумма нескольких сигналов.

Позволяет комбинировать базовый сигнал с трендами, шумами
и другими компонентами. Используется для построения
сложных сигналов, включая неисправности.
Методы:
- `def __init__(self, signals: Optional[List[SignalGenerator]]) -> None`
  - Args:
    signals: Список вложенных сигналов для суммирования.
- `def add_signal(self, signal: SignalGenerator) -> None`
  - Добавить сигнал в композицию.
- `def remove_signal(self, signal: SignalGenerator) -> None`
  - Удалить сигнал из композиции.
- `def get_value(self, time_ms: int) -> float`
  - Сумма значений всех вложенных сигналов.
- `def get_params(self) -> Dict[str, Any]`
  - Параметры всех вложенных сигналов.
##### `class SawtoothSignal(SignalGenerator)`
> Пилообразный сигнал: линейный рост от min_val до max_val за период,
затем резкий сброс к min_val.
Методы:
- `def __init__(self, min_val: float, max_val: float, period_ms: int, offset: float) -> None`
- `def get_value(self, time_ms: int) -> float`
- `def get_params(self) -> Dict[str, Any]`
##### `class TriangleSignal(SignalGenerator)`
> Треугольный сигнал (симметричная пила): линейный рост от min_val до max_val,
затем линейное падение обратно к min_val.
Методы:
- `def __init__(self, min_val: float, max_val: float, period_ms: int, offset: float) -> None`
- `def get_value(self, time_ms: int) -> float`
- `def get_params(self) -> Dict[str, Any]`
##### `class SineSignal(SignalGenerator)`
> Синусоидальный сигнал.
Методы:
- `def __init__(self, amplitude: float, period_ms: int, phase: float, offset: float) -> None`
- `def get_value(self, time_ms: int) -> float`
- `def get_params(self) -> Dict[str, Any]`
##### `class StepSignal(SignalGenerator)`
> Ступенчатый сигнал: первая половина периода — min_val,
вторая половина — max_val.
Методы:
- `def __init__(self, min_val: float, max_val: float, period_ms: int, offset: float) -> None`
- `def get_value(self, time_ms: int) -> float`
- `def get_params(self) -> Dict[str, Any]`
##### `class LinearSignal(SignalGenerator)`
> Линейный сигнал (тренд).

Параметр rate_per_sec — скорость изменения значения за секунду.
Например, rate_per_sec = 0.01 означает, что за 1 секунду значение
увеличивается на 0.01.
Методы:
- `def __init__(self, start_val: float, rate_per_sec: float, offset: float) -> None`
- `def get_value(self, time_ms: int) -> float`
- `def get_params(self) -> Dict[str, Any]`
##### `class SquareSignal(SignalGenerator)`
> Прямоугольный сигнал (меандр) с настраиваемым коэффициентом заполнения.

duty_cycle — доля периода, в течение которой сигнал находится в max_val.
Методы:
- `def __init__(self, min_val: float, max_val: float, period_ms: int, duty_cycle: float, offset: float) -> None`
- `def get_value(self, time_ms: int) -> float`
- `def get_params(self) -> Dict[str, Any]`
##### `class ExponentialSignal(SignalGenerator)`
> Экспоненциальный сигнал.

Значение: offset + amplitude * exp(rate_per_sec * t_sec).
При отрицательном rate_per_sec получаем затухающую экспоненту.
Методы:
- `def __init__(self, amplitude: float, rate_per_sec: float, offset: float) -> None`
- `def get_value(self, time_ms: int) -> float`
- `def get_params(self) -> Dict[str, Any]`
##### `class NoiseSignal(SignalGenerator)`
> Случайный шум (гауссовский).

Каждый вызов `get_value` возвращает новое случайное значение
с нормальным распределением. Параметр sigma задаёт силу шума.
Методы:
- `def __init__(self, mean: float, sigma: float) -> None`
- `def get_value(self, time_ms: int) -> float`
- `def get_params(self) -> Dict[str, Any]`
##### `class ConstantSignal(SignalGenerator)`
> Постоянное значение.
Методы:
- `def __init__(self, value: float) -> None`
- `def get_value(self, time_ms: int) -> float`
- `def get_params(self) -> Dict[str, Any]`
##### `class SignalFactory`
> Фабрика для создания генераторов сигналов по типу.

Поддерживает все зарегистрированные типы сигналов.
Методы:
- `@classmethod def register(cls, name: str, signal_class: type) -> None`
  - Зарегистрировать новый тип сигнала.
- `@classmethod def create(cls, signal_type: str, params: Optional[Dict[str, Any]]) -> SignalGenerator`
  - Создать генератор сигнала по типу и параметрам.

Args:
    signal_type: Строковый тип сигнала.
    params: Словарь параметров для инициализации.

Returns:
    SignalGenerator: Экземпляр сигнала. При ошибке — ConstantSignal(0).
- `@classmethod def available_types(cls) -> List[str]`
  - Вернуть список доступных типов сигналов.

### Файл: `main.py`

## Граф зависимостей между файлами
(Файл -> импортируемый модуль)
- `clock.py` → `PyQt6.QtCore`
- `clock.py` → `logging`
- `clock.py` → `typing`
- `config.py` → `datetime`
- `config.py` → `json`
- `config.py` → `logging`
- `config.py` → `pathlib`
- `config.py` → `typing`
- `faults.py` → `abc`
- `faults.py` → `logging`
- `faults.py` → `math`
- `faults.py` → `random`
- `faults.py` → `typing`
- `scheduler.py` → `dataclasses`
- `scheduler.py` → `logging`
- `scheduler.py` → `random`
- `scheduler.py` → `typing`
- `signals.py` → `abc`
- `signals.py` → `logging`
- `signals.py` → `math`
- `signals.py` → `random`
- `signals.py` → `typing`
