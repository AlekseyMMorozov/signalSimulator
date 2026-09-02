"""
analytics/signal_preprocessor.py

Препроцессор сигналов — извлечение информативных параметров из сырых данных.
Работает O(1) по памяти на точку, адаптирован для реального времени.

Для каждого типа сигнала извлекает свой информативный параметр:
- Синус, Треугольник → амплитуда (скользящая огибающая)
- Меандр, Ступеньки → значения на плато (бимодальная фильтрация)
- Пила → наклон линейного участка
- Постоянный, Линейный, Экспонента, Шум → сырое значение
"""

import logging
from collections import deque
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)


class SignalPreprocessor:
    """
    Препроцессор сигналов для извлечения информативных параметров.
    Применяет сигнал-специфичную фильтрацию перед детекцией аномалий.
    """

    # Типы сигналов, требующие бимодальной фильтрации (два устойчивых уровня)
    BIMODAL_SIGNALS = {"square", "step"}

    # Типы сигналов, требующие анализа огибающей (периодические с плавными изменениями)
    ENVELOPE_SIGNALS = {"sine", "triangle"}

    # Типы сигналов, требующие анализа наклона
    SLOPE_SIGNALS = {"sawtooth"}

    # Типы сигналов, для которых используется сырое значение
    RAW_SIGNALS = {"constant", "linear", "exponential", "noise", "composite", "unknown"}

    def __init__(self, signal_type: str, window_size: int = 100) -> None:
        """
        Инициализация препроцессора.

        Args:
            signal_type: Тип сигнала (sine, square, sawtooth и т.д.).
            window_size: Размер скользящего окна для анализа.
        """
        self.signal_type = signal_type
        self.window_size = window_size

        # Общие буферы
        self._values: deque[float] = deque(maxlen=window_size)
        self._times: deque[int] = deque(maxlen=window_size)

        # Для бимодальной фильтрации
        self._level_a: float = 0.0
        self._level_b: float = 0.0
        self._bimodal_initialized: bool = False

        # Для огибающей
        self._envelope_max: float = 0.0
        self._envelope_min: float = 0.0

        logger.debug(f"SignalPreprocessor инициализирован для типа '{signal_type}'")

    def process(self, time_ms: int, value: float) -> float | None:
        """
        Обработать точку и вернуть информативный параметр.

        Args:
            time_ms: Логическое время в миллисекундах.
            value: Сырое значение сигнала.

        Returns:
            Информативный параметр (амплитуда, наклон, уровень и т.д.)
            или None, если недостаточно данных для анализа.
        """
        self._values.append(value)
        self._times.append(time_ms)

        # Проверяем, достаточно ли данных
        if len(self._values) < 10:
            return None

        try:
            if self.signal_type in self.BIMODAL_SIGNALS:
                return self._process_bimodal(value)
            elif self.signal_type in self.ENVELOPE_SIGNALS:
                return self._process_envelope(value)
            elif self.signal_type in self.SLOPE_SIGNALS:
                return self._process_slope(value)
            elif self.signal_type in self.RAW_SIGNALS:
                return value
            else:
                # Неизвестный тип — возвращаем сырое значение
                logger.warning(f"Неизвестный тип сигнала '{self.signal_type}', используется сырое значение")
                return value
        except Exception as e:
            logger.error(f"Ошибка препроцессинга сигнала: {e}")
            return value

    def _process_bimodal(self, value: float) -> float | None:
        """
        Бимодальная фильтрация для меандра/ступенек.
        Игнорирует фронты, возвращает значение на устойчивом уровне.
        """
        if not self._bimodal_initialized:
            self._initialize_bimodal_levels()
            return None

        # Определяем, к какому уровню ближе точка
        dist_a = abs(value - self._level_a)
        dist_b = abs(value - self._level_b)

        # Мёртвая зона между уровнями (фронт)
        level_gap = abs(self._level_b - self._level_a)
        mid = (self._level_a + self._level_b) / 2.0
        dead_zone = level_gap * 0.2

        if abs(value - mid) < dead_zone and level_gap > 1e-6:
            # Точка на фронте — игнорируем
            return None

        # Обновляем статистику уровня
        if dist_a < dist_b:
            self._update_level("a", value)
            return self._level_a
        else:
            self._update_level("b", value)
            return self._level_b

    def _initialize_bimodal_levels(self) -> None:
        """Инициализация двух уровней по квантилям."""
        arr = np.array(self._values, dtype=np.float64)
        q25 = float(np.percentile(arr, 25))
        q75 = float(np.percentile(arr, 75))

        if abs(q75 - q25) < 0.05 * (np.max(arr) - np.min(arr)):
            # Квантили слишком близки — используем min/max
            self._level_a = float(np.min(arr))
            self._level_b = float(np.max(arr))
        else:
            self._level_a = q25
            self._level_b = q75

        self._bimodal_initialized = True
        logger.debug(f"Бимодальные уровни инициализированы: A={self._level_a:.4f}, B={self._level_b:.4f}")

    def _update_level(self, level: str, value: float) -> None:
        """Обновить скользящее среднее уровня."""
        alpha = 0.1  # Коэффициент сглаживания
        if level == "a":
            self._level_a = alpha * value + (1 - alpha) * self._level_a
        else:
            self._level_b = alpha * value + (1 - alpha) * self._level_b

    def _process_envelope(self, value: float) -> float | None:
        """
        Анализ огибающей для синуса/треугольника.
        Возвращает амплитуду (размах) сигнала.
        """
        arr = np.array(self._values, dtype=np.float64)

        # Скользящий max и min
        self._envelope_max = float(np.max(arr))
        self._envelope_min = float(np.min(arr))

        # Амплитуда = (max - min) / 2
        amplitude = (self._envelope_max - self._envelope_min) / 2.0

        return amplitude if amplitude > 1e-6 else None

    def _process_slope(self, value: float) -> float | None:
        """
        Анализ наклона для пилы.
        Возвращает скорость изменения на линейном участке.
        """
        if len(self._values) < 5:
            return None

        # Берём последние N точек для регрессии
        recent_values = np.array(list(self._values)[-10:], dtype=np.float64)
        recent_times = np.array(list(self._times)[-10:], dtype=np.float64)

        # Нормализуем время
        t0 = recent_times[0]
        t_sec = (recent_times - t0) / 1000.0

        # Линейная регрессия: value = slope * t + intercept
        t_mean = np.mean(t_sec)
        v_mean = np.mean(recent_values)
        numerator = np.sum((t_sec - t_mean) * (recent_values - v_mean))
        denominator = np.sum((t_sec - t_mean) ** 2)

        if abs(denominator) < 1e-9:
            return None

        slope = float(numerator / denominator)

        # Для пилы характерны резкие сбросы — проверяем, что наклон стабильный
        # (не находимся на фронте сброса)
        if len(recent_values) >= 3:
            diffs = np.diff(recent_values)
            # Если есть резкий скачок, игнорируем (это фронт)
            if np.max(np.abs(diffs)) > 2 * np.median(np.abs(diffs)):
                return None

        return slope

    def reset(self) -> None:
        """Сброс состояния препроцессора."""
        self._values.clear()
        self._times.clear()
        self._bimodal_initialized = False
        self._level_a = 0.0
        self._level_b = 0.0
        self._envelope_max = 0.0
        self._envelope_min = 0.0
        logger.debug("SignalPreprocessor сброшен")

    def get_state(self) -> dict[str, Any]:
        """Получить текущее состояние для отладки."""
        return {
            "signal_type": self.signal_type,
            "window_size": self.window_size,
            "buffer_size": len(self._values),
            "level_a": self._level_a,
            "level_b": self._level_b,
            "envelope_max": self._envelope_max,
            "envelope_min": self._envelope_min,
        }
