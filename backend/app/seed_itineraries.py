"""Hand-curated seed itineraries — used when Gemini is unavailable.

These are taken directly from the prototype's data.jsx so the offline demo
matches the design file 1:1.
"""
from __future__ import annotations

S = lambda kind, name, meta="": {"kind": kind, "name": name, "meta": meta}


TOKYO_OFFBEAT = [
    {
        "title": "Slow Arrival in Yanaka",
        "sub": "Old Tokyo · low-key",
        "area": "yanaka",
        "why": "Eases in via the cat-loved old district instead of Shibuya chaos. Walking-heavy, hidden-gem heavy, and the kissaten on Yanaka Ginza beats any chain coffee.",
        "slots": [
            {"when": "Morning", "stops": [
                S("travel", "Land at Haneda → Yanaka guesthouse", "Train · 38 min"),
                S("food", "Kayaba Coffee — kissaten breakfast", "¥ · 7-min walk"),
            ]},
            {"when": "Afternoon", "stops": [
                S("hidden", "Yanaka Ginza shotengai stroll", "Local market street"),
                S("hidden", "SCAI The Bathhouse — gallery in old sento", "¥ ·  local art"),
            ]},
            {"when": "Evening", "stops": [
                S("food", "Hantei — kushiage in 100-yr machiya", "¥¥ · book ahead"),
            ]},
        ],
    },
    {
        "title": "Shimokita & Shibuya backstreets",
        "sub": "Vintage · indie · vinyl",
        "area": "shibuya",
        "why": "Skips the Scramble and routes you through Shimokitazawa for vintage and live-music dives. You wanted hidden gems with culture and food — this is the day.",
        "slots": [
            {"when": "Morning", "stops": [
                S("hidden", "Shimokitazawa vintage walk", "Flash, Stick Out, Toyo Hyakkaten"),
                S("food", "Bear Pond Espresso", "¥ · queue worth it"),
            ]},
            {"when": "Afternoon", "stops": [
                S("hidden", "Cat Street + Ura-Hara backstreets", "Skip the Takeshita crowd"),
                S("food", "Path bakery — late lunch", "¥¥ · vegetarian-friendly"),
            ]},
            {"when": "Evening", "stops": [
                S("hidden", "Nonbei Yokocho — drink alley", "Tiny 4-seat bars · cash only"),
                S("food", "Vegan Ramen UZU", "¥¥ · teamLab cafe"),
            ]},
        ],
    },
    {
        "title": "Sumida + Kuramae craft",
        "sub": "Riverside · makers",
        "area": "asakusa",
        "why": "Asakusa without the Senso-ji selfie crush — early Senso-ji at dawn, then Kuramae's leather, paper and coffee makers across the river.",
        "slots": [
            {"when": "Morning", "stops": [
                S("hidden", "Senso-ji at 06:30 — empty grounds", "Free · 20 min"),
                S("food", "Pelican Bakery — toast set", "¥ · since 1942"),
            ]},
            {"when": "Afternoon", "stops": [
                S("hidden", "Kuramae makers walk", "Kakimori, Koncent, Dandelion"),
                S("food", "Convivial — Italian by the river", "¥¥ · veg menu"),
            ]},
            {"when": "Evening", "stops": [
                S("hidden", "Sumida sunset stroll", "Free · 40 min walk"),
            ]},
        ],
    },
    {
        "title": "Daikanyama + Nakameguro day",
        "sub": "Books · canal · slow",
        "area": "nakameguro",
        "why": "Pace deliberately drops mid-trip. Tsutaya T-Site for two unhurried hours, then a canal walk that locals actually do.",
        "slots": [
            {"when": "Morning", "stops": [
                S("hidden", "Tsutaya T-Site Daikanyama", "Books · cafe · 90 min"),
                S("food", "Onibus Coffee Nakameguro", "¥ · third wave"),
            ]},
            {"when": "Afternoon", "stops": [
                S("hidden", "Meguro river walk", "Free · 25 min"),
                S("food", "Higashiyama Tofu Honten", "¥¥ · vegetarian set"),
            ]},
            {"when": "Evening", "stops": [
                S("hidden", "Bar Trench (Ebisu) — apéritif", "¥¥ · pre-dinner"),
                S("food", "Ahiru Store — natural wine", "¥¥¥ · book ahead"),
            ]},
        ],
    },
    {
        "title": "West side · Kichijoji + Inokashira",
        "sub": "Park · jazz · last meal",
        "area": "shinjuku",
        "why": "Closes on something quiet. Inokashira park, jazz kissa in the afternoon, and a last-night izakaya on the way back to Haneda.",
        "slots": [
            {"when": "Morning", "stops": [
                S("hidden", "Inokashira Park · row a boat", "Free · 60 min"),
                S("food", "Sometaro — okonomiyaki on the floor", "¥¥ · vegetarian ok"),
            ]},
            {"when": "Afternoon", "stops": [
                S("hidden", "Jazz kissa Funky", "¥ · listen-only café"),
                S("hidden", "Harmonica Yokocho", "Drink alley by Kichijoji"),
            ]},
            {"when": "Evening", "stops": [
                S("food", "Tonki — Meguro tonkatsu (or veg ramen alt)", "¥¥"),
                S("travel", "Train → Haneda for departure", "45 min"),
            ]},
        ],
    },
]


