"""
signalSimulator/simulation/signals.py

Генераторы базовых сигналов для симуляции телеметрических данных.
Каждый генератор возвращает значение сигнала в заданный момент логического времени.
"""

import logging
import math
import random
from abc import ABC, abstractmethod
from typing import Any, ClassVar

logger = logging.getLogger(__name__)


class SignalGenerator(ABC):
    """
    Абстрактный базовый класс для всех генераторов сигналов.

    Определяет контракт: метод `get_value(time_ms)` возвращает
    значение сигнала в момент времени `time_ms` (в миллисекундах).
    """

    @abstractmethod
    def get_value(self, time_ms: int) -> float:
        """
        Получить значение сигнала в заданный момент времени.

        Args:
            time_ms: Логическое время в миллисекундах.

        Returns:
            float: Значение сигнала.
        """

    @abstractmethod
    def get_params(self) -> dict[str, Any]:
        """
        Получить параметры сигнала в виде словаря (для сериализации).

        Returns:
            dict: Словарь параметров.
        """


class CompositeSignal(SignalGenerator):
    """
    Композитный сигнал — сумма нескольких сигналов.

    Позволяет комбинировать базовый сигнал с трендами, шумами
    и другими компонентами. Используется для построения
    сложных сигналов, включая неисправности.
    """

    def __init__(self, signals: list[SignalGenerator] | None = None) -> None:
        """
        Args:
            signals: Список вложенных сигналов для суммирования.
        """
        self._signals: list[SignalGenerator] = signals or []

    def add_signal(self, signal: SignalGenerator) -> None:
        """Добавить сигнал в композицию."""
        if signal is not None:
            self._signals.append(signal)
            logger.debug(f"Добавлен сигнал в композицию. Всего: {len(self._signals)}")

    def remove_signal(self, signal: SignalGenerator) -> None:
        """Удалить сигнал из композиции."""
        try:
            self._signals.remove(signal)
            logger.debug(f"Сигнал удалён из композиции. Осталось: {len(self._signals)}")
        except ValueError:
            logger.warning("Попытка удалить несуществующий сигнал из композиции.")

    def get_value(self, time_ms: int) -> float:
        """Сумма значений всех вложенных сигналов."""
        try:
            return sum(s.get_value(time_ms) for s in self._signals)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка при вычислении композитного сигнала: {e}")
            return 0.0

    def get_params(self) -> dict[str, Any]:
        """Параметры всех вложенных сигналов."""
        return {
            "type": "composite",
            "signals": [s.get_params() for s in self._signals]
        }


class SawtoothSignal(SignalGenerator):
    """
    Пилообразный сигнал: линейный рост от min_val до max_val за период,
    затем резкий сброс к min_val.
    """

    def __init__(
        self,
        min_val: float = 0.0,
        max_val: float = 10.0,
        period_ms: int = 10000,
        offset: float = 0.0
    ) -> None:
        self.min_val = float(min_val)
        self.max_val = float(max_val)
        self.period_ms = max(1, int(period_ms))
        self.offset = float(offset)

    def get_value(self, time_ms: int) -> float:
        try:
            phase = (time_ms % self.period_ms) / self.period_ms
            return self.offset + self.min_val + (self.max_val - self.min_val) * phase
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка вычисления sawtooth: {e}")
            return self.offset + self.min_val

    def get_params(self) -> dict[str, Any]:
        return {
            "type": "sawtooth",
            "min_val": self.min_val,
            "max_val": self.max_val,
            "period_ms": self.period_ms,
            "offset": self.offset,
        }


class TriangleSignal(SignalGenerator):
    """
    Треугольный сигнал (симметричная пила): линейный рост от min_val до max_val,
    затем линейное падение обратно к min_val.
    """

    def __init__(
        self,
        min_val: float = 0.0,
        max_val: float = 10.0,
        period_ms: int = 10000,
        offset: float = 0.0
    ) -> None:
        self.min_val = float(min_val)
        self.max_val = float(max_val)
        self.period_ms = max(1, int(period_ms))
        self.offset = float(offset)

    def get_value(self, time_ms: int) -> float:
        try:
            phase = (time_ms % self.period_ms) / self.period_ms
            if phase < 0.5:
                value = self.min_val + (self.max_val - self.min_val) * (2 * phase)
            else:
                value = self.max_val - (self.max_val - self.min_val) * (2 * (phase - 0.5))
            return self.offset + value
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка вычисления triangle: {e}")
            return self.offset + self.min_val

    def get_params(self) -> dict[str, Any]:
        return {
            "type": "triangle",
            "min_val": self.min_val,
            "max_val": self.max_val,
            "period_ms": self.period_ms,
            "offset": self.offset,
        }


