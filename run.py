#!/usr/bin/env python3
"""
run.py — meniu interactiv pentru dgpt (cross-platform).

Rulare:  python run.py
"""
from __future__ import annotations
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY   = sys.executable   # foloseste interpretul Python curent (din .venv daca e activat)


def ensure_dirs():
    """Creeaza directoarele necesare daca lipsesc (cross-platform)."""
    for sub in ('data', 'output', 'temp'):
        (ROOT / sub).mkdir(exist_ok=True)


ensure_dirs()


# ─── helpers cross-platform ──────────────────────────────────────────

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    print()
    input('Apasa Enter pentru a continua...')


def open_with_default_app(path: Path):
    """Deschide path-ul cu aplicatia default a sistemului."""
    if not path.exists():
        print(f'Fisier inexistent: {path}')
        return
    if platform.system() == 'Windows':
        os.startfile(str(path))  # type: ignore[attr-defined]
    elif platform.system() == 'Darwin':
        subprocess.run(['open', str(path)], check=False)
    else:
        subprocess.run(['xdg-open', str(path)], check=False)


def run_script(script_path: Path):
    """Ruleaza un script Python in subprocess, in directorul proiectului."""
    if not script_path.exists():
        print(f'Lipseste: {script_path}')
        return
    subprocess.run([PY, str(script_path)], cwd=ROOT, check=False)


# ─── verificari ──────────────────────────────────────────────────────

def check_data() -> bool:
    """Verifica fisierele de date. Daca lipsesc, ofera auto-copy din examples/."""
    needed = {
        ROOT / 'data' / 'medici.xlsx':       ROOT / 'examples' / 'medici.xlsx',
        ROOT / 'data' / 'asistenti.xlsx':    ROOT / 'examples' / 'asistenti.xlsx',
        ROOT / 'data' / 'event_detail.xlsx': ROOT / 'examples' / 'event_detail.xlsx',
    }
    missing = {dst: src for dst, src in needed.items() if not dst.exists()}
    if not missing:
        return True

    print('Lipsesc fisiere de date:')
    for dst in missing:
        print(f'  {dst.relative_to(ROOT)}')
    print()
    answer = input('Copiez exemplele din examples/ ca punct de pornire? [Y/n] ').strip().lower()
    if answer not in ('', 'y', 'da'):
        print('OK, completeaza fisierele manual si reruleaza.')
        return False

    for dst, src in missing.items():
        if not src.exists():
            print(f'  EROARE: lipseste si exemplul {src.relative_to(ROOT)}')
            return False
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, dst)
        print(f'  copiat: {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}')
    print()
    print('Editeaza acum fisierele copiate (optiunile 4-7) inainte de a genera.')
    return True


# ─── actiuni meniu ───────────────────────────────────────────────────

def gen_planse():
    if check_data():
        run_script(ROOT / 'src' / 'generate_planse.py')


def gen_diplome():
    if check_data():
        run_script(ROOT / 'src' / 'generate_diplome.py')


def gen_all():
    if check_data():
        run_script(ROOT / 'src' / 'generate_planse.py')
        print()
        run_script(ROOT / 'src' / 'generate_diplome.py')


def open_output():
    open_with_default_app(ROOT / 'output')


def open_templates_folder():
    print('Deschid templates/ — editeaza PPTX-urile in PowerPoint / Keynote / LibreOffice.')
    open_with_default_app(ROOT / 'templates')


def commit_push():
    finalize = ROOT / 'finalize.py'
    if not finalize.exists():
        print('finalize.py lipseste.')
        return
    msg = input("Mesaj commit (Enter = 'update'): ").strip() or 'update'
    subprocess.run([PY, str(finalize), msg], cwd=ROOT, check=False)


# ─── meniu principal ─────────────────────────────────────────────────

BANNER = """\
╔══════════════════════════════════════════════════════════╗
║              dgpt — meniu principal                      ║
╚══════════════════════════════════════════════════════════╝"""

MENU = """
  GENERARE
    1) Genereaza TOT (planse + toate diplomele)
    2) Genereaza doar planse cabinete
    3) Genereaza doar diplome (medici + asistente + diverse)

  DATE
    4) Editeaza data/medici.xlsx
    5) Editeaza data/asistenti.xlsx
    6) Editeaza data/alte_diplome.xlsx (titulatura + nume)
    7) Editeaza data/event_detail.xlsx (data + locatie)
    8) Editeaza template-uri (inlocuieste placeholderele [Nume ...])

  IESIRI / GIT
    o) Deschide folderul output/
    g) Commit + push pe GitHub

    0) Iesire
"""


ACTIONS = {
    '1': gen_all,
    '2': gen_planse,
    '3': gen_diplome,
    '4': lambda: open_with_default_app(ROOT / 'data' / 'medici.xlsx'),
    '5': lambda: open_with_default_app(ROOT / 'data' / 'asistenti.xlsx'),
    '6': lambda: open_with_default_app(ROOT / 'data' / 'alte_diplome.xlsx'),
    '7': lambda: open_with_default_app(ROOT / 'data' / 'event_detail.xlsx'),
    '8': open_templates_folder,
    'o': open_output, 'O': open_output,
    'g': commit_push, 'G': commit_push,
}


def main():
    while True:
        clear_screen()
        print(BANNER)
        print(MENU)
        choice = input('Alege: ').strip()
        print()
        if choice in ('0', 'q', 'Q'):
            print('Pa.')
            return
        action = ACTIONS.get(choice)
        if action is None:
            print(f'Optiune invalida: {choice!r}')
            pause()
            continue
        try:
            action()
        except KeyboardInterrupt:
            print('\n[intrerupt]')
        pause()


if __name__ == '__main__':
    main()
