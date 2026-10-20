"""
Data-only fixture catalog for the AfroLink Adventures luxury seed command.

This module intentionally contains NO Django imports. It exists purely to hold
curated structures (dicts, lists, tuples of plain strings/bools/numbers) that a
management command (e.g. ``seed_destination_data.py`` or a future
``luxury_seed_catalog`` command) can import and turn into model instances.

Model choice fields (``PropertyType``, ``CourseStyle``, ``Category``,
``DurationChoice``) are represented here as their plain string values so this
module never has to import ``destination_cms.models``:

- Accommodation.property_type: 'hotel' | 'safari_lodge' | 'golf_resort' | 'boutique' | 'villa'
- GolfCourse.course_style: 'parkland' | 'links' | 'resort' | 'mountain'
- WellnessExperience.category: 'spa' | 'recovery' | 'yoga' | 'massage' | 'thermal' | 'other'
- WellnessExperience.duration_choice: '60_min' | 'half_day' | 'full_day' | 'multi_day'

``region_key`` on every record refers to the same regional hub keys used by
``seed_destination_data.py``: 'nairobi', 'rift', 'mount_kenya', 'coast'.
"""

# ---------------------------------------------------------------------------
# 1. Curated image pool, organised by strict category so hero/gallery images
#    never mix golf, safari, wellness, and stay photography.
# ---------------------------------------------------------------------------

IMG = {
    'golf': [
        'https://images.unsplash.com/photo-1535131749006-b7f58c99034b?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1535132011086-b8818f016104?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1600679472829-3044539ce8ed?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1459865264687-595d652de67e?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1593111774240-d529f12cf4bb?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1592919505780-303950717480?auto=format&fit=crop&w=1400&q=80',
    ],
    'safari': [
        'https://images.unsplash.com/photo-1516426122078-c23e76319801?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1547970810-dc1eac37d174?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1546182990-dffeafbe841d?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1564760055775-d63b17a55c44?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1535941339077-2dd1c7963098?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1614027164847-1b28cfe1df60?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1552410260-0fd9b577afa6?auto=format&fit=crop&w=1400&q=80',
    ],
    'wellness': [
        'https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1600334129128-685c5582fd35?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1571902943202-507ec2618e8f?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1591343395082-e120087004b4?auto=format&fit=crop&w=1400&q=80',
    ],
    'stay': [
        'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1571896349842-33c89424de2d?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1582719508461-905c673771fd?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1564501049412-61c2a3083791?auto=format&fit=crop&w=1400&q=80',
    ],
}


# ---------------------------------------------------------------------------
# 2. Accommodations
# ---------------------------------------------------------------------------

ACCOMMODATIONS = [
    {
        'key': 'hemingways',
        'region_key': 'nairobi',
        'name': 'Hemingways Nairobi',
        'slug': 'hemingways-nairobi',
        'property_type': 'boutique',
        'star_rating': 5,
        'description_en': 'A colonial-revival estate hotel in Karen, five minutes from the club and twenty from the national park gate.',
        'description_de': 'Ein Anwesen im Kolonialstil in Karen, fuenf Minuten vom Club und zwanzig von der Nationalpark-Einfahrt entfernt.',
        'overview': (
            'Hemingways sits inside the Karen residential belt rather than downtown, which makes it the '
            'natural opening and closing base for a Nairobi-anchored itinerary. Guests land at JKIA, settle '
            'into a suite by mid-afternoon, and can be teeing off at Karen Country Club the next morning '
            'without fighting the city\'s worst traffic corridors.'
        ),
        'style': 'Colonial-revival estate architecture with wraparound verandas over landscaped gardens',
        'atmosphere': 'Formal and hushed, run more like a private members\' house than a resort',
        'ideal_guests': 'Couples, solo executives, and small groups of up to four who prefer a quiet city base',
        'room_style': 'Suites with four-poster beds, free-standing tubs, and private garden-facing verandas',
        'room_categories': 'Nairobi Suite\nGarden Suite\nHemingway Suite\nPresidential Suite',
        'occupancy': 'Most suites sleep 2 adults; the Presidential Suite can accommodate 3 with an extra bed',
        'bed_types': 'King or twin configuration available on request',
        'room_size': '45 to 75 square metres depending on category',
        'has_balcony': True,
        'room_view': 'Private gardens, or the Ngong Hills on the western-facing suites',
        'best_for': 'Arrival and departure nights, and slower city days threaded between golf rounds',
        'location_access': (
            'Set inside Karen, roughly 5 minutes from Karen Country Club by car, 20 minutes from the '
            'Langata gate of Nairobi National Park, and within reach of the Blixen Museum and Karen Blixen '
            'Coffee Garden for an easy half-day out.'
        ),
        'distance_from_airport': '35-50 minutes from JKIA outside rush hour; allow up to 90 minutes at peak times',
        'latitude': -1.3567,
        'longitude': 36.7204,
        'dining_wellness': (
            'Best used for unhurried breakfasts on the veranda, a founder-led itinerary briefing over tea, '
            'and a spa treatment before an early safari or golf start the next day.'
        ),
        'restaurants': 'The Tea Lounge for all-day dining and a proper afternoon tea; The Chef\'s Table for a seasonal set menu',
        'breakfast_included': True,
        'private_dining': True,
        'dietary_options': 'Halal, vegetarian, and gluten-free menus prepared with 24 hours\' notice',
        'has_pool': True,
        'has_gym': True,
        'has_spa': True,
        'has_restaurant': True,
        'has_bar': True,
        'has_concierge': True,
        'has_business_centre': True,
        'has_wifi': True,
        'check_in_time': '14:00',
        'check_out_time': '11:00',
        'early_check_in': True,
        'late_check_out': True,
        'family_friendly': True,
        'adults_only': False,
        'accessibility_notes': 'Ground-floor garden suites suit guests with mobility needs; request this at the time of booking.',
        'smoking_policy': 'Non-smoking throughout the main house; designated outdoor terrace areas only',
        'pet_policy': 'Service animals only',
        'need_to_know': (
            'Best used after long-haul arrivals, before early golf or safari starts.\n'
            'Ask the concierge to sequence JKIA transfers with a traffic buffer, especially for afternoon arrivals.\n'
            'Karen Country Club, Nairobi National Park, and Giraffe Manor are all a short drive away.'
        ),
        'amenities_json': {'style': 'colonial boutique', 'features': ['butler service', 'garden suites', 'private verandas']},
        'is_featured': True,
        'meta_title': 'Hemingways Nairobi | Karen Boutique Hotel | AfroLink Adventures',
        'meta_description': 'A polished Karen base for golf, safari, and city arrival nights, five minutes from Karen Country Club.',
        'hero_image_url': IMG['stay'][0],
    },
    {
        'key': 'loldia',
        'region_key': 'rift',
        'name': 'Loldia House',
        'slug': 'loldia-house',
        'property_type': 'safari_lodge',
        'star_rating': 5,
        'description_en': 'A working farmhouse-turned-lodge on the shore of Lake Naivasha, built for lake safaris and Rift Valley golf recovery.',
        'description_de': 'Ein zum Lodge umgebautes Farmhaus am Ufer des Lake Naivasha fuer Seesafaris und Erholung nach Rift-Valley-Golf.',
        'overview': (
            'Loldia is a family farmhouse that still runs cattle and crops alongside its handful of guest '
            'cottages, which gives it a working-lake-estate feel rather than a manufactured lodge atmosphere. '
            'Its jetty puts hippo and boat safaris a five-minute walk from bed, and it sits close enough to '
            'Great Rift Valley Lodge & Golf Resort to make golf and lake days into one loop.'
        ),
        'style': 'Heritage farmhouse and thatched cottages set in working gardens above the lakeshore',
        'atmosphere': 'Relaxed and unpolished by design, favouring a homely pace over formality',
        'ideal_guests': 'Couples, birders, and golfers wanting a quieter counterpoint to city hotels',
        'room_style': 'Cottage rooms with garden entrances, mosquito-net beds, and lake-facing sitting areas',
        'room_categories': 'Garden Cottage\nLake View Cottage\nFamily Cottage',
        'occupancy': 'Garden and lake view cottages sleep 2; family cottages sleep up to 4',
        'bed_types': 'King, twin, or family bunk configuration on request',
        'room_size': '35 to 60 square metres',
        'has_balcony': True,
        'room_view': 'Working farm gardens or the open water of Lake Naivasha',
        'best_for': 'Rift Valley decompression, birding, and lake safari access',
        'location_access': (
            'A working farm estate on the Lake Naivasha shoreline, roughly 20 minutes from Great Rift Valley '
            'Lodge & Golf Resort, 15 minutes from the Crescent Island boat launch, and under an hour from '
            'Hell\'s Gate National Park\'s Elsa Gate.'
        ),
        'distance_from_airport': 'About 1.5 to 2 hours from Nairobi (JKIA) by road, traffic-dependent',
        'latitude': -0.7746,
        'longitude': 36.3299,
        'dining_wellness': 'Best for relaxed farmhouse dining, garden downtime, and gentle recovery between escarpment golf and lake activity.',
        'restaurants': 'Communal farmhouse dining room serving set menus from the estate garden and lake fish where available',
        'breakfast_included': True,
        'private_dining': False,
        'dietary_options': 'Vegetarian and most allergies accommodated with advance notice; kitchen is small and menu-led',
        'has_pool': False,
        'has_gym': False,
        'has_spa': False,
        'has_restaurant': True,
        'has_bar': True,
        'has_concierge': True,
        'has_business_centre': False,
        'has_wifi': True,
        'check_in_time': '14:00',
        'check_out_time': '10:30',
        'early_check_in': False,
        'late_check_out': False,
        'family_friendly': True,
        'adults_only': False,
        'accessibility_notes': 'Uneven garden paths and a handful of steps; not well suited to wheelchairs.',
        'smoking_policy': 'Outdoor smoking only, away from the main dining terrace',
        'pet_policy': 'Resident farm dogs on site; no guest pets accommodated',
        'need_to_know': (
            'Lake weather can change quickly, so pack light layers even in the dry season.\n'
            'Boat and walking safari timings should be confirmed the evening before around wind and water conditions.\n'
            'This is a stay for setting and pace rather than nightlife or spa facilities.'
        ),
        'amenities_json': {'style': 'heritage lakeside farmhouse', 'features': ['private jetty', 'working farm gardens', 'boat safaris']},
        'is_featured': False,
        'meta_title': 'Loldia House | Lake Naivasha Lodge | AfroLink Adventures',
        'meta_description': 'A working lakeshore farmhouse near Great Rift Valley golf, built for hippo boat safaris and quiet recovery.',
        'hero_image_url': IMG['stay'][3],
    },
    {
        'key': 'fairmont',
        'region_key': 'mount_kenya',
        'name': 'Fairmont Mount Kenya Safari Club',
        'slug': 'fairmont-mount-kenya-safari-club-accommodation',
        'property_type': 'golf_resort',
        'star_rating': 5,
        'description_en': 'A historic equator-line club estate with its own 9-hole course, stables, and direct routing toward Ol Pejeta.',
        'description_de': 'Ein historisches Club-Anwesen an der Aequatorlinie mit eigenem 9-Loch-Platz, Stallungen und direkter Anbindung an Ol Pejeta.',
        'overview': (
            'Founded in the 1960s as a private members\' retreat, the Safari Club still carries that '
            'old-world highland character: fireplaces lit by early evening, gardens dotted with peacocks, '
            'and a straddle-the-equator photo stop most guests can\'t resist. At 2,150 metres the air is '
            'noticeably cooler than Nairobi, which makes it a natural reset point before or after Ol Pejeta.'
        ),
        'style': 'Historic highland clubhouse architecture with formal gardens and equator-line grounds',
        'atmosphere': 'Old-world and fireside, calmer than a typical golf resort',
        'ideal_guests': 'Golfers combining equator play and conservancy days; couples wanting highland scenery',
        'room_style': 'Cottage-style rooms and suites with fireplaces and mountain or garden views',
        'room_categories': 'Garden Cottage\nMountain View Suite\nWilliam Holden Cottage',
        'occupancy': 'Most cottages sleep 2; the William Holden Cottage sleeps up to 4',
        'bed_types': 'King or twin configuration on request',
        'room_size': '40 to 90 square metres',
        'has_balcony': True,
        'room_view': 'Formal gardens, the 9-hole course, or Mount Kenya on a clear morning',
        'best_for': 'Mount Kenya golf, highland recovery, and staging before or after Ol Pejeta',
        'location_access': (
            'Located just outside Nanyuki town, roughly 15 minutes from Nanyuki\'s airstrip and under an '
            'hour by road from Ol Pejeta Conservancy\'s main gate.'
        ),
        'distance_from_airport': 'About 3 to 3.5 hours by road from JKIA, or a short domestic flight into Nanyuki',
        'latitude': 0.0163,
        'longitude': 37.0714,
        'dining_wellness': 'Strong for fireside evenings, spa recovery, and slower mornings after conservancy or long transfer days.',
        'restaurants': 'The Zebar for casual dining and sundowners; the main dining room for a set highland menu',
        'breakfast_included': True,
        'private_dining': True,
        'dietary_options': 'Vegetarian, vegan, and most allergies catered to with advance notice',
        'has_pool': True,
        'has_gym': True,
        'has_spa': True,
        'has_restaurant': True,
        'has_bar': True,
        'has_concierge': True,
        'has_business_centre': False,
        'has_wifi': True,
        'check_in_time': '14:00',
        'check_out_time': '11:00',
        'early_check_in': False,
        'late_check_out': True,
        'family_friendly': True,
        'adults_only': False,
        'accessibility_notes': 'Grounds are spread across gentle slopes; buggies available for guests who need them.',
        'smoking_policy': 'Non-smoking rooms; smoking permitted on private terraces',
        'pet_policy': 'Not accommodated, aside from resident animal sanctuary residents',
        'need_to_know': (
            'Cool mornings and evenings require a light jacket even in the dry season.\n'
            'Build in transfer time when pairing a stay here with Ol Pejeta game drives.\n'
            'The altitude and quieter setting make this a recovery-forward stay rather than a nightlife base.'
        ),
        'amenities_json': {'style': 'highland club resort', 'features': ['equator marker', 'animal sanctuary', 'stables']},
        'is_featured': False,
        'meta_title': 'Fairmont Mount Kenya Safari Club | Nanyuki Highland Resort | AfroLink Adventures',
        'meta_description': 'A historic equator-line club estate near Ol Pejeta, with its own course, stables, and fireside dining.',
        'hero_image_url': IMG['stay'][6],
    },
    {
        'key': 'vipingo_villas',
        'region_key': 'coast',
        'name': 'Vipingo Ridge Private Villas',
        'slug': 'vipingo-ridge-private-villas',
        'property_type': 'villa',
        'star_rating': 5,
        'description_en': 'Private ocean-air villas built into the Vipingo Ridge estate, steps from the Baobab Course clubhouse.',
        'description_de': 'Private Villen mit Meeresluft im Vipingo-Ridge-Anwesen, wenige Schritte vom Baobab-Course-Clubhaus entfernt.',
        'overview': (
            'These are privately owned villas released for guest stays inside a members\' golf estate, so '
            'the setting feels closer to a private residence than a hotel. Families or golf groups get a '
            'full kitchen, a private pool, and direct buggy access to the Baobab Course, with Mombasa\'s '
            'restaurants and Tsavo\'s wilderness both within a manageable drive.'
        ),
        'style': 'Contemporary coastal villas in coral-stone and dark timber, set within golf-estate grounds',
        'atmosphere': 'Private and residential, with resort-level service on call rather than always present',
        'ideal_guests': 'Families, multi-generational groups, and golf parties wanting space and privacy',
        'room_style': 'Multi-bedroom villas with private pools, open-plan living, and ocean-facing terraces',
        'room_categories': '3-Bedroom Villa\n4-Bedroom Villa\n5-Bedroom Villa',
        'occupancy': 'Villas sleep 6 to 10 guests depending on configuration',
        'bed_types': 'King, twin, and children\'s bunk rooms available across villa sizes',
        'room_size': '250 to 450 square metres of living space per villa',
        'has_balcony': True,
        'room_view': 'Golf fairways, tropical gardens, or glimpses of the Indian Ocean depending on villa position',
        'best_for': 'Coastal golf, family privacy, and heat recovery beside a private pool',
        'location_access': (
            'Inside the Vipingo Ridge estate on Kenya\'s north coast, a two-minute buggy ride from the '
            'Baobab Course clubhouse and roughly 45 minutes from Mombasa\'s Moi International Airport.'
        ),
        'distance_from_airport': '30-45 minutes from Mombasa (MBA) or the Vipingo airstrip when in use',
        'latitude': -3.8667,
        'longitude': 39.8333,
        'dining_wellness': 'Works well for villa-based private chef dining, beach recovery, and pool downtime after heat-exposed coastal golf.',
        'restaurants': 'Private in-villa chef service, plus clubhouse dining at the Baobab Course',
        'breakfast_included': False,
        'private_dining': True,
        'dietary_options': 'Fully flexible via private chef; advise dietary needs before arrival',
        'has_pool': True,
        'has_gym': False,
        'has_spa': False,
        'has_restaurant': True,
        'has_bar': False,
        'has_concierge': True,
        'has_business_centre': False,
        'has_wifi': True,
        'check_in_time': '14:00',
        'check_out_time': '10:00',
        'early_check_in': True,
        'late_check_out': False,
        'family_friendly': True,
        'adults_only': False,
        'accessibility_notes': 'Villas are single or split-level; request a single-storey unit if stairs are a concern.',
        'smoking_policy': 'Outdoor smoking only, away from shared pool areas',
        'pet_policy': 'Not accommodated',
        'need_to_know': (
            'Coastal heat makes early tee times preferable; afternoons are better spent by the pool.\n'
            'Confirm villa configuration early for couples, families, or multi-generational groups.\n'
            'Groceries and a private chef can be arranged ahead of arrival for self-catered stretches.'
        ),
        'amenities_json': {'style': 'private golf-estate villa', 'features': ['private pool', 'buggy access to course', 'private chef on request']},
        'is_featured': True,
        'meta_title': 'Vipingo Ridge Private Villas | Coastal Golf Estate | AfroLink Adventures',
        'meta_description': 'Private pool villas inside the Vipingo Ridge golf estate, steps from the Baobab Course and Kenya\'s north coast.',
        'hero_image_url': IMG['stay'][2],
    },
    {
        'key': 'giraffes',
        'region_key': 'nairobi',
        'name': 'Giraffe Manor',
        'slug': 'giraffe-manor',
        'property_type': 'boutique',
        'star_rating': 5,
        'description_en': 'A 1930s manor house in Lang\'ata where resident Rothschild giraffes visit the breakfast terrace and windows.',
        'description_de': 'Ein Herrenhaus aus den 1930er Jahren in Lang\'ata, in dem Rothschild-Giraffen zur Fruehstuecksterrasse kommen.',
        'overview': (
            'Only a dozen rooms and a resident herd of Rothschild giraffe make this the smallest and most '
            'in-demand stay in the portfolio, so it works best as a two-night anchor booked well ahead rather '
            'than a flexible add-on. Its location inside the Giraffe Centre sanctuary keeps it a short hop '
            'from Karen Country Club and Nairobi National Park.'
        ),
        'style': '1930s English manor house furnished with period antiques and botanical prints',
        'atmosphere': 'Intimate and slightly theatrical, built around the giraffe encounters rather than around it',
        'ideal_guests': 'Couples, families with older children, and guests booking well in advance for a signature two nights',
        'room_style': 'Individually decorated manor rooms, several with giraffe-height windows',
        'room_categories': 'Manor Room\nGarden Room\nKaren Suite',
        'occupancy': 'Most rooms sleep 2; the Karen Suite can accommodate a small family',
        'bed_types': 'King or twin configuration available',
        'room_size': '30 to 55 square metres',
        'has_balcony': False,
        'room_view': 'Manicured lawns where the resident giraffe herd roams each morning and evening',
        'best_for': 'A signature two-night stay bookended by Karen golf and Nairobi National Park',
        'location_access': (
            'Set inside the Giraffe Centre sanctuary in Lang\'ata, roughly 10 minutes from Karen Country '
            'Club and 15 minutes from the Nairobi National Park Langata gate.'
        ),
        'distance_from_airport': '40-60 minutes from JKIA outside rush hour',
        'latitude': -1.3756,
        'longitude': 36.7516,
        'dining_wellness': 'Best for giraffe feeding at breakfast and dusk, garden downtime, and an early, unhurried pace before golf or safari.',
        'restaurants': 'Communal dining room and garden terrace serving set breakfast, lunch, and dinner menus',
        'breakfast_included': True,
        'private_dining': False,
        'dietary_options': 'Vegetarian and most allergies accommodated with advance notice',
        'has_pool': False,
        'has_gym': False,
        'has_spa': False,
        'has_restaurant': True,
        'has_bar': True,
        'has_concierge': True,
        'has_business_centre': False,
        'has_wifi': True,
        'check_in_time': '14:00',
        'check_out_time': '11:00',
        'early_check_in': False,
        'late_check_out': False,
        'family_friendly': True,
        'adults_only': False,
        'accessibility_notes': 'A heritage house with narrow staircases and no lift; ground-floor rooms are limited.',
        'smoking_policy': 'Non-smoking throughout; designated outdoor smoking area',
        'pet_policy': 'Not accommodated',
        'need_to_know': (
            'Book well ahead; only twelve rooms exist and giraffe encounters happen at set morning and evening times.\n'
            'Children should be briefed on calm behaviour around the giraffe before arrival.\n'
            'This stay is better suited to two focused nights than a one-night stopover.'
        ),
        'amenities_json': {'style': 'manor house sanctuary stay', 'features': ['resident giraffe herd', 'heritage furnishings', 'sanctuary grounds']},
        'is_featured': True,
        'meta_title': 'Giraffe Manor | Nairobi Boutique Sanctuary Stay | AfroLink Adventures',
        'meta_description': 'A twelve-room Lang\'ata manor house where resident Rothschild giraffe visit the breakfast terrace each morning.',
        'hero_image_url': IMG['stay'][4],
    },
    {
        'key': 'sarova_salt',
        'region_key': 'mount_kenya',
        'name': 'Sweetwaters Serena Camp',
        'slug': 'sweetwaters-serena-camp',
        'property_type': 'safari_lodge',
        'star_rating': 4,
        'description_en': 'A tented camp inside Ol Pejeta Conservancy, positioned on a former airstrip facing a floodlit waterhole.',
        'description_de': 'Ein Zeltcamp innerhalb der Ol-Pejeta-Conservancy an einem angestrahlten Wasserloch auf einer ehemaligen Landebahn.',
        'overview': (
            'Sweetwaters sits inside the conservancy fence rather than outside it, so the game drive begins '
            'the moment guests step off the vehicle. Its raised tents face a floodlit waterhole where '
            'elephant and buffalo pass through most nights, making it the most immersive base for an Ol '
            'Pejeta-anchored stretch of the itinerary.'
        ),
        'style': 'Raised safari tents on wooden decks facing an open, floodlit waterhole',
        'atmosphere': 'Immersive and bush-facing, with wildlife audible from the tents after dark',
        'ideal_guests': 'Safari-focused couples and families wanting to stay inside the conservancy itself',
        'room_style': 'En-suite canvas tents with private decks and waterhole-facing views',
        'room_categories': 'Standard Tent\nFamily Tent',
        'occupancy': 'Standard tents sleep 2; family tents connect two rooms for up to 4',
        'bed_types': 'King or twin configuration on request',
        'room_size': 'Approximately 40 square metres including the deck',
        'has_balcony': True,
        'room_view': 'A floodlit waterhole with regular elephant and buffalo activity after dark',
        'best_for': 'Guests prioritising wildlife immersion over resort facilities during the Ol Pejeta stretch',
        'location_access': (
            'Inside Ol Pejeta Conservancy on a former World War II airstrip, roughly 45 minutes from the '
            'conservancy\'s main gate and under an hour from Fairmont Mount Kenya Safari Club.'
        ),
        'distance_from_airport': 'About 3.5 hours by road from JKIA, or a short flight to Nanyuki plus a road transfer',
        'latitude': 0.0167,
        'longitude': 36.9333,
        'dining_wellness': 'Best for waterhole-facing dinners, early and late game drives, and simple downtime between drives rather than spa treatments.',
        'restaurants': 'Main dining tent serving set breakfast, lunch, and dinner, with occasional bush dinners by arrangement',
        'breakfast_included': True,
        'private_dining': False,
        'dietary_options': 'Vegetarian and common allergies accommodated with advance notice',
        'has_pool': True,
        'has_gym': False,
        'has_spa': False,
        'has_restaurant': True,
        'has_bar': True,
        'has_concierge': True,
        'has_business_centre': False,
        'has_wifi': True,
        'check_in_time': '14:00',
        'check_out_time': '10:00',
        'early_check_in': False,
        'late_check_out': False,
        'family_friendly': True,
        'adults_only': False,
        'accessibility_notes': 'Raised wooden walkways connect the tents; not well suited to wheelchairs.',
        'smoking_policy': 'Outdoor smoking only, away from the dining tent',
        'pet_policy': 'Not accommodated',
        'need_to_know': (
            'Wildlife can approach the camp perimeter after dark, so guests are escorted between tents at night.\n'
            'Pack a warm layer for early-morning game drives even in the dry season.\n'
            'This stay favours wildlife immersion over spa or resort facilities.'
        ),
        'amenities_json': {'style': 'tented safari camp', 'features': ['in-conservancy access', 'floodlit waterhole', 'former airstrip setting']},
        'is_featured': False,
        'meta_title': 'Sweetwaters Serena Camp | Ol Pejeta Tented Camp | AfroLink Adventures',
        'meta_description': 'A tented camp inside Ol Pejeta Conservancy facing a floodlit waterhole, for guests who want to stay inside the fence.',
        'hero_image_url': IMG['stay'][5],
    },
]


