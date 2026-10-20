from datetime import date, time

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from destination_cms.models import (
    Accommodation,
    BasePackage,
    DayActivity,
    ExperienceFAQ,
    ExperienceOfferItem,
    GalleryImage,
    GolfCourse,
    GolfEvent,
    JournalArticle,
    PackageItineraryDay,
    PackagePricingSeason,
    Region,
    RelatedExperience,
    SafariDestination,
    WellnessExperience,
)

from .luxury_seed_catalog import (
    ACCOMMODATIONS,
    GOLF_COURSES,
    SAFARI_DESTINATIONS,
    WELLNESS,
    IMG,
    GALLERIES,
    FAQS,
    OFFERS,
    RELATED,
    ACCOMMODATION_NAMES,
    SAFARI_NAMES,
    WELLNESS_NAMES,
    COURSE_SLUGS,
)
from .journal_seed_catalog import JOURNAL_ARTICLES, JOURNAL_SLUGS


REGION_SLUGS = [
    'nairobi-environs',
    'great-rift-valley',
    'mount-kenya-region',
    'coastal-strip',
]

PACKAGE_SLUGS = [
    'executive-equator-wilderness-challenge',
    'ultimate-odyssey',
    'nairobi-championship-golf-week',
    'kenya-grand-golf-circuit',
]

EVENT_SLUGS = [
    'tuesday-nairobi-members-guest-round',
    'vipingo-ridge-coastal-invitational',
    'great-rift-valley-twilight-members-evening',
]


