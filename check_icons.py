#!/usr/bin/env python3
"""
Audit every icon reference in index.html and data/*.json against the icons/ directory.

Exit code 1 if any referenced local icon file is missing → use in CI / before commit.

Usage:
    python3 check_icons.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(ROOT, 'icons')

# Files that contain icon references (HTML + JSON data sources).
SCAN_FILES = ['index.html', 'data/tools.json', 'data/models.json',
              'data/languages.json', 'data/databases.json', 'data/github.json']

# Match both JSON-style ("icon": "./icons/x.png") and JS-object style (icon: './icons/x.png')
ICON_RE = re.compile(r'"icon"\s*:\s*"\./icons/([^"]+)"|icon\s*:\s*\'\./icons/([^\'"]+)\'')


def collect_refs():
    """Return {filename: set(missing_icon_basenames)} for local ./icons refs."""
    broken = {}
    for rel in SCAN_FILES:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        missing = set()
        for m in ICON_RE.finditer(text):
            name = m.group(1) or m.group(2)
            if not name:
                continue
            if not os.path.exists(os.path.join(ICONS_DIR, name)):
                missing.add(name)
        if missing:
            broken[rel] = missing
    return broken


def main():
    broken = collect_refs()
    if not broken:
        print('✅ All icon references resolve to files in icons/.')
        return 0
    total = sum(len(v) for v in broken.values())
    print(f'❌ {total} broken icon reference(s) found:\n')
    for rel in sorted(broken):
        for name in sorted(broken[rel]):
            print(f'  {rel}: ./icons/{name}')
    print('\nFix: python3 download_icons.py  (or manually drop the logo into icons/)')
    return 1


if __name__ == '__main__':
    sys.exit(main())