# ---------------------------------------------------------------------------
# 3. Golf courses
# ---------------------------------------------------------------------------

GOLF_COURSES = [
    {
        'key': 'karen',
        'region_key': 'nairobi',
        'name': 'Karen Country Club',
        'slug': 'karen-country-club',
        'overview': (
            'A mature Karen parkland round dating to 1937 that rewards shape control and quiet club '
            'pacing over raw distance, played between Nairobi arrivals and the first safari day.'
        ),
        'holes_and_par': '18 holes | Par 71 | approx. 6,893 yards',
        'holes': 18,
        'par': 71,
        'course_length': '18 holes, mature parkland routing',
        'architect_designer': 'Remy Martin, with historical parkland routing refined over decades',
        'year_opened': 1937,
        'course_style': 'parkland',
        'turf_grass_type': 'Mature kikuyu fairways with fast, well-drained greens',
        'signature_features': (
            'Pro tip: Karen rewards shape control more than raw length. Favour position off the tee, respect '
            'the tree corridors, and treat the closing stretch as a par-protection sequence.'
        ),
        'signature_holes': 'Tree-lined corridors on the middle holes and a demanding closing stretch built for par protection',
        'difficulty_level': 'Strategic and tree-lined, placement over power',
        'best_suited_for': 'Strategic players who prefer positioning off the tee to bombing driver',
        'best_time_to_play': 'Early morning tee times for cooler air and smoother city logistics',
        'is_championship': True,
        'practice_range': True,
        'putting_green': True,
        'short_game_area': False,
        'golf_academy': False,
        'clubhouse': True,
        'restaurant': True,
        'pro_shop': True,
        'walking_allowed': True,
        'golf_carts': False,
        'caddies': True,
        'rental_clubs': False,
        'locker_rooms': True,
        'changing_rooms': True,
        'booking_window': 'Request preferred times 2-4 weeks ahead, longer around member competitions',
        'average_playing_time': '4 to 4.5 hours with a caddie',
        'peak_season': 'July-September and December-February',
        'best_playing_months': 'June-October',
        'collared_shirts_required': True,
        'soft_spikes_required': True,
        'denim_allowed': False,
        'dress_code': 'Collared shirts, tailored shorts or trousers, and soft-spike golf shoes; no denim or beachwear',
        'facilities': 'Clubhouse and dining\nPractice range and putting green\nCaddie support subject to availability\nPro shop',
        'booking_notes': 'Preferred tee times should be requested early, especially around member days and weekends',
        'arrival_notes': 'Arrive at least 30 minutes before play so the concierge can manage check-in and caddie coordination',
        'distance_from_airport': 'About 45-75 minutes from JKIA depending on traffic',
        'latitude': -1.3598,
        'longitude': 36.7401,
        'is_featured': True,
        'meta_title': 'Karen Country Club | Nairobi Parkland Golf | AfroLink Adventures',
        'meta_description': 'Play Nairobi\'s classic 1937 parkland course, five minutes from Hemingways and Nairobi National Park.',
        'hero_image_url': IMG['golf'][0],
    },
    {
        'key': 'muthaiga',
        'region_key': 'nairobi',
        'name': 'Muthaiga Golf Club',
        'slug': 'muthaiga-golf-club',
        'overview': (
            'A polished members\' club test dating to 1913, with tournament-conditioned surfaces and a '
            'guest-access process that rewards booking through a coordinated concierge rather than direct inquiry.'
        ),
        'holes_and_par': '18 holes | Par 71 | approx. 7,228 yards',
        'holes': 18,
        'par': 71,
        'course_length': '18 holes, mature championship parkland',
        'architect_designer': 'Peter Matkovich championship renovation over the original 1913 Nairobi routing',
        'year_opened': 1913,
        'course_style': 'parkland',
        'turf_grass_type': 'Kikuyu fairways with tournament-conditioned greens',
        'signature_features': (
            'Pro tip: Muthaiga asks for disciplined driving lines and controlled long-iron approaches. The '
            'professional play is to work back from the green complexes and avoid short-sided misses.'
        ),
        'signature_holes': 'A demanding closing run of holes that has hosted multiple Kenya Open editions',
        'difficulty_level': 'Polished member-club test with a premium on accuracy',
        'best_suited_for': 'Disciplined golfers who enjoy a premium club atmosphere',
        'best_time_to_play': 'Morning rounds avoid Nairobi traffic pressure and keep afternoons free for dining',
        'is_championship': True,
        'practice_range': True,
        'putting_green': True,
        'short_game_area': True,
        'golf_academy': True,
        'clubhouse': True,
        'restaurant': True,
        'pro_shop': True,
        'walking_allowed': True,
        'golf_carts': False,
        'caddies': True,
        'rental_clubs': False,
        'locker_rooms': True,
        'changing_rooms': True,
        'booking_window': 'Confirm guest access and introduction requirements at least 3-4 weeks ahead',
        'average_playing_time': '4 to 4.5 hours with a caddie',
        'peak_season': 'Dry season months and competition weeks',
        'best_playing_months': 'June-October',
        'collared_shirts_required': True,
        'soft_spikes_required': True,
        'denim_allowed': False,
        'dress_code': 'Conservative club attire: collared shirts and proper golf shoes; no denim or casual sportswear',
        'facilities': 'Historic clubhouse\nPractice range and short game area\nCaddie support subject to availability\nDining and locker facilities',
        'booking_notes': 'Guest access is managed carefully; confirm availability, introductions, and competition dates before finalizing routing',
        'arrival_notes': 'Allow time for security check-in and a brief club etiquette introduction before the round',
        'distance_from_airport': 'About 40-70 minutes from JKIA',
        'latitude': -1.2447,
        'longitude': 36.8206,
        'is_featured': False,
        'meta_title': 'Muthaiga Golf Club | Historic Nairobi Championship Course | AfroLink Adventures',
        'meta_description': 'A 1913 Nairobi members\' club course with tournament-conditioned greens and a managed guest-access process.',
        'hero_image_url': IMG['golf'][6],
    },
    {
        'key': 'windsor',
        'region_key': 'nairobi',
        'name': 'Windsor Golf & Country Club',
        'slug': 'windsor-golf-country-club',
        'overview': (
            'A forest-estate championship layout built into a former coffee farm, best known for a punishing '
            '640-yard closing par five and a resort lunch pace that suits a relaxed second Nairobi round.'
        ),
        'holes_and_par': '18 holes | Par 72 | approx. 7,277 yards | includes a 640-yard Par 5',
        'holes': 18,
        'par': 72,
        'course_length': '18 holes with resort-style forest routing',
        'architect_designer': 'Tom Macauley forest estate routing over a former coffee farm',
        'year_opened': 1994,
        'course_style': 'resort',
        'turf_grass_type': 'Tree-lined kikuyu fairways with water-influenced approach zones',
        'signature_features': (
            'Pro tip: Windsor punishes impatient hero lines. On the 640-yard closing Par 5, treat the second '
            'shot as a placement decision and keep the third wedge below the hole.'
        ),
        'signature_holes': 'The 640-yard 18th, one of the longest closing par fives in East African golf',
        'difficulty_level': 'Demanding carries, mature trees, and a strong finishing stretch',
        'best_suited_for': 'Longer hitters who enjoy a forest-estate resort setting',
        'best_time_to_play': 'Earlier starts for cooler conditions and a relaxed resort lunch afterward',
        'is_championship': True,
        'practice_range': True,
        'putting_green': True,
        'short_game_area': True,
        'golf_academy': False,
        'clubhouse': True,
        'restaurant': True,
        'pro_shop': True,
        'walking_allowed': True,
        'golf_carts': True,
        'caddies': True,
        'rental_clubs': True,
        'locker_rooms': True,
        'changing_rooms': True,
        'booking_window': 'Confirm cart and caddie preference 1-2 weeks ahead',
        'average_playing_time': '4.5 hours',
        'peak_season': 'July-September and over the December holidays',
        'best_playing_months': 'June-October',
        'collared_shirts_required': True,
        'soft_spikes_required': True,
        'denim_allowed': False,
        'dress_code': 'Smart golf attire recommended; avoid denim, collarless tops, and non-golf footwear',
        'facilities': 'Resort clubhouse\nDriving range and short game area\nGolf carts subject to availability\nResort dining',
        'booking_notes': 'Confirm cart needs, caddie preference, and guest access before locking the day around airport or safari transfers',
        'arrival_notes': 'Build a wider arrival buffer because the resort grounds are larger with dedicated security checks',
        'distance_from_airport': 'About 50-80 minutes from JKIA',
        'latitude': -1.2189,
        'longitude': 36.8886,
        'is_featured': False,
        'meta_title': 'Windsor Golf & Country Club | Nairobi Forest Resort Course | AfroLink Adventures',
        'meta_description': 'Play a former coffee-farm resort course with a famous 640-yard closing par five near Nairobi.',
        'hero_image_url': IMG['golf'][2],
    },
    {
        'key': 'great_rift',
        'region_key': 'rift',
        'name': 'Great Rift Valley Lodge & Golf Resort',
        'slug': 'great-rift-valley-lodge-golf-resort',
        'overview': (
            'An elevated escarpment layout above Lake Naivasha where wind, altitude, and long downhill '
            'views change how every yardage plays, best scheduled before the lake softens into boat safari time.'
        ),
        'holes_and_par': '18 holes | Par 71 | approx. 6,580 yards',
        'holes': 18,
        'par': 71,
        'course_length': '18 holes, elevated Rift Valley routing',
        'architect_designer': 'Thomas Fjastad escarpment resort routing',
        'year_opened': 2008,
        'course_style': 'mountain',
        'turf_grass_type': 'High-altitude kikuyu with firm escarpment lies',
        'signature_features': (
            'Pro tip: the Rift changes yardage perception. Account for elevation, wind, and downhill release '
            'before attacking pins that look shorter than they play.'
        ),
        'signature_holes': 'A run of escarpment-edge holes with views over Lake Naivasha and the valley floor',
        'difficulty_level': 'Scenic but exposed, with wind and elevation changing club selection',
        'best_suited_for': 'Golfers who enjoy dramatic scenery and are comfortable adjusting for wind and altitude',
        'best_time_to_play': 'Morning play for the clearest light and calmer wind before lake activity',
        'is_championship': True,
        'practice_range': True,
        'putting_green': True,
        'short_game_area': False,
        'golf_academy': False,
        'clubhouse': True,
        'restaurant': True,
        'pro_shop': False,
        'walking_allowed': True,
        'golf_carts': True,
        'caddies': True,
        'rental_clubs': True,
        'locker_rooms': True,
        'changing_rooms': False,
        'booking_window': 'Reserve tee times 1-2 weeks ahead, longer during the dry-season peak',
        'average_playing_time': '4 hours',
        'peak_season': 'Dry months with clearer escarpment views',
        'best_playing_months': 'June-September',
        'collared_shirts_required': True,
        'soft_spikes_required': True,
        'denim_allowed': False,
        'dress_code': 'Standard golf attire with a light layer, since the escarpment can shift from cool to bright quickly',
        'facilities': 'Resort clubhouse\nPractice range and putting green\nCaddie support subject to availability\nLodge dining nearby',
        'booking_notes': 'Pair tee times carefully with Naivasha boat safaris or Crescent Island walks so the day does not feel rushed',
        'arrival_notes': 'Allow time for the drive up the escarpment and for guests to settle before play',
        'distance_from_airport': 'About 2 to 2.5 hours from Nairobi',
        'latitude': -0.7205,
        'longitude': 36.3532,
        'is_featured': False,
        'meta_title': 'Great Rift Valley Lodge & Golf Resort | Escarpment Golf | AfroLink Adventures',
        'meta_description': 'Play an elevated escarpment course above Lake Naivasha, paired naturally with hippo and walking safaris.',
        'hero_image_url': IMG['golf'][4],
    },
    {
        'key': 'fairmont',
        'region_key': 'mount_kenya',
        'name': 'Fairmont Mount Kenya Safari Club',
        'slug': 'fairmont-mount-kenya-safari-club',
        'overview': (
            'A relaxed 9-hole equator-line course at 2,150 metres, used more for tempo reset and wedge '
            'calibration than as the trip\'s competitive centerpiece.'
        ),
        'holes_and_par': '9 holes | Par 27 executive course | equator-line layout',
        'holes': 9,
        'par': 27,
        'course_length': '9-hole equator-line resort course',
        'architect_designer': 'Historic Mount Kenya Safari Club estate course',
        'year_opened': 1959,
        'course_style': 'resort',
        'turf_grass_type': 'Cool highland kikuyu with compact target greens',
        'signature_features': (
            'Pro tip: this is precision practice at altitude, not a power test. Use it for wedge-distance '
            'calibration and a tempo reset before longer championship rounds.'
        ),
        'signature_holes': 'A short par 3 played directly across the equator line, a favourite photo stop',
        'difficulty_level': 'Relaxed highland golf where altitude and setting are the main character',
        'best_suited_for': 'Golfers wanting a scenic, low-pressure round between longer championship days',
        'best_time_to_play': 'Late morning or early afternoon, after the cool highland start has warmed',
        'is_championship': False,
        'practice_range': True,
        'putting_green': True,
        'short_game_area': False,
        'golf_academy': False,
        'clubhouse': True,
        'restaurant': True,
        'pro_shop': False,
        'walking_allowed': True,
        'golf_carts': False,
        'caddies': True,
        'rental_clubs': True,
        'locker_rooms': True,
        'changing_rooms': True,
        'booking_window': 'Can usually be arranged with a day\'s notice through the resort',
        'average_playing_time': '1.5 to 2 hours',
        'peak_season': 'Year-round; altitude keeps conditions mild',
        'best_playing_months': 'June-October, January-February',
        'collared_shirts_required': True,
        'soft_spikes_required': True,
        'denim_allowed': False,
        'dress_code': 'Smart casual golf attire; bring a light layer for highland conditions',
        'facilities': 'Resort golf access\nClubhouse support\nEquipment coordination subject to availability\nSpa and dining nearby',
        'booking_notes': 'Best positioned as a scenic recovery round rather than the most competitive golf day in the itinerary',
        'arrival_notes': 'Guests should account for altitude, cooler air, and a slower resort pace',
        'distance_from_airport': 'About 3-3.5 hours from Nairobi, or a short domestic hop via Nanyuki',
        'latitude': 0.0163,
        'longitude': 37.0714,
        'is_featured': False,
        'meta_title': 'Fairmont Mount Kenya Safari Club Golf | Equator-Line Course | AfroLink Adventures',
        'meta_description': 'Play a relaxed 9-hole course straddling the equator at 2,150 metres, before or after Ol Pejeta.',
        'hero_image_url': IMG['golf'][5],
    },
    {
        'key': 'vipingo',
        'region_key': 'coast',
        'name': 'Vipingo Ridge (Baobab Course)',
        'slug': 'vipingo-ridge-baobab-course',
        'overview': (
            'A wind-first coastal championship test through ancient baobab groves, best played early before '
            'the sea breeze builds, then recovered beside villa pools and ocean air.'
        ),
        'holes_and_par': '18 holes | Par 72 | approx. 7,255 yards',
        'holes': 18,
        'par': 72,
        'course_length': '18 holes, coastal championship routing',
        'architect_designer': 'David Jones coastal championship design',
        'year_opened': 2010,
        'course_style': 'resort',
        'turf_grass_type': 'Paspalum coastal turf built for humid Indian Ocean conditions',
        'signature_features': (
            'Pro tip: Baobab Course strategy is wind-first. Hold flighted approaches against the coastal '
            'breeze and choose conservative landing shelves when pins sit near run-offs.'
        ),
        'signature_holes': 'Several holes routed directly around centuries-old baobab trees left in play',
        'difficulty_level': 'Premium coastal test with wind, heat, and strategic carries',
        'best_suited_for': 'Golfers comfortable shaping shots against a strong sea breeze',
        'best_time_to_play': 'Early tee times, strongly preferred to avoid peak coastal heat and wind',
        'is_championship': True,
        'practice_range': True,
        'putting_green': True,
        'short_game_area': True,
        'golf_academy': True,
        'clubhouse': True,
        'restaurant': True,
        'pro_shop': True,
        'walking_allowed': True,
        'golf_carts': True,
        'caddies': True,
        'rental_clubs': True,
        'locker_rooms': True,
        'changing_rooms': True,
        'booking_window': 'Confirm tee times and villa logistics together, especially in peak holiday windows',
        'average_playing_time': '4 to 4.5 hours',
        'peak_season': 'December-March and July-August',
        'best_playing_months': 'January-March, July-September',
        'collared_shirts_required': True,
        'soft_spikes_required': True,
        'denim_allowed': False,
        'dress_code': 'Lightweight golf attire, sun protection, and proper golf shoes; avoid denim and heavy fabrics',
        'facilities': 'Clubhouse and dining\nPractice range and short game area\nGolf carts subject to availability\nCoastal villa access nearby',
        'booking_notes': 'Confirm tee times and villa logistics together, especially in peak holiday windows',
        'arrival_notes': 'Guests should hydrate early and use sunscreen; coastal conditions feel more demanding than the scorecard suggests',
        'distance_from_airport': 'About 30-45 minutes from Mombasa (MBA) / Vipingo airstrip access',
        'latitude': -3.8701,
        'longitude': 39.8305,
        'is_featured': True,
        'meta_title': 'Vipingo Ridge Baobab Course | Kenya Coastal Golf | AfroLink Adventures',
        'meta_description': 'Play a wind-first championship course through ancient baobab groves on Kenya\'s north coast.',
        'hero_image_url': IMG['golf'][3],
    },
]