class Command(BaseCommand):
    help = 'Seed Kenyan destination CMS and itinerary data for local production testing.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Seeding destination CMS data...'))

        with transaction.atomic():
            self.flush_seed_records()
            regions = self.create_regions()
            self.create_region_gallery_images(regions)
            accommodations = self.create_accommodations(regions)
            courses = self.create_golf_courses(regions)
            safaris = self.create_safari_destinations(regions)
            wellness = self.create_wellness_experiences(regions)
            self.create_gallery_images(courses, safaris, accommodations, wellness)
            self.enrich_experience_decision_content(
                courses, safaris, accommodations, wellness
            )
            self.create_journal_articles()
            self.create_golf_events(regions, courses)
            self.create_packages(courses, safaris, wellness, accommodations)

        self.stdout.write(self.style.SUCCESS('Destination seed data loaded successfully.'))
        self.stdout.write(self.style.SUCCESS(
            'Created 4 regions, 6 accommodations, 6 golf courses, 7 safari destinations, '
            '6 wellness experiences, 2 golf events, and 4 signature packages.'
        ))

    def flush_seed_records(self):
        self.stdout.write('Flushing existing matching seed records...')

        deleted_events, _ = GolfEvent.objects.filter(slug__in=EVENT_SLUGS).delete()
        deleted_packages, _ = BasePackage.objects.filter(slug__in=PACKAGE_SLUGS).delete()

        # Match seed regions up front so any leftover experiences from a prior
        # seed run (even ones created under since-renamed names/slugs) are
        # cleaned up before we try to delete the regions themselves.
        region_ids = list(Region.objects.filter(slug__in=REGION_SLUGS).values_list('pk', flat=True))

        deleted_accommodations, _ = Accommodation.objects.filter(
            Q(name__in=ACCOMMODATION_NAMES) | Q(region_id__in=region_ids)
        ).delete()
        deleted_courses, _ = GolfCourse.objects.filter(
            Q(slug__in=COURSE_SLUGS) | Q(region_id__in=region_ids)
        ).delete()
        deleted_safaris, _ = SafariDestination.objects.filter(
            Q(name__in=SAFARI_NAMES) | Q(region_id__in=region_ids)
        ).delete()
        deleted_wellness, _ = WellnessExperience.objects.filter(
            Q(name_en__in=WELLNESS_NAMES) | Q(region_id__in=region_ids)
        ).delete()
        deleted_articles, _ = JournalArticle.objects.filter(slug__in=JOURNAL_SLUGS).delete()
        deleted_regions, _ = Region.objects.filter(pk__in=region_ids).delete()

        self.stdout.write(
            f'Flushed events={deleted_events}, packages={deleted_packages}, accommodations={deleted_accommodations}, '
            f'golf_courses={deleted_courses}, safaris={deleted_safaris}, '
            f'wellness={deleted_wellness}, articles={deleted_articles}, '
            f'regions={deleted_regions}.'
        )

    def create_regions(self):
        self.stdout.write('Creating Kenyan regional hubs...')

        region_payloads = [
            {
                'key': 'nairobi',
                'name_en': 'Nairobi & Environs',
                'name_de': 'Nairobi & Umgebung',
                'country_en': 'Kenya',
                'country_de': 'Kenia',
                'slug': 'nairobi-environs',
                'description_en': (
                    'Kenya\'s capital corridor gives executive travelers the rare ability to combine '
                    'classic parkland golf, colonial garden estates, private Nairobi dining, and a '
                    'true wildlife drive inside the only national park bordering a major world city.'
                ),
                'description_de': (
                    'Der Grossraum Nairobi verbindet klassisches Parkland-Golf, elegante Garden '
                    'Estates, diskrete Stadthotellerie und echte Wildbeobachtung im einzigen '
                    'Nationalpark direkt an einer internationalen Metropole.'
                ),
                'meta_title': 'Nairobi Golf, Safari & Wellness Hub | AfroLink Adventures',
                'meta_description': (
                    'Explore Karen, Muthaiga, Windsor, Nairobi National Park, and private Blixen-style '
                    'wellness experiences from Kenya\'s capital base.'
                ),
            },
            {
                'key': 'rift',
                'name_en': 'The Great Rift Valley',
                'name_de': 'Das Grosse Rift Valley',
                'country_en': 'Kenya',
                'country_de': 'Kenia',
                'slug': 'great-rift-valley',
                'description_en': (
                    'A high-drama escarpment landscape where elevated fairways, Lake Naivasha hippo '
                    'waters, volcanic geology, and open walking safari terrain create the strongest '
                    'golf-and-wilderness contrast in the Kenyan circuit.'
                ),
                'description_de': (
                    'Eine dramatische Grabenbruchlandschaft mit erhoehten Fairways, den Hippo-Gewaessern '
                    'des Lake Naivasha, vulkanischer Geologie und offenen Walking-Safari Flaechen.'
                ),
                'meta_title': 'Great Rift Valley Golf & Safari Extensions | AfroLink Adventures',
                'meta_description': (
                    'Plan elevated golf at Great Rift Valley Lodge with Lake Naivasha hippo safaris, '
                    'Crescent Island walks, and volcanic mud recovery rituals.'
                ),
            },
            {
                'key': 'mount_kenya',
                'name_en': 'The Mount Kenya Region',
                'name_de': 'Die Mount-Kenya-Region',
                'country_en': 'Kenya',
                'country_de': 'Kenia',
                'slug': 'mount-kenya-region',
                'description_en': (
                    'A cool high-altitude zone anchored by equator-line golf, alpine air, equine trails, '
                    'and direct access to Ol Pejeta\'s rhino, predator, and private conservancy network.'
                ),
                'description_de': (
                    'Eine kuehle Hoehenregion mit Golf an der Aequatorlinie, alpiner Luft, Reitpfaden '
                    'und direkter Anbindung an Ol Pejetas Nashorn- und Raubkatzen-Schutzgebiet.'
                ),
                'meta_title': 'Mount Kenya Golf, Ol Pejeta & Alpine Wellness | AfroLink Adventures',
                'meta_description': (
                    'Connect Fairmont Mount Kenya Safari Club golf with equine mountain treks and '
                    'Ol Pejeta Conservancy wildlife access.'
                ),
            },
            {
                'key': 'coast',
                'name_en': 'The Coastal Strip',
                'name_de': 'Der Kuestenstreifen',
                'country_en': 'Kenya',
                'country_de': 'Kenia',
                'slug': 'coastal-strip',
                'description_en': (
                    'Kenya\'s Indian Ocean edge pairs Baobab Course shot-making, monsoon-softened coastal '
                    'light, reef conservation walks, and strategic onward access to Tsavo East and West.'
                ),
                'description_de': (
                    'Kenias Indischer-Ozean-Kueste kombiniert das Shot-Making des Baobab Course, '
                    'weiches Kuestenlicht, Riffschutz-Spaziergaenge und die Weiterreise nach Tsavo East und West.'
                ),
                'meta_title': 'Kenya Coast Golf, Reef Conservation & Tsavo Safari | AfroLink Adventures',
                'meta_description': (
                    'Discover Vipingo Ridge, Kuruwitu coral reef restoration, and Tsavo East/West safari '
                    'extensions on Kenya\'s coastal strip.'
                ),
            },
        ]

        regions = {}
        for payload in region_payloads:
            key = payload.pop('key')
            regions[key] = Region.objects.create(**payload)

        self.stdout.write(self.style.SUCCESS('Regions created.'))
        return regions

    def create_region_gallery_images(self, regions):
        self.stdout.write('Creating backend gallery images for regional hubs...')

        gallery_payloads = [
            (regions['nairobi'], 'https://images.unsplash.com/photo-1489392191049-fc10c97e64b6?auto=format&fit=crop&w=1400&q=80', 'Nairobi access, private city pacing, and parkland golf corridors.', 'Nairobi-Zugang, privates Stadttempo und Parkland-Golfkorridore.'),
            (regions['nairobi'], 'https://images.unsplash.com/photo-1516426122078-c23e76319801?auto=format&fit=crop&w=1400&q=80', 'Wildlife viewing within reach of Karen, Muthaiga, and Windsor.', 'Wildbeobachtung in Reichweite von Karen, Muthaiga und Windsor.'),
            (regions['rift'], 'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1400&q=80', 'Escarpment light, lake safaris, and elevated golf routing.', 'Escarpment-Licht, Seesafaris und erhoehtes Golf-Routing.'),
            (regions['mount_kenya'], 'https://images.unsplash.com/photo-1526481280693-3bfa7568e0f3?auto=format&fit=crop&w=1400&q=80', 'Highland air, equator golf, and conservancy access.', 'Highland-Luft, Aequatorgolf und Conservancy-Zugang.'),
            (regions['coast'], 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1400&q=80', 'Indian Ocean recovery, Baobab Course routing, and reef walks.', 'Indischer-Ozean-Erholung, Baobab-Course-Routing und Riffspaziergaenge.'),
        ]

        image_records = []
        for display_order, (region, image_url, caption_en, caption_de) in enumerate(gallery_payloads, start=1):
            image_records.append(
                GalleryImage(
                    content_type=ContentType.objects.get_for_model(region),
                    object_id=region.pk,
                    image_url=image_url,
                    caption_en=caption_en,
                    caption_de=caption_de,
                    display_order=display_order,
                )
            )

        GalleryImage.objects.bulk_create(image_records)
        self.stdout.write(self.style.SUCCESS('Regional gallery images created.'))

    def create_accommodations(self, regions):
        self.stdout.write('Creating associated accommodation anchors...')

        accommodations = {}
        for entry in ACCOMMODATIONS:
            payload = dict(entry)
            key = payload.pop('key')
            region_key = payload.pop('region_key')
            payload['region'] = regions[region_key]
            accommodations[key] = Accommodation.objects.create(**payload)

        self.stdout.write(self.style.SUCCESS('Accommodation anchors created.'))
        return accommodations

    def create_golf_courses(self, regions):
        self.stdout.write('Creating championship golf course profiles...')

        courses = {}
        for entry in GOLF_COURSES:
            payload = dict(entry)
            key = payload.pop('key')
            region_key = payload.pop('region_key')
            payload['region'] = regions[region_key]
            courses[key] = GolfCourse.objects.create(**payload)

        self.stdout.write(self.style.SUCCESS('Golf course profiles created.'))
        return courses

    def create_safari_destinations(self, regions):
        self.stdout.write('Creating safari destination records...')

        safaris = {}
        for entry in SAFARI_DESTINATIONS:
            payload = dict(entry)
            key = payload.pop('key')
            region_key = payload.pop('region_key')
            payload['region'] = regions[region_key]
            safaris[key] = SafariDestination.objects.create(**payload)

        self.stdout.write(self.style.SUCCESS('Safari destinations created.'))
        return safaris

    def create_gallery_images(self, courses, safaris, accommodations, wellness):
        self.stdout.write(
            'Creating backend gallery images for stay, course, safari, and wellness detail pages...'
        )

        type_map = {
            'stay': accommodations,
            'course': courses,
            'safari': safaris,
            'wellness': wellness,
        }

        image_records = []
        for type_key, objects in type_map.items():
            for key, obj in objects.items():
                ct = ContentType.objects.get_for_model(obj)
                gallery_entries = GALLERIES.get(type_key, {}).get(key, [])
                for display_order, (image_url, caption_en, caption_de) in enumerate(
                    gallery_entries, start=1
                ):
                    image_records.append(
                        GalleryImage(
                            content_type=ct,
                            object_id=obj.pk,
                            image_url=image_url,
                            caption_en=caption_en,
                            caption_de=caption_de,
                            display_order=display_order,
                        )
                    )

        GalleryImage.objects.bulk_create(image_records)
        self.stdout.write(self.style.SUCCESS('Gallery images created.'))

    def enrich_experience_decision_content(
        self, courses, safaris, accommodations, wellness
    ):
        self.stdout.write('Creating FAQs, offers, and related experience links...')

        type_map = {
            'stay': accommodations,
            'course': courses,
            'safari': safaris,
            'wellness': wellness,
        }

        def add_offers(obj, offer_payload):
            ct = ContentType.objects.get_for_model(obj)
            for order, label in enumerate(offer_payload.get('included', []), start=1):
                ExperienceOfferItem.objects.create(
                    content_type=ct,
                    object_id=obj.pk,
                    kind=ExperienceOfferItem.Kind.INCLUDED,
                    label=label,
                    display_order=order,
                )
            for order, label in enumerate(offer_payload.get('optional', []), start=1):
                ExperienceOfferItem.objects.create(
                    content_type=ct,
                    object_id=obj.pk,
                    kind=ExperienceOfferItem.Kind.OPTIONAL,
                    label=label,
                    display_order=order,
                )

        def add_faqs(obj, pairs):
            ct = ContentType.objects.get_for_model(obj)
            for order, (question, answer) in enumerate(pairs, start=1):
                ExperienceFAQ.objects.create(
                    content_type=ct,
                    object_id=obj.pk,
                    question=question,
                    answer=answer,
                    display_order=order,
                )

        for type_key, objects in type_map.items():
            for key, obj in objects.items():
                offer_payload = OFFERS.get(type_key, {}).get(key)
                if offer_payload:
                    add_offers(obj, offer_payload)

                faq_pairs = FAQS.get(type_key, {}).get(key)
                if faq_pairs:
                    add_faqs(obj, faq_pairs)

        for from_type, from_key, to_type, to_key, label, order in RELATED:
            from_obj = type_map[from_type][from_key]
            to_obj = type_map[to_type][to_key]
            RelatedExperience.objects.create(
                from_content_type=ContentType.objects.get_for_model(from_obj),
                from_object_id=from_obj.pk,
                to_content_type=ContentType.objects.get_for_model(to_obj),
                to_object_id=to_obj.pk,
                label=label,
                display_order=order,
            )

        self.stdout.write(self.style.SUCCESS('Experience decision content enriched.'))

    def create_journal_articles(self):
        self.stdout.write('Creating journal editorial articles...')

        created = {}
        for entry in JOURNAL_ARTICLES:
            payload = dict(entry)
            related_slugs = payload.pop('related_slugs', [])
            article = JournalArticle(**payload)
            article.save()
            created[article.slug] = (article, related_slugs)

        for article, related_slugs in created.values():
            related = [
                created[slug][0]
                for slug in related_slugs
                if slug in created and slug != article.slug
            ]
            if related:
                article.related_articles.set(related)

        self.stdout.write(
            self.style.SUCCESS(f'Journal articles created ({len(created)}).')
        )

    def create_wellness_experiences(self, regions):
        self.stdout.write('Creating wellness experience records...')

        wellness = {}
        for entry in WELLNESS:
            payload = dict(entry)
            key = payload.pop('key')
            region_key = payload.pop('region_key')
            payload['region'] = regions[region_key]
            wellness[key] = WellnessExperience.objects.create(**payload)

        self.stdout.write(self.style.SUCCESS('Wellness experiences created.'))
        return wellness

    def create_golf_events(self, regions, courses):
        self.stdout.write('Creating upcoming golf events...')

        events = [
            GolfEvent(
                title_en='Tuesday Nairobi Members Guest Round',
                title_de='Dienstag Nairobi Members Guest Round',
                slug='tuesday-nairobi-members-guest-round',
                region=regions['nairobi'],
                golf_course=courses['muthaiga'],
                summary_en=(
                    'A recurring Tuesday golf day for visitors who want a structured club experience '
                    'while staying close to Nairobi routing.'
                ),
                summary_de=(
                    'Ein wiederkehrender Dienstag-Golftag fuer Gaeste, die ein strukturiertes '
                    'Club-Erlebnis nahe der Nairobi-Route wuenschen.'
                ),
                description_en=(
                    'This members-guest format is designed for travelers who want authentic Nairobi club '
                    'golf without forcing a full tournament week into the itinerary.\n\n'
                    'The day typically opens with a composed morning round, followed by clubhouse recovery '
                    'and enough afternoon flexibility to keep dinner, transfers, or a light wellness session '
                    'on schedule. AfroLink uses this event as an anchor when guests need one strong highland '
                    'round inside a wider golf-and-safari route.'
                ),
                format_label='Members Guest Day',
                duration_label='Morning round · about 5 hours',
                dress_code='Club-appropriate golf attire; soft spikes preferred',
                eligibility_notes=(
                    'Guest play is arranged through the hosting member or concierge introduction. '
                    'A current handicap certificate is recommended.'
                ),
                inclusions=(
                    'Green fee coordination\n'
                    'Shared cart where available\n'
                    'Clubhouse lunch option on request\n'
                    'Transfer timing advice around the round'
                ),
                need_to_know=(
                    'Arrive at least 45 minutes before the first tee time\n'
                    'Confirm caddie or cart preference in advance\n'
                    'Keep the afternoon light if a safari departure follows the next morning'
                ),
                venue_notes=(
                    'Meet at the Muthaiga clubhouse reception. Private transfers from Karen, Muthaiga, '
                    'or selected Nairobi hotels can be arranged with the AfroLink team.'
                ),
                event_date=date(2026, 8, 4),
                start_time=time(9, 0),
                recurrence=GolfEvent.Recurrence.WEEKLY,
                recurrence_weekday=GolfEvent.Weekday.TUESDAY,
                accepts_inquiries=True,
                image_url='https://images.unsplash.com/photo-1535131749006-b7f58c99034b?auto=format&fit=crop&w=1600&q=80',
                meta_title='Tuesday Nairobi Members Guest Round | AfroLink Events',
                meta_description=(
                    'Recurring Tuesday members-guest golf at Muthaiga for visitors planning '
                    'Nairobi highland rounds inside a private Kenya itinerary.'
                ),
            ),
            GolfEvent(
                title_en='Vipingo Ridge Coastal Invitational',
                title_de='Vipingo Ridge Coastal Invitational',
                slug='vipingo-ridge-coastal-invitational',
                region=regions['coast'],
                golf_course=courses['vipingo'],
                summary_en=(
                    'A coastal invitational pairing Indian Ocean golf with private post-round recovery '
                    'and lodge routing along Kenya’s shore.'
                ),
                summary_de=(
                    'Ein kuestenorientiertes Invitational mit Indian-Ocean-Golf, privater Erholung '
                    'nach der Runde und Lodge-Routing.'
                ),
                description_en=(
                    'The Vipingo Ridge Coastal Invitational is built for guests who want championship-feeling '
                    'coastal golf without losing the calm of a private journey.\n\n'
                    'Expect ocean-influenced wind, an early start, and a day paced for serious play followed by '
                    'recovery rather than another long transfer. AfroLink sequences this event as either a polished '
                    'coastal opening or a composed finale after highland golf and inland safari.'
                ),
                format_label='Coastal Invitational',
                duration_label='Full golf day · tee to clubhouse recovery',
                dress_code='Tournament-ready golf attire; soft spikes required',
                eligibility_notes=(
                    'Invitation or concierge-arranged entry. Confirmed handicap and passport details '
                    'required for guest registration.'
                ),
                inclusions=(
                    'Event registration coordination\n'
                    'Practice-area access where available\n'
                    'On-course staging notes\n'
                    'Post-round recovery recommendations\n'
                    'Lodge and transfer sequencing around the event'
                ),
                need_to_know=(
                    'Plan arrival on the coast at least one night before competition day\n'
                    'Hydration and morning tee times matter in coastal humidity\n'
                    'Do not schedule a long safari transfer the same evening'
                ),
                venue_notes=(
                    'Vipingo Ridge clubhouse is the primary meeting point. Private transfers from selected '
                    'coastal lodges and Mombasa-area arrivals can be arranged.'
                ),
                event_date=date(2026, 9, 18),
                start_time=time(8, 30),
                accepts_inquiries=True,
                is_promoted=True,
                promotion_priority=10,
                image_url='https://images.unsplash.com/photo-1592919505780-303950717480?auto=format&fit=crop&w=1600&q=80',
                meta_title='Vipingo Ridge Coastal Invitational | AfroLink Events',
                meta_description=(
                    'Coastal invitational golf at Vipingo Ridge with private recovery and Kenya lodge routing '
                    'coordinated by AfroLink Adventures.'
                ),
            ),
            GolfEvent(
                title_en='Great Rift Valley Twilight Members Evening',
                title_de='Great Rift Valley Twilight Members Evening',
                slug='great-rift-valley-twilight-members-evening',
                region=regions['rift'],
                golf_course=courses['great_rift'],
                summary_en=(
                    'An elevated evening golf format overlooking the Rift — ideal when guests want one '
                    'signature highland round with sunset atmosphere.'
                ),
                summary_de=(
                    'Ein gehobenes Abend-Golf-Format mit Blick auf den Rift — ideal fuer eine '
                    'signaturhafte Hochland-Runde mit Sonnenuntergang.'
                ),
                description_en=(
                    'This twilight members evening is for guests who want the drama of Rift Valley golf '
                    'without committing to a full multi-day tournament block.\n\n'
                    'The round is timed for softer light and cooler air, then closes with clubhouse dining. '
                    'It works especially well between Nairobi arrival and a following safari departure, '
                    'provided transfers are protected.'
                ),
                format_label='Twilight Members Evening',
                duration_label='Late afternoon round · dinner optional',
                dress_code='Smart golf attire; layers recommended for evening cool',
                eligibility_notes=(
                    'Guest slots are limited and arranged through the club or AfroLink concierge. '
                    'Prior golf experience on parkland or highland courses is helpful.'
                ),
                inclusions=(
                    'Tee-time coordination\n'
                    'Course orientation notes\n'
                    'Optional clubhouse dinner reservation\n'
                    'Transfer window planning'
                ),
                need_to_know=(
                    'Carry a light layer for temperature drop after sunset\n'
                    'Confirm dinner plans before the round if staying on property\n'
                    'Avoid same-evening long-distance road transfers'
                ),
                venue_notes=(
                    'Meet at the Great Rift Valley clubhouse. Private transfers from Nairobi or nearby '
                    'highland stays should be timed to the first tee, not to an optimistic traffic estimate.'
                ),
                event_date=date(2026, 10, 9),
                start_time=time(15, 30),
                accepts_inquiries=True,
                image_url='https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?auto=format&fit=crop&w=1600&q=80',
                meta_title='Great Rift Valley Twilight Members Evening | AfroLink Events',
                meta_description=(
                    'Twilight members golf overlooking Kenya’s Great Rift Valley, sequenced for private '
                    'highland itineraries by AfroLink Adventures.'
                ),
            ),
        ]

        GolfEvent.objects.bulk_create(events)
        self.stdout.write(self.style.SUCCESS('Golf events created.'))
        return events

    def create_packages(self, courses, safaris, wellness, accommodations):
        self.stdout.write('Creating signature package itineraries and seasonal pricing...')

        executive = BasePackage.objects.create(
            title_en='10-Day Highlands Golf & Safari Circuit',
            title_de='10 Tage Highlands Golf & Safari Circuit',
            summary_en=(
                'Five distinctive rounds across Nairobi, the Rift Valley, Mount Kenya, and the coast, '
                'balanced with two carefully timed wildlife days and private recovery between regions.'
            ),
            summary_de=(
                'Fuenf charaktervolle Golfrunden in Nairobi, im Rift Valley, am Mount Kenya und an der '
                'Kueste, kombiniert mit zwei gezielt geplanten Wildlife-Tagen und privater Erholung.'
            ),
            inclusions_en=(
                'Private airport meet-and-assist on arrival and departure\n'
                'All accommodation listed in the itinerary, subject to availability\n'
                'Daily breakfast and selected hosted dining experiences\n'
                'Pre-arranged tee times, green fees, and golf cart coordination where available\n'
                'Private road transfers between listed regions and experiences\n'
                'Safari park entry fees and professional guiding for listed safari activities\n'
                'Concierge itinerary design, local coordination, and WhatsApp support during travel'
            ),
            inclusions_de=(
                'Private Flughafenbetreuung bei Ankunft und Abreise\n'
                'Alle im Reiseverlauf genannten Unterkuenfte, vorbehaltlich Verfuegbarkeit\n'
                'Taegliches Fruehstueck und ausgewaehlte begleitete Dinner-Erlebnisse\n'
                'Vorab koordinierte Tee Times, Greenfees und Golfcart-Abstimmung wo verfuegbar\n'
                'Private Strassentransfers zwischen den genannten Regionen und Erlebnissen\n'
                'Safari-Parkgebuehren und professionelle Fuehrung fuer gelistete Safari-Aktivitaeten\n'
                'Concierge-Routenplanung, lokale Koordination und WhatsApp-Support waehrend der Reise'
            ),
            exclusions_en=(
                'International flights and visas\n'
                'Travel insurance, medical cover, and evacuation insurance\n'
                'Premium alcohol, cellar selections, and personal minibar charges\n'
                'Caddie gratuities, guide gratuities, and discretionary staff tips\n'
                'Optional helicopter, charter flight, or private aircraft upgrades\n'
                'Items of a personal nature, laundry, and excess baggage handling'
            ),
            exclusions_de=(
                'Internationale Fluege und Visa\n'
                'Reiseversicherung, medizinische Absicherung und Evakuierungsversicherung\n'
                'Premium-Alkohol, Weinauswahl und persoenliche Minibar-Kosten\n'
                'Caddie-Trinkgelder, Guide-Trinkgelder und freiwillige Staff Tips\n'
                'Optionale Helikopter-, Charterflug- oder Privatflugzeug-Upgrades\n'
                'Persoenliche Ausgaben, Waescherei und Handling von Uebergepaeck'
            ),
            duration_days=10,
            slug='executive-equator-wilderness-challenge',
            card_image_url=IMG['golf'][0],
            hero_image_url=IMG['golf'][1],
        )
        self.create_pricing(
            executive,
            peak_price=12850,
            green_price=10450,
        )
        self.create_itinerary_days(
            executive,
            [
                ('Private Nairobi arrival and golf-trip briefing in Karen', 'Private Ankunft in Nairobi und Golf-Reisebriefing in Karen', accommodations['hemingways'], [wellness['blixen_tea']]),
                ('Karen Country Club opening round and guided course review', 'Auftaktrunde im Karen Country Club und gefuehrte Course Review', accommodations['hemingways'], [courses['karen']]),
                ('Muthaiga Golf Club championship round', 'Championship-Runde im Muthaiga Golf Club', accommodations['hemingways'], [courses['muthaiga']]),
                ('Nairobi National Park morning drive and unhurried recovery', 'Morgendlicher Nairobi National Park Drive und ruhige Erholung', accommodations['hemingways'], [safaris['nairobi_np'], wellness['blixen_tea']]),
                ('Great Rift Valley escarpment round above Lake Naivasha', 'Great-Rift-Valley-Runde oberhalb des Lake Naivasha', accommodations['loldia'], [courses['great_rift']]),
                ('Lake Naivasha boat safari and Crescent Island walk', 'Lake-Naivasha-Bootssafari und Crescent-Island-Wanderung', accommodations['loldia'], [safaris['naivasha_hippo'], safaris['crescent_island']]),
                ('Mount Kenya transfer and equator golf at Fairmont', 'Transfer zum Mount Kenya und Aequatorgolf im Fairmont', accommodations['fairmont'], [courses['fairmont']]),
                ('Ol Pejeta private conservancy day', 'Privater Conservancy-Tag in Ol Pejeta', accommodations['fairmont'], [safaris['ol_pejeta']]),
                ('Vipingo Ridge Baobab Course coastal finale', 'Kuestenfinale auf dem Baobab Course im Vipingo Ridge', accommodations['vipingo_villas'], [courses['vipingo']]),
                ('Oceanfront recovery and private departure transfer', 'Erholung am Meer und privater Abreisetransfer', accommodations['vipingo_villas'], [wellness['kuruwitu_reef']]),
            ],
        )

        odyssey = BasePackage.objects.create(
            title_en='15-Day Kenya Championship Golf Odyssey',
            title_de='15 Tage Kenya Championship Golf Odyssey',
            summary_en=(
                'Kenya’s most complete golf-led route: six rounds from Nairobi’s historic clubs to '
                'Rift Valley escarpments and Vipingo Ridge, with conservancy and coastal days built in.'
            ),
            summary_de=(
                'Kenyas umfassendste golfgefuehrte Route: sechs Runden von Nairobis historischen Clubs '
                'ueber das Rift Valley bis Vipingo Ridge, ergaenzt durch Conservancy- und Kuestentage.'
            ),
            inclusions_en=(
                'Private airport meet-and-assist on arrival and departure\n'
                'All accommodation listed in the itinerary, subject to availability\n'
                'Daily breakfast and selected hosted dining experiences\n'
                'Pre-arranged tee times, green fees, and golf cart coordination where available\n'
                'Private road transfers and planned regional flight coordination\n'
                'Safari park and conservancy entry fees for listed wildlife experiences\n'
                'Professional guiding for listed safari and conservation activities\n'
                'Concierge itinerary design, local coordination, and WhatsApp support during travel'
            ),
            inclusions_de=(
                'Private Flughafenbetreuung bei Ankunft und Abreise\n'
                'Alle im Reiseverlauf genannten Unterkuenfte, vorbehaltlich Verfuegbarkeit\n'
                'Taegliches Fruehstueck und ausgewaehlte begleitete Dinner-Erlebnisse\n'
                'Vorab koordinierte Tee Times, Greenfees und Golfcart-Abstimmung wo verfuegbar\n'
                'Private Strassentransfers und geplante Koordination regionaler Flugsegmente\n'
                'Park- und Conservancy-Gebuehren fuer gelistete Wildlife-Erlebnisse\n'
                'Professionelle Fuehrung fuer gelistete Safari- und Conservation-Aktivitaeten\n'
                'Concierge-Routenplanung, lokale Koordination und WhatsApp-Support waehrend der Reise'
            ),
            exclusions_en=(
                'International flights and visas\n'
                'Travel insurance, medical cover, and evacuation insurance\n'
                'Premium alcohol, cellar selections, and personal minibar charges\n'
                'Caddie gratuities, guide gratuities, and discretionary staff tips\n'
                'Optional helicopter, private charter, or aircraft upgrades beyond the planned routing\n'
                'Items of a personal nature, laundry, spa treatments not listed, and excess baggage handling'
            ),
            exclusions_de=(
                'Internationale Fluege und Visa\n'
                'Reiseversicherung, medizinische Absicherung und Evakuierungsversicherung\n'
                'Premium-Alkohol, Weinauswahl und persoenliche Minibar-Kosten\n'
                'Caddie-Trinkgelder, Guide-Trinkgelder und freiwillige Staff Tips\n'
                'Optionale Helikopter-, Privat-Charter- oder Flugzeug-Upgrades ausserhalb der geplanten Route\n'
                'Persoenliche Ausgaben, Waescherei, nicht gelistete Spa-Behandlungen und Handling von Uebergepaeck'
            ),
            duration_days=15,
            slug='ultimate-odyssey',
            card_image_url=IMG['golf'][2],
            hero_image_url=IMG['golf'][3],
        )
        self.create_pricing(
            odyssey,
            peak_price=18950,
            green_price=14950,
        )
        self.create_itinerary_days(
            odyssey,
            [
                ('Private Nairobi arrival and Karen Estate Spa Ritual orientation', 'Private Nairobi-Ankunft und Karen Estate Spa Ritual Orientierung', accommodations['hemingways'], [wellness['blixen_tea']]),
                ('Karen Country Club positioning round', 'Karen Country Club Positionsrunde', accommodations['hemingways'], [courses['karen']]),
                ('Nairobi National Park black rhino drive and recovery afternoon', 'Nairobi National Park Black-Rhino-Drive und Recovery Afternoon', accommodations['hemingways'], [safaris['nairobi_np'], wellness['blixen_tea']]),
                ('Muthaiga Golf Club championship test', 'Muthaiga Golf Club Championship-Test', accommodations['hemingways'], [courses['muthaiga']]),
                ('Windsor Golf & Country Club forest estate round', 'Windsor Golf & Country Club Forest-Estate-Runde', accommodations['hemingways'], [courses['windsor']]),
                ('Great Rift Valley transfer and escarpment golf', 'Great-Rift-Valley-Transfer und Escarpment-Golf', accommodations['loldia'], [courses['great_rift']]),
                ('Lake Naivasha hippo safari and volcanic mud therapy', 'Lake-Naivasha-Hippo-Safari und vulkanische Schlammtherapie', accommodations['loldia'], [safaris['naivasha_hippo'], wellness['volcanic_mud']]),
                ('Crescent Island walking safari and lakeside recovery', 'Crescent Island Walking Safari und Lakeside Recovery', accommodations['loldia'], [safaris['crescent_island']]),
                ('Mount Kenya arrival and Highland Yoga Retreat', 'Mount-Kenya-Ankunft und Highland-Yoga-Retreat', accommodations['fairmont'], [wellness['equine_treks']]),
                ('Fairmont Mount Kenya Safari Club equator golf', 'Fairmont Mount Kenya Safari Club Aequatorgolf', accommodations['fairmont'], [courses['fairmont']]),
                ('Ol Pejeta Conservancy predator and rhino access', 'Ol Pejeta Conservancy Raubkatzen- und Nashornzugang', accommodations['fairmont'], [safaris['ol_pejeta']]),
                ('Coastal flight and Vipingo Ridge decompression', 'Kuestenflug und Vipingo Ridge Dekompression', accommodations['vipingo_villas'], [wellness['kuruwitu_reef']]),
                ('Vipingo Ridge Baobab Course championship round', 'Vipingo Ridge Baobab Course Championship-Runde', accommodations['vipingo_villas'], [courses['vipingo']]),
                ('Tsavo East/West red elephant extension', 'Tsavo East/West Red-Elephant Extension', accommodations['vipingo_villas'], [safaris['tsavo']]),
                ('Vipingo Oceanfront Spa Recovery and private departure', 'Vipingo Oceanfront Spa Recovery und private Abreise', accommodations['vipingo_villas'], [wellness['kuruwitu_reef']]),
            ],
        )

        nairobi_week = BasePackage.objects.create(
            title_en='7-Day Nairobi Championship Golf Week',
            title_de='7 Tage Nairobi Championship Golf Week',
            summary_en=(
                'Four serious rounds at Karen, Muthaiga, Windsor, and Great Rift Valley, based from '
                'two well-positioned properties with one Nairobi wildlife morning between tee times.'
            ),
            summary_de=(
                'Vier anspruchsvolle Runden in Karen, Muthaiga, Windsor und im Great Rift Valley, '
                'mit zwei strategisch gelegenen Unterkuenften und einem Wildlife-Morgen in Nairobi.'
            ),
            inclusions_en=(
                'Six nights in the listed accommodation, including daily breakfast\n'
                'Four pre-arranged golf rounds with green fees\n'
                'Shared caddie or golf cart where required and available by the host club\n'
                'Private airport, hotel, golf club, and Rift Valley road transfers\n'
                'Nairobi National Park entry fees and a private professional guide\n'
                'Daily bottled water, golf bag handling, and local concierge support'
            ),
            inclusions_de=(
                'Sechs Naechte in den genannten Unterkuenften mit taeglichem Fruehstueck\n'
                'Vier vorab koordinierte Golfrunden inklusive Greenfees\n'
                'Geteilter Caddie oder Golfcart, sofern vom Club vorgeschrieben und verfuegbar\n'
                'Private Flughafen-, Hotel-, Golfclub- und Rift-Valley-Transfers\n'
                'Eintritt in den Nairobi National Park und privater professioneller Guide\n'
                'Taegliches Trinkwasser, Golfgepaeck-Handling und lokaler Concierge-Support'
            ),
            exclusions_en=(
                'International flights, visas, and travel insurance\n'
                'Clubhouse meals, drinks, and dinners unless specifically hosted\n'
                'Golf club rental, shoes, balls, and personal equipment purchases\n'
                'Caddie gratuities and discretionary staff tips\n'
                'Personal expenses, laundry, and optional spa treatments'
            ),
            exclusions_de=(
                'Internationale Fluege, Visa und Reiseversicherung\n'
                'Clubhouse-Mahlzeiten, Getraenke und Dinner, sofern nicht ausdruecklich inkludiert\n'
                'Leihschlaeger, Golfschuhe, Baelle und persoenliche Ausruestungskaeufe\n'
                'Caddie-Trinkgelder und freiwillige Staff Tips\n'
                'Persoenliche Ausgaben, Waescherei und optionale Spa-Behandlungen'
            ),
            duration_days=7,
            slug='nairobi-championship-golf-week',
            card_image_url=IMG['golf'][4],
            hero_image_url=IMG['golf'][5],
        )
        self.create_pricing(
            nairobi_week,
            peak_price=7850,
            green_price=6450,
        )
        self.create_itinerary_days(
            nairobi_week,
            [
                ('Nairobi arrival, equipment check, and Karen briefing', 'Ankunft in Nairobi, Equipment Check und Karen Briefing', accommodations['hemingways'], [wellness['blixen_tea']]),
                ('Karen Country Club opening round', 'Auftaktrunde im Karen Country Club', accommodations['hemingways'], [courses['karen']]),
                ('Muthaiga Golf Club championship round', 'Championship-Runde im Muthaiga Golf Club', accommodations['hemingways'], [courses['muthaiga']]),
                ('Nairobi National Park dawn drive and recovery afternoon', 'Nairobi National Park Dawn Drive und Erholungsnachmittag', accommodations['hemingways'], [safaris['nairobi_np']]),
                ('Windsor forest course and closing-hole strategy', 'Windsor Forest Course und Strategie fuer das Schlussloch', accommodations['hemingways'], [courses['windsor']]),
                ('Great Rift Valley escarpment round and Naivasha transfer', 'Great-Rift-Valley-Runde und Transfer nach Naivasha', accommodations['loldia'], [courses['great_rift']]),
                ('Lake Naivasha breakfast, Nairobi return, and departure', 'Fruehstueck am Lake Naivasha, Rueckkehr nach Nairobi und Abreise', accommodations['loldia'], [safaris['naivasha_hippo']]),
            ],
        )

        grand_circuit = BasePackage.objects.create(
            title_en='12-Day Fairways of Kenya: Capital to Coast',
            title_de='12 Tage Fairways of Kenya: Hauptstadt bis Kueste',
            summary_en=(
                'A six-round progression from Nairobi’s mature parkland clubs to high-altitude fairways '
                'and the Baobab Course at Vipingo Ridge, with measured wildlife and recovery days.'
            ),
            summary_de=(
                'Sechs Golfrunden von Nairobis klassischen Parkland-Clubs ueber Hochland-Fairways '
                'bis zum Baobab Course im Vipingo Ridge, mit ausgewogenen Wildlife- und Erholungstagen.'
            ),
            inclusions_en=(
                'Eleven nights in the listed boutique hotels, lodges, and golf-estate villas\n'
                'Six pre-arranged golf rounds with green fees\n'
                'Golf carts where available and mandatory caddie coordination\n'
                'Private road transfers plus scheduled domestic flight coordination to the coast\n'
                'Park and conservancy fees for the listed wildlife experiences\n'
                'Daily breakfast, selected hosted meals, and bottled water during transfers\n'
                'Golf bag handling and on-trip concierge support'
            ),
            inclusions_de=(
                'Elf Naechte in den genannten Boutique-Hotels, Lodges und Golf-Estate-Villen\n'
                'Sechs vorab koordinierte Golfrunden inklusive Greenfees\n'
                'Golfcarts wo verfuegbar und Koordination vorgeschriebener Caddies\n'
                'Private Strassentransfers sowie Koordination des Linien-Inlandsflugs an die Kueste\n'
                'Park- und Conservancy-Gebuehren fuer die genannten Wildlife-Erlebnisse\n'
                'Taegliches Fruehstueck, ausgewaehlte begleitete Mahlzeiten und Wasser bei Transfers\n'
                'Golfgepaeck-Handling und Concierge-Support waehrend der Reise'
            ),
            exclusions_en=(
                'International flights, visas, and comprehensive travel insurance\n'
                'Domestic flight fare, charged at the confirmed ticket cost\n'
                'Premium drinks, personal minibar charges, and unlisted meals\n'
                'Golf equipment rental and excess airline baggage fees for golf bags\n'
                'Caddie, guide, driver, and villa staff gratuities\n'
                'Optional treatments, private chef upgrades, and personal expenses'
            ),
            exclusions_de=(
                'Internationale Fluege, Visa und umfassende Reiseversicherung\n'
                'Inlandsflugpreis, berechnet zum bestaetigten Ticketpreis\n'
                'Premium-Getraenke, persoenliche Minibar-Kosten und nicht gelistete Mahlzeiten\n'
                'Leihschlaeger und zusaetzliche Airline-Gepaeckgebuehren fuer Golfbags\n'
                'Trinkgelder fuer Caddies, Guides, Fahrer und Villa-Personal\n'
                'Optionale Behandlungen, Private-Chef-Upgrades und persoenliche Ausgaben'
            ),
            duration_days=12,
            slug='kenya-grand-golf-circuit',
            card_image_url=IMG['golf'][6],
            hero_image_url=IMG['golf'][3],
        )
        self.create_pricing(
            grand_circuit,
            peak_price=15750,
            green_price=12950,
        )
        self.create_itinerary_days(
            grand_circuit,
            [
                ('Private Nairobi arrival and golf concierge briefing', 'Private Ankunft in Nairobi und Golf-Concierge-Briefing', accommodations['hemingways'], [wellness['blixen_tea']]),
                ('Karen Country Club parkland opener', 'Parkland-Auftakt im Karen Country Club', accommodations['hemingways'], [courses['karen']]),
                ('Muthaiga Golf Club championship round', 'Championship-Runde im Muthaiga Golf Club', accommodations['hemingways'], [courses['muthaiga']]),
                ('Windsor forest course and hosted clubhouse debrief', 'Windsor Forest Course und Clubhouse-Debrief', accommodations['hemingways'], [courses['windsor']]),
                ('Nairobi National Park dawn drive and travel reset', 'Nairobi National Park Dawn Drive und Reisepause', accommodations['hemingways'], [safaris['nairobi_np']]),
                ('Great Rift Valley escarpment golf above Naivasha', 'Great-Rift-Valley-Golf oberhalb von Naivasha', accommodations['loldia'], [courses['great_rift']]),
                ('Crescent Island walk and lakeside recovery', 'Crescent-Island-Wanderung und Erholung am See', accommodations['loldia'], [safaris['crescent_island'], wellness['volcanic_mud']]),
                ('Mount Kenya transfer and equator practice session', 'Transfer zum Mount Kenya und Aequator-Training', accommodations['fairmont'], [wellness['equine_treks']]),
                ('Fairmont Mount Kenya highland round', 'Hochlandrunde im Fairmont Mount Kenya', accommodations['fairmont'], [courses['fairmont']]),
                ('Ol Pejeta conservancy and rhino tracking day', 'Ol-Pejeta-Conservancy und Rhino-Tracking-Tag', accommodations['fairmont'], [safaris['ol_pejeta']]),
                ('Coastal flight and Vipingo Ridge Baobab Course', 'Kuestenflug und Baobab Course im Vipingo Ridge', accommodations['vipingo_villas'], [courses['vipingo']]),
                ('Second Vipingo round, ocean recovery, and departure preparation', 'Zweite Vipingo-Runde, Erholung am Meer und Abreisevorbereitung', accommodations['vipingo_villas'], [courses['vipingo'], wellness['kuruwitu_reef']]),
            ],
        )

        self.stdout.write(self.style.SUCCESS('Signature package itineraries created.'))

    def create_pricing(self, base_package, peak_price, green_price):
        PackagePricingSeason.objects.bulk_create(
            [
                PackagePricingSeason(
                    base_package=base_package,
                    season_name='Peak',
                    start_date=date(2027, 7, 1),
                    end_date=date(2027, 10, 31),
                    price_usd=peak_price,
                ),
                PackagePricingSeason(
                    base_package=base_package,
                    season_name='Green',
                    start_date=date(2027, 4, 1),
                    end_date=date(2027, 6, 30),
                    price_usd=green_price,
                ),
            ]
        )

    def create_itinerary_days(self, base_package, day_payloads):
        for index, (title_en, title_de, accommodation, activities) in enumerate(day_payloads, start=1):
            day = PackageItineraryDay.objects.create(
                base_package=base_package,
                day_number=index,
                title_en=title_en,
                title_de=title_de,
                accommodation=accommodation,
            )
            self.create_day_activities(day, activities)

    def create_day_activities(self, itinerary_day, activities):
        day_activity_records = []

        for display_order, activity in enumerate(activities, start=1):
            day_activity_records.append(
                DayActivity(
                    itinerary_day=itinerary_day,
                    content_type=ContentType.objects.get_for_model(activity),
                    object_id=activity.pk,
                    display_order=display_order,
                )
            )

        DayActivity.objects.bulk_create(day_activity_records)
