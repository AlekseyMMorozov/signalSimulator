"""
generate_structure.py

Скрипт для генерации структуры проекта в формате Markdown.
Собирает метаданные, дерево файлов, сигнатуры классов/функций и граф зависимостей.
Поддерживает полный вывод содержимого для указанных файлов (models, schemas).
"""

import ast
import sys

from collections import defaultdict
from pathlib import Path
from typing import Any, TypedDict

import tomllib

PROJECT_ROOT = Path(__file__).parent.resolve()
IGNORE_DIRS: set[str] = {
    '.git', '.hg', '.svn', '.idea', '.venv', '.env', '__pycache__',
    'logs', 'files', '.pytest_cache', '.mypy_cache', '.ruff_cache',
    '.coverage', 'htmlcov', '.tox', '.eggs', 'dist', 'build', 'files'
}
IGNORE_FILES: set[str] = {
    'test_db_connection.py',
    'temp.py',
    'generate_structure.py',
    'compact_code.py'
}
OUTPUT_FILE = PROJECT_ROOT / 'files' / 'structure.md'

# Паттерны для файлов, содержимое которых нужно выводить полностью
# (не только сигнатуры, а весь код)
FULL_CONTENT_PATTERNS: list[str] = [
    'database/models.py',
    'database/schemas.py',
    'database/models/',
    'database/schemas/',
]


class CodeAnalysis(TypedDict):
    imports: list[str]
    classes: list[dict[str, Any]]
    functions: list[dict[str, Any]]
    doc: str  # docstring модуля


class TreeNode(TypedDict):
    name: str
    type: str
    path: str
    children: list['TreeNode']
    imports: list[str]
    classes: list[dict[str, Any]]
    functions: list[dict[str, Any]]
    doc: str  # для файлов – docstring модуля


def get_project_metadata(root: Path) -> dict[str, Any]:
    """Собирает метаинформацию о проекте из README, pyproject.toml, requirements.txt."""
    meta = {
        'name': root.name,
        'description': '',
        'version': '',
        'dependencies': [],
        'entry_points': []
    }
    # README
    readme = root / 'README.md'
    if readme.exists():
        try:
            text = readme.read_text(encoding='utf-8')
            # Берём первую непустую строку или первые 500 символов
            lines = [l for l in text.splitlines() if l.strip()]
            if lines:
                meta['description'] = lines[0][:500]
        except Exception:
            pass

    # pyproject.toml (используем tomllib, если доступно)
    pyproject = root / 'pyproject.toml'
    if pyproject.exists():
        try:
            with open(pyproject, 'rb') as f:
                data = tomllib.load(f)
            project = data.get('project', {})
            meta['name'] = project.get('name', meta['name'])
            meta['version'] = project.get('version', '')
            deps = project.get('dependencies', [])
            if isinstance(deps, list):
                meta['dependencies'].extend(deps)
        except Exception:
            pass

    # requirements.txt
    req = root / 'requirements.txt'
    if req.exists():
        try:
            lines = req.read_text(encoding='utf-8').splitlines()
            # Убираем комментарии и пустые строки
            deps = [l for l in lines if l.strip() and not l.startswith('#')]
            meta['dependencies'].extend(deps)
        except Exception:
            pass

    # Поиск точек входа (файлы с if __name__ == "__main__")
    for py in root.rglob('*.py'):
        try:
            if 'if __name__ == "__main__"' in py.read_text(encoding='utf-8', errors='ignore'):
                meta['entry_points'].append(str(py.relative_to(root)))
        except Exception:
            continue

    return meta


def analyze_code(content: str, file_path: str = '') -> dict[str, str | None | list[str] | list[dict[str, Any]]] | None:
    """Парсит Python-код и возвращает импорты, классы, функции и docstring модуля."""
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print(f"Ошибка синтаксиса в {file_path}: {e}")
        return None
    analyzer = CodeAnalyzer()
    analyzer.visit(tree)
    module_doc = ast.get_docstring(tree) or ''
    return {
        'imports': analyzer.imports,
        'classes': analyzer.classes,
        'functions': analyzer.functions,
        'doc': module_doc
    }