# ---------------------------------------------------------------------------
# 4. Safari destinations
# ---------------------------------------------------------------------------

SAFARI_DESTINATIONS = [
    {
        'key': 'nairobi_np',
        'region_key': 'nairobi',
        'name': 'Nairobi National Park',
        'slug': 'nairobi-national-park',
        'overview': (
            'The only national park bordering a major capital, offering real big-game timing without '
            'abandoning Karen golf logistics or a same-day return to the city.'
        ),
        'history': 'Gazetted in 1946 as Kenya\'s first national park, established to protect wildlife corridors against Nairobi\'s expansion.',
        'conservation_significance': 'Safeguards black rhino, lion, and plains game habitat directly beside a city of five million people.',
        'landscape_description': 'Open savannah and acacia woodland framed by the Nairobi skyline on clear mornings.',
        'key_wildlife': 'Black rhino, lion, buffalo, plains game, and skyline-backed game drives timed around Karen, Muthaiga, and Windsor tee sheets.',
        'big_five_available': True,
        'common_wildlife': 'Zebra, giraffe, buffalo, eland, and a strong resident bird population',
        'rare_wildlife': 'Black rhino sightings when conditions align; occasional leopard',
        'birdwatching': True,
        'seasonal_migration': False,
        'photography_opportunities': 'Skyline-backed game drives at golden hour are the park\'s signature shot',
        'game_drives': True,
        'walking_safaris': False,
        'night_drives': False,
        'boat_safaris': False,
        'balloon_safaris': False,
        'guided_tours': True,
        'self_drive_allowed': True,
        'best_season': 'Excellent year-round, with drier months offering easier wildlife visibility',
        'peak_season': 'June-October and January-February',
        'green_season': 'March-May, quieter roads and lush landscapes',
        'migration_season': 'Not applicable; this park does not host the wildebeest migration',
        'best_months': 'June-October, January-February',
        'typical_duration': 'Half day to full day',
        'experience_style': 'Urban-edge game drive with rare proximity to the city',
        'distance_from_airport': '20-45 minutes from JKIA / Wilson depending on gate used',
        'driving_time': '30-60 minutes from Karen-area golf clubs',
        'internal_flights_available': False,
        'park_opening_hours': '06:00 to 19:00; early entry preferred',
        'access_notes': 'Best routed from Karen, Langata, or central Nairobi with early starts to reduce traffic and maximize wildlife activity',
        'clothing_recommendations': 'Neutral layers, closed shoes, and a sun hat',
        'weather_notes': 'Cool mornings; sun strengthens quickly by mid-morning',
        'camera_recommendations': 'Binoculars plus a mid-range zoom lens for open savannah distances',
        'luggage_recommendations': 'Not applicable for a half or full day visit',
        'park_regulations': 'Stay inside the vehicle except at designated picnic points; follow ranger guidance at all times',
        'packing_notes': 'Sun protection, binoculars, and a light jacket for early starts',
        'conservation_notes': 'A high-value conservation area because it protects wildlife movement beside a major capital city',
        'need_to_know': (
            'Early morning drives are usually stronger than late starts.\n'
            'Traffic buffers matter when pairing this with golf or airport transfers.\n'
            'This is a real park experience, not a fenced wildlife park.'
        ),
        'latitude': -1.3733,
        'longitude': 36.8172,
        'is_featured': True,
        'meta_title': 'Nairobi National Park | Big Game Beside the Capital | AfroLink Adventures',
        'meta_description': 'A city-edge game drive for black rhino, lion, and plains game, minutes from Karen and Nairobi\'s golf clubs.',
        'hero_image_url': IMG['safari'][0],
    },
    {
        'key': 'naivasha_hippo',
        'region_key': 'rift',
        'name': 'Lake Naivasha',
        'slug': 'lake-naivasha',
        'overview': (
            'A soft-adventure boat safari across freshwater channels thick with hippo, fish eagle, and '
            'papyrus birdlife, timed for golden hour after a morning round at Great Rift Valley.'
        ),
        'history': 'A working farming lake since the early 1900s, now Kenya\'s main freshwater boat-safari destination.',
        'conservation_significance': 'A Ramsar wetland site supporting one of East Africa\'s densest hippo populations.',
        'landscape_description': 'A freshwater lake edged by papyrus beds, yellow-barked acacia, and open escarpment views.',
        'key_wildlife': 'Boat-based hippo encounters, fish eagles, papyrus-edge birdlife, and golden-hour water access after Great Rift Valley Lodge golf.',
        'big_five_available': False,
        'common_wildlife': 'Hippo, fish eagle, pelican, cormorant, and giraffe on the lakeshore ranches',
        'rare_wildlife': 'Occasional sightings of African fish eagle hunting displays and rare waterbird species',
        'birdwatching': True,
        'seasonal_migration': False,
        'photography_opportunities': 'Low-boat hippo shots and fish eagle hunting sequences at golden hour',
        'game_drives': False,
        'walking_safaris': False,
        'night_drives': False,
        'boat_safaris': True,
        'balloon_safaris': False,
        'guided_tours': True,
        'self_drive_allowed': False,
        'best_season': 'Good year-round, with wind and lake conditions shaping exact timings',
        'peak_season': 'June-September, calmer water most mornings',
        'green_season': 'March-May, higher lake levels and lush shoreline',
        'migration_season': 'Not applicable',
        'best_months': 'Year-round with a morning preference',
        'typical_duration': '1 to 2 hours on the water',
        'experience_style': 'Soft adventure boat safari with birdlife and hippo viewing',
        'distance_from_airport': 'About 1.5-2 hours from Nairobi',
        'driving_time': '20 minutes from Loldia House or Great Rift Valley Lodge',
        'internal_flights_available': False,
        'park_opening_hours': 'Boat departures typically run 07:00-18:00',
        'access_notes': 'Best paired with Loldia House, Great Rift Valley golf, or a relaxed lake-facing day',
        'clothing_recommendations': 'Light layers and sun protection; a hat that ties on is useful on open water',
        'weather_notes': 'Wind typically builds by early afternoon, affecting boat comfort',
        'camera_recommendations': 'A dry bag or protective pouch for cameras is essential on the water',
        'luggage_recommendations': 'Not applicable for this excursion',
        'park_regulations': 'Respect posted hippo viewing distances; boat operators set minimum approach limits',
        'packing_notes': 'Light layer, sun protection, and a dry bag or protective pouch for cameras',
        'conservation_notes': 'Lake ecology is sensitive, so responsible boat operators and respectful viewing distances matter',
        'need_to_know': (
            'Boat departures depend on weather and water conditions.\n'
            'This is gentle but still exposed to sun and wind; a hat and sunscreen matter.\n'
            'Best kept unrushed rather than squeezed between long transfers.'
        ),
        'latitude': -0.7714,
        'longitude': 36.3492,
        'is_featured': False,
        'meta_title': 'Lake Naivasha Hippo Safaris | Rift Valley Boat Safari | AfroLink Adventures',
        'meta_description': 'A golden-hour boat safari among hippo channels and fish eagles, paired naturally with Rift Valley golf.',
        'hero_image_url': IMG['safari'][1],
    },
    {
        'key': 'crescent_island',
        'region_key': 'rift',
        'name': 'Crescent Island',
        'slug': 'crescent-island',
        'overview': (
            'A rare predator-free walking safari across an open peninsula where giraffe, zebra, and '
            'antelope graze in the open, ideal for low-impact movement between golf and spa recovery.'
        ),
        'history': 'A former film location turned private wildlife sanctuary on a peninsula jutting into Lake Naivasha.',
        'conservation_significance': 'A predator-free environment that allows safe, close walking access to plains game.',
        'landscape_description': 'Open grassland peninsula bordered by Lake Naivasha on three sides.',
        'key_wildlife': 'Guided walking safari terrain with giraffe, zebra, antelope, and open-lake views suited to low-impact movement between golf and spa recovery.',
        'big_five_available': False,
        'common_wildlife': 'Giraffe, zebra, waterbuck, impala, and wildebeest',
        'rare_wildlife': 'Occasional colobus monkey sightings along the tree line',
        'birdwatching': True,
        'seasonal_migration': False,
        'photography_opportunities': 'Close, ground-level shots of giraffe and zebra without a vehicle in frame',
        'game_drives': False,
        'walking_safaris': True,
        'night_drives': False,
        'boat_safaris': True,
        'balloon_safaris': False,
        'guided_tours': True,
        'self_drive_allowed': False,
        'best_season': 'Best in dry or lightly wet conditions when walking trails are comfortable',
        'peak_season': 'June-September',
        'green_season': 'March-May, greener grazing but muddier trails',
        'migration_season': 'Not applicable',
        'best_months': 'June-October',
        'typical_duration': '2 to 3 hours',
        'experience_style': 'Guided walking safari among plains game',
        'distance_from_airport': 'About 1.5-2 hours from Nairobi',
        'driving_time': '15 minutes by boat transfer from the Naivasha shoreline',
        'internal_flights_available': False,
        'park_opening_hours': 'Access typically 07:00-17:00 via boat transfer',
        'access_notes': 'Works well from Naivasha lodges and pairs naturally with Rift Valley golf',
        'clothing_recommendations': 'Comfortable walking shoes, neutral clothing, and a sun hat',
        'weather_notes': 'Open ground offers little shade; midday heat is more noticeable than on the water',
        'camera_recommendations': 'A standard zoom is sufficient given the close walking proximity to wildlife',
        'luggage_recommendations': 'Not applicable for this excursion',
        'park_regulations': 'Guests must stay with the guide at all times; no approaching wildlife directly',
        'packing_notes': 'Comfortable walking shoes, neutral clothing, sun protection, and water',
        'conservation_notes': 'Walking experiences require careful guiding and calm guest behaviour around wildlife',
        'need_to_know': (
            'This is a walking activity, so mobility and comfort on uneven ground matter.\n'
            'Midday heat can reduce comfort; morning slots are preferred.\n'
            'Guests should follow guide instructions closely at all times.'
        ),
        'latitude': -0.7659,
        'longitude': 36.3057,
        'is_featured': False,
        'meta_title': 'Crescent Island Walking Safaris | Naivasha Peninsula | AfroLink Adventures',
        'meta_description': 'A rare predator-free walking safari among giraffe and zebra on a Lake Naivasha peninsula.',
        'hero_image_url': IMG['safari'][2],
    },
    {
        'key': 'ol_pejeta',
        'region_key': 'mount_kenya',
        'name': 'Ol Pejeta Conservancy',
        'slug': 'ol-pejeta-conservancy',
        'overview': (
            'A private conservancy built on rhino protection and predator research, with the kind of '
            'off-road and night-drive access national parks rarely allow, best given a full day or an overnight extension.'
        ),
        'history': 'Converted from a cattle ranch into East Africa\'s largest black rhino sanctuary, now a leading community-conservation model.',
        'conservation_significance': 'Home to the last two northern white rhino and a flagship black rhino breeding programme.',
        'landscape_description': 'Open savannah and acacia bushland at the base of the Mount Kenya massif.',
        'key_wildlife': 'Rhino conservation, predator tracking, collared lion pride monitoring, and high-value private conservancy access from the Mount Kenya circuit.',
        'big_five_available': True,
        'common_wildlife': 'Elephant, buffalo, zebra, giraffe, and healthy predator populations',
        'rare_wildlife': 'The world\'s last two northern white rhino, plus regular black rhino and chimpanzee sanctuary visits',
        'birdwatching': True,
        'seasonal_migration': False,
        'photography_opportunities': 'Off-road access for close predator and rhino photography, rare among Kenyan parks',
        'game_drives': True,
        'walking_safaris': True,
        'night_drives': True,
        'boat_safaris': False,
        'balloon_safaris': False,
        'guided_tours': True,
        'self_drive_allowed': False,
        'best_season': 'Excellent year-round, with dry windows often improving predator and rhino visibility',
        'peak_season': 'June-October and January-February',
        'green_season': 'March-May, lush landscapes with fewer vehicles on the ground',
        'migration_season': 'Not applicable',
        'best_months': 'June-October, January-February',
        'typical_duration': 'Full day or overnight extension',
        'experience_style': 'Private conservancy safari with rhino, predator, and conservation depth',
        'distance_from_airport': 'About 3 hours by road from JKIA, or a short domestic hop to Nanyuki',
        'driving_time': '45 minutes to 1 hour from Mount Kenya circuit bases',
        'internal_flights_available': True,
        'park_opening_hours': 'Game drives run dawn to dusk, with pre-arranged night drives after dark',
        'access_notes': 'Best routed from the Mount Kenya region with enough time for both transfer and game viewing',
        'clothing_recommendations': 'Neutral layers, binoculars, camera equipment, and a warm layer for early drives',
        'weather_notes': 'Mornings are cool at this altitude; midday warms quickly under open sky',
        'camera_recommendations': 'A longer telephoto zoom rewards off-road proximity to predators and rhino',
        'luggage_recommendations': 'Soft bags recommended if combining with a domestic flight sector',
        'park_regulations': 'Night drives and off-road tracking require conservancy permits, arranged in advance by the concierge',
        'packing_notes': 'Neutral layers, binoculars, camera equipment, sun protection, and a warm layer for early drives',
        'conservation_notes': 'Important rhino protection and conservancy work make this a strong fit for guests who value impact as well as sightings',
        'need_to_know': (
            'Do not treat this as a short add-on if wildlife is a priority; it rewards a full day.\n'
            'Early and late drives are more rewarding than midday movement.\n'
            'Night drives and chimpanzee sanctuary visits should be confirmed ahead of time.'
        ),
        'latitude': 0.0084,
        'longitude': 36.9508,
        'is_featured': True,
        'meta_title': 'Ol Pejeta Conservancy | Rhino & Predator Safari | AfroLink Adventures',
        'meta_description': 'A private conservancy safari for rhino conservation, predator tracking, and night drives near Mount Kenya.',
        'hero_image_url': IMG['safari'][4],
    },
    {
        'key': 'tsavo',
        'region_key': 'coast',
        'name': 'Tsavo National Parks',
        'slug': 'tsavo-national-parks',
        'overview': (
            'Red-earth wilderness on a genuinely large scale, best used as a multi-night bridge between '
            'coastal golf and inland travel rather than a rushed day trip.'
        ),
        'history': 'Gazetted in 1948 as one of Kenya\'s original national parks, once notorious for its early lion prides.',
        'conservation_significance': 'One of the world\'s largest protected elephant populations, with ongoing anti-poaching operations.',
        'landscape_description': 'Vast red-earth savannah, lava flows, and baobab-dotted plains split into East and West sectors.',
        'key_wildlife': 'Red elephant country, lava flows, big-sky wilderness, and a strong coastal-to-bush safari extension after Vipingo Ridge.',
        'big_five_available': True,
        'common_wildlife': 'Elephant, buffalo, giraffe, zebra, and healthy lion prides',
        'rare_wildlife': 'Occasional leopard sightings and the endemic Hirola antelope near the Tsavo boundary',
        'birdwatching': True,
        'seasonal_migration': False,
        'photography_opportunities': 'Red-dust elephant herds against big-sky landscapes, especially at Mzima Springs',
        'game_drives': True,
        'walking_safaris': False,
        'night_drives': False,
        'boat_safaris': False,
        'balloon_safaris': False,
        'guided_tours': True,
        'self_drive_allowed': False,
        'best_season': 'Dry periods generally improve wildlife visibility; green season can be excellent for landscape photography',
        'peak_season': 'June-October and January-February',
        'green_season': 'March-May, dramatic skies and fewer vehicles',
        'migration_season': 'Not applicable',
        'best_months': 'June-October, January-March',
        'typical_duration': 'Overnight or multi-night extension',
        'experience_style': 'Large-scale wilderness safari with red-earth landscapes and elephant movement',
        'distance_from_airport': 'Accessible from Mombasa (MBA) or coastal airstrips',
        'driving_time': '2 to 3 hours from Vipingo Ridge depending on the gate used',
        'internal_flights_available': True,
        'park_opening_hours': '06:00 to 19:00',
        'access_notes': 'Best paired with coastal routing or used as a wilderness bridge between coast and inland travel',
        'clothing_recommendations': 'Soft luggage, neutral clothing, sun protection, and binoculars',
        'weather_notes': 'Heat can be significant year-round, especially in Tsavo East\'s lower-lying terrain',
        'camera_recommendations': 'A mid-to-long zoom lens suits the park\'s open distances',
        'luggage_recommendations': 'Soft-sided bags recommended for light-aircraft sectors',
        'park_regulations': 'Stay on designated tracks; off-road driving is not permitted in either sector',
        'packing_notes': 'Soft luggage, neutral clothing, sun protection, binoculars, and patience for larger landscapes',
        'conservation_notes': 'Tsavo rewards guests who appreciate space, tracking, and ecosystem scale rather than only checklist sightings',
        'need_to_know': (
            'Distances are large, so pacing matters more here than in smaller parks.\n'
            'Heat can be significant, especially in Tsavo East.\n'
            'This extension works best with at least one overnight stay.'
        ),
        'latitude': -3.3833,
        'longitude': 38.5667,
        'is_featured': False,
        'meta_title': 'Tsavo East & West National Parks | Kenya Wilderness Safari | AfroLink Adventures',
        'meta_description': 'A multi-night red-earth wilderness extension for elephant country, bridging coastal golf and inland Kenya.',
        'hero_image_url': IMG['safari'][3],
    },
    {
        'key': 'amboseli',
        'region_key': 'nairobi',
        'name': 'Amboseli National Park',
        'slug': 'amboseli-national-park',
        'overview': (
            'The classic elephant-against-Kilimanjaro shot, reached by a short flight or a half-day drive '
            'from Nairobi and best scheduled for early morning when the mountain is least likely to be cloud-hidden.'
        ),
        'history': 'Gazetted in 1974 around the seasonal Amboseli swamp system that has sustained elephant herds for generations.',
        'conservation_significance': 'Supports one of Africa\'s best-studied and most habituated elephant populations.',
        'landscape_description': 'Dry lake-bed plains and swamp-fed grassland directly beneath Mount Kilimanjaro.',
        'key_wildlife': 'Large elephant herds set against Kilimanjaro\'s backdrop, plus healthy plains game and swamp birdlife.',
        'big_five_available': True,
        'common_wildlife': 'Elephant, zebra, wildebeest, giraffe, and hippo in the swamp channels',
        'rare_wildlife': 'Occasional cheetah sightings on the open lake-bed plains',
        'birdwatching': True,
        'seasonal_migration': False,
        'photography_opportunities': 'Elephant herds framed against Kilimanjaro, strongest at sunrise before cloud builds',
        'game_drives': True,
        'walking_safaris': False,
        'night_drives': False,
        'boat_safaris': False,
        'balloon_safaris': False,
        'guided_tours': True,
        'self_drive_allowed': False,
        'best_season': 'Excellent June-October and January-February when skies are clearest',
        'peak_season': 'June-October, January-February',
        'green_season': 'March-May, greener swamp margins but frequent cloud cover on Kilimanjaro',
        'migration_season': 'Not applicable',
        'best_months': 'June-October, January-February',
        'typical_duration': 'Full day, or overnight for a sunrise and sunset drive combination',
        'experience_style': 'Classic elephant safari with an iconic mountain backdrop',
        'distance_from_airport': 'About 45 minutes by air from Nairobi, or 4 hours by road via Namanga',
        'driving_time': '4 hours from Nairobi via Namanga',
        'internal_flights_available': True,
        'park_opening_hours': '06:00 to 18:30',
        'access_notes': 'Best combined with a Nairobi base via a short flight rather than a same-day round trip by road',
        'clothing_recommendations': 'Neutral layers, sun protection, and a hat with a chin strap for open-vehicle dust',
        'weather_notes': 'Dust is a factor on the dry lake bed; cloud often builds over Kilimanjaro by mid-morning',
        'camera_recommendations': 'A wide-angle lens captures the mountain backdrop alongside a zoom for elephant detail',
        'luggage_recommendations': 'Soft-sided bags recommended if flying in',
        'park_regulations': 'Off-road driving is not permitted; stay on designated tracks',
        'packing_notes': 'Neutral clothing, sun protection, and a dust-proof camera bag',
        'conservation_notes': 'Long-term elephant research here has shaped much of what is known about elephant family structure across Africa',
        'need_to_know': (
            'Kilimanjaro is most visible at sunrise, before afternoon cloud builds.\n'
            'Flying in saves significant time compared with the Namanga road route.\n'
            'Dust can be heavy in dry months; pack accordingly for camera gear.'
        ),
        'latitude': -2.6527,
        'longitude': 37.2606,
        'is_featured': False,
        'meta_title': 'Amboseli National Park | Elephants & Kilimanjaro | AfroLink Adventures',
        'meta_description': 'A classic elephant safari beneath Mount Kilimanjaro, reachable by short flight from Nairobi.',
        'hero_image_url': IMG['safari'][5],
    },
    {
        'key': 'hells_gate',
        'region_key': 'rift',
        'name': 'Hell\'s Gate National Park',
        'slug': 'hells-gate-national-park',
        'overview': (
            'One of the only Kenyan parks where guests can cycle or walk freely among plains game, set '
            'inside a dramatic gorge of volcanic cliffs and geothermal steam vents near Lake Naivasha.'
        ),
        'history': 'Named by early explorers for its towering red cliffs, later developed with geothermal power stations that still operate within the park boundary.',
        'conservation_significance': 'A low-predator environment that permits rare self-guided walking and cycling access to wildlife.',
        'landscape_description': 'A dramatic gorge of red volcanic cliffs, geothermal steam vents, and open grassland.',
        'key_wildlife': 'Zebra, giraffe, buffalo, and klipspringer across open grassland and gorge walls, with active geothermal steam vents throughout.',
        'big_five_available': False,
        'common_wildlife': 'Zebra, giraffe, eland, buffalo, and warthog',
        'rare_wildlife': 'Klipspringer on the gorge cliffs and occasional verreaux\'s eagle overhead',
        'birdwatching': True,
        'seasonal_migration': False,
        'photography_opportunities': 'Cyclists and walkers framed against Fischer\'s Tower and the volcanic gorge walls',
        'game_drives': True,
        'walking_safaris': True,
        'night_drives': False,
        'boat_safaris': False,
        'balloon_safaris': False,
        'guided_tours': True,
        'self_drive_allowed': True,
        'best_season': 'Comfortable year-round; drier months make gorge trails easier underfoot',
        'peak_season': 'June-September',
        'green_season': 'March-May, greener gorge walls but slippery trails',
        'migration_season': 'Not applicable',
        'best_months': 'June-October',
        'typical_duration': '2 to 4 hours for cycling or the gorge walk',
        'experience_style': 'Self-guided walking and cycling safari through a volcanic gorge',
        'distance_from_airport': 'About 1.5-2 hours from Nairobi',
        'driving_time': '20-30 minutes from Naivasha-area lodges',
        'internal_flights_available': False,
        'park_opening_hours': '06:00 to 18:00',
        'access_notes': 'Best paired with a Naivasha stay; the gorge walk requires a licensed local guide',
        'clothing_recommendations': 'Sturdy walking shoes, sun protection, and a light jacket for the cooler gorge floor',
        'weather_notes': 'The gorge floor stays cooler than the open plains above it',
        'camera_recommendations': 'A wide lens for the gorge walls; a zoom for wildlife on the plains above',
        'luggage_recommendations': 'Not applicable for this excursion',
        'park_regulations': 'A licensed guide is mandatory for the lower gorge walk; cycling is permitted on marked routes only',
        'packing_notes': 'Sturdy shoes, water, and sun protection for an active, partly on-foot day',
        'conservation_notes': 'Geothermal operations and conservation coexist here, making it a useful example of shared-use land management',
        'need_to_know': (
            'A licensed guide is mandatory for the lower gorge walk, arranged at the gate.\n'
            'Cycling among wildlife is genuinely self-guided but requires reasonable fitness.\n'
            'Flash flooding can close the lower gorge without notice in wet weather.'
        ),
        'latitude': -0.9131,
        'longitude': 36.3183,
        'is_featured': False,
        'meta_title': 'Hell\'s Gate National Park | Cycling & Gorge Walks | AfroLink Adventures',
        'meta_description': 'Cycle or walk freely among zebra and giraffe through a volcanic gorge near Lake Naivasha.',
        'hero_image_url': IMG['safari'][6],
    },
]


