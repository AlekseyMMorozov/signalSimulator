from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set
import ast
import re
import json

PROJECT_ROOT = Path(__file__).parent.resolve()
IGNORE_DIRS = {'.venv', '.idea', 'logs', '__pycache__', 'files'}
OUTPUT_FILE = PROJECT_ROOT / 'files' / 'project_context.md'
IGNORE_LIST_FILE = PROJECT_ROOT / 'files' / 'ignore_list.json'
USER_CHOICES_FILE = PROJECT_ROOT / 'files' / 'user_choices.json'
INCLUDE_EXTENSIONS = {'.py'}


class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.imports: List[str] = []
        self.classes: List[str] = []
        self.functions: List[str] = []
        self._in_class = False

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            name = alias.name + (f" as {alias.asname}" if alias.asname else "")
            self.imports.append(name)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        bases = ", ".join(ast.unparse(b) for b in node.bases)
        sig = f"{node.name}({bases})" if bases else node.name
        self.classes.append(sig)

        old_flag = self._in_class
        self._in_class = True
        for child in node.body:
            if isinstance(child, ast.FunctionDef):
                self.functions.append(self._get_sig(child))
        self.generic_visit(node)
        self._in_class = old_flag

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if not self._in_class:
            self.functions.append(self._get_sig(node))
        self.generic_visit(node)

    def _get_sig(self, node: ast.FunctionDef) -> str:
        args = []
        for a in node.args.args:
            arg_s = a.arg + (f":{ast.unparse(a.annotation)}" if a.annotation else "")
            args.append(arg_s)
        sig = f"{node.name}({', '.join(args)})"
        if node.returns:
            sig += f"->{ast.unparse(node.returns)}"
        return sig


def analyze_code(content: str) -> Dict[str, List[str]]:
    try:
        tree = ast.parse(content)
        analyzer = CodeAnalyzer()
        analyzer.visit(tree)
        return {'imports': analyzer.imports, 'classes': analyzer.classes, 'functions': analyzer.functions}
    except Exception:
        return {'imports': [], 'classes': [], 'functions': []}


def load_json(path: Path) -> any:
    if path.exists():
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return set() if path == IGNORE_LIST_FILE else {}


def save_json(path: Path, data: any) -> None:
    path.parent.mkdir(exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(list(data) if isinstance(data, set) else data, f, ensure_ascii=False, indent=2)


def collect_files(root: Path, ignore_list: Set[str], user_choices: Dict[str, str]) -> List[Path]:
    all_files = sorted([
        p for p in root.rglob('*')
        if p.suffix in INCLUDE_EXTENSIONS and p.is_file() and not any(d in IGNORE_DIRS for d in p.parts)
    ])

    files_to_process = []
    new_ignore = ignore_list.copy()
    new_choices = user_choices.copy()
    should_stop = False

    for fp in all_files:
        rel = str(fp.relative_to(PROJECT_ROOT))
        if rel in ignore_list:
            continue
        if rel in user_choices:
            ch = user_choices[rel]
            if ch == 'y': files_to_process.append(fp)
            continue

        print(f"\nНайден: {rel}")
        while True:
            resp = input("(y/n/a/r/s): ").strip().lower()
            if resp in ('y', 'n', 'a'):
                new_choices[rel] = resp
                if resp == 'y':
                    files_to_process.append(fp)
                elif resp == 'a':
                    new_ignore.add(rel)
                break
            elif resp == 'r':
                print("Сброс выборов. Запускаем заново...")
                return collect_files(root, ignore_list, {})
            elif resp == 's':
                should_stop = True
                break
        if should_stop: break

    if new_ignore != ignore_list: save_json(IGNORE_LIST_FILE, new_ignore)
    if new_choices != user_choices: save_json(USER_CHOICES_FILE, new_choices)
    return files_to_process


def compress_code(code: str) -> str:
    """Удаляет комментарии, докстринги и пустые строки. Сохраняет отступы для парсинга LLM."""
    code = re.sub(r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\')', '', code)
    cleaned = []
    for line in code.split('\n'):
        line = line.rstrip()
        # Удаляем inline-комментарии (базовая эвристика)
        if '#' in line:
            idx = line.find('#')
            if idx > 0 and line[idx - 1] not in ('"', "'"):
                line = line[:idx].rstrip()
        if line:
            cleaned.append(line)
    return '\n'.join(cleaned)


def generate_compact_report(files: List[Path]) -> str:
    lines = []
    for f in files:
        rel = f.relative_to(PROJECT_ROOT)
        mod = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d")
        content = f.read_text(encoding='utf-8')
        if not content.strip(): continue

        analysis = analyze_code(content)
        clean_code = compress_code(content)

        # Формат оптимизирован под парсинг LLM: маркеры + 2 пробела отступа
        lines.append(f"> {rel} [{mod}]")
        if analysis['imports']: lines.append(f"  i: {', '.join(analysis['imports'])}")
        if analysis['classes']: lines.append(f"  c: {', '.join(analysis['classes'])}")
        if analysis['functions']: lines.append(f"  f: {', '.join(analysis['functions'])}")
        if clean_code:
            lines.append("  code:")
            lines.append(clean_code)
        lines.append("---")
    return "\n".join(lines)


def main() -> None:
    ignore_list = load_json(IGNORE_LIST_FILE)
    if not isinstance(ignore_list, set): ignore_list = set(ignore_list)
    if ignore_list: print(f"Загружен ignore_list ({len(ignore_list)})")

    user_choices = load_json(USER_CHOICES_FILE)
    if not isinstance(user_choices, dict): user_choices = {}
    if user_choices: print(f"Загружены выборы ({len(user_choices)})")

    files = collect_files(PROJECT_ROOT, ignore_list, user_choices)
    if not files:
        print("Нет файлов для обработки.")
        return

    report = generate_compact_report(files)
    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    OUTPUT_FILE.write_text(report, encoding='utf-8')
    print(f"\nОтчёт сохранён: {OUTPUT_FILE}")
    print(f"Обработано файлов: {len(files)}")


if __name__ == "__main__":
    main()
