"""
ui/__init__.py

Инициализация пакета `ui` — графический интерфейс приложения.
Содержит модули главного окна, окон графиков, неисправностей,
журнала событий и диалогов создания/настройки.
"""

from ui.main_window import MainWindow
from ui.plot_window import PlotWindow
from ui.log_window import LogWindow
from ui.plot_creation_dialog import PlotCreationDialog
from ui.fault_window import FaultWindow
from ui.fault_template_dialog import FaultTemplateDialog
from ui.fault_rule_dialog import FaultRuleDialog


__all__ = [
    "MainWindow",
    "PlotWindow",
    "LogWindow",
    "PlotCreationDialog",
    "FaultWindow",
    "FaultTemplateDialog",
    "FaultRuleDialog",
]
