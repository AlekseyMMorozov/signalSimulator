"""
signalSimulator/core/clock.py

Модуль управления глобальным логическим временем симуляции.
Обеспечивает единый источник времени для всех компонентов системы.
"""

import logging
from typing import Optional
from PyQt6.QtCore import QObject, QTimer, pyqtSignal

# Настройка логирования
logger = logging.getLogger(__name__)


class GlobalClock(QObject):
    """
    Глобальные часы симуляции с поддержкой ускорения времени.

    Реализует паттерн Singleton для обеспечения единого источника времени
    во всем приложении. Генерирует периодические сигналы обновления времени.

    Attributes:
        time_updated (pyqtSignal): Сигнал, испускаемый при каждом обновлении времени.
            Передает текущее логическое время в миллисекундах.
    """

    # Сигнал обновления времени (передает время в мс)
    time_updated = pyqtSignal(int)

    # Допустимые множители ускорения
    ALLOWED_MULTIPLIERS = [1, 10, 100, 1000, 10000]

    # Интервал тика в миллисекундах реального времени
    TICK_INTERVAL_MS = 1000

    _instance: Optional['GlobalClock'] = None

    def __new__(cls, *args, **kwargs) -> 'GlobalClock':
        """Реализация паттерна Singleton."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, parent: Optional[QObject] = None) -> None:
        """
        Инициализация глобальных часов.

        Args:
            parent: Родительский QObject для управления временем жизни.
        """
        if self._initialized:
            return

        super().__init__(parent)

        # Логическое время в миллисекундах
        self._current_time_ms: int = 0

        # Множитель ускорения времени
        self._speed_multiplier: int = 1

        # Флаг состояния (запущено/остановлено)
        self._is_running: bool = False

        # Таймер для генерации тиков
        self._timer = QTimer(self)
        self._timer.setInterval(self.TICK_INTERVAL_MS)
        self._timer.timeout.connect(self._on_tick)

        self._initialized = True
        logger.info(f"GlobalClock инициализирован. Интервал тика: {self.TICK_INTERVAL_MS}мс")

    def start(self) -> None:
        """Запуск симуляции времени."""
        try:
            if not self._is_running:
                self._is_running = True
                self._timer.start()
                logger.info("Симуляция времени запущена")
            else:
                logger.warning("Симуляция уже запущена")
        except Exception as e:
            logger.error(f"Ошибка при запуске симуляции: {e}")
            raise

    def stop(self) -> None:
        """Остановка симуляции времени."""
        try:
            if self._is_running:
                self._is_running = False
                self._timer.stop()
                logger.info("Симуляция времени остановлена")
            else:
                logger.warning("Симуляция уже остановлена")
        except Exception as e:
            logger.error(f"Ошибка при остановке симуляции: {e}")
            raise

    def reset(self) -> None:
        """Сброс времени в 0 миллисекунд."""
        try:
            was_running = self._is_running
            if was_running:
                self.stop()

            self._current_time_ms = 0
            logger.info("Время сброшено в 0")

            if was_running:
                self.start()
        except Exception as e:
            logger.error(f"Ошибка при сбросе времени: {e}")
            raise

    def set_speed_multiplier(self, multiplier: int) -> None:
        """
        Установка множителя ускорения времени.

        Args:
            multiplier: Множитель ускорения (должен быть в ALLOWED_MULTIPLIERS).

        Raises:
            ValueError: Если множитель не входит в список допустимых.
        """
        try:
            if multiplier not in self.ALLOWED_MULTIPLIERS:
                raise ValueError(
                    f"Недопустимый множитель: {multiplier}. "
                    f"Допустимые значения: {self.ALLOWED_MULTIPLIERS}"
                )

            self._speed_multiplier = multiplier
            logger.info(f"Множитель ускорения установлен: x{multiplier}")
        except ValueError as e:
            logger.error(f"Ошибка установки множителя: {e}")
            raise
        except Exception as e:
            logger.error(f"Непредвиденная ошибка при установке множителя: {e}")
            raise

    def get_current_time_ms(self) -> int:
        """
        Получение текущего логического времени.

        Returns:
            int: Текущее время в миллисекундах.
        """
        return self._current_time_ms

    def get_speed_multiplier(self) -> int:
        """
        Получение текущего множителя ускорения.

        Returns:
            int: Текущий множитель ускорения.
        """
        return self._speed_multiplier

    def is_running(self) -> bool:
        """
        Проверка состояния симуляции.

        Returns:
            bool: True если симуляция запущена, False иначе.
        """
        return self._is_running

    def get_formatted_time(self) -> str:
        """
        Получение времени в формате ЧЧ:ММ:СС.мс.

        Returns:
            str: Отформатированное время (например, "00:05:23.456").
        """
        try:
            total_seconds = self._current_time_ms // 1000
            milliseconds = self._current_time_ms % 1000

            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60

            return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        except Exception as e:
            logger.error(f"Ошибка форматирования времени: {e}")
            return "00:00:00.000"

    def _on_tick(self) -> None:
        """Обработка тика таймера - обновление логического времени."""
        try:
            # Вычисляем приращение логического времени
            delta_ms = self.TICK_INTERVAL_MS * self._speed_multiplier
            self._current_time_ms += delta_ms

            # Испускаем сигнал обновления
            self.time_updated.emit(self._current_time_ms)

            logger.debug(
                f"Тик времени: {self.get_formatted_time()} "
                f"(x{self._speed_multiplier})"
            )
        except Exception as e:
            logger.error(f"Ошибка при обработке тика: {e}")