# ---------------------------------------------------------------------------
# 5. Wellness experiences
# ---------------------------------------------------------------------------

WELLNESS = [
    {
        'key': 'blixen_tea',
        'region_key': 'nairobi',
        'name_en': 'Karen Estate Spa Ritual',
        'name_de': 'Karen Estate Spa Ritual',
        'slug': 'karen-estate-spa-ritual',
        'category': 'spa',
        'overview': (
            'A private garden spa session designed for arrival decompression, built around a signature '
            'massage and quiet terrace time rather than a full treatment menu.'
        ),
        'wellness_purpose': 'Arrival decompression and gentle Nairobi recovery after long-haul travel',
        'typical_duration': '2 to 3 hours',
        'duration_choice': 'half_day',
        'treatment_style': 'Private garden treatment rooms with a signature massage and quiet terrace time',
        'ideal_for': 'Arrival decompression, non-golf partners, and gentle Nairobi recovery',
        'has_massage': True,
        'has_hydrotherapy': False,
        'has_sauna': False,
        'has_steam_room': False,
        'has_yoga': False,
        'has_meditation': False,
        'has_fitness': False,
        'has_pool': True,
        'has_spa': True,
        'has_gym': False,
        'has_relaxation_lounge': True,
        'has_private_treatment_rooms': True,
        'inclusions': 'Private treatment room booking\n60-minute signature massage\nGarden terrace relaxation time\nHerbal tea service',
        'preparation_notes': 'Best scheduled after arrival or a morning round, when guests need calm rather than another transfer.',
        'arrival_time': 'Arrive 15 minutes early to settle before treatment',
        'clothing_notes': 'Comfortable loungewear; a spa robe is provided',
        'suitability_notes': 'Suitable for most guests, and especially useful when part of a group wants a lighter day.',
        'medical_considerations': 'Advise the therapist of pregnancy or recent injuries before the massage begins',
        'age_restrictions': 'Adult-focused treatments; confirm suitability for teens in advance',
        'health_notice': 'This is a leisure and recovery experience, not a medical treatment.',
        'is_featured': True,
        'meta_title': 'Karen Estate Spa Ritual | Nairobi Private Spa | AfroLink Adventures',
        'meta_description': 'A private garden spa session in Karen built for arrival decompression and gentle recovery.',
        'hero_image_url': IMG['wellness'][0],
    },
    {
        'key': 'volcanic_mud',
        'region_key': 'rift',
        'name_en': 'Rift Valley Mineral Mud Therapy',
        'name_de': 'Rift-Valley-Mineralschlammtherapie',
        'slug': 'rift-valley-mineral-mud-therapy',
        'category': 'thermal',
        'overview': (
            'A mineral-rich mud and thermal water treatment drawn from the Rift Valley\'s volcanic geology, '
            'aimed squarely at muscle recovery after escarpment golf or a long walking safari.'
        ),
        'wellness_purpose': 'Muscle recovery and thermal reset after golf or walking activity',
        'typical_duration': '60 to 90 minutes',
        'duration_choice': '60_min',
        'treatment_style': 'Thermal mud application followed by mineral-water hydrotherapy',
        'ideal_for': 'Guests recovering from consecutive golf, walking, or transfer-heavy days',
        'has_massage': True,
        'has_hydrotherapy': True,
        'has_sauna': True,
        'has_steam_room': False,
        'has_yoga': False,
        'has_meditation': False,
        'has_fitness': False,
        'has_pool': False,
        'has_spa': True,
        'has_gym': False,
        'has_relaxation_lounge': True,
        'has_private_treatment_rooms': True,
        'inclusions': 'Thermal mud application\nMineral-water hydrotherapy circuit\nRecovery time buffer\nPrivate transfer coordination',
        'preparation_notes': 'Bring swimwear, sandals, sun protection, and a change of clothing.',
        'arrival_time': 'Arrive 20 minutes before the scheduled slot',
        'clothing_notes': 'Swimwear required for the hydrotherapy sections; a robe is provided',
        'suitability_notes': 'Guests with sensitive skin or heat sensitivity should flag this before final scheduling.',
        'medical_considerations': 'Advise the therapist of cardiovascular concerns or skin conditions before treatment',
        'age_restrictions': 'Recommended for adults; confirm suitability for guests under 16',
        'health_notice': 'This is a wellness experience. Guests with medical concerns should consult their own practitioner before thermal or heat-based treatments.',
        'is_featured': False,
        'meta_title': 'Rift Valley Mineral Mud Therapy | Naivasha Thermal Recovery | AfroLink Adventures',
        'meta_description': 'A mineral mud and hydrotherapy treatment for muscle recovery after Rift Valley golf and safaris.',
        'hero_image_url': IMG['wellness'][2],
    },
    {
        'key': 'equine_treks',
        'region_key': 'mount_kenya',
        'name_en': 'Mount Kenya Highland Yoga Retreat',
        'name_de': 'Mount-Kenya-Highland-Yoga-Retreat',
        'slug': 'mount-kenya-highland-yoga-retreat',
        'category': 'yoga',
        'overview': (
            'A morning yoga and breathwork session set in the highland gardens below Mount Kenya, using '
            'the cooler altitude air as part of the practice rather than fighting against coastal or city heat.'
        ),
        'wellness_purpose': 'Active outdoor reset and breath-led recovery at altitude',
        'typical_duration': '90 minutes to half day',
        'duration_choice': 'half_day',
        'treatment_style': 'Guided vinyasa and breathwork practice in open highland gardens',
        'ideal_for': 'Guests wanting active recovery between Mount Kenya golf and conservancy days',
        'has_massage': False,
        'has_hydrotherapy': False,
        'has_sauna': False,
        'has_steam_room': False,
        'has_yoga': True,
        'has_meditation': True,
        'has_fitness': True,
        'has_pool': True,
        'has_spa': False,
        'has_gym': False,
        'has_relaxation_lounge': True,
        'has_private_treatment_rooms': False,
        'inclusions': 'Guided morning yoga session\nBreathwork and meditation close\nMats and props provided\nHerbal tea after practice',
        'preparation_notes': 'Best scheduled early morning while the highland air is coolest.',
        'arrival_time': 'Arrive 10 minutes early to settle mats before the session starts',
        'clothing_notes': 'Comfortable, breathable layers; the highland morning air is cool before the sun rises fully',
        'suitability_notes': 'Suitable for all experience levels; the guide adapts pacing to the group.',
        'medical_considerations': 'Guests with joint or mobility concerns should mention this before the session so poses can be modified',
        'age_restrictions': 'Suitable for teens and adults; confirm for younger children',
        'health_notice': 'This is a wellness and movement practice, not a substitute for medical care.',
        'is_featured': False,
        'meta_title': 'Mount Kenya Highland Yoga Retreat | Nanyuki Wellness | AfroLink Adventures',
        'meta_description': 'A morning yoga and breathwork session in the highland gardens below Mount Kenya.',
        'hero_image_url': IMG['wellness'][5],
    },
    {
        'key': 'kuruwitu_reef',
        'region_key': 'coast',
        'name_en': 'Vipingo Oceanfront Spa Recovery',
        'name_de': 'Vipingo Oceanfront Spa Recovery',
        'slug': 'vipingo-oceanfront-spa-recovery',
        'category': 'spa',
        'overview': (
            'An ocean-air spa session built for post-round recovery after coastal golf, pairing a '
            'muscle-focused massage with villa-side pool downtime rather than a full resort spa menu.'
        ),
        'wellness_purpose': 'Post-round muscle recovery and heat relief after coastal golf',
        'typical_duration': '75 to 120 minutes',
        'duration_choice': '60_min',
        'treatment_style': 'Villa-based massage therapy with ocean-air relaxation time',
        'ideal_for': 'Golfers recovering from heat-exposed coastal rounds, and families wanting villa-side spa time',
        'has_massage': True,
        'has_hydrotherapy': False,
        'has_sauna': False,
        'has_steam_room': False,
        'has_yoga': False,
        'has_meditation': False,
        'has_fitness': False,
        'has_pool': True,
        'has_spa': True,
        'has_gym': False,
        'has_relaxation_lounge': True,
        'has_private_treatment_rooms': True,
        'inclusions': 'In-villa deep tissue or Swedish massage\nCooling face and scalp treatment\nOcean-air relaxation time\nChilled towel and hydration service',
        'preparation_notes': 'Best scheduled for late afternoon, directly after a round of golf.',
        'arrival_time': 'Therapist arrives at the villa at the scheduled time; no travel required',
        'clothing_notes': 'Light, breathable clothing; therapist provides draping for the massage',
        'suitability_notes': 'Suitable for most guests; mention sunburn or heat exhaustion symptoms before booking.',
        'medical_considerations': 'Flag any sunburn, dehydration, or muscle strain from the round so pressure can be adjusted',
        'age_restrictions': 'Adult-focused massage menu; separate light treatments available for teens',
        'health_notice': 'This is a leisure and recovery experience, not a medical treatment.',
        'is_featured': False,
        'meta_title': 'Vipingo Oceanfront Spa Recovery | Coastal Golf Spa | AfroLink Adventures',
        'meta_description': 'A villa-based ocean-air massage for post-round recovery after Baobab Course golf.',
        'hero_image_url': IMG['wellness'][3],
    },
    {
        'key': 'nanyuki_spa',
        'region_key': 'mount_kenya',
        'name_en': 'Fairmont Mount Kenya Club Spa',
        'name_de': 'Fairmont Mount Kenya Club Spa',
        'slug': 'fairmont-mount-kenya-club-spa',
        'category': 'spa',
        'overview': (
            'The Safari Club\'s resident spa, set in a converted highland wing with fireside relaxation '
            'areas, best used to recover from a conservancy game drive or the equator-line 9-hole round.'
        ),
        'wellness_purpose': 'Fireside recovery and highland relaxation after golf or conservancy days',
        'typical_duration': '60 to 150 minutes',
        'duration_choice': 'half_day',
        'treatment_style': 'Full-menu resort spa with massage, facials, and body treatments',
        'ideal_for': 'Guests recovering from Ol Pejeta game drives or the equator-line golf round',
        'has_massage': True,
        'has_hydrotherapy': True,
        'has_sauna': True,
        'has_steam_room': True,
        'has_yoga': False,
        'has_meditation': False,
        'has_fitness': True,
        'has_pool': True,
        'has_spa': True,
        'has_gym': True,
        'has_relaxation_lounge': True,
        'has_private_treatment_rooms': True,
        'inclusions': 'Choice of massage or facial treatment\nSauna and steam room access\nFireside relaxation lounge\nHerbal tea service',
        'preparation_notes': 'Best scheduled for late afternoon after a game drive or golf round.',
        'arrival_time': 'Arrive 15 minutes early to use the sauna or steam room before treatment',
        'clothing_notes': 'Swimwear for the sauna and steam circuit; a robe is provided throughout',
        'suitability_notes': 'Suitable for most guests; the full menu accommodates a range of preferences.',
        'medical_considerations': 'Advise on any heat sensitivity or cardiovascular concerns before using the sauna or steam room',
        'age_restrictions': 'Sauna and steam room typically restricted to guests over 16',
        'health_notice': 'This is a resort spa service, not a medical facility.',
        'is_featured': False,
        'meta_title': 'Fairmont Mount Kenya Club Spa | Nanyuki Resort Spa | AfroLink Adventures',
        'meta_description': 'A full-menu highland resort spa for recovery after Ol Pejeta game drives and equator-line golf.',
        'hero_image_url': IMG['wellness'][1],
    },
    {
        'key': 'naivasha_sauna',
        'region_key': 'rift',
        'name_en': 'Lake Naivasha Sauna & Steam Circuit',
        'name_de': 'Lake-Naivasha-Sauna-und-Dampf-Zirkel',
        'slug': 'lake-naivasha-sauna-steam-circuit',
        'category': 'recovery',
        'overview': (
            'A simple sauna and steam circuit built into a lakeshore lodge wing, used mainly to ease '
            'stiffness after escarpment golf or a long walking safari on Crescent Island.'
        ),
        'wellness_purpose': 'Muscle and joint recovery after escarpment golf or walking safaris',
        'typical_duration': '45 to 75 minutes',
        'duration_choice': '60_min',
        'treatment_style': 'Alternating sauna and steam room circuit with cool-down intervals',
        'ideal_for': 'Guests wanting quick, practical recovery rather than a full spa treatment',
        'has_massage': False,
        'has_hydrotherapy': True,
        'has_sauna': True,
        'has_steam_room': True,
        'has_yoga': False,
        'has_meditation': False,
        'has_fitness': False,
        'has_pool': False,
        'has_spa': False,
        'has_gym': False,
        'has_relaxation_lounge': True,
        'has_private_treatment_rooms': False,
        'inclusions': 'Sauna and steam room circuit access\nCool-down lounge time\nHerbal infusion service\nTowel and robe provided',
        'preparation_notes': 'Best scheduled for early evening after a full day of golf or walking.',
        'arrival_time': 'No booking required beyond confirming a time slot with the lodge',
        'clothing_notes': 'Swimwear required throughout the circuit',
        'suitability_notes': 'Suitable for most guests; those with heat sensitivity should limit session length.',
        'medical_considerations': 'Guests with cardiovascular conditions should consult a doctor before sauna or steam use',
        'age_restrictions': 'Recommended for guests over 16',
        'health_notice': 'This is a leisure recovery facility, not a supervised medical treatment.',
        'is_featured': False,
        'meta_title': 'Lake Naivasha Sauna & Steam Circuit | Rift Valley Recovery | AfroLink Adventures',
        'meta_description': 'A lakeshore sauna and steam circuit for easing stiffness after Rift Valley golf and walking safaris.',
        'hero_image_url': IMG['wellness'][4],
    },
]


