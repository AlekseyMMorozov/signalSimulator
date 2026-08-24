"""
simulation/scheduler.py

Механизм случайного внедрения неисправностей. Каждые N секунд проверяется
генератор случайных чисел, и с вероятностью X активируется неисправность
на целевых графиках. Параметры N и X задаёт оператор. Поддерживается
несколько независимых правил и реестр заготовленных шаблонов неисправностей.
"""

import logging
import random
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


logger = logging.getLogger(__name__)


@dataclass
class FaultInjectionEvent:
    """
    Событие внедрения неисправности.

    Генерируется планировщиком при срабатывании правила и обрабатывается
    внешним менеджером симуляции (создание экземпляра неисправности,
    добавление в цепочку графика, активация, запись в журнал).
    """
    time_ms: int
    plot_id: str
    fault_type: str
    fault_params: Dict[str, Any]
    template_id: str = ""
    rule_id: str = ""


@dataclass
class FaultTemplate:
    """
    Шаблон неисправности (заготовка).

    Создаётся оператором и хранится в реестре планировщика. При срабатывании
    правила планировщик использует шаблон для генерации события внедрения.

    Режимы внедрения (target_mode):
        - "one": один случайный график из списка
        - "all": все графики из списка
        - "random_subset": случайное подмножество размера subset_count
    """
    template_id: str
    fault_type: str
    fault_params: Dict[str, Any] = field(default_factory=dict)
    target_plot_ids: List[str] = field(default_factory=list)
    target_mode: str = "one"
    subset_count: int = 1

    def select_target_plot_ids(self, available_plot_ids: List[str]) -> List[str]:
        """
        Определить целевые графики согласно режиму внедрения.

        Если `target_plot_ids` пуст, используются все доступные графики
        из `available_plot_ids`.

        Args:
            available_plot_ids: Список всех доступных графиков.

        Returns:
            Список целевых графиков.
        """
        try:
            candidates = self.target_plot_ids if self.target_plot_ids else available_plot_ids
            if not candidates:
                logger.warning(f"Шаблон {self.template_id}: нет доступных целевых графиков.")
                return []

            if self.target_mode == "all":
                return list(candidates)
            elif self.target_mode == "random_subset":
                count = min(self.subset_count, len(candidates))
                if count <= 0:
                    return []
                return random.sample(candidates, count)
            else:
                # Режим "one" по умолчанию
                return [random.choice(candidates)]
        except Exception as e:
            logger.error(f"Ошибка выбора целевых графиков для шаблона {self.template_id}: {e}")
            return []


@dataclass
class RandomFaultRule:
    """
    Правило случайного внедрения неисправностей.

    Каждые `check_interval_ms` миллисекунд проверяется генератор случайных
    чисел. Если случайное число меньше `probability`, правило срабатывает
    и выбирает один из шаблонов для внедрения.

    Вероятность задаётся в долях: 0.0 — никогда, 1.0 — всегда.
    """
    rule_id: str
    check_interval_ms: int
    probability: float
    template_ids: List[str] = field(default_factory=list)
    last_check_time_ms: int = 0
    enabled: bool = True
    initialized: bool = False