class SineSignal(SignalGenerator):
    """Синусоидальный сигнал."""

    def __init__(
        self,
        amplitude: float = 1.0,
        period_ms: int = 10000,
        phase: float = 0.0,
        offset: float = 0.0
    ) -> None:
        self.amplitude = float(amplitude)
        self.period_ms = max(1, int(period_ms))
        self.phase = float(phase)
        self.offset = float(offset)

    def get_value(self, time_ms: int) -> float:
        try:
            omega = 2 * math.pi / self.period_ms
            return self.offset + self.amplitude * math.sin(omega * time_ms + self.phase)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка вычисления sine: {e}")
            return self.offset

    def get_params(self) -> dict[str, Any]:
        return {
            "type": "sine",
            "amplitude": self.amplitude,
            "period_ms": self.period_ms,
            "phase": self.phase,
            "offset": self.offset,
        }


class StepSignal(SignalGenerator):
    """
    Ступенчатый сигнал: первая половина периода — min_val,
    вторая половина — max_val.
    """

    def __init__(
        self,
        min_val: float = 0.0,
        max_val: float = 10.0,
        period_ms: int = 10000,
        offset: float = 0.0
    ) -> None:
        self.min_val = float(min_val)
        self.max_val = float(max_val)
        self.period_ms = max(1, int(period_ms))
        self.offset = float(offset)

    def get_value(self, time_ms: int) -> float:
        try:
            phase = (time_ms % self.period_ms) / self.period_ms
            value = self.max_val if phase >= 0.5 else self.min_val
            return self.offset + value
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка вычисления step: {e}")
            return self.offset + self.min_val

    def get_params(self) -> dict[str, Any]:
        return {
            "type": "step",
            "min_val": self.min_val,
            "max_val": self.max_val,
            "period_ms": self.period_ms,
            "offset": self.offset,
        }


class LinearSignal(SignalGenerator):
    """
    Линейный сигнал (тренд).

    Параметр rate_per_sec — скорость изменения значения за секунду.
    Например, rate_per_sec = 0.01 означает, что за 1 секунду значение
    увеличивается на 0.01.
    """

    def __init__(
        self,
        start_val: float = 0.0,
        rate_per_sec: float = 0.0,
        offset: float = 0.0
    ) -> None:
        self.start_val = float(start_val)
        self.rate_per_sec = float(rate_per_sec)
        self.offset = float(offset)

    def get_value(self, time_ms: int) -> float:
        try:
            time_sec = time_ms / 1000.0
            return self.offset + self.start_val + self.rate_per_sec * time_sec
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка вычисления linear: {e}")
            return self.offset + self.start_val

    def get_params(self) -> dict[str, Any]:
        return {
            "type": "linear",
            "start_val": self.start_val,
            "rate_per_sec": self.rate_per_sec,
            "offset": self.offset,
        }


class SquareSignal(SignalGenerator):
    """
    Прямоугольный сигнал (меандр) с настраиваемым коэффициентом заполнения.

    duty_cycle — доля периода, в течение которой сигнал находится в max_val.
    """

    def __init__(
        self,
        min_val: float = 0.0,
        max_val: float = 10.0,
        period_ms: int = 10000,
        duty_cycle: float = 0.5,
        offset: float = 0.0
    ) -> None:
        self.min_val = float(min_val)
        self.max_val = float(max_val)
        self.period_ms = max(1, int(period_ms))
        self.duty_cycle = max(0.0, min(1.0, float(duty_cycle)))
        self.offset = float(offset)

    def get_value(self, time_ms: int) -> float:
        try:
            phase = (time_ms % self.period_ms) / self.period_ms
            value = self.max_val if phase < self.duty_cycle else self.min_val
            return self.offset + value
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка вычисления square: {e}")
            return self.offset + self.min_val

    def get_params(self) -> dict[str, Any]:
        return {
            "type": "square",
            "min_val": self.min_val,
            "max_val": self.max_val,
            "period_ms": self.period_ms,
            "duty_cycle": self.duty_cycle,
            "offset": self.offset,
        }