# ---------------------------------------------------------------------------
# 6. Galleries (2-3 images per key, strictly category-matched to IMG pools)
#
# NOTE: 'fairmont' is a valid key in both ACCOMMODATIONS (the Safari Club
# hotel) and GOLF_COURSES (the equator-line 9-hole course). To keep every
# key unambiguous, GALLERIES/FAQS/OFFERS below are nested one level deeper
# by experience type: 'course' | 'safari' | 'stay' | 'wellness', matching
# the same type vocabulary used in RELATED.
# ---------------------------------------------------------------------------

GALLERIES = {
    'stay': {
        'hemingways': [
            (IMG['stay'][0], 'Garden suite verandas facing the Karen lawns.', 'Garden-Suite-Veranden mit Blick auf die Karen-Rasenflaechen.'),
            (IMG['stay'][1], 'Quiet city recovery before Karen and Muthaiga rounds.', 'Ruhige Stadterholung vor Karen- und Muthaiga-Runden.'),
        ],
        'loldia': [
            (IMG['stay'][3], 'Cottage rooms opening directly onto working farm gardens.', 'Cottage-Zimmer mit direktem Zugang zu Farmgaerten.'),
            (IMG['stay'][7], 'Lakeside pacing between escarpment golf and boat safaris.', 'Seenahes Tempo zwischen Escarpment-Golf und Bootssafaris.'),
        ],
        'fairmont': [
            (IMG['stay'][6], 'Highland club grounds framing the equator-line course.', 'Highland-Club-Anlage rund um den Aequatorlinien-Platz.'),
            (IMG['stay'][1], 'Fireside lounges for cooler mountain evenings.', 'Kaminlounges fuer kuehlere Bergabende.'),
        ],
        'vipingo_villas': [
            (IMG['stay'][2], 'Private villa pools beside the Baobab Course fairways.', 'Private Villenpools neben den Baobab-Course-Fairways.'),
            (IMG['stay'][7], 'Open-plan villa living built for family groups.', 'Offenes Villenwohnen fuer Familiengruppen.'),
        ],
        'giraffes': [
            (IMG['stay'][4], 'Manor lawns where the resident giraffe herd roams.', 'Herrenhausrasen, auf dem die ansaessige Giraffenherde umherzieht.'),
            (IMG['stay'][1], 'Period furnishings inside the 1930s manor house.', 'Historische Einrichtung im Herrenhaus aus den 1930er Jahren.'),
        ],
        'sarova_salt': [
            (IMG['stay'][5], 'Raised tents facing the floodlit conservancy waterhole.', 'Erhoehte Zelte mit Blick auf das angestrahlte Wasserloch.'),
            (IMG['stay'][6], 'Deck seating for evening wildlife watching.', 'Terrassensitzplaetze fuer abendliche Tierbeobachtung.'),
        ],
    },
    'course': {
        'karen': [
            (IMG['golf'][0], 'Tree-lined Nairobi parkland routing and approach angles.', 'Baumgesaeumtes Nairobi-Parkland-Routing und Angriffswinkel.'),
            (IMG['golf'][1], 'Green complex discipline along mature fairway corridors.', 'Gruenkomplex-Disziplin entlang reifer Fairway-Korridore.'),
        ],
        'muthaiga': [
            (IMG['golf'][6], 'Championship tee strategy on tournament-conditioned surfaces.', 'Championship-Tee-Strategie auf turnierfaehigen Spielflaechen.'),
            (IMG['golf'][3], 'Approach precision into protected Nairobi greens.', 'Praezise Annaeherung in geschuetzte Nairobi-Gruens.'),
        ],
        'windsor': [
            (IMG['golf'][2], 'Forest-estate routing with patient par-five decision points.', 'Forest-Estate-Routing mit geduldigen Par-5-Entscheidungen.'),
            (IMG['golf'][1], 'Water-influenced approach zones under mature tree cover.', 'Wasserbeeinflusste Annaeherungszonen unter altem Baumbestand.'),
        ],
        'great_rift': [
            (IMG['golf'][4], 'Escarpment golf shaped by elevation, wind, and release.', 'Escarpment-Golf gepraegt von Hoehe, Wind und Ballrelease.'),
            (IMG['golf'][5], 'Long Rift Valley views from the elevated back nine.', 'Weite Rift-Valley-Ausblicke vom erhoehten hinteren Neun.'),
        ],
        'fairmont': [
            (IMG['golf'][5], 'Highland air and equator-line short-game calibration.', 'Highland-Luft und Short-Game-Kalibrierung an der Aequatorlinie.'),
            (IMG['golf'][4], 'Compact target greens set against mountain backdrops.', 'Kompakte Zielgruens vor Bergpanorama.'),
        ],
        'vipingo': [
            (IMG['golf'][3], 'Coastal shot-making and wind-first Baobab Course strategy.', 'Kuesten-Shot-Making und windorientierte Baobab-Course-Strategie.'),
            (IMG['golf'][2], 'Championship carries routed around centuries-old baobabs.', 'Championship-Carries rund um jahrhundertealte Baobabs.'),
        ],
    },
    'safari': {
        'nairobi_np': [
            (IMG['safari'][0], 'Big game viewing framed by Nairobi access and golf timing.', 'Grosswildbeobachtung mit Nairobi-Zugang und Golf-Timing.'),
            (IMG['safari'][7], 'Lion and plains game on the capital\'s only park circuit.', 'Loewen und Steppenwild auf der einzigen Parkrunde der Hauptstadt.'),
        ],
        'naivasha_hippo': [
            (IMG['safari'][1], 'Boat channels through papyrus where hippo pods surface at close range.', 'Bootskanaele durch Papyrus, wo Flusspferdgruppen nah auftauchen.'),
            (IMG['safari'][3], 'Open lake light and shoreline birdlife after Rift Valley golf.', 'Offenes Seelicht und Ufervogelwelt nach Rift-Valley-Golf.'),
        ],
        'crescent_island': [
            (IMG['safari'][2], 'Guided walking among giraffe and zebra on the island peninsula.', 'Gefuehrte Wanderungen zwischen Giraffen und Zebras auf der Inselhalbinsel.'),
            (IMG['safari'][0], 'Quiet plains-game terrain without vehicles between golf days.', 'Ruhiges Steppenwild-Gelaende ohne Fahrzeuge zwischen Golftagen.'),
        ],
        'ol_pejeta': [
            (IMG['safari'][7], 'Lion country on private conservancy roads after dark.', 'Loewenlandschaft auf privaten Conservancy-Wegen nach Einbruch der Dunkelheit.'),
            (IMG['safari'][5], 'Big-game habitat alongside active rhino conservation programmes.', 'Grosswild-Habitat neben aktiven Nashornschutz-Programmen.'),
        ],
        'tsavo': [
            (IMG['safari'][4], 'Red-earth elephant country across Tsavo East and West.', 'Rote Elefantenerde quer durch Tsavo Ost und West.'),
            (IMG['safari'][3], 'Big-sky wilderness between the coast and inland bush.', 'Weite Wildnis zwischen Kueste und Inland-Busch.'),
        ],
        'amboseli': [
            (IMG['safari'][4], 'Elephant herds on swamp-fed grassland beneath Kilimanjaro.', 'Elefantenherden auf sumpfgetraenktem Grasland unter dem Kilimanjaro.'),
            (IMG['safari'][0], 'Open Amboseli light for photography and long game-drive loops.', 'Offenes Amboseli-Licht fuer Fotografie und lange Game-Drive-Schleifen.'),
        ],
        'hells_gate': [
            (IMG['safari'][3], 'Open Rift Valley grassland inside a rare walkable national park.', 'Offenes Rift-Valley-Grasland in einem selten begehbaren Nationalpark.'),
            (IMG['safari'][2], 'Zebra and giraffe grazing near the geothermal steam vents.', 'Zebras und Giraffen nahe den geothermischen Dampfquellen.'),
        ],
    },
    'wellness': {
        'blixen_tea': [
            (IMG['wellness'][0], 'Private garden recovery and soft Nairobi pacing.', 'Private Gartenerholung und sanftes Nairobi-Tempo.'),
            (IMG['wellness'][6], 'Quiet terrace seating for post-treatment tea.', 'Ruhige Terrassensitzplaetze fuer Tee nach der Behandlung.'),
        ],
        'volcanic_mud': [
            (IMG['wellness'][2], 'Thermal recovery after Rift Valley golf and movement.', 'Thermische Erholung nach Rift-Valley-Golf und Bewegung.'),
            (IMG['wellness'][1], 'Mineral-water hydrotherapy following the mud application.', 'Mineralwasser-Hydrotherapie nach der Schlammanwendung.'),
        ],
        'equine_treks': [
            (IMG['wellness'][5], 'Highland yoga practice framed by Mount Kenya air.', 'Highland-Yoga-Praxis in der Bergluft des Mount Kenya.'),
            (IMG['wellness'][6], 'Breathwork close beneath open highland skies.', 'Atemuebungen unter offenem Highland-Himmel.'),
        ],
        'kuruwitu_reef': [
            (IMG['wellness'][3], 'Ocean-air spa recovery shaped by Vipingo golf pacing.', 'Meeresluft-Spa-Erholung im Rhythmus des Vipingo-Golfs.'),
            (IMG['wellness'][4], 'Villa-side treatment tables set for coastal downtime.', 'Behandlungstische an der Villa fuer Kuestenerholung.'),
        ],
        'nanyuki_spa': [
            (IMG['wellness'][1], 'Fireside relaxation lounges inside the highland resort spa.', 'Kaminlounges im Highland-Resort-Spa.'),
            (IMG['wellness'][3], 'Sauna and steam circuit after conservancy game drives.', 'Sauna- und Dampfzirkel nach Conservancy-Pirschfahrten.'),
        ],
        'naivasha_sauna': [
            (IMG['wellness'][4], 'Lakeshore sauna wing built for practical recovery.', 'Sauna-Trakt am Seeufer fuer praktische Erholung.'),
            (IMG['wellness'][2], 'Steam room intervals after a full day of golf.', 'Dampfbad-Intervalle nach einem vollen Golftag.'),
        ],
    },
}


