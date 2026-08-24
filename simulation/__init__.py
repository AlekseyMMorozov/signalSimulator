"""
simulation/__init__.py
Инициализация пакета `simulation` — слой симуляции сигналов и неисправностей.
Содержит генераторы сигналов, типы неисправностей и планировщик случайного внедрения.
"""

from simulation.signals import (
    SignalGenerator,
    CompositeSignal,
    SawtoothSignal,
    TriangleSignal,
    SineSignal,
    StepSignal,
    LinearSignal,
    SquareSignal,
    ExponentialSignal,
    NoiseSignal,
    ConstantSignal,
    SignalFactory,
)

from simulation.faults import (
    Fault,
    DropoutFault,
    SpikeFault,
    NoiseFault,
    DegradationFault,
    FaultChain,
    FaultFactory,
)

from simulation.scheduler import (
    FaultInjectionEvent,
    FaultTemplate,
    RandomFaultRule,
    FaultScheduler,
)

__all__ = [
    # Генераторы сигналов
    "SignalGenerator",
    "CompositeSignal",
    "SawtoothSignal",
    "TriangleSignal",
    "SineSignal",
    "StepSignal",
    "LinearSignal",
    "SquareSignal",
    "ExponentialSignal",
    "NoiseSignal",
    "ConstantSignal",
    "SignalFactory",
    # Неисправности
    "Fault",
    "DropoutFault",
    "SpikeFault",
    "NoiseFault",
    "DegradationFault",
    "FaultChain",
    "FaultFactory",
    # Планировщик
    "FaultInjectionEvent",
    "FaultTemplate",
    "RandomFaultRule",
    "FaultScheduler",
]
