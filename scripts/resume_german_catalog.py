"""Resume filling empty German msgstr entries."""
from __future__ import annotations

import sys
import time
from pathlib import Path

import polib
from deep_translator import GoogleTranslator

PO_PATH = Path('locale/de/LC_MESSAGES/django.po')


def translate_text(translator: GoogleTranslator, text: str) -> str:
    protected = (
        text.replace('AfroLink Adventures', '«BRAND»')
        .replace('AfroLink', '«BRAND_SHORT»')
    )
    try:
        result = translator.translate(protected[:4500])
    except Exception as exc:  # noqa: BLE001
        print(f'  fail: {exc!s} :: {text[:70]!r}', flush=True)
        return ''
    if not result:
        return ''
    return (
        result.replace('«BRAND»', 'AfroLink Adventures')
        .replace('«BRAND_SHORT»', 'AfroLink')
    )


def main() -> None:
    po = polib.pofile(str(PO_PATH))
    translator = GoogleTranslator(source='en', target='de')
    pending = [
        e for e in po
        if e.msgid and not e.msgstr and not e.obsolete
    ]
    print(f'Resuming {len(pending)} empty strings', flush=True)
    done = 0
    for index, entry in enumerate(pending, start=1):
        german = translate_text(translator, entry.msgid)
        if german:
            entry.msgstr = german
            done += 1
        if index % 20 == 0:
            po.save()
            print(f'  saved {index}/{len(pending)} (ok {done})', flush=True)
            time.sleep(0.6)
        else:
            time.sleep(0.12)
    po.save()
    empty = sum(1 for e in po if e.msgid and not e.msgstr and not e.obsolete)
    print(f'Finished. Newly filled {done}. Remaining empty: {empty}', flush=True)


if __name__ == '__main__':
    main()