# ---------------------------------------------------------------------------
# 7. FAQs (2-3 unique Q&A pairs per key)
# ---------------------------------------------------------------------------

FAQS = {
    'stay': {
        'hemingways': [
            ('How far is Hemingways from Karen Country Club?', 'About five minutes by car, making it easy to schedule an early tee time without a long transfer.'),
            ('Is early check-in available after an overnight flight?', 'Early check-in is offered subject to availability; the concierge will confirm once the previous night\'s occupancy is known.'),
            ('Can non-golfing partners be kept busy nearby?', 'Yes. The Blixen Museum, Karen Blixen Coffee Garden, and Giraffe Centre are all within a short drive.'),
        ],
        'loldia': [
            ('Is Loldia suitable for non-adventurous guests?', 'Yes. Guests can enjoy the gardens and lake views without joining a boat or walking safari.'),
            ('How far is Loldia from Great Rift Valley golf?', 'About 20 minutes by road, making it straightforward to pair a morning round with an afternoon boat safari.'),
            ('Does the property have a spa?', 'No. Spa treatments are best arranged at Great Rift Valley Lodge or scheduled for a later stop on the itinerary.'),
        ],
        'fairmont': [
            ('Can we fly directly to the property?', 'Yes. Nanyuki has a small airstrip roughly 15 minutes away, avoiding the 3.5-hour road transfer from Nairobi.'),
            ('Is there a spa on site?', 'Yes, the resort spa is a short walk from every room category and is best booked after a game drive or round.'),
            ('How cold does it get at night?', 'Evenings can drop into single digits Celsius at this altitude; pack a warm layer even in the dry season.'),
        ],
        'vipingo_villas': [
            ('Do villas come with a private chef?', 'Yes, a private chef can be arranged for the full stay or selected meals; advise dietary needs in advance.'),
            ('How close is the villa to the golf course?', 'Most villas are a two-minute buggy ride from the Baobab Course clubhouse.'),
            ('Is this a good base for families?', 'Yes, the private pool and multi-bedroom layout suit families and multi-generational groups well.'),
        ],
        'giraffes': [
            ('How far in advance should we book?', 'As far ahead as possible; only twelve rooms exist and dates fill months in advance, especially in peak season.'),
            ('What time do the giraffe visit the house?', 'Giraffe typically approach during breakfast and again in the late afternoon, though timing varies by day.'),
            ('Is Giraffe Manor suitable for young children?', 'It suits families with older children best; very young children should be closely supervised near the giraffe.'),
        ],
        'sarova_salt': [
            ('Is it safe to stay inside the conservancy fence at night?', 'Yes, tents are on raised platforms and guests are escorted between tents after dark by camp staff.'),
            ('How far is the camp from the main Ol Pejeta gate?', 'About 45 minutes by road, which is factored into the game drive schedule.'),
            ('Does the camp have wifi and a pool?', 'Yes to both, though the property is positioned for wildlife immersion rather than resort facilities.'),
        ],
    },
    'course': {
        'karen': [
            ('How far in advance should tee times be requested?', 'Two to four weeks ahead is standard, longer around member competitions and weekends.'),
            ('What should guests wear?', 'Collared shirts, tailored shorts or trousers, and soft-spike golf shoes; denim and beachwear are not permitted.'),
            ('Are caddies compulsory?', 'Caddies are the norm rather than compulsory, and strongly recommended for guests unfamiliar with the layout.'),
        ],
        'muthaiga': [
            ('Can any visitor book a round here?', 'Guest access is managed through club introductions; the concierge arranges this ahead of the visit.'),
            ('How does Muthaiga compare to Karen?', 'Muthaiga plays longer and demands more accuracy off the tee, with tournament-conditioned greens.'),
            ('Is there a dress code beyond golf attire?', 'Yes, conservative club attire is expected in the clubhouse as well as on the course.'),
        ],
        'windsor': [
            ('What makes the 640-yard closing hole notable?', 'It is one of the longest closing par fives in East African golf, rewarding a patient three-shot strategy.'),
            ('Are golf carts available?', 'Yes, carts are available and commonly used given the resort\'s larger grounds.'),
            ('Is Windsor suitable for a relaxed second Nairobi round?', 'Yes, its resort pace and dining make it a good complement to a more formal club round elsewhere.'),
        ],
        'great_rift': [
            ('Why does the course feel harder than the yardage suggests?', 'Altitude and escarpment wind both add distance perception challenges not reflected on the scorecard.'),
            ('Can this be paired with a lake safari the same day?', 'Yes, an early tee time leaves the afternoon free for a Naivasha boat safari or Crescent Island walk.'),
            ('Are caddies available?', 'Yes, caddie support is available and recommended given the course\'s elevation changes.'),
        ],
        'fairmont': [
            ('Is this course walkable?', 'Yes, the short 9-hole layout is easily walked, even at altitude.'),
            ('How long does a round take?', 'Around 1.5 to 2 hours, making it easy to fit alongside a spa treatment or game drive.'),
            ('Is equipment rental available?', 'Yes, rental clubs can be arranged through the resort with advance notice.'),
        ],
        'vipingo': [
            ('When is the best time to tee off?', 'Early morning, before the coastal sea breeze builds through the afternoon.'),
            ('Is the course walkable in the heat?', 'Carts are recommended given coastal heat and humidity, though walking is permitted.'),
            ('Are there facilities for non-golfing family members?', 'Yes, clubhouse dining and nearby villa pools give non-golfers plenty to do during a round.'),
        ],
    },
    'safari': {
        'nairobi_np': [
            ('How long should we allocate?', 'A half day covers the main circuits well; a full day allows for a picnic stop and better rhino odds.'),
            ('What should we pack?', 'Neutral clothing, sun protection, and binoculars; mornings are cool enough for a light jacket.'),
            ('Can this be combined with golf the same day?', 'Yes, an early drive followed by a late-morning tee time at a nearby club works well.'),
        ],
        'naivasha_hippo': [
            ('How long should we allocate?', 'One to two hours on the water is typical, depending on wind and hippo activity.'),
            ('What should we pack?', 'A light layer, sun protection, and a dry bag or protective pouch for cameras.'),
            ('Is this suitable for children?', 'Yes, with life jackets provided and calm boat operators experienced with young guests.'),
        ],
        'crescent_island': [
            ('How long should we allocate?', 'Two to three hours, including the boat transfer to and from the peninsula.'),
            ('What should we pack?', 'Comfortable walking shoes, neutral clothing, sun protection, and water.'),
            ('Is this genuinely safe to walk without a vehicle?', 'Yes, the island has no resident predators, which is what allows guided walking access.'),
        ],
        'ol_pejeta': [
            ('How long should we allocate?', 'A full day is the minimum; an overnight extension allows for a night drive and better predator odds.'),
            ('What should we pack?', 'Neutral layers, binoculars, camera equipment, and a warm layer for early or night drives.'),
            ('Can we visit the chimpanzee sanctuary?', 'Yes, sanctuary visits can be arranged as part of the day and are worth confirming ahead of time.'),
        ],
        'tsavo': [
            ('How long should we allocate?', 'At least one overnight; the park\'s scale does not suit a rushed day trip.'),
            ('What should we pack?', 'Soft luggage, neutral clothing, sun protection, binoculars, and patience for larger landscapes.'),
            ('Is Tsavo East or West better for our itinerary?', 'Tsavo East suits open-plains elephant viewing, while Tsavo West offers more varied terrain and Mzima Springs.'),
        ],
        'amboseli': [
            ('When is Kilimanjaro most visible?', 'At sunrise, before afternoon cloud typically builds around the peak.'),
            ('Should we fly or drive from Nairobi?', 'Flying saves significant time; the Namanga road route takes around four hours.'),
            ('Is dust a serious issue?', 'It can be in the dry season on the lake-bed plains; a dust-proof camera bag is worth packing.'),
        ],
        'hells_gate': [
            ('Do we need a guide?', 'A licensed guide is mandatory for the lower gorge walk, arranged at the park gate.'),
            ('Can beginners cycle through the park?', 'Yes, the marked routes are gentle enough for moderately fit beginners.'),
            ('What happens if it rains?', 'The lower gorge can flood quickly in wet weather and may be closed without notice.'),
        ],
    },
    'wellness': {
        'blixen_tea': [
            ('How long does it take?', 'Two to three hours including the massage and terrace relaxation time.'),
            ('Any health considerations?', 'This is a leisure and recovery experience, not a medical treatment; mention any injuries beforehand.'),
            ('Can this be booked for a non-golfing partner only?', 'Yes, it is commonly booked for partners while others are on the course.'),
        ],
        'volcanic_mud': [
            ('How long does it take?', 'Sixty to ninety minutes for the full mud and hydrotherapy circuit.'),
            ('Any health considerations?', 'Guests with heat sensitivity or cardiovascular concerns should consult their own practitioner first.'),
            ('What should we bring?', 'Swimwear, sandals, and a change of clothing for after the treatment.'),
        ],
        'equine_treks': [
            ('How long does it take?', 'Ninety minutes to half a day, depending on the group\'s pace and preference.'),
            ('Any health considerations?', 'Guests with joint or mobility concerns should mention this so poses can be modified.'),
            ('Is this suitable for beginners?', 'Yes, the guide adapts pacing for all experience levels, from first-timers to regular practitioners.'),
        ],
        'kuruwitu_reef': [
            ('How long does it take?', 'Seventy-five to one hundred and twenty minutes, delivered directly at the villa.'),
            ('Any health considerations?', 'Mention any sunburn or heat exhaustion symptoms from golf before booking.'),
            ('Do we need to travel to a spa?', 'No, the therapist comes to the villa, so no additional transfer is required.'),
        ],
        'nanyuki_spa': [
            ('How long does it take?', 'Sixty to one hundred and fifty minutes depending on the treatment combination chosen.'),
            ('Any health considerations?', 'Guests with heat sensitivity should limit sauna and steam room time and stay hydrated.'),
            ('Is this open to non-resident guests?', 'Access is generally reserved for resort guests; the concierge can confirm current policy.'),
        ],
        'naivasha_sauna': [
            ('How long does it take?', 'Forty-five to seventy-five minutes for the full sauna and steam circuit.'),
            ('Any health considerations?', 'Guests with cardiovascular conditions should consult a doctor before extended heat exposure.'),
            ('Is booking required?', 'A time slot should be confirmed with the lodge in advance to avoid overlap with other guests.'),
        ],
    },
}