TOKYO_FAMILY = [
    {
        "title": "Easy arrival · Asakusa",
        "sub": "Anchor · rest · early dinner",
        "area": "asakusa",
        "why": "Light first day with one anchor sight, a long lunch, and a rest block before an early dinner. No late-night moves.",
        "slots": [
            {"when": "Morning", "stops": [S("travel", "Haneda → Asakusa hotel", "Train · 50 min · luggage forwarded")]},
            {"when": "Afternoon", "stops": [
                S("", "Senso-ji + Nakamise street", "Free · stroller-friendly"),
                S("food", "Asakusa Sometaro — okonomiyaki", "¥¥ · kid-friendly · vegetarian options"),
                S("rest", "Hotel rest block", "90 min · post-lunch"),
            ]},
            {"when": "Evening", "stops": [S("food", "Early dinner near hotel", "¥¥ · before 19:30 · vegetarian set")]},
        ],
    },
    {
        "title": "teamLab Planets day",
        "sub": "Big-hit attraction · controlled crowds",
        "area": "odaiba",
        "why": "One major experience the kids will remember, booked at off-peak slot. Lunch and rest baked in, no late return.",
        "slots": [
            {"when": "Morning", "stops": [
                S("travel", "To Toyosu", "Train · 25 min"),
                S("", "teamLab Planets (10:00 entry)", "¥¥¥ · book ahead"),
            ]},
            {"when": "Afternoon", "stops": [
                S("food", "Toyosu market lunch", "¥¥ · veg sushi available"),
                S("rest", "Hotel rest", "90 min"),
            ]},
            {"when": "Evening", "stops": [S("", "Sumida riverboat", "¥¥ · 40 min · safe")]},
        ],
    },
    {
        "title": "Ueno parks + zoo",
        "sub": "Open air · easy pace",
        "area": "ueno",
        "why": "Open-air day with the zoo and museum optionals — short walks, lots of benches, and a safe early dinner spot.",
        "slots": [
            {"when": "Morning", "stops": [S("", "Ueno Zoo", "¥ · 2 hrs"), S("food", "Ueno park café", "¥¥ · veg set")]},
            {"when": "Afternoon", "stops": [S("", "Tokyo Nat. Museum (1 wing only)", "¥¥ · 90 min"), S("rest", "Park rest", "30 min")]},
            {"when": "Evening", "stops": [S("food", "Family izakaya near hotel", "¥¥ · before 20:00 · vegetarian set")]},
        ],
    },
    {
        "title": "Shibuya light + Harajuku",
        "sub": "Daytime · bright streets",
        "area": "harajuku",
        "why": "Crowded districts visited in daylight only, with a known kid-safe lunch and a rest stop before heading back.",
        "slots": [
            {"when": "Morning", "stops": [S("", "Yoyogi Park", "Free · open green"), S("", "Meiji Jingu shrine", "Free · forested walk")]},
            {"when": "Afternoon", "stops": [
                S("", "Harajuku Takeshita street", "Daytime only"),
                S("food", "T's Tantan — vegan ramen Tokyo Stn", "¥¥"),
                S("rest", "Hotel rest", "90 min"),
            ]},
            {"when": "Evening", "stops": [S("", "Shibuya Sky (sunset slot)", "¥¥¥ · seated viewing")]},
        ],
    },
    {
        "title": "Goodbye Tokyo · gentle close",
        "sub": "Brunch · pack · airport",
        "area": "ginza",
        "why": "Slow morning, an easy brunch, and a pre-booked airport limo bus from the hotel — no luggage stress.",
        "slots": [
            {"when": "Morning", "stops": [S("food", "Hotel brunch", "¥¥ · veg set"), S("", "Ginza window-shop walk", "30 min")]},
            {"when": "Afternoon", "stops": [S("travel", "Airport limo bus", "75 min · door-to-door")]},
            {"when": "Evening", "stops": [S("rest", "Travel day — no plans", "Open block")]},
        ],
    },
]


