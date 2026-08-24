"""
simulation/faults.py

Типы неисправностей для симуляции аномалий в телеметрических сигналах.
Каждая неисправность модифицирует базовое значение сигнала в заданный момент
логического времени. Поддерживаются активация/деактивация, периодичность
и композиция (последовательное применение нескольких неисправностей).
"""

import logging
import math
import random
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


logger = logging.getLogger(__name__)


class Fault(ABC):
    """
    Абстрактный базовый класс для всех неисправностей.

    Неисправность активируется в определённый момент времени и может быть
    однократной или периодической. Логика периодичности реализована в `is_active`.
    Конкретные неисправности реализуют `_apply_effect`.

    Attributes:
        duration_ms: Длительность активности в мс. `None` означает бесконечность.
        period_ms: Период повторения в мс. `None` или `0` — однократная неисправность.
        activation_time_ms: Время активации (для скрытых меток на графике).
    """

    def __init__(
        self,
        duration_ms: Optional[int] = None,
        period_ms: Optional[int] = None
    ) -> None:
        self.duration_ms = duration_ms
        self.period_ms = period_ms
        self.activation_time_ms: Optional[int] = None

    def activate(self, time_ms: int) -> None:
        """Активировать неисправность в заданный момент времени."""
        self.activation_time_ms = time_ms
        logger.info(
            f"{self.__class__.__name__} активирована в {time_ms} мс. "
            f"Длительность: {self.duration_ms}, период: {self.period_ms}."
        )

    def deactivate(self) -> None:
        """Деактивировать неисправность."""
        logger.info(f"{self.__class__.__name__} деактивирована.")
        self.activation_time_ms = None

    def is_active(self, time_ms: int) -> bool:
        """
        Проверить, активна ли неисправность в заданный момент времени.

        Для периодической неисправности активна в окнах
        `[activation + k*period, activation + k*period + duration]`.
        Для однократной активна в `[activation, activation + duration]`.

        Args:
            time_ms: Логическое время в миллисекундах.

        Returns:
            bool: Активна ли неисправность.
        """
        if self.activation_time_ms is None:
            return False
        elapsed = time_ms - self.activation_time_ms
        if elapsed < 0:
            return False
        try:
            if self.period_ms and self.period_ms > 0:
                # Периодическая неисправность: проверяем попадание в окно
                phase = elapsed % self.period_ms
                return phase < self._effective_duration()
            # Однократная неисправность
            if self.duration_ms is None:
                return True
            return elapsed < self.duration_ms
        except Exception as e:
            logger.error(f"Ошибка проверки активности {self.__class__.__name__}: {e}")
            return False

    def _effective_duration(self) -> int:
        """Эффективная длительность для проверки окна (при периодичности)."""
        if self.duration_ms is None:
            return self.period_ms if self.period_ms else 0
        return self.duration_ms

    def apply(self, time_ms: int, base_value: float) -> float:
        """
        Применить неисправность к базовому значению.

        Если неисправность не активна в данный момент, возвращает исходное значение.

        Args:
            time_ms: Логическое время в миллисекундах.
            base_value: Базовое значение сигнала.

        Returns:
            float: Модифицированное значение.
        """
        try:
            if not self.is_active(time_ms):
                return base_value
            return self._apply_effect(time_ms, base_value)
        except Exception as e:
            logger.error(f"Ошибка применения {self.__class__.__name__}: {e}")
            return base_value

    @abstractmethod
    def _apply_effect(self, time_ms: int, base_value: float) -> float:
        """
        Внутренний метод применения эффекта неисправности.

        Вызывается только когда неисправность активна.

        Args:
            time_ms: Логическое время в миллисекундах.
            base_value: Базовое значение сигнала.

        Returns:
            float: Модифицированное значение.
        """

    @abstractmethod
    def get_params(self) -> Dict[str, Any]:
        """
        Получить параметры неисправности для сериализации.

        Returns:
            dict: Словарь параметров.
        """