# ---------------------------------------------------------------------------
# 8. Offer items (included / optional extras per key)
# ---------------------------------------------------------------------------

OFFERS = {
    'stay': {
        'hemingways': {
            'included': ['Nightly accommodation in a garden or Nairobi suite', 'Daily breakfast on the veranda', 'Concierge coordination for golf and safari timing'],
            'optional': ['Private dining on the terrace', 'Spa treatments at the on-site spa', 'Early check-in or late check-out, subject to availability'],
        },
        'loldia': {
            'included': ['Nightly accommodation in a garden or lake-view cottage', 'Daily farmhouse breakfast', 'Concierge coordination for boat and walking safaris'],
            'optional': ['Private boat safari upgrade', 'In-room picnic lunch for a lakeside day', 'Extended stay discount for three or more nights'],
        },
        'fairmont': {
            'included': ['Nightly accommodation in a highland cottage or suite', 'Daily breakfast', 'Concierge coordination for golf and Ol Pejeta transfers'],
            'optional': ['Spa treatments at the resort spa', 'Private equator-line photo session with a guide', 'Late check-out, subject to availability'],
        },
        'vipingo_villas': {
            'included': ['Nightly villa accommodation', 'Housekeeping and villa concierge service', 'Buggy access to the Baobab Course clubhouse'],
            'optional': ['Private chef service for the full stay', 'Grocery pre-stocking before arrival', 'Poolside massage therapy'],
        },
        'giraffes': {
            'included': ['Nightly accommodation in a manor or garden room', 'Full board dining', 'Two guided giraffe feeding sessions'],
            'optional': ['Private garden breakfast setup', 'Extended stay for a third night when available', 'Photography guide for the giraffe feeding sessions'],
        },
        'sarova_salt': {
            'included': ['Nightly tented accommodation', 'Full board dining', 'Two daily conservancy game drives'],
            'optional': ['Night drive add-on', 'Chimpanzee sanctuary visit', 'Private bush dinner by the waterhole'],
        },
    },
    'course': {
        'karen': {
            'included': ['Green fees coordination', 'Caddie arrangement where available', 'Concierge tee-time management'],
            'optional': ['Club rental', 'Private coaching session with a club professional', 'Post-round clubhouse lunch'],
        },
        'muthaiga': {
            'included': ['Green fees and guest introduction coordination', 'Caddie arrangement where available', 'Concierge tee-time management'],
            'optional': ['Private coaching session', 'Post-round clubhouse dining', 'Club history tour with a member host'],
        },
        'windsor': {
            'included': ['Green fees coordination', 'Golf cart arrangement', 'Concierge tee-time management'],
            'optional': ['Club rental', 'Private coaching session', 'Resort lunch package'],
        },
        'great_rift': {
            'included': ['Green fees coordination', 'Caddie arrangement where available', 'Concierge tee-time management around lake safari timing'],
            'optional': ['Club rental', 'Private coaching session', 'Lodge lunch package after the round'],
        },
        'fairmont': {
            'included': ['Green fees coordination', 'Equipment coordination where available', 'Concierge tee-time management'],
            'optional': ['Private wedge-distance coaching session', 'Equator-line photo package', 'Spa booking immediately after the round'],
        },
        'vipingo': {
            'included': ['Green fees coordination', 'Golf cart arrangement', 'Concierge tee-time management around villa logistics'],
            'optional': ['Club rental', 'Private coaching session', 'Post-round clubhouse lunch'],
        },
    },
    'safari': {
        'nairobi_np': {
            'included': ['Park entry fee coordination', 'Guided game drive vehicle', 'Itinerary timing around golf days'],
            'optional': ['Private vehicle upgrade', 'Specialist photography guide', 'Extended full-day drive'],
        },
        'naivasha_hippo': {
            'included': ['Boat safari coordination', 'Life jackets and safety briefing', 'Itinerary timing around golf days'],
            'optional': ['Private boat upgrade', 'Specialist birding guide', 'Sundowner add-on on the water'],
        },
        'crescent_island': {
            'included': ['Boat transfer to the island', 'Guided walking safari', 'Itinerary timing around golf and spa days'],
            'optional': ['Private guide upgrade', 'Extended walking route', 'Picnic breakfast on the island'],
        },
        'ol_pejeta': {
            'included': ['Conservancy entry fee coordination', 'Guided game drive vehicle', 'Itinerary timing around Mount Kenya golf'],
            'optional': ['Night drive add-on', 'Chimpanzee sanctuary visit', 'Private vehicle upgrade'],
        },
        'tsavo': {
            'included': ['Park entry fee coordination', 'Guided game drive vehicle', 'Multi-night routing support'],
            'optional': ['Private vehicle upgrade', 'Specialist photography guide', 'Fly-in transfer coordination'],
        },
        'amboseli': {
            'included': ['Park entry fee coordination', 'Guided game drive vehicle', 'Nairobi flight or road transfer coordination'],
            'optional': ['Sunrise departure upgrade for clearer Kilimanjaro views', 'Private vehicle upgrade', 'Overnight extension for a sunset drive'],
        },
        'hells_gate': {
            'included': ['Park entry fee coordination', 'Licensed guide for the gorge walk', 'Bicycle hire coordination'],
            'optional': ['Extended cycling route', 'Private photography guide', 'Combined half-day with Crescent Island'],
        },
    },
    'wellness': {
        'blixen_tea': {
            'included': ['Signature massage treatment', 'Garden terrace relaxation time', 'Herbal tea service'],
            'optional': ['Extended treatment time', 'Private add-on facial', 'In-room treatment upgrade'],
        },
        'volcanic_mud': {
            'included': ['Thermal mud application', 'Mineral-water hydrotherapy access', 'Recovery time buffer'],
            'optional': ['Extended treatment time', 'Private add-on massage', 'Transfer coordination to and from the lodge'],
        },
        'equine_treks': {
            'included': ['Guided yoga and breathwork session', 'Mats and props provided', 'Herbal tea after practice'],
            'optional': ['Private one-on-one session', 'Extended meditation close', 'Sunrise session scheduling'],
        },
        'kuruwitu_reef': {
            'included': ['In-villa massage treatment', 'Cooling face and scalp treatment', 'Chilled towel and hydration service'],
            'optional': ['Extended treatment time', 'Second therapist for couples\' sessions', 'Poolside treatment setup'],
        },
        'nanyuki_spa': {
            'included': ['Choice of massage or facial treatment', 'Sauna and steam room access', 'Fireside relaxation lounge'],
            'optional': ['Extended treatment time', 'Private couples\' treatment room', 'Full-day spa package'],
        },
        'naivasha_sauna': {
            'included': ['Sauna and steam room circuit access', 'Cool-down lounge time', 'Herbal infusion service'],
            'optional': ['Extended circuit time', 'Private session scheduling outside standard hours', 'Combined booking with a massage elsewhere on property'],
        },
    },
}