TOKYO_BLEISURE = [
    {
        "title": "Land + work-evening",
        "sub": "Compact · Wi-Fi café · early sleep",
        "area": "shinjuku",
        "why": "You arrive on a working day. Plan locks to the 17:30–22:00 evening window after work — single neighborhood, no long transfers.",
        "slots": [
            {"when": "Morning", "stops": [S("travel", "Haneda → hotel · check email", "Train · 35 min"), S("", "Work block", "Hotel desk")]},
            {"when": "Afternoon", "stops": [S("", "Work block", "Hotel desk"), S("food", "Blue Bottle Shinjuku — fast lunch", "¥¥ · Wi-Fi")]},
            {"when": "Evening", "stops": [S("food", "Tsuta Japanese Soba — Michelin ramen", "¥¥ · 25 min"), S("", "Omoide Yokocho 30-min walk", "Free · light")]},
        ],
    },
    {
        "title": "Pre-work morning · post-work walk",
        "sub": "07:00–09:00 · 17:30–22:00",
        "area": "roppongi",
        "why": "Bookended around your work block. Morning run + breakfast meeting; evening view + dinner. Nothing in between.",
        "slots": [
            {"when": "Morning", "stops": [S("", "Imperial Palace east garden run", "Free · 30 min"), S("food", "Toranomon Coffee — meeting-friendly", "¥ · Wi-Fi")]},
            {"when": "Afternoon", "stops": [S("", "Work block", "Off-itinerary")]},
            {"when": "Evening", "stops": [S("", "Mori Tower observation", "¥¥¥ · 60 min"), S("food", "Maruhachi — late dinner", "¥¥ · open till 23:00")]},
        ],
    },
    {
        "title": "Half-day Saturday · day-tripable",
        "sub": "Saturday · longer window",
        "area": "asakusa",
        "why": "Saturday opens the only long window for a fuller half-day. Two anchors, lunch, no full-day excursion (validator blocked Hakone).",
        "slots": [
            {"when": "Morning", "stops": [S("", "Senso-ji + Asakusa", "Free · 90 min"), S("food", "Daikokuya tempura", "¥¥")]},
            {"when": "Afternoon", "stops": [S("", "Tokyo Nat. Museum (1 wing)", "¥¥ · 90 min"), S("rest", "Café break · email", "45 min")]},
            {"when": "Evening", "stops": [S("food", "Counter sushi · Ginza", "¥¥¥ · 90 min")]},
        ],
    },
    {
        "title": "Sunday · long form",
        "sub": "Full day · the one excursion",
        "area": "yanaka",
        "why": "Sunday is the only weekday where a full-day excursion is allowed. Yanaka + Nezu walking circuit, all returnable to hotel by 19:00.",
        "slots": [
            {"when": "Morning", "stops": [S("", "Yanaka Ginza walk", "Free · 90 min"), S("food", "Kayaba Coffee", "¥ · breakfast")]},
            {"when": "Afternoon", "stops": [S("", "Nezu shrine + alleys", "Free · 60 min"), S("food", "Hantei kushiage", "¥¥¥ · book")]},
            {"when": "Evening", "stops": [S("", "Hotel · prep next week", "Off-itinerary")]},
        ],
    },
    {
        "title": "Last morning · airport",
        "sub": "Brief · efficient",
        "area": "ginza",
        "why": "Single café, clean exit. Airport limo from hotel; no transfers with luggage.",
        "slots": [
            {"when": "Morning", "stops": [S("food", "Hotel breakfast", "¥¥"), S("travel", "Airport limo bus", "75 min")]},
            {"when": "Afternoon", "stops": [S("rest", "Travel home", "Open")]},
            {"when": "Evening", "stops": [S("rest", "Travel home", "Open")]},
        ],
    },
]


