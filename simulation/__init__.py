"""
simulation/__init__.py
Инициализация пакета `simulation` — слой симуляции сигналов и неисправностей.
Содержит генераторы сигналов, типы неисправностей и планировщик случайного внедрения.
"""

from simulation.faults import (
    DegradationFault,
    DropoutFault,
    Fault,
    FaultChain,
    FaultFactory,
    NoiseFault,
    SpikeFault,
)
from simulation.scheduler import (
    FaultInjectionEvent,
    FaultScheduler,
    FaultTemplate,
    RandomFaultRule,
)
from simulation.signals import (
    CompositeSignal,
    ConstantSignal,
    ExponentialSignal,
    LinearSignal,
    NoiseSignal,
    SawtoothSignal,
    SignalFactory,
    SignalGenerator,
    SineSignal,
    SquareSignal,
    StepSignal,
    TriangleSignal,
)

__all__ = [
    "CompositeSignal",
    "ConstantSignal",
    "DegradationFault",
    "DropoutFault",
    "ExponentialSignal",
    "Fault",
    "FaultChain",
    "FaultFactory",
    "FaultInjectionEvent",
    "FaultScheduler",
    "FaultTemplate",
    "LinearSignal",
    "NoiseFault",
    "NoiseSignal",
    "RandomFaultRule",
    "SawtoothSignal",
    "SignalFactory",
    "SignalGenerator",
    "SineSignal",
    "SpikeFault",
    "SquareSignal",
    "StepSignal",
    "TriangleSignal",
]