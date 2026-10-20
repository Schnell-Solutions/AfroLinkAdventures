"""Apply German translations to locale/de/LC_MESSAGES/django.po."""
from __future__ import annotations

import re
from pathlib import Path

PO_PATH = Path('locale/de/LC_MESSAGES/django.po')

# High-quality German UI strings. Unlisted msgids keep English (still usable).
TRANSLATIONS: dict[str, str] = {
    # Nav / chrome
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
    'Site footer': 'Seitenfuß',
    'Explore': 'Entdecken',
    'Company': 'Unternehmen',
    'Contact': 'Kontakt',
    'Privacy': 'Datenschutz',
    'Terms': 'AGB',
    'Legal Notice': 'Impressum',
    'Legal': 'Rechtliches',
    'Request consultation': 'Beratung anfordern',
    'View Offer': 'Angebot ansehen',
    'Featured': 'Empfohlen',
    'Original price': 'Originalpreis',
    'Days': 'Tage',
    'Day Journey': 'Tage-Reise',
    'Back to journeys': 'Zurück zu den Reisen',
    'Full pricing in enquiry panel': 'Vollständige Preise im Anfragebereich',
    'Enquire about this journey': 'Diese Reise anfragen',
    'Private journey': 'Private Reise',
    'Enquire about this route and refine it with our team.': (
        'Fragen Sie diese Route an und verfeinern Sie sie mit unserem Team.'
    ),
    'Length': 'Dauer',
    'Pricing': 'Preise',
    'In the package': 'Im Paket',
    'Included': 'Inbegriffen',
    'Billed separately': 'Separat berechnet',
    'Not Included': 'Nicht inbegriffen',
    'Special Offers': 'Sonderangebote',
    'Limited-time promotional journeys with clear savings. Customize or extend any itinerary with the concierge team.': (
        'Zeitlich begrenzte Angebotsreisen mit klaren Ersparnissen. Passen Sie jede Route mit dem Concierge-Team an oder erweitern Sie sie.'
    ),
    'Special offers': 'Sonderangebote',
    'Journey Image': 'Reisebild',
    'View Offer →': 'Angebot ansehen →',
    'Explore Journey →': 'Reise entdecken →',
    'Featured Journeys': 'Empfohlene Reisen',
    'Featured journeys': 'Empfohlene Reisen',
    'Featured journeys are being prepared.': 'Empfohlene Reisen werden vorbereitet.',
    'Add active BasePackage records in the backend to feature live journeys here.': (
        'Fügen Sie aktive Reise-Pakete im Backend hinzu, um sie hier zu zeigen.'
    ),
    'View All Journeys →': 'Alle Reisen ansehen →',
    'Explore The Regions': 'Die Regionen entdecken',
    'Featured Event': 'Empfohlenes Event',
    'Every': 'Jeden',
    'View Featured Event →': 'Empfohlenes Event ansehen →',
    'Featured Event Image': 'Event-Bild',
    'Explore Signature Journeys': 'Signaturreisen entdecken',
    'The Afrolink Approach': 'Der AfroLink-Ansatz',
    'Expert-Led. Personally Curated. We reject generic, automated booking platforms and begin every journey with direct founder-led planning. From tee-sheet strategy and safari access windows to lodge pacing, transfers, and golf-bag handling, every movement is designed as one accountable system for a stress-free East African experience.': (
        'Expertengeführt. Persönlich kuratiert. Wir verzichten auf generische Buchungsplattformen und beginnen jede Reise mit direkter, founder-geführter Planung. Von Tee-Zeiten und Safari-Fenstern bis zu Lodge-Rhythmus, Transfers und Golfgepäck – jede Bewegung ist als ein verantwortliches System für ein stressfreies ostafrikanisches Erlebnis gedacht.'
    ),
    'The Vision': 'Die Vision',
    'Define your travel windows, golf handicap, and the specific wildlife encounters on your bucket list.': (
        'Definieren Sie Ihre Reisezeiten, Ihr Handicap und die Wildtier-Begegnungen auf Ihrer Wunschliste.'
    ),
    'Search': 'Suche',
    'Journey name or theme': 'Reisename oder Thema',
    'Duration': 'Dauer',
    'Up to 7 days': 'Bis 7 Tage',
    '8 - 12 days': '8–12 Tage',
    '13+ days': '13+ Tage',
    'Any length': 'Beliebige Länge',
    'Offers': 'Angebote',
    'Special offers only': 'Nur Sonderangebote',
    'All journeys': 'Alle Reisen',
    'Sort By': 'Sortieren nach',
    'Price: Low to High': 'Preis: aufsteigend',
    'Price: High to Low': 'Preis: absteigend',
    'Recommended': 'Empfohlen',
    'Apply': 'Anwenden',
    'Clear': 'Zurücksetzen',
    'Journey image': 'Reisebild',
    'No journeys match these filters.': 'Keine Reisen entsprechen diesen Filtern.',
    'Try clearing a filter or broadening your search.': (
        'Setzen Sie einen Filter zurück oder erweitern Sie die Suche.'
    ),
    'Privacy': 'Datenschutz',
    'Terms': 'AGB',
    'Legal Notice': 'Impressum',
    'How AfroLink Adventures collects, uses, and protects personal information shared through our website and enquiry process.': (
        'Wie AfroLink Adventures personenbezogene Daten erhebt, nutzt und schützt, die über unsere Website und den Anfrageprozess geteilt werden.'
    ),
    'This notice explains how AfroLink Adventures handles personal information when you browse our site, start a planner brief, or submit an enquiry for a private journey.': (
        'Dieser Hinweis erklärt, wie AfroLink Adventures personenbezogene Daten verarbeitet, wenn Sie unsere Website nutzen, eine Planungsanfrage starten oder eine Anfrage für eine private Reise absenden.'
    ),
    'Regions': 'Regionen',
    'Golf': 'Golf',
    'Safari': 'Safari',
    'Stays': 'Unterkünfte',
    'Wellness': 'Wellness',
    'All experiences': 'Alle Erlebnisse',
    'Filter': 'Filtern',
    'Read more': 'Weiterlesen',
    'Continue reading': 'Weiterlesen',
    'Related articles': 'Verwandte Artikel',
    'Share': 'Teilen',
    'Published': 'Veröffentlicht',
    'min read': 'Min. Lesezeit',
    'Back to journal': 'Zurück zum Journal',
    'Start planning': 'Planung starten',
    'Request a consultation': 'Beratung anfordern',
    'Your shortlist': 'Ihre Shortlist',
    'Continue': 'Weiter',
    'Submit enquiry': 'Anfrage senden',
    'Thank you': 'Vielen Dank',
    'We received your enquiry': 'Wir haben Ihre Anfrage erhalten',
    'Next steps': 'Nächste Schritte',
    'WhatsApp': 'WhatsApp',
    'Email': 'E-Mail',
    'Phone': 'Telefon',
    'Full name': 'Vollständiger Name',
    'Message': 'Nachricht',
    'Send': 'Senden',
    'Cancel': 'Abbrechen',
    'Add to shortlist': 'Zur Shortlist hinzufügen',
    'Remove': 'Entfernen',
    'View details': 'Details ansehen',
    'Learn more': 'Mehr erfahren',
    'See all': 'Alle ansehen',
    'Partners': 'Partner',
    'Featured Event': 'Empfohlenes Event',
    'Safari Focused': 'Safari-fokussiert',
    'Golf Focused': 'Golf-fokussiert',
    'Safari + Golf': 'Safari + Golf',
}