# ---------------------------------------------------------------------------
# 9. Related experiences (geographically and logically sensible pairings)
# ---------------------------------------------------------------------------

RELATED = [
    ('course', 'karen', 'stay', 'hemingways', 'Recommended stay', 1),
    ('course', 'karen', 'safari', 'nairobi_np', 'Pair with safari', 2),
    ('course', 'karen', 'wellness', 'blixen_tea', 'Recovery after golf', 3),
    ('course', 'muthaiga', 'stay', 'hemingways', 'Recommended stay', 1),
    ('course', 'muthaiga', 'safari', 'nairobi_np', 'Pair with safari', 2),
    ('course', 'windsor', 'stay', 'hemingways', 'Recommended stay', 1),
    ('course', 'windsor', 'wellness', 'blixen_tea', 'Recovery after golf', 2),
    ('stay', 'hemingways', 'course', 'karen', 'On-site club access', 1),
    ('stay', 'hemingways', 'safari', 'nairobi_np', 'Nearby safari', 2),
    ('stay', 'hemingways', 'wellness', 'blixen_tea', 'On-site spa', 3),
    ('stay', 'giraffes', 'course', 'karen', 'Nearby golf', 1),
    ('stay', 'giraffes', 'safari', 'nairobi_np', 'Nearby safari', 2),
    ('stay', 'giraffes', 'wellness', 'blixen_tea', 'Recovery', 3),
    ('safari', 'nairobi_np', 'course', 'karen', 'Nearby golf', 1),
    ('safari', 'nairobi_np', 'stay', 'hemingways', 'Nearby stay', 2),
    ('safari', 'nairobi_np', 'stay', 'giraffes', 'Nearby stay', 3),
    ('wellness', 'blixen_tea', 'stay', 'hemingways', 'Nearby stay', 1),
    ('wellness', 'blixen_tea', 'course', 'karen', 'Pair with golf', 2),

    ('course', 'great_rift', 'stay', 'loldia', 'On-site lodge', 1),
    ('course', 'great_rift', 'safari', 'naivasha_hippo', 'Pair with safari', 2),
    ('course', 'great_rift', 'safari', 'hells_gate', 'Pair with safari', 3),
    ('stay', 'loldia', 'safari', 'naivasha_hippo', 'Nearby safari', 1),
    ('stay', 'loldia', 'safari', 'crescent_island', 'Nearby safari', 2),
    ('stay', 'loldia', 'wellness', 'naivasha_sauna', 'Recovery', 3),
    ('safari', 'naivasha_hippo', 'stay', 'loldia', 'Nearby stay', 1),
    ('safari', 'naivasha_hippo', 'course', 'great_rift', 'Nearby golf', 2),
    ('safari', 'crescent_island', 'stay', 'loldia', 'Nearby stay', 1),
    ('safari', 'crescent_island', 'safari', 'naivasha_hippo', 'Combine with boat safari', 2),
    ('safari', 'hells_gate', 'stay', 'loldia', 'Nearby stay', 1),
    ('safari', 'hells_gate', 'safari', 'naivasha_hippo', 'Combine safaris', 2),
    ('wellness', 'naivasha_sauna', 'course', 'great_rift', 'Pair with golf', 1),
    ('wellness', 'naivasha_sauna', 'stay', 'loldia', 'On-site recovery', 2),

    ('course', 'fairmont', 'stay', 'fairmont', 'On-site stay', 1),
    ('course', 'fairmont', 'safari', 'ol_pejeta', 'Pair with safari', 2),
    ('course', 'fairmont', 'wellness', 'nanyuki_spa', 'Recovery', 3),
    ('stay', 'fairmont', 'safari', 'ol_pejeta', 'Nearby safari', 1),
    ('stay', 'fairmont', 'wellness', 'nanyuki_spa', 'On-site spa', 2),
    ('stay', 'fairmont', 'wellness', 'equine_treks', 'Highland yoga retreat', 3),
    ('safari', 'ol_pejeta', 'stay', 'fairmont', 'Nearby stay', 1),
    ('safari', 'ol_pejeta', 'stay', 'sarova_salt', 'Nearby stay', 2),
    ('safari', 'ol_pejeta', 'course', 'fairmont', 'Nearby golf', 3),
    ('stay', 'sarova_salt', 'safari', 'ol_pejeta', 'On conservancy grounds', 1),
    ('stay', 'sarova_salt', 'stay', 'fairmont', 'Nearby golf resort', 2),
    ('wellness', 'nanyuki_spa', 'course', 'fairmont', 'Pair with golf', 1),
    ('wellness', 'nanyuki_spa', 'safari', 'ol_pejeta', 'Pair with safari', 2),
    ('wellness', 'equine_treks', 'safari', 'ol_pejeta', 'Pair with safari', 1),
    ('wellness', 'equine_treks', 'stay', 'fairmont', 'On-site retreat', 2),

    ('course', 'vipingo', 'stay', 'vipingo_villas', 'On-site villas', 1),
    ('course', 'vipingo', 'safari', 'tsavo', 'Safari extension', 2),
    ('course', 'vipingo', 'wellness', 'kuruwitu_reef', 'Recovery', 3),
    ('stay', 'vipingo_villas', 'safari', 'tsavo', 'Safari extension', 1),
    ('stay', 'vipingo_villas', 'safari', 'amboseli', 'Safari extension via flight', 2),
    ('stay', 'vipingo_villas', 'wellness', 'kuruwitu_reef', 'On-site spa', 3),
    ('safari', 'tsavo', 'stay', 'vipingo_villas', 'Nearby stay', 1),
    ('safari', 'tsavo', 'course', 'vipingo', 'Combine with coastal golf', 2),
    ('safari', 'amboseli', 'stay', 'vipingo_villas', 'Coastal extension via flight', 1),
    ('safari', 'amboseli', 'stay', 'hemingways', 'Nairobi base before flight', 2),
    ('wellness', 'kuruwitu_reef', 'course', 'vipingo', 'Pair with golf', 1),
    ('wellness', 'kuruwitu_reef', 'stay', 'vipingo_villas', 'On-site recovery', 2),
]


# ---------------------------------------------------------------------------
# 10. Derived name/slug exports
# ---------------------------------------------------------------------------

ACCOMMODATION_NAMES = [item['name'] for item in ACCOMMODATIONS]
SAFARI_NAMES = [item['name'] for item in SAFARI_DESTINATIONS]
WELLNESS_NAMES = [item['name_en'] for item in WELLNESS]
COURSE_SLUGS = [item['slug'] for item in GOLF_COURSES]
