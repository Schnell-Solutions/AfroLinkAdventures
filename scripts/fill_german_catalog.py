"""Fill empty German msgstr entries: curated map first, then machine assist."""
from __future__ import annotations

import time
from pathlib import Path

import polib
from deep_translator import GoogleTranslator

PO_PATH = Path('locale/de/LC_MESSAGES/django.po')

# Prefer these over machine output for core UI.
CURATED: dict[str, str] = {
    'Primary navigation': 'Hauptnavigation',
    'Menu': 'Menü',
    'Close menu': 'Menü schließen',
    'Journeys': 'Reisen',
    'Destinations': 'Destinationen',
    'Destination links': 'Destinationen-Links',
    'All Destinations': 'Alle Destinationen',
    'Events': 'Events',
    'About Us': 'Über uns',
    'The Journal': 'Das Journal',
    'Language': 'Sprache',
    'Enquire': 'Anfragen',
    'Complete enquiry for your shortlist': 'Anfrage für Ihre Shortlist abschließen',
    'Start an enquiry or request a consultation': 'Anfrage starten oder Beratung anfordern',
    'Promotions': 'Angebote',
    'Dismiss this promotion': 'Dieses Angebot schließen',
    'Luxury golf, safari, and wellness journeys across Africa, crafted by AfroLink Adventures.': (
        'Luxuriöse Golf-, Safari- und Wellnessreisen durch Afrika – gestaltet von AfroLink Adventures.'
    ),
    'Special Offers': 'Sonderangebote',
    'Special offers': 'Sonderangebote',
    'Special offers only': 'Nur Sonderangebote',
    'All journeys': 'Alle Reisen',
    'Offers': 'Angebote',
    'Search': 'Suche',
    'Duration': 'Dauer',
    'Sort By': 'Sortieren nach',
    'Recommended': 'Empfohlen',
    'Apply': 'Anwenden',
    'Clear': 'Zurücksetzen',
    'Privacy': 'Datenschutz',
    'Terms': 'AGB',
    'Legal Notice': 'Impressum',
    'Legal': 'Rechtliches',
    'View Offer': 'Angebot ansehen',
    'View Offer →': 'Angebot ansehen →',
    'Explore Journey →': 'Reise entdecken →',
    'Back to journeys': 'Zurück zu den Reisen',
    'Featured': 'Empfohlen',
    'Days': 'Tage',
    'Pricing': 'Preise',
    'Included': 'Inbegriffen',
    'Not Included': 'Nicht inbegriffen',
    'Original price': 'Originalpreis',
    'Enquire about this journey': 'Diese Reise anfragen',
    'Private journey': 'Private Reise',
    'Length': 'Dauer',
    'Safari Focused': 'Safari-fokussiert',
    'Golf Focused': 'Golf-fokussiert',
    'Safari + Golf': 'Safari + Golf',
}


def translate_text(translator: GoogleTranslator, text: str) -> str:
    if not text.strip():
        return text
    # Keep brand names stable.
    protected = text.replace('AfroLink Adventures', '«BRAND»').replace(
        'AfroLink', '«BRAND_SHORT»'
    )
    try:
        result = translator.translate(protected)
    except Exception as exc:  # noqa: BLE001
        print(f'  skip ({exc}): {text[:60]!r}')
        return ''
    if not result:
        return ''
    return (
        result.replace('«BRAND»', 'AfroLink Adventures')
        .replace('«BRAND_SHORT»', 'AfroLink')
        .replace('« Brand »', 'AfroLink Adventures')
    )


def main() -> None:
    po = polib.pofile(str(PO_PATH))
    translator = GoogleTranslator(source='en', target='de')
    curated_n = 0
    machine_n = 0
    pending = []

    for entry in po:
        if not entry.msgid or entry.obsolete:
            continue
        if entry.msgstr:
            continue
        if entry.msgid in CURATED:
            entry.msgstr = CURATED[entry.msgid]
            curated_n += 1
        else:
            pending.append(entry)

    print(f'Curated fills: {curated_n}; machine pending: {len(pending)}')

    for index, entry in enumerate(pending, start=1):
        german = translate_text(translator, entry.msgid)
        if german:
            entry.msgstr = german
            machine_n += 1
        if index % 25 == 0:
            print(f'  … {index}/{len(pending)}')
            po.save()
            time.sleep(0.4)
        else:
            time.sleep(0.08)

    po.save()
    print(f'Done. Machine fills: {machine_n}. Saving {PO_PATH}')


if __name__ == '__main__':
    main()