class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.imports: list[str] = []
        self.classes: list[dict[str, Any]] = []
        self.functions: list[dict[str, Any]] = []
        self.class_stack: list[str] = []

    def visit_Import(self, node: ast.Import) -> None:
        parts = []
        for alias in node.names:
            parts.append(f"{alias.name} as {alias.asname}" if alias.asname else alias.name)
        self.imports.append(f"import {', '.join(parts)}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module = node.module if node.module is not None else ''
        level = '.' * node.level if node.level else ''
        names = []
        for alias in node.names:
            names.append(f"{alias.name} as {alias.asname}" if alias.asname else alias.name)
        self.imports.append(f"from {level}{module} import {', '.join(names)}")
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.class_stack.append(node.name)
        class_info: dict[str, Any] = {
            'name': node.name,
            'methods': [],
            'bases': [self._safe_unparse(b) for b in node.bases],
            'doc': ast.get_docstring(node) or '',
            'decorators': [self._safe_unparse(d) for d in node.decorator_list]
        }
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                class_info['methods'].append(self._parse_function(item))
        self.classes.append(class_info)
        self.generic_visit(node)
        self.class_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if not self.class_stack:
            self.functions.append(self._parse_function(node))
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        if not self.class_stack:
            func = self._parse_function(node)
            func['async'] = True
            self.functions.append(func)
        self.generic_visit(node)

    def _parse_function(self, node: ast.AST) -> dict[str, Any]:
        is_async = isinstance(node, ast.AsyncFunctionDef)
        return {
            'name': node.name,
            'args': self._parse_arguments(node.args),
            'returns': self._safe_unparse(node.returns) if hasattr(node, 'returns') and node.returns else None,
            'decorators': [self._safe_unparse(d) for d in node.decorator_list],
            'async': is_async,
            'doc': ast.get_docstring(node) or ''
        }

    def _parse_arguments(self, args: ast.arguments) -> list[dict[str, str | None]]:
        params: list[dict[str, str | None]] = []
        for arg in args.args:
            params.append({
                'name': arg.arg,
                'type': self._safe_unparse(arg.annotation) if arg.annotation else None
            })
        if args.vararg:
            params.append({
                'name': '*' + args.vararg.arg,
                'type': self._safe_unparse(args.vararg.annotation) if args.vararg.annotation else None
            })
        for kwarg, default_expr in zip(args.kwonlyargs, args.kw_defaults):
            default = self._safe_unparse(default_expr) if default_expr else None
            params.append({
                'name': kwarg.arg,
                'type': self._safe_unparse(kwarg.annotation) if kwarg.annotation else None,
                'default': default
            })
        if args.kwarg:
            params.append({
                'name': '**' + args.kwarg.arg,
                'type': self._safe_unparse(args.kwarg.annotation) if args.kwarg.annotation else None
            })
        return params

    @staticmethod
    def _safe_unparse(node: ast.AST) -> str:
        try:
            return ast.unparse(node)
        except Exception:
            return '...'


def build_project_tree(root_path: Path, ignore_dirs: set[str], ignore_files: set[str]) -> TreeNode:
    project_tree: TreeNode = {
        'name': root_path.name,
        'type': 'directory',
        'path': '',
        'children': [],
        'imports': [],
        'classes': [],
        'functions': [],
        'doc': ''
    }

    for path in sorted(root_path.iterdir(), key=lambda p: (not p.is_dir(), p.name)):
        if path.name in ignore_dirs or (path.is_dir() and path.name.startswith('.')):
            continue
        if path.is_dir():
            project_tree['children'].append(build_project_tree(path, ignore_dirs, ignore_files))
        elif path.suffix == '.py' and path.name not in ignore_files:
            try:
                content = path.read_text(encoding='utf-8')
            except Exception as e:
                print(f"Не удалось прочитать файл {path}: {e}")
                continue
            analysis = analyze_code(content, str(path))
            if analysis is None:
                print(f"Пропускаем файл (ошибка парсинга): {path}")
                continue
            project_tree['children'].append({
                'name': path.name,
                'type': 'file',
                'path': str(path.relative_to(root_path)),
                'children': [],
                'imports': analysis['imports'],
                'classes': analysis['classes'],
                'functions': analysis['functions'],
                'doc': analysis['doc']
            })
    return project_tree


def collect_stats(node: TreeNode) -> dict[str, int]:
    stats = {
        'dirs': 0,
        'py_files': 0,
        'total_files': 0,
        'classes': 0,
        'functions': 0,
    }
    if node['type'] == 'directory':
        stats['dirs'] += 1
        for child in node['children']:
            sub = collect_stats(child)
            for k in stats:
                stats[k] += sub[k]
    else:
        stats['total_files'] += 1
        if node['name'].endswith('.py'):
            stats['py_files'] += 1
            stats['classes'] += len(node['classes'])
            stats['functions'] += len(node['functions'])
    return stats


def generate_tree_lines(node: TreeNode, level: int = 0) -> list[str]:
    lines = []
    indent = '  ' * level
    suffix = '/' if node['type'] == 'directory' else ''
    lines.append(f"{indent}{node['name']}{suffix}")
    children = sorted(node['children'], key=lambda x: (x['type'] == 'file', x['name']))
    for child in children:
        lines.extend(generate_tree_lines(child, level + 1))
    return lines


def get_stdlib_module_names() -> set[str]:
    """Возвращает множество имён стандартных модулей Python (доступно в 3.10+)."""
    if hasattr(sys, 'stdlib_module_names'):
        return set(sys.stdlib_module_names)
    # fallback для старых версий – примерный список (неполный)
    return {
        'abc', 'aifc', 'argparse', 'array', 'ast', 'asyncio', 'base64',
        'bdb', 'binascii', 'bisect', 'builtins', 'bz2', 'calendar', 'cgi',
        'cmath', 'cmd', 'code', 'codecs', 'collections', 'colorsys', 'compileall',
        'concurrent', 'configparser', 'contextlib', 'copy', 'copyreg', 'cProfile',
        'csv', 'ctypes', 'curses', 'dataclasses', 'datetime', 'dbm', 'decimal',
        'difflib', 'dis', 'distutils', 'doctest', 'email', 'encodings', 'enum',
        'errno', 'faulthandler', 'fcntl', 'filecmp', 'fileinput', 'fnmatch',
        'fractions', 'ftplib', 'functools', 'gc', 'getopt', 'getpass', 'gettext',
        'glob', 'gzip', 'hashlib', 'heapq', 'hmac', 'http', 'imaplib', 'imp',
        'importlib', 'inspect', 'io', 'ipaddress', 'itertools', 'json', 'keyword',
        'linecache', 'locale', 'logging', 'lzma', 'mailbox', 'mailcap', 'marshal',
        'math', 'mimetypes', 'mmap', 'modulefinder', 'msilib', 'msvcrt', 'multiprocessing',
        'netrc', 'nis', 'nntplib', 'numbers', 'operator', 'optparse', 'os', 'pathlib',
        'pdb', 'pickle', 'pickletools', 'pipes', 'pkgutil', 'platform', 'plistlib',
        'poplib', 'posix', 'pprint', 'profile', 'pstats', 'pty', 'pwd', 'pyclbr',
        'pycompile', 'pyexpat', 'pydoc', 'queue', 'quopri', 'random', 're', 'readline',
        'reprlib', 'resource', 'rlcompleter', 'runpy', 'sched', 'secrets', 'select',
        'selectors', 'shelve', 'shlex', 'shutil', 'signal', 'site', 'smtplib', 'sndhdr',
        'socket', 'socketserver', 'spwd', 'sqlite3', 'ssl', 'stat', 'statistics', 'string',
        'stringprep', 'struct', 'subprocess', 'sunau', 'symbol', 'symtable', 'sys',
        'sysconfig', 'syslog', 'tabnanny', 'tarfile', 'telnetlib', 'tempfile', 'termios',
        'test', 'textwrap', 'threading', 'time', 'timeit', 'tkinter', 'token', 'tokenize',
        'trace', 'traceback', 'tracemalloc', 'tty', 'turtle', 'types', 'typing',
        'unicodedata', 'unittest', 'urllib', 'uu', 'uuid', 'venv', 'warnings', 'wave',
        'weakref', 'webbrowser', 'winreg', 'winsound', 'wsgiref', 'xdrlib', 'xml',
        'xmlrpc', 'zipfile', 'zipimport', 'zlib'
    }


STDLIB_MODULES = get_stdlib_module_names()


def categorize_import(imp: str) -> str:
    """
    Определяет категорию импорта: 'stdlib', 'local', 'third_party'.
    Принимает строку импорта, например 'import os' или 'from .utils import foo'.
    """
    # Извлекаем имя модуля
    if imp.startswith('import '):
        module_part = imp[len('import '):].strip()
        # может быть несколько через запятую, берём первый
        module_name = module_part.split(',')[0].strip()
        # убираем 'as ...'
        if ' as ' in module_name:
            module_name = module_name.split(' as ')[0].strip()
    elif imp.startswith('from '):
        # from package import ...
        rest = imp[len('from '):]
        module_part = rest.split(' import ')[0].strip()
        module_name = module_part
    else:
        return 'unknown'

    # Если модуль начинается с точки – относительный импорт (локальный)
    if module_name.startswith('.'):
        return 'local'

    # Если это абсолютный импорт, проверяем, не входит ли в стандартную библиотеку
    # Берём первую часть до точки
    top_module = module_name.split('.')[0]
    if top_module in STDLIB_MODULES:
        return 'stdlib'
    else:
        # Предполагаем, что всё остальное – стороннее (или локальное, но без точки)
        return 'third_party'


def build_dependency_graph(node: TreeNode, root_path: Path) -> list[tuple[str, str]]:
    """
    Строит список рёбер (файл -> импортируемый модуль).
    Возвращает список кортежей (from_file, to_module_name).
    to_module_name – имя модуля (может быть относительным).
    """
    edges = []
    for child in node['children']:
        if child['type'] == 'file':
            file_path = child['path']  # относительный путь
            for imp in child['imports']:
                # Извлекаем имя модуля
                if imp.startswith('import '):
                    module_part = imp[len('import '):].strip()
                    # может быть несколько, берём первый
                    module_name = module_part.split(',')[0].strip()
                    if ' as ' in module_name:
                        module_name = module_name.split(' as ')[0].strip()
                elif imp.startswith('from '):
                    rest = imp[len('from '):]
                    module_part = rest.split(' import ')[0].strip()
                    module_name = module_part
                else:
                    continue
                edges.append((file_path, module_name))
        elif child['type'] == 'directory':
            edges.extend(build_dependency_graph(child, root_path))
    return edges


def generate_dependency_section(edges: list[tuple[str, str]]) -> list[str]:
    """Формирует Markdown-раздел с графом зависимостей."""
    lines = []
    lines.append("## Граф зависимостей между файлами")
    lines.append("(Файл -> импортируемый модуль)")
    if not edges:
        lines.append("Нет зависимостей.")
        return lines
    # Сортируем для стабильности
    for from_file, to_module in sorted(edges):
        lines.append(f"- `{from_file}` → `{to_module}`")
    return lines


def should_include_full_content(file_path: str) -> bool:
    """
    Проверяет, нужно ли выводить полное содержимое файла.
    Сравнивает путь с паттернами из FULL_CONTENT_PATTERNS.
    """
    file_path_lower = file_path.lower()
    for pattern in FULL_CONTENT_PATTERNS:
        if pattern in file_path_lower:
            return True
    return False


def generate_file_contents(node: TreeNode, root_path: Path) -> list[str]:
    """Генерирует содержимое файлов: импорты (с категориями), классы, функции с docstring.
       Для файлов, подпадающих под FULL_CONTENT_PATTERNS, выводит полный код.
    """
    lines = []
    children = sorted(node['children'], key=lambda x: (x['type'] == 'file', x['name']))
    for child in children:
        if child['type'] == 'directory':
            lines.extend(generate_file_contents(child, root_path))
        else:
            rel_path = child['path']
            lines.append(f"\n### Файл: `{rel_path}`")

            # Проверяем, нужно ли выводить полное содержимое
            if should_include_full_content(rel_path):
                lines.append("#### Полное содержимое файла")
                # Читаем исходный файл
                file_path = root_path / rel_path
                try:
                    content = file_path.read_text(encoding='utf-8')
                    lines.append("```python")
                    lines.append(content)
                    lines.append("```")
                except Exception as e:
                    lines.append(f"*Ошибка чтения файла: {e}*")
                # Добавляем разделитель, чтобы не дублировать сигнатуры
                lines.append("---")
                continue

            # docstring модуля
            if child['doc']:
                lines.append(f"> {child['doc']}")

            # Импорты с категориями
            if child['imports']:
                lines.append("#### Импорты")
                # Группируем по категориям
                categories = defaultdict(list)
                for imp in child['imports']:
                    cat = categorize_import(imp)
                    categories[cat].append(imp)
                for cat in ['stdlib', 'third_party', 'local', 'unknown']:
                    if categories.get(cat):
                        label = {
                            'stdlib': 'Стандартная библиотека',
                            'third_party': 'Сторонние библиотеки',
                            'local': 'Локальные модули',
                            'unknown': 'Неопределённые'
                        }.get(cat, cat)
                        lines.append(f"- **{label}:**")
                        for imp in sorted(categories[cat]):
                            lines.append(f"  - `{imp}`")
            # Классы
            if child['classes']:
                lines.append("#### Классы")
                for cls in child['classes']:
                    decorators = ' '.join(f"@{d}" for d in cls.get('decorators', []))
                    bases = f"({', '.join(cls['bases'])})" if cls['bases'] else ''
                    lines.append(f"##### `{decorators} class {cls['name']}{bases}`" if decorators else f"##### `class {cls['name']}{bases}`")
                    if cls['doc']:
                        lines.append(f"> {cls['doc']}")
                    if cls['methods']:
                        lines.append("Методы:")
                        for method in cls['methods']:
                            sig = format_signature(method)
                            lines.append(f"- `{sig}`")
                            if method.get('doc'):
                                lines.append(f"  - {method['doc']}")
            # Функции
            if child['functions']:
                lines.append("#### Функции")
                for func in child['functions']:
                    sig = format_signature(func)
                    lines.append(f"- `{sig}`")
                    if func.get('doc'):
                        lines.append(f"  - {func['doc']}")
    return lines


def format_signature(func: dict[str, Any]) -> str:
    params = []
    for arg in func['args']:
        p = arg['name']
        if arg.get('type'):
            p += f": {arg['type']}"
        if arg.get('default'):
            p += f" = {arg['default']}"
        params.append(p)

    ret = f" -> {func['returns']}" if func.get('returns') else ''
    decs = ' '.join(f"@{d}" for d in func['decorators'])
    prefix = f"{decs} " if decs else ''
    async_prefix = "async " if func.get('async') else ""
    return f"{prefix}{async_prefix}def {func['name']}({', '.join(params)}){ret}"


def main() -> None:
    print("Сборка структуры проекта...")
    # 1. Метаданные
    meta = get_project_metadata(PROJECT_ROOT)

    # 2. Построение дерева
    project_tree = build_project_tree(PROJECT_ROOT, IGNORE_DIRS, IGNORE_FILES)

    # 3. Статистика
    stats = collect_stats(project_tree)

    # 4. Граф зависимостей
    edges = build_dependency_graph(project_tree, PROJECT_ROOT)

    # 5. Генерация отчёта
    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# Структура и метаданные проекта\n\n")

        # Метаданные
        f.write("## Метаданные проекта\n")
        f.write(f"- **Название:** {meta['name']}\n")
        f.write(f"- **Версия:** {meta['version'] or 'не указана'}\n")
        f.write(f"- **Описание:** {meta['description'] or 'нет'}\n")
        if meta['dependencies']:
            f.write(f"- **Зависимости:** {', '.join(meta['dependencies'][:10])}")
            if len(meta['dependencies']) > 10:
                f.write(f" и ещё {len(meta['dependencies']) - 10}")
            f.write("\n")
        else:
            f.write("- **Зависимости:** не найдены\n")
        if meta['entry_points']:
            f.write(f"- **Точки входа:** {', '.join(meta['entry_points'])}\n")
        else:
            f.write("- **Точки входа:** не обнаружены\n")
        f.write("\n")

        # Статистика
        f.write("## Статистика проекта\n")
        f.write(f"- Папок: {stats['dirs']}\n")
        f.write(f"- Python-файлов: {stats['py_files']}\n")
        f.write(f"- Всего файлов: {stats['total_files']}\n")
        f.write(f"- Классов: {stats['classes']}\n")
        f.write(f"- Функций: {stats['functions']}\n")
        f.write("\n")

        # Дерево
        f.write("## Дерево проекта\n")
        f.write("```\n")
        tree_lines = generate_tree_lines(project_tree)
        f.write('\n'.join(tree_lines))
        f.write("\n```\n\n")

        # Содержимое файлов
        f.write("## Содержимое файлов (сигнатуры с docstring)\n")
        content_lines = generate_file_contents(project_tree, PROJECT_ROOT)
        f.write('\n'.join(content_lines))
        f.write("\n\n")

        # Граф зависимостей
        dep_lines = generate_dependency_section(edges)
        f.write('\n'.join(dep_lines))
        f.write("\n")

    print(f"Отчёт сохранён: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
