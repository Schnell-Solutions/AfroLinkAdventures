from django.db import migrations


ARTICLES = [
    {
        'title_en': 'Why East African golf journeys should be designed from the transfer map backwards.',
        'title_de': 'Warum ostafrikanische Golfreisen vom Transferplan rueckwaerts gedacht werden sollten.',
        'slug': 'design-east-african-golf-journeys-backwards',
        'category_en': 'Founder Notes / Golf & Safari Routing',
        'category_de': 'Founder Notes / Golf- & Safari-Routing',
        'excerpt_en': (
            'The strongest routes are rarely built by stacking attractions. They are designed around '
            'altitude, road time, tee sheet pressure, game-drive windows, and recovery.'
        ),
        'excerpt_de': (
            'Die staerksten Routen entstehen selten durch das Stapeln von Attraktionen. Sie werden um '
            'Hoehe, Fahrzeiten, Tee-Time-Druck, Safari-Fenster und Erholung gebaut.'
        ),
        'body_en': (
            'A luxury journey fails when its logic is decorative rather than operational. In East Africa, '
            'the best itinerary is designed from the transfer map backwards: where the body needs rest, '
            'where the roads steal time, when the tee sheet is strongest, and which wildlife windows are '
            'worth protecting. This is why AfroLink treats routing as the first act of hospitality. Golf, '
            'safari, lodge pacing, and wellness recovery only feel effortless when the invisible movement '
            'between them has been engineered first.'
        ),
        'body_de': (
            'Eine Luxusreise scheitert, wenn ihre Logik dekorativ statt operativ ist. In Ostafrika entsteht '
            'die beste Route vom Transferplan rueckwaerts: wo der Koerper Ruhe braucht, wo Strassen Zeit '
            'kosten, wann Tee Times am staerksten sind und welche Safari-Fenster geschuetzt werden sollten.'
        ),
        'hero_image_url': 'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1400&q=80',
        'published_at': '2026-07-15',
        'is_featured': True,
    },
    {
        'title_en': 'Why private access matters more than simply adding more parks.',
        'title_de': 'Warum privater Zugang wichtiger ist als einfach mehr Parks hinzuzufuegen.',
        'slug': 'private-access-more-than-more-parks',
        'category_en': 'Safari Timing',
        'category_de': 'Safari Timing',
        'excerpt_en': (
            'A stronger safari day depends on guide quality, concession access, seasonal movement, and '
            'avoiding crowded routing wherever possible.'
        ),
        'excerpt_de': (
            'Ein staerkerer Safaritag haengt von Guide-Qualitaet, Concession-Zugang, saisonaler Bewegung '
            'und dem Vermeiden ueberfuellter Routen ab.'
        ),
        'body_en': (
            'More parks do not automatically create a better safari. In a premium itinerary, less can often '
            'mean more: fewer transfers, better guides, stronger concession access, and enough time in the '
            'field to let animal movement reveal itself. Private access protects silence, timing, and guide '
            'decision-making. It also helps a golf-and-safari itinerary avoid the common mistake of exhausting '
            'guests in pursuit of quantity.'
        ),
        'body_de': (
            'Mehr Parks erzeugen nicht automatisch eine bessere Safari. In einer Premium-Reise bedeutet weniger '
            'oft mehr: weniger Transfers, bessere Guides, staerkerer Zugang und ausreichend Zeit im Feld.'
        ),
        'hero_image_url': 'https://images.unsplash.com/photo-1516426122078-c23e76319801?auto=format&fit=crop&w=1400&q=80',
        'published_at': '2026-07-10',
        'is_featured': False,
    },
    {
        'title_en': 'The role of a stay is not decoration. It is recovery infrastructure.',
        'title_de': 'Die Rolle einer Unterkunft ist nicht Dekoration. Sie ist Erholungsinfrastruktur.',
        'slug': 'accommodation-as-recovery-infrastructure',
        'category_en': 'Lodge Selection',
        'category_de': 'Lodge Selection',
        'excerpt_en': (
            'The right accommodation anchor protects rest, transfer logic, privacy, and the emotional rhythm '
            'of the entire journey.'
        ),
        'excerpt_de': (
            'Die richtige Unterkunft schuetzt Ruhe, Transferlogik, Privatsphaere und den emotionalen Rhythmus '
            'der gesamten Reise.'
        ),
        'body_en': (
            'A lodge is not simply where a guest sleeps. It is the recovery infrastructure of the route. The '
            'best property protects privacy, shortens critical transfers, supports early departures, and '
            'restores the guest after demanding golf or safari days. When accommodation is selected only for '
            'visual appeal, the journey begins to leak energy. When selected for purpose, the whole route '
            'becomes calmer.'
        ),
        'body_de': (
            'Eine Lodge ist nicht nur der Ort, an dem ein Gast schlaeft. Sie ist die Erholungsinfrastruktur '
            'der Route und schuetzt Privatsphaere, Transferlogik und den Rhythmus der Reise.'
        ),
        'hero_image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1400&q=80',
        'published_at': '2026-07-05',
        'is_featured': False,
    },
]


def populate_articles(apps, schema_editor):
    journal_article = apps.get_model('destination_cms', 'JournalArticle')
    slugs = [article['slug'] for article in ARTICLES]
    journal_article.objects.filter(slug__in=slugs).delete()
    journal_article.objects.bulk_create(
        journal_article(**article) for article in ARTICLES
    )


def clear_articles(apps, schema_editor):
    journal_article = apps.get_model('destination_cms', 'JournalArticle')
    slugs = [article['slug'] for article in ARTICLES]
    journal_article.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('destination_cms', '0009_journalarticle'),
    ]

    operations = [
        migrations.RunPython(populate_articles, clear_articles),
    ]
