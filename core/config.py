"""
signalSimulator/core/config.py

Менеджер конфигураций: загрузка, сохранение и валидация настроек
графиков и неисправностей в формате JSON.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

# Настройка логирования
logger = logging.getLogger(__name__)

# Корневая директория проекта и папка конфигураций
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIGS_DIR = PROJECT_ROOT / "configs"

# Допустимые типы сигналов
ALLOWED_SIGNAL_TYPES = [
    "sawtooth", "sine", "step", "linear", "square", "noise", "constant"
]

# Допустимые типы неисправностей
ALLOWED_FAULT_TYPES = [
    "dropout", "spike", "noise", "degradation"
]


class ConfigError(Exception):
    """Кастомное исключение для ошибок конфигурации."""


class ConfigManager:
    """
    Менеджер конфигураций симулятора.

    Отвечает за сохранение и загрузку конфигураций в формате JSON,
    а также за мягкую валидацию структуры данных.
    """

    def __init__(self, configs_dir: Path | None = None) -> None:
        """
        Инициализация менеджера конфигураций.

        Args:
            configs_dir: Путь к директории конфигураций.
                         По умолчанию используется папка 'configs/' проекта.
        """
        self._configs_dir = configs_dir if configs_dir else CONFIGS_DIR
        try:
            self._configs_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"ConfigManager инициализирован. Директория: {self._configs_dir}")
        except OSError as e:
            logger.error(f"Ошибка создания директории конфигураций: {e}")
            raise ConfigError(f"Не удалось создать директорию: {self._configs_dir}") from e

    def save_config(self, config_data: dict) -> str:
        """
        Сохранение конфигурации в JSON-файл с автогенерацией имени.

        Args:
            config_data: Словарь конфигурации для сохранения.

        Returns:
            str: Путь к сохранённому файлу.

        Raises:
            ConfigError: При ошибке записи файла.
        """
        try:
            validated = self.validate_config(config_data)
            filename = self._generate_filename()
            filepath = self._configs_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(validated, f, ensure_ascii=False, indent=2)

            logger.info(f"Конфигурация сохранена: {filepath}")
            return str(filepath)
        except ConfigError:
            raise
        except OSError as e:
            logger.error(f"Ошибка записи файла конфигурации: {e}")
            raise ConfigError(f"Не удалось сохранить конфигурацию: {e}") from e
        except Exception as e:
            logger.error(f"Непредвиденная ошибка при сохранении: {e}")
            raise ConfigError(f"Непредвиденная ошибка: {e}") from e

    def load_config(self, filepath: str) -> dict:
        """
        Загрузка конфигурации из JSON-файла.

        Args:
            filepath: Путь к файлу конфигурации.

        Returns:
            dict: Словарь загруженной конфигурации (после мягкой валидации).

        Raises:
            ConfigError: При ошибке чтения или парсинга файла.
        """
        try:
            path = Path(filepath)
            if not path.exists():
                raise ConfigError(f"Файл не найден: {filepath}")

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            validated = self.validate_config(data)
            logger.info(f"Конфигурация загружена: {filepath}")
            return validated
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка парсинга JSON в файле {filepath}: {e}")
            raise ConfigError(f"Некорректный JSON в файле: {filepath}") from e
        except OSError as e:
            logger.error(f"Ошибка чтения файла конфигурации: {e}")
            raise ConfigError(f"Не удалось прочитать файл: {filepath}") from e
        except ConfigError:
            raise
        except Exception as e:
            logger.error(f"Непредвиденная ошибка при загрузке: {e}")
            raise ConfigError(f"Непредвиденная ошибка: {e}") from e

    def validate_config(self, config_data: dict) -> dict:
        """
        Мягкая валидация конфигурации.
        Дополняет отсутствующие поля значениями по умолчанию.

        Args:
            config_data: Исходный словарь конфигурации.

        Returns:
            dict: Валидированная конфигурация с заполненными полями.
        """
        try:
            if not isinstance(config_data, dict):
                logger.warning("Конфигурация не является словарём. Создаётся пустой шаблон.")
                return self.get_default_config()

            result = self.get_default_config()

            # Заполняем поля верхнего уровня
            result["name"] = config_data.get("name", result["name"])
            result["created_at"] = config_data.get("created_at", result["created_at"])

            # Валидация списка графиков
            if "plots" in config_data and isinstance(config_data["plots"], list):
                result["plots"] = [
                    self._validate_plot(p, i)
                    for i, p in enumerate(config_data["plots"])
                ]

            # Валидация списка неисправностей
            if "faults" in config_data and isinstance(config_data["faults"], list):
                result["faults"] = [
                    self._validate_fault(f) for f in config_data["faults"]
                ]

            logger.debug("Валидация конфигурации завершена успешно")
            return result
        except Exception as e:
            logger.error(f"Ошибка валидации конфигурации: {e}")
            raise ConfigError(f"Ошибка валидации: {e}") from e

    def list_configs(self) -> list[str]:
        """
        Получение списка сохранённых конфигураций.

        Returns:
            list[str]: Список имён файлов конфигураций.
        """
        try:
            files = sorted(
                [f.name for f in self._configs_dir.glob("*.json")],
                reverse=True
            )
            logger.debug(f"Найдено конфигураций: {len(files)}")
            return files
        except OSError as e:
            logger.error(f"Ошибка получения списка конфигураций: {e}")
            return []

    def get_default_config(self) -> dict:
        """
        Получение пустой конфигурации-шаблона.

        Returns:
            dict: Шаблон конфигурации со значениями по умолчанию.
        """
        return {
            "name": "Без названия",
            "created_at": datetime.now().isoformat(),
            "plots": [],
            "faults": []
        }

    def _validate_plot(self, plot: Any, index: int) -> dict:
        """
        Мягкая валидация одного графика.

        Args:
            plot: Исходные данные графика.
            index: Индекс графика в списке (для генерации ID).

        Returns:
            dict: Валидированный график.
        """
        defaults = {
            "id": f"plot_{index}",
            "name": "Без названия",
            "unit": "",
            "max_unit_value": 10.0,
            "signal_type": "sine",
            "signal_params": {},
            "observation_interval_ms": 60000,
            "min_allowed": 0.0,
            "max_allowed": 10.0
        }

        if not isinstance(plot, dict):
            logger.warning(f"График #{index} не является словарём. Используются значения по умолчанию.")
            return defaults

        result = defaults.copy()
        for key in defaults:
            if key in plot:
                result[key] = plot[key]

        # Проверка типа сигнала
        if result["signal_type"] not in ALLOWED_SIGNAL_TYPES:
            logger.warning(
                f"Недопустимый тип сигнала '{result['signal_type']}' "
                f"для графика #{index}. Заменён на 'sine'."
            )
            result["signal_type"] = "sine"

        return result

    def _validate_fault(self, fault: Any) -> dict:
        """
        Мягкая валидация одной неисправности.

        Args:
            fault: Исходные данные неисправности.

        Returns:
            dict: Валидированная неисправность.
        """
        defaults = {
            "plot_id": "",
            "fault_type": "noise",
            "params": {}
        }

        if not isinstance(fault, dict):
            logger.warning("Неисправность не является словарём. Используются значения по умолчанию.")
            return defaults

        result = defaults.copy()
        for key in defaults:
            if key in fault:
                result[key] = fault[key]

        # Проверка типа неисправности
        if result["fault_type"] not in ALLOWED_FAULT_TYPES:
            logger.warning(
                f"Недопустимый тип неисправности '{result['fault_type']}'. "
                f"Заменён на 'noise'."
            )
            result["fault_type"] = "noise"

        return result

    def _generate_filename(self) -> str:
        """
        Автогенерация имени файла конфигурации.

        Returns:
            str: Имя файла в формате 'config_YYYYMMDD_HHMMSS.json'.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"config_{timestamp}.json"
        logger.debug(f"Сгенерировано имя файла: {filename}")
        return filename
