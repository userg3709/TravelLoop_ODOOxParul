from datetime import date

from werkzeug.security import generate_password_hash

from app.db import db
from app.models import ItineraryItem, Region, Trip, User


SEED_TRIP_CODES = {
    "TL-SEED-GOLDEN-TRIANGLE",
    "TL-SEED-WESTERN-GHATS",
    "TL-SEED-HAMPI",
}


def ensure_seed_data():
    if Trip.query.filter(Trip.trip_code.in_(SEED_TRIP_CODES)).first():
        return

    user = User.query.order_by(User.id.asc()).first()
    if not user:
        user = User(
            first_name="TravelLoop",
            last_name="Planner",
            email="planner@travelloop.local",
            phone_number="+91 98765 43210",
            city="Vadodara",
            country="India",
            description="Curated planning profile with India-focused routes, budgets, and editable itinerary sections.",
            password_hash=generate_password_hash("travelloop"),
        )
        db.session.add(user)
        db.session.flush()

    trips = [
        {
            "trip_code": "TL-SEED-GOLDEN-TRIANGLE",
            "trip_name": "Golden Triangle Heritage Route",
            "start_date": date(2026, 11, 12),
            "end_date": date(2026, 11, 18),
            "description": "A one-week Delhi, Agra, and Jaipur route built around monuments, markets, and classic rail transfers.",
            "status": "planned",
            "regions": [
                ("Delhi", "India", "Delhi", date(2026, 11, 12), date(2026, 11, 14)),
                ("Agra", "India", "Agra", date(2026, 11, 15), date(2026, 11, 15)),
                ("Jaipur", "India", "Jaipur", date(2026, 11, 16), date(2026, 11, 18)),
            ],
            "items": [
                ("Delhi heritage walk", "Guided walk through Chandni Chowk, Jama Masjid, and Red Fort exteriors.", 3500, "INR", 0),
                ("Gatimaan Express to Agra", "Morning train from Delhi to Agra Cantt with buffer time for station transfers.", 1800, "INR", 1),
                ("Taj Mahal sunrise entry", "Book sunrise entry and keep a backup slot if fog affects visibility.", 1300, "INR", 1),
                ("Amber Fort and City Palace", "Full-day Jaipur circuit with local transport and lunch near the old city.", 4200, "INR", 2),
            ],
        },
        {
            "trip_code": "TL-SEED-WESTERN-GHATS",
            "trip_name": "Western Ghats Monsoon Trail",
            "start_date": date(2026, 8, 6),
            "end_date": date(2026, 8, 11),
            "description": "A compact nature route across Munnar and Thekkady with tea estates, viewpoints, and spice country stays.",
            "status": "planned",
            "regions": [
                ("Munnar", "India", "Munnar", date(2026, 8, 6), date(2026, 8, 8)),
                ("Thekkady", "India", "Thekkady", date(2026, 8, 9), date(2026, 8, 11)),
            ],
            "items": [
                ("Eravikulam National Park permit", "Reserve the park slot early during the monsoon travel window.", 2200, "INR", 0),
                ("Tea estate visit", "Late afternoon estate visit with tasting and short factory tour.", 1500, "INR", 0),
                ("Periyar lake boat safari", "Morning safari slot with transport from the homestay.", 2800, "INR", 1),
            ],
        },
        {
            "trip_code": "TL-SEED-HAMPI",
            "trip_name": "Hampi Weekend Ruins Walk",
            "start_date": date(2025, 12, 5),
            "end_date": date(2025, 12, 7),
            "description": "A completed short break around Hampi's temple complexes, boulder viewpoints, and riverside cafes.",
            "status": "completed",
            "regions": [
                ("Hampi", "India", "Hampi", date(2025, 12, 5), date(2025, 12, 7)),
            ],
            "items": [
                ("Virupaksha Temple and Hampi Bazaar", "Early morning temple visit before walking the bazaar ruins.", 900, "INR", 0),
                ("Coracle ride near Tungabhadra", "Evening river crossing and sunset viewpoint plan.", 1200, "INR", 0),
            ],
        },
    ]

    for trip_data in trips:
        trip = Trip(
            trip_code=trip_data["trip_code"],
            user_id=user.id,
            trip_name=trip_data["trip_name"],
            start_date=trip_data["start_date"],
            end_date=trip_data["end_date"],
            description=trip_data["description"],
            status=trip_data["status"],
        )
        db.session.add(trip)
        db.session.flush()

        regions = []
        for name, country, city, start_date, end_date in trip_data["regions"]:
            region = Region(
                trip_id=trip.id,
                name=name,
                country=country,
                city=city,
                start_date=start_date,
                end_date=end_date,
            )
            db.session.add(region)
            regions.append(region)
        db.session.flush()

        for title, description, budget, currency, region_index in trip_data["items"]:
            db.session.add(
                ItineraryItem(
                    trip_id=trip.id,
                    region_id=regions[region_index].id,
                    title=title,
                    description=description,
                    budget_amount=budget,
                    currency=currency,
                )
            )

    db.session.commit()