class DropoutFault(Fault):
    """
    Пропадание сигнала.

    Во время активности сигнал заменяется на заданное значение
    (по умолчанию 0.0). Может быть однократным или периодическим.
    """

    def __init__(
        self,
        duration_ms: Optional[int] = None,
        period_ms: Optional[int] = None,
        dropout_value: float = 0.0
    ) -> None:
        super().__init__(duration_ms, period_ms)
        self.dropout_value = float(dropout_value)

    def _apply_effect(self, time_ms: int, base_value: float) -> float:
        return self.dropout_value

    def get_params(self) -> Dict[str, Any]:
        return {
            "type": "dropout",
            "duration_ms": self.duration_ms,
            "period_ms": self.period_ms,
            "dropout_value": self.dropout_value,
        }


class SpikeFault(Fault):
    """
    Скачок (импульс).

    Величина скачка задаётся в процентах от базового значения.
    Например, `magnitude_percent=100` удваивает значение.
    Для имитации короткого замыкания задайте большой процент
    и `duration_ms=None` (бесконечная длительность).
    """

    def __init__(
        self,
        magnitude_percent: float = 100.0,
        duration_ms: Optional[int] = 1000,
        period_ms: Optional[int] = None
    ) -> None:
        super().__init__(duration_ms, period_ms)
        self.magnitude_percent = float(magnitude_percent)

    def _apply_effect(self, time_ms: int, base_value: float) -> float:
        return base_value + base_value * (self.magnitude_percent / 100.0)

    def get_params(self) -> Dict[str, Any]:
        return {
            "type": "spike",
            "magnitude_percent": self.magnitude_percent,
            "duration_ms": self.duration_ms,
            "period_ms": self.period_ms,
        }


class NoiseFault(Fault):
    """
    Шум (гауссовский).

    Добавляет случайное значение с нормальным распределением к базовому сигналу.
    Сила шума задаётся параметром `sigma`. Неисправность активна всё время
    после активации (по умолчанию длительность бесконечная).
    """

    def __init__(
        self,
        mean: float = 0.0,
        sigma: float = 1.0,
        duration_ms: Optional[int] = None,
        period_ms: Optional[int] = None
    ) -> None:
        super().__init__(duration_ms, period_ms)
        self.mean = float(mean)
        self.sigma = max(0.0, float(sigma))

    def _apply_effect(self, time_ms: int, base_value: float) -> float:
        try:
            return base_value + random.gauss(self.mean, self.sigma)
        except Exception as e:
            logger.error(f"Ошибка генерации шума: {e}")
            return base_value

    def get_params(self) -> Dict[str, Any]:
        return {
            "type": "noise",
            "mean": self.mean,
            "sigma": self.sigma,
            "duration_ms": self.duration_ms,
            "period_ms": self.period_ms,
        }


class DegradationFault(Fault):
    """
    Деградация (линейный тренд).

    Скорость деградации задаётся в процентах в секунду от базового значения,
    зафиксированного в момент активации. Знак `rate_percent_per_sec` определяет
    направление: положительный — рост, отрицательный — убывание.

    Пример: `rate_percent_per_sec=-0.001` означает уменьшение на 0.001% в секунду.
    """

    def __init__(
        self,
        rate_percent_per_sec: float = 0.0,
        duration_ms: Optional[int] = None
    ) -> None:
        super().__init__(duration_ms, period_ms=None)
        self.rate_percent_per_sec = float(rate_percent_per_sec)
        self._base_at_activation: Optional[float] = None

    def activate(self, time_ms: int) -> None:
        """Активация с сбросом зафиксированного базового значения."""
        super().activate(time_ms)
        self._base_at_activation = None

    def _apply_effect(self, time_ms: int, base_value: float) -> float:
        try:
            if self._base_at_activation is None:
                self._base_at_activation = base_value
                logger.debug(
                    f"Деградация: зафиксировано базовое значение {base_value}."
                )
            elapsed_sec = (time_ms - self.activation_time_ms) / 1000.0
            degradation = (
                self._base_at_activation
                * (self.rate_percent_per_sec / 100.0)
                * elapsed_sec
            )
            return base_value + degradation
        except Exception as e:
            logger.error(f"Ошибка вычисления деградации: {e}")
            return base_value

    def get_params(self) -> Dict[str, Any]:
        return {
            "type": "degradation",
            "rate_percent_per_sec": self.rate_percent_per_sec,
            "duration_ms": self.duration_ms,
        }


