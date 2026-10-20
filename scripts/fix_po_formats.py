"""Fix broken python-format placeholders in German catalog and fill empties."""
from __future__ import annotations

import re
from pathlib import Path

import polib

PO_PATH = Path('locale/de/LC_MESSAGES/django.po')
NAMED = re.compile(r'%\(([^)]+)\)([a-zA-Z])')
POSITIONAL = re.compile(r'%(?:\d+\$)?([sdif])')


def placeholders(text: str) -> set[str]:
    named = {f'%({name}){spec}' for name, spec in NAMED.findall(text)}
    positional = {f'%{spec}' for spec in POSITIONAL.findall(text)}
    return named | positional


def main() -> None:
    po = polib.pofile(str(PO_PATH))
    fixed = 0
    filled = 0

    for entry in po:
        if not entry.msgid or entry.obsolete:
            continue

        if 'item shortlisted' in entry.msgid and not entry.msgstr.strip():
            # Preserve counter placeholder from msgid.
            ph = placeholders(entry.msgid)
            if '%(counter)s' in ph:
                entry.msgstr = (
                    '%(counter)s Eintrag auf der Shortlist – noch nichts ist bestätigt.'
                )
            else:
                entry.msgstr = entry.msgid
            filled += 1
            continue

        if not entry.msgstr:
            continue

        src = placeholders(entry.msgid)
        dst = placeholders(entry.msgstr)
        if src and src != dst:
            print('reset:', entry.msgid[:70].replace('\n', ' '))
            print('  src', src, 'dst', dst)
            print('  was', entry.msgstr[:70].replace('\n', ' '))
            entry.msgstr = entry.msgid
            fixed += 1

    po.save()
    print(f'Filled empties: {filled}; reset broken format strings: {fixed}')


if __name__ == '__main__':
    main()