TOKYO_SENIOR = [
    {
        "title": "Calm arrival · gardens",
        "sub": "Late start · low walking",
        "area": "ginza",
        "why": "Day starts at 10:30, ends 18:30. One quiet anchor, lots of seating, no stairs, accessible transport throughout.",
        "slots": [
            {"when": "Morning", "stops": [S("travel", "Haneda → hotel · taxi", "45 min · door-to-door")]},
            {"when": "Afternoon", "stops": [S("", "Hamarikyu Garden — flat paths", "¥ · benches every 80m"), S("food", "Garden tea house", "¥¥ · seated")]},
            {"when": "Evening", "stops": [S("food", "Hotel restaurant — early dinner", "¥¥ · 18:00")]},
        ],
    },
    {
        "title": "Asakusa · accessible Senso-ji",
        "sub": "Step-free route · taxi-anchored",
        "area": "asakusa",
        "why": "Step-free route around Senso-ji, with a tea-house lunch and an early return. No long queues, no steep climbs.",
        "slots": [
            {"when": "Morning", "stops": [S("travel", "Taxi to Asakusa", "25 min"), S("", "Senso-ji step-free path", "Free · 45 min")]},
            {"when": "Afternoon", "stops": [S("food", "Mugitoro — yam rice, seated", "¥¥"), S("rest", "Hotel rest", "90 min")]},
            {"when": "Evening", "stops": [S("food", "Hotel area dinner", "¥¥ · 18:00")]},
        ],
    },
    {
        "title": "Tokyo Nat. Museum · slow",
        "sub": "1 wing · seated bench loop",
        "area": "ueno",
        "why": "Single wing of the museum at a slow pace — calm, accessible, no crowd. Park café for lunch with shade.",
        "slots": [
            {"when": "Morning", "stops": [S("", "Tokyo National Museum", "¥¥ · 1 wing · 90 min"), S("food", "Park café", "¥¥ · seated")]},
            {"when": "Afternoon", "stops": [S("rest", "Hotel rest", "90 min"), S("", "Ginza window walk", "30 min · benches")]},
            {"when": "Evening", "stops": [S("food", "Hotel dining", "¥¥")]},
        ],
    },
    {
        "title": "Hamarikyu boat · Ginza",
        "sub": "Boat · café · light",
        "area": "ginza",
        "why": "Boat across the bay (seated, scenic), an unhurried Ginza coffee, and an early dinner. Validator removed Roppongi nightlife.",
        "slots": [
            {"when": "Morning", "stops": [S("", "Hamarikyu → Asakusa boat", "¥¥ · seated 35 min"), S("food", "Asakusa lunch — quiet", "¥¥")]},
            {"when": "Afternoon", "stops": [S("", "Ginza Sony Park", "Free · 30 min"), S("rest", "Hotel rest", "90 min")]},
            {"when": "Evening", "stops": [S("food", "Hotel restaurant", "¥¥ · 18:00")]},
        ],
    },
    {
        "title": "Quiet goodbye",
        "sub": "Brunch · taxi · airport",
        "area": "ginza",
        "why": "Door-to-door taxi to Haneda. Nothing rushed.",
        "slots": [
            {"when": "Morning", "stops": [S("food", "Hotel brunch", "¥¥"), S("travel", "Taxi → Haneda", "45 min")]},
            {"when": "Afternoon", "stops": [S("rest", "Travel home", "Open")]},
            {"when": "Evening", "stops": [S("rest", "Travel home", "Open")]},
        ],
    },
]


SEED = {
    "tokyo": {
        "off_beat_explorer": TOKYO_OFFBEAT,
        "first_time_family": TOKYO_FAMILY,
        "bleisure_professional": TOKYO_BLEISURE,
        "senior_couple": TOKYO_SENIOR,
    },
}


def seed_for(destination: str, persona: str) -> list[dict]:
    """Return a deep copy of the seed days for a (destination, persona) pair.

    Falls back to off_beat Tokyo if the pair is unknown — matches the prototype.
    """
    import copy

    dest = SEED.get(destination)
    if dest:
        days = dest.get(persona) or dest["off_beat_explorer"]
    else:
        days = TOKYO_OFFBEAT
    return copy.deepcopy(days)