def unescape_po(value: str) -> str:
    return (
        value.replace(r'\\', '\0')
        .replace(r'\"', '"')
        .replace(r'\n', '\n')
        .replace(r'\t', '\t')
        .replace('\0', '\\')
    )


def escape_po(value: str) -> str:
    return (
        value.replace('\\', r'\\')
        .replace('"', r'\"')
        .replace('\n', r'\n')
        .replace('\t', r'\t')
    )


def parse_msgid_block(block: str) -> str | None:
    lines = []
    capturing = False
    for line in block.splitlines():
        if line.startswith('msgid '):
            capturing = True
            part = line[6:].strip()
            if part.startswith('"') and part.endswith('"'):
                lines.append(unescape_po(part[1:-1]))
            continue
        if capturing:
            if line.startswith('"') and line.endswith('"'):
                lines.append(unescape_po(line[1:-1]))
                continue
            break
    if not lines:
        return None
    return ''.join(lines)


def main() -> None:
    text = PO_PATH.read_text(encoding='utf-8')
    # Split on message boundaries while keeping msgstr empty pairs replaceable.
    pattern = re.compile(
        r'(msgid (?:"(?:\\.|[^"\\])*"\s*)+)\s*msgstr ""\s*(?=\n|$)',
        re.MULTILINE,
    )

    translated = 0
    missing_samples: list[str] = []

    def repl(match: re.Match[str]) -> str:
        nonlocal translated
        msgid_block = match.group(1)
        msgid = parse_msgid_block(msgid_block)
        if not msgid:
            return match.group(0)
        german = TRANSLATIONS.get(msgid)
        if not german:
            if len(missing_samples) < 40 and msgid not in missing_samples:
                missing_samples.append(msgid)
            return match.group(0)
        translated += 1
        if '\n' in german or len(german) > 70:
            # multiline msgstr
            parts = german.split('\n')
            body = '\n'.join(f'"{escape_po(part)}"' for part in parts)
            return f'{msgid_block}msgstr ""\n{body}\n'
        return f'{msgid_block}msgstr "{escape_po(german)}"\n'

    new_text = pattern.sub(repl, text)
    PO_PATH.write_text(new_text, encoding='utf-8')
    print(f'Translated {translated} strings')
    print(f'Sample untranslated ({len(missing_samples)}):')
    for item in missing_samples[:25]:
        preview = item.replace('\n', ' ')[:90]
        print(f'  - {preview}')


if __name__ == '__main__':
    main()
