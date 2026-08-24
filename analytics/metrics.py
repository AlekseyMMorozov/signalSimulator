"""
analytics/metrics.py

Подсчёт метрик сравнения эффективности обнаружения неисправностей оператором
и детектором. Строится на основе событий из журнала. Позволяет оценить,
на сколько процентов детектор быстрее оператора, а также число ложных
срабатываний и пропусков.
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from core.event_log import EventRecord, EventType


logger = logging.getLogger(__name__)

# Типы неисправностей, для которых выход за порог считается индикатором пропуска
DEFAULT_TREND_FAULT_TYPES: Set[str] = {"degradation"}


@dataclass
class FaultAnalysisRecord:
    """Результат анализа одной неисправности."""
    plot_id: str
    fault_type: str
    injection_time_ms: int
    operator_detection_ms: Optional[int] = None
    detector_detection_ms: Optional[int] = None
    operator_delay_ms: Optional[int] = None
    detector_delay_ms: Optional[int] = None
    is_missed: bool = False


@dataclass
class MetricsSummary:
    """Агрегированные метрики сравнения оператора и детектора."""
    total_faults: int = 0
    operator_detected: int = 0
    detector_detected: int = 0
    both_detected: int = 0
    operator_only: int = 0
    detector_only: int = 0
    missed_faults: int = 0
    operator_avg_delay_ms: float = 0.0
    detector_avg_delay_ms: float = 0.0
    operator_false_positives: int = 0
    detector_false_positives: int = 0
    detector_faster_percent: float = 0.0

    def to_dict(self) -> Dict[str, float]:
        """Сериализация метрик в словарь."""
        return {
            "total_faults": self.total_faults,
            "operator_detected": self.operator_detected,
            "detector_detected": self.detector_detected,
            "both_detected": self.both_detected,
            "operator_only": self.operator_only,
            "detector_only": self.detector_only,
            "missed_faults": self.missed_faults,
            "operator_avg_delay_ms": self.operator_avg_delay_ms,
            "detector_avg_delay_ms": self.detector_avg_delay_ms,
            "operator_false_positives": self.operator_false_positives,
            "detector_false_positives": self.detector_false_positives,
            "detector_faster_percent": self.detector_faster_percent,
        }


class MetricsCalculator:
    """
    Калькулятор метрик сравнения оператора и детектора.

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
    """

    def __init__(self, trend_fault_types: Optional[Set[str]] = None) -> None:
        """
        Инициализация калькулятора метрик.

        Args:
            trend_fault_types: Множество типов неисправностей, для которых
                выход за порог считается индикатором пропуска.
                По умолчанию — {"degradation"}.
        """
        self._trend_fault_types = trend_fault_types if trend_fault_types is not None else DEFAULT_TREND_FAULT_TYPES.copy()
        logger.info(f"MetricsCalculator инициализирован. Трендовые типы: {self._trend_fault_types}.")

    def calculate(self, events: List[EventRecord]) -> MetricsSummary:
        """
        Вычислить метрики по списку событий журнала.

        Args:
            events: Список записей журнала событий.

        Returns:
            MetricsSummary: Агрегированные метрики.
        """
        try:
            # Группировка событий по графикам
            faults_by_plot = self._extract_events(events, EventType.FAULT_INJECTED)
            operator_by_plot = self._extract_events(events, EventType.OPERATOR_DETECTION)
            detector_by_plot = self._extract_events(events, EventType.DETECTOR_DETECTION)
            limits_by_plot = self._extract_events(events, EventType.LIMIT_EXCEEDED)

            all_plot_ids = set(faults_by_plot.keys()) | set(operator_by_plot.keys()) | set(detector_by_plot.keys())

            analysis_records: List[FaultAnalysisRecord] = []
            operator_fp = 0
            detector_fp = 0

            for plot_id in all_plot_ids:
                plot_faults = sorted(faults_by_plot.get(plot_id, []), key=lambda e: e.time_ms)
                plot_operator = sorted(operator_by_plot.get(plot_id, []), key=lambda e: e.time_ms)
                plot_detector = sorted(detector_by_plot.get(plot_id, []), key=lambda e: e.time_ms)
                plot_limits = sorted(limits_by_plot.get(plot_id, []), key=lambda e: e.time_ms)

                records, op_fp, det_fp = self._analyze_plot(
                    plot_id, plot_faults, plot_operator, plot_detector, plot_limits
                )
                analysis_records.extend(records)
                operator_fp += op_fp
                detector_fp += det_fp

            summary = self._aggregate(analysis_records, operator_fp, detector_fp)
            logger.info(f"Метрики вычислены: всего неисправностей {summary.total_faults}.")
            return summary
        except Exception as e:
            logger.error(f"Ошибка вычисления метрик: {e}")
            return MetricsSummary()

    def _extract_events(self, events: List[EventRecord], event_type: EventType) -> Dict[str, List[EventRecord]]:
        """Группировка событий по идентификатору графика."""
        result: Dict[str, List[EventRecord]] = {}
        try:
            for event in events:
                if event.event_type == event_type and event.plot_id is not None:
                    result.setdefault(event.plot_id, []).append(event)
        except Exception as e:
            logger.error(f"Ошибка группировки событий: {e}")
        return result

    def _analyze_plot(
        self,
        plot_id: str,
        faults: List[EventRecord],
        operator_detections: List[EventRecord],
        detector_detections: List[EventRecord],
        limit_exceeded: List[EventRecord]
    ) -> tuple:
        """
        Анализ неисправностей для одного графика.

        Возвращает кортеж (список записей анализа, ложные оператора, ложные детектора).
        """
        records: List[FaultAnalysisRecord] = []
        used_operator: Set[int] = set()
        used_detector: Set[int] = set()

        try:
            for i, fault_event in enumerate(faults):
                fault_type = fault_event.metadata.get("fault_type", "unknown")
                injection_time = fault_event.time_ms
                # Окно: до следующей неисправности или до бесконечности
                next_injection_time = faults[i + 1].time_ms if i + 1 < len(faults) else float("inf")

                record = FaultAnalysisRecord(
                    plot_id=plot_id,
                    fault_type=fault_type,
                    injection_time_ms=injection_time,
                )

                # Поиск обнаружения оператора в окне
                op_det = self._find_first_detection(operator_detections, injection_time, next_injection_time)
                if op_det is not None:
                    record.operator_detection_ms = op_det.time_ms
                    record.operator_delay_ms = op_det.time_ms - injection_time
                    used_operator.add(op_det.time_ms)

                # Поиск обнаружения детектора в окне
                det_det = self._find_first_detection(detector_detections, injection_time, next_injection_time)
                if det_det is not None:
                    record.detector_detection_ms = det_det.time_ms
                    record.detector_delay_ms = det_det.time_ms - injection_time
                    used_detector.add(det_det.time_ms)

                # Определение пропуска
                record.is_missed = self._is_missed(
                    fault_type, record, next_injection_time, limit_exceeded
                )
                records.append(record)

            # Подсчёт ложных срабатываний (обнаружения без сопоставленной неисправности)
            operator_fp = sum(
                1 for det in operator_detections
                if det.time_ms not in used_operator and not self._has_preceding_fault(faults, det.time_ms)
            )
            detector_fp = sum(
                1 for det in detector_detections
                if det.time_ms not in used_detector and not self._has_preceding_fault(faults, det.time_ms)
            )
        except Exception as e:
            logger.error(f"Ошибка анализа графика '{plot_id}': {e}")

        return records, operator_fp, detector_fp

    def _find_first_detection(
        self,
        detections: List[EventRecord],
        start_ms: int,
        end_ms: float
    ) -> Optional[EventRecord]:
        """Поиск первого обнаружения в временном окне [start_ms, end_ms)."""
        try:
            for det in detections:
                if start_ms <= det.time_ms < end_ms:
                    return det
        except Exception as e:
            logger.error(f"Ошибка поиска обнаружения: {e}")
        return None

    def _has_preceding_fault(self, faults: List[EventRecord], time_ms: int) -> bool:
        """Проверка, была ли неисправность до указанного времени."""
        try:
            return any(f.time_ms <= time_ms for f in faults)
        except Exception as e:
            logger.error(f"Ошибка проверки предшествующей неисправности: {e}")
            return False

    def _is_missed(
        self,
        fault_type: str,
        record: FaultAnalysisRecord,
        next_injection_time: float,
        limit_exceeded: List[EventRecord]
    ) -> bool:
        """
        Определение, является ли неисправность пропущенной.

        Для трендовых неисправностей: пропуск, если не обнаружена до выхода за порог.
        Для остальных: пропуск, если не обнаружена до следующей неисправности.
        """
        try:
            # Если обнаружена хотя бы одним способом — не пропуск
            if record.operator_detection_ms is not None or record.detector_detection_ms is not None:
                return False

            if fault_type in self._trend_fault_types:
                # Трендовая неисправность: проверяем выход за порог до следующей неисправности
                for limit_event in limit_exceeded:
                    if record.injection_time_ms < limit_event.time_ms < next_injection_time:
                        return True
                return False
            else:
                # Нетрендовая неисправность: пропуск, если есть следующая неисправность
                return next_injection_time != float("inf")
        except Exception as e:
            logger.error(f"Ошибка определения пропуска: {e}")
            return False

    def _aggregate(
        self,
        records: List[FaultAnalysisRecord],
        operator_fp: int,
        detector_fp: int
    ) -> MetricsSummary:
        """Агрегация результатов анализа в итоговые метрики."""
        summary = MetricsSummary()
        try:
            summary.total_faults = len(records)
            operator_delays: List[int] = []
            detector_delays: List[int] = []
            comparison_ratios: List[float] = []

            for rec in records:
                op_detected = rec.operator_delay_ms is not None
                det_detected = rec.detector_delay_ms is not None

                if op_detected:
                    summary.operator_detected += 1
                    operator_delays.append(rec.operator_delay_ms)
                if det_detected:
                    summary.detector_detected += 1
                    detector_delays.append(rec.detector_delay_ms)
                if op_detected and det_detected:
                    summary.both_detected += 1
                    # Вычисление процентного соотношения
                    if rec.operator_delay_ms > 0:
                        ratio = (rec.operator_delay_ms - rec.detector_delay_ms) / rec.operator_delay_ms * 100.0
                        comparison_ratios.append(ratio)
                elif op_detected and not det_detected:
                    summary.operator_only += 1
                elif det_detected and not op_detected:
                    summary.detector_only += 1

                if rec.is_missed:
                    summary.missed_faults += 1

            if operator_delays:
                summary.operator_avg_delay_ms = sum(operator_delays) / len(operator_delays)
            if detector_delays:
                summary.detector_avg_delay_ms = sum(detector_delays) / len(detector_delays)
            if comparison_ratios:
                summary.detector_faster_percent = sum(comparison_ratios) / len(comparison_ratios)

            summary.operator_false_positives = operator_fp
            summary.detector_false_positives = detector_fp
        except Exception as e:
            logger.error(f"Ошибка агрегации метрик: {e}")
        return summary
