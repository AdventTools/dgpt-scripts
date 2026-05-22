#!/usr/bin/env python3
"""
finalize.py — commit + push pentru proiectul dgpt.

Rulare:  python finalize.py "mesaj de commit"

Reguli protejate:
- data/, temp/, output/, reports/ NU urca pe git (au nume reale / sunt regenerabile)
- Daca un fisier din data/ sau temp/ ajunge staged (M sau A), refuza si avertizeaza
"""
from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(cmd, *, check=True, capture=False):
    """Wrapper subprocess.run cu cwd la radacina proiectului."""
    if capture:
        return subprocess.run(cmd, cwd=ROOT, check=check, capture_output=True, text=True)
    return subprocess.run(cmd, cwd=ROOT, check=check)


def check_protected_staged() -> list[str]:
    """Returneaza fisierele din data/ sau temp/ care sunt ADDED/MODIFIED in staging."""
    res = run(['git', 'diff', '--cached', '--name-status'], check=False, capture=True)
    bad = []
    for line in res.stdout.splitlines():
        parts = line.split('\t', 1)
        if len(parts) != 2:
            continue
        status, path = parts
        # Acceptam stergerile (D) — sunt safe (curatare)
        if status[0] in ('A', 'M') and (path.startswith('data/') or path.startswith('temp/')):
            bad.append(path)
    return bad


def has_anything_staged() -> bool:
    res = run(['git', 'diff', '--cached', '--quiet'], check=False)
    return res.returncode != 0


def main():
    ap = argparse.ArgumentParser(description='Commit + push cu siguranta pentru dgpt')
    ap.add_argument('message', nargs='?', default='update', help='Mesaj de commit')
    args = ap.parse_args()

    # 1) Stage tot, apoi scoate data/ si temp/
    run(['git', 'add', '-A'])
    run(['git', 'reset', '-q', 'HEAD', 'data/', 'temp/'], check=False)

    # 2) Sanity check
    bad = check_protected_staged()
    if bad:
        print('EROARE: fisiere cu nume reale sunt staged:', file=sys.stderr)
        for p in bad:
            print(f'  {p}', file=sys.stderr)
        print('Anuleaza cu: git reset HEAD data/ temp/', file=sys.stderr)
        sys.exit(1)

    # 3) Daca nu sunt modificari, iesi curat
    if not has_anything_staged():
        print('Nimic de comis.')
        return

    # 4) Commit
    run(['git', 'commit', '-m', args.message])

    # 5) Push (upstream daca e nevoie)
    branch = run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture=True).stdout.strip()
    has_upstream = run(
        ['git', 'rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}'],
        check=False, capture=True
    ).returncode == 0
    if has_upstream:
        run(['git', 'push'])
    else:
        run(['git', 'push', '-u', 'origin', branch])

    print('Gata.')


if __name__ == '__main__':
    main()