class ExponentialSignal(SignalGenerator):
    """
    Экспоненциальный сигнал.

    Значение: offset + amplitude * exp(rate_per_sec * t_sec).
    При отрицательном rate_per_sec получаем затухающую экспоненту.
    """

    def __init__(
        self,
        amplitude: float = 1.0,
        rate_per_sec: float = 0.0,
        offset: float = 0.0
    ) -> None:
        self.amplitude = float(amplitude)
        self.rate_per_sec = float(rate_per_sec)
        self.offset = float(offset)

    def get_value(self, time_ms: int) -> float:
        try:
            time_sec = time_ms / 1000.0
            # Защита от переполнения при больших значениях
            exponent = self.rate_per_sec * time_sec
            if exponent > 700:
                logger.warning(f"Экспонента переполнена: exponent={exponent}")
                return self.offset + self.amplitude * math.exp(700)
            if exponent < -700:
                return self.offset
            return self.offset + self.amplitude * math.exp(exponent)
        except OverflowError:
            logger.error("Переполнение при вычислении экспоненты.")
            return self.offset
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка вычисления exponential: {e}")
            return self.offset

    def get_params(self) -> dict[str, Any]:
        return {
            "type": "exponential",
            "amplitude": self.amplitude,
            "rate_per_sec": self.rate_per_sec,
            "offset": self.offset,
        }


class NoiseSignal(SignalGenerator):
    """
    Случайный шум (гауссовский).

    Каждый вызов `get_value` возвращает новое случайное значение
    с нормальным распределением. Параметр sigma задаёт силу шума.
    """

    def __init__(self, mean: float = 0.0, sigma: float = 1.0) -> None:
        self.mean = float(mean)
        self.sigma = max(0.0, float(sigma))

    def get_value(self, time_ms: int) -> float:
        try:
            return random.gauss(self.mean, self.sigma)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка генерации шума: {e}")
            return self.mean

    def get_params(self) -> dict[str, Any]:
        return {
            "type": "noise",
            "mean": self.mean,
            "sigma": self.sigma,
        }


class ConstantSignal(SignalGenerator):
    """Постоянное значение."""

    def __init__(self, value: float = 0.0) -> None:
        self.value = float(value)

    def get_value(self, time_ms: int) -> float:
        return self.value

    def get_params(self) -> dict[str, Any]:
        return {"type": "constant", "value": self.value}


class SignalFactory:
    """
    Фабрика для создания генераторов сигналов по типу.

    Поддерживает все зарегистрированные типы сигналов.
    """

    _registry: ClassVar[dict[str, type]] = {
        "sawtooth": SawtoothSignal,
        "triangle": TriangleSignal,
        "sine": SineSignal,
        "step": StepSignal,
        "linear": LinearSignal,
        "square": SquareSignal,
        "exponential": ExponentialSignal,
        "noise": NoiseSignal,
        "constant": ConstantSignal,
    }

    @classmethod
    def register(cls, name: str, signal_class: type) -> None:
        """Зарегистрировать новый тип сигнала."""
        if not issubclass(signal_class, SignalGenerator):
            logger.error(f"Попытка зарегистрировать не-SignalGenerator: {signal_class}")
            return
        cls._registry[name] = signal_class
        logger.info(f"Зарегистрирован новый тип сигнала: {name}")

    @classmethod
    def create(cls, signal_type: str, params: dict[str, Any] | None = None) -> SignalGenerator:
        """
        Создать генератор сигнала по типу и параметрам.

        Args:
            signal_type: Строковый тип сигнала.
            params: Словарь параметров для инициализации.

        Returns:
            SignalGenerator: Экземпляр сигнала. При ошибке — ConstantSignal(0).
        """
        params = params or {}
        try:
            if signal_type not in cls._registry:
                logger.warning(
                    f"Неизвестный тип сигнала '{signal_type}'. "
                    f"Доступные: {list(cls._registry.keys())}. "
                    f"Возвращён ConstantSignal(0)."
                )
                return ConstantSignal(0.0)

            signal_class = cls._registry[signal_type]
            return signal_class(**params)
        except TypeError as e:
            logger.error(
                f"Некорректные параметры для сигнала '{signal_type}': {params}. "
                f"Ошибка: {e}. Возвращён ConstantSignal(0)."
            )
            return ConstantSignal(0.0)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Непредвиденная ошибка создания сигнала '{signal_type}': {e}")
            return ConstantSignal(0.0)

    @classmethod
    def available_types(cls) -> list[str]:
        """Вернуть список доступных типов сигналов."""
        return list(cls._registry.keys())