class FaultChain:
    """
    Цепочка неисправностей для последовательного применения к сигналу.

    Позволяет комбинировать несколько неисправностей на одном графике,
    например: базовый сигнал + шум + деградация.
    """

    def __init__(self, faults: Optional[List[Fault]] = None) -> None:
        self._faults: List[Fault] = faults or []

    def add_fault(self, fault: Fault) -> None:
        """Добавить неисправность в цепочку."""
        if fault is not None:
            self._faults.append(fault)
            logger.debug(
                f"Добавлена неисправность {fault.__class__.__name__}. "
                f"Всего в цепочке: {len(self._faults)}."
            )

    def remove_fault(self, fault: Fault) -> None:
        """Удалить неисправность из цепочки."""
        try:
            self._faults.remove(fault)
            logger.debug(f"Неисправность удалена. Осталось: {len(self._faults)}.")
        except ValueError:
            logger.warning("Попытка удалить несуществующую неисправность из цепочки.")

    def clear(self) -> None:
        """Очистить цепочку."""
        self._faults.clear()
        logger.debug("Цепочка неисправностей очищена.")

    def get_faults(self) -> List[Fault]:
        """Получить список неисправностей в цепочке."""
        return list(self._faults)

    def apply_all(self, time_ms: int, base_value: float) -> float:
        """
        Применить все активные неисправности последовательно.

        Args:
            time_ms: Логическое время в миллисекундах.
            base_value: Базовое значение сигнала.

        Returns:
            float: Значение после применения всех неисправностей.
        """
        result = base_value
        for fault in self._faults:
            try:
                result = fault.apply(time_ms, result)
            except Exception as e:
                logger.error(
                    f"Ошибка применения {fault.__class__.__name__} в цепочке: {e}"
                )
        return result

    def deactivate_all(self) -> None:
        """Деактивировать все неисправности в цепочке."""
        for fault in self._faults:
            fault.deactivate()
        logger.info("Все неисправности в цепочке деактивированы.")


class FaultFactory:
    """Фабрика для создания неисправностей по строковому типу."""

    _registry: Dict[str, type] = {
        "dropout": DropoutFault,
        "spike": SpikeFault,
        "noise": NoiseFault,
        "degradation": DegradationFault,
    }

    @classmethod
    def register(cls, name: str, fault_class: type) -> None:
        """Зарегистрировать новый тип неисправности."""
        if not issubclass(fault_class, Fault):
            logger.error(f"Попытка зарегистрировать не-наследника Fault: {fault_class}")
            return
        cls._registry[name] = fault_class
        logger.info(f"Зарегистрирован новый тип неисправности: {name}")

    @classmethod
    def create(cls, fault_type: str, params: Optional[Dict[str, Any]] = None) -> Optional[Fault]:
        """
        Создать неисправность по типу и параметрам.

        Args:
            fault_type: Строковый тип неисправности.
            params: Словарь параметров.

        Returns:
            Fault: Экземпляр неисправности. При ошибке — `None`.
        """
        params = params or {}
        try:
            if fault_type not in cls._registry:
                logger.warning(
                    f"Неизвестный тип неисправности '{fault_type}'. "
                    f"Доступные: {list(cls._registry.keys())}."
                )
                return None
            fault_class = cls._registry[fault_type]
            return fault_class(**params)
        except TypeError as e:
            logger.error(
                f"Некорректные параметры для неисправности '{fault_type}': {params}. "
                f"Ошибка: {e}."
            )
            return None
        except Exception as e:
            logger.error(f"Непредвиденная ошибка создания неисправности '{fault_type}': {e}")
            return None

    @classmethod
    def available_types(cls) -> List[str]:
        """Вернуть список доступных типов неисправностей."""
        return list(cls._registry.keys())