class FaultScheduler:
    """
    Планировщик случайного внедрения неисправностей.

    Хранит реестр шаблонов неисправностей и список правил. На каждом тике
    времени (`tick`) проверяет правила и генерирует события внедрения.
    Планировщик не знает о графиках и экземплярах неисправностей — он только
    генерирует события, которые обрабатываются внешним менеджером.
    """

    def __init__(self) -> None:
        """Инициализация планировщика с пустыми реестрами."""
        self._templates: Dict[str, FaultTemplate] = {}
        self._rules: Dict[str, RandomFaultRule] = {}
        logger.info("FaultScheduler инициализирован.")

    def add_template(self, template: FaultTemplate) -> None:
        """Добавить шаблон неисправности в реестр."""
        try:
            self._templates[template.template_id] = template
            logger.info(f"Добавлен шаблон неисправности: {template.template_id}.")
        except Exception as e:
            logger.error(f"Ошибка добавления шаблона: {e}")

    def remove_template(self, template_id: str) -> None:
        """Удалить шаблон неисправности из реестра."""
        if template_id in self._templates:
            del self._templates[template_id]
            logger.info(f"Удалён шаблон неисправности: {template_id}.")
        else:
            logger.warning(f"Попытка удалить несуществующий шаблон: {template_id}.")

    def get_template(self, template_id: str) -> Optional[FaultTemplate]:
        """Получить шаблон по ID."""
        return self._templates.get(template_id)

    def list_templates(self) -> List[FaultTemplate]:
        """Получить список всех шаблонов."""
        return list(self._templates.values())

    def add_rule(self, rule: RandomFaultRule) -> None:
        """Добавить правило случайного внедрения."""
        try:
            self._rules[rule.rule_id] = rule
            logger.info(
                f"Добавлено правило: {rule.rule_id} "
                f"(интервал {rule.check_interval_ms} мс, вероятность {rule.probability})."
            )
        except Exception as e:
            logger.error(f"Ошибка добавления правила: {e}")

    def remove_rule(self, rule_id: str) -> None:
        """Удалить правило случайного внедрения."""
        if rule_id in self._rules:
            del self._rules[rule_id]
            logger.info(f"Удалено правило: {rule_id}.")
        else:
            logger.warning(f"Попытка удалить несуществующее правило: {rule_id}.")

    def get_rule(self, rule_id: str) -> Optional[RandomFaultRule]:
        """Получить правило по ID."""
        return self._rules.get(rule_id)

    def list_rules(self) -> List[RandomFaultRule]:
        """Получить список всех правил."""
        return list(self._rules.values())

    def tick(self, current_time_ms: int, available_plot_ids: List[str]) -> List[FaultInjectionEvent]:
        """
        Обработка одного тика времени.

        Для каждого активного правила проверяет, наступило ли время проверки.
        Если да — генерирует случайное число и при срабатывании создаёт
        события внедрения. Корректно обрабатывает ускорение времени:
        все пропущенные интервалы проверяются последовательно.

        Args:
            current_time_ms: Текущее логическое время в миллисекундах.
            available_plot_ids: Список всех доступных графиков.

        Returns:
            Список событий внедрения неисправностей.
        """
        events: List[FaultInjectionEvent] = []
        try:
            for rule in self._rules.values():
                if not rule.enabled:
                    continue
                if not rule.initialized:
                    rule.last_check_time_ms = current_time_ms
                    rule.initialized = True
                    logger.debug(f"Правило {rule.rule_id} инициализировано в {current_time_ms} мс.")
                    continue

                # Обрабатываем все пропущенные интервалы (важно при ускорении времени)
                while current_time_ms - rule.last_check_time_ms >= rule.check_interval_ms:
                    rule.last_check_time_ms += rule.check_interval_ms
                    if random.random() < rule.probability:
                        rule_events = self._inject_from_rule(rule, rule.last_check_time_ms, available_plot_ids)
                        events.extend(rule_events)
        except Exception as e:
            logger.error(f"Ошибка в планировщике при обработке тика: {e}")
        return events

    def _inject_from_rule(
        self,
        rule: RandomFaultRule,
        time_ms: int,
        available_plot_ids: List[str]
    ) -> List[FaultInjectionEvent]:
        """
        Внутренний метод генерации событий при срабатывании правила.

        Выбирает случайный шаблон из списка правила, определяет целевые
        графики и создаёт события внедрения для каждого целевого графика.

        Args:
            rule: Сработавшее правило.
            time_ms: Время срабатывания.
            available_plot_ids: Список всех доступных графиков.

        Returns:
            Список событий внедрения.
        """
        events: List[FaultInjectionEvent] = []
        try:
            if not rule.template_ids:
                logger.warning(f"Правило {rule.rule_id}: нет шаблонов для внедрения.")
                return events

            template_id = random.choice(rule.template_ids)
            template = self._templates.get(template_id)
            if template is None:
                logger.warning(f"Правило {rule.rule_id}: шаблон {template_id} не найден в реестре.")
                return events

            target_ids = template.select_target_plot_ids(available_plot_ids)
            if not target_ids:
                logger.warning(f"Правило {rule.rule_id}: не определены целевые графики.")
                return events

            for plot_id in target_ids:
                event = FaultInjectionEvent(
                    time_ms=time_ms,
                    plot_id=plot_id,
                    fault_type=template.fault_type,
                    fault_params=dict(template.fault_params),
                    template_id=template.template_id,
                    rule_id=rule.rule_id,
                )
                events.append(event)

            logger.info(
                f"Правило {rule.rule_id} сработало в {time_ms} мс: "
                f"шаблон {template_id}, целевые графики {target_ids}."
            )
        except Exception as e:
            logger.error(f"Ошибка генерации событий для правила {rule.rule_id}: {e}")
        return events

    def reset(self) -> None:
        """Сброс состояния всех правил (при сбросе симуляции)."""
        for rule in self._rules.values():
            rule.last_check_time_ms = 0
            rule.initialized = False
        logger.info("Состояние планировщика сброшено.")

    def clear(self) -> None:
        """Очистка реестров шаблонов и правил."""
        self._templates.clear()
        self._rules.clear()
        logger.info("Реестры планировщика очищены.")
