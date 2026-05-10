from datetime import datetime
from uuid import uuid4

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user

from app.db import db
from app.models import ItineraryItem, Region, Trip, User


main = Blueprint("main", __name__)


CURATED_DESTINATIONS = [
    {"code": "DEL", "city": "Delhi", "country": "India", "price": "From INR 18,000", "tag": "Heritage"},
    {"code": "MUN", "city": "Munnar", "country": "India", "price": "From INR 22,500", "tag": "Nature"},
    {"code": "HAM", "city": "Hampi", "country": "India", "price": "From INR 12,000", "tag": "Weekend"},
    {"code": "JAI", "city": "Jaipur", "country": "India", "price": "From INR 16,500", "tag": "Culture"},
]


ACTIVITY_CATALOG = [
    {"title": "Old Delhi Food and Heritage Walk", "location": "Chandni Chowk, Delhi", "category": "Culture", "price": 3500, "currency": "INR", "rating": 4.8, "duration": "3.5 hrs"},
    {"title": "Taj Mahal Sunrise Guided Visit", "location": "Agra, Uttar Pradesh", "category": "History", "price": 1300, "currency": "INR", "rating": 4.9, "duration": "2 hrs"},
    {"title": "Amber Fort and City Palace Circuit", "location": "Jaipur, Rajasthan", "category": "Sightseeing", "price": 4200, "currency": "INR", "rating": 4.7, "duration": "6 hrs"},
    {"title": "Munnar Tea Estate Tour", "location": "Munnar, Kerala", "category": "Nature", "price": 1500, "currency": "INR", "rating": 4.6, "duration": "2.5 hrs"},
    {"title": "Periyar Lake Boat Safari", "location": "Thekkady, Kerala", "category": "Wildlife", "price": 2800, "currency": "INR", "rating": 4.5, "duration": "2 hrs"},
    {"title": "Hampi Bazaar and Virupaksha Walk", "location": "Hampi, Karnataka", "category": "History", "price": 900, "currency": "INR", "rating": 4.8, "duration": "3 hrs"},
]


def _active_user():
    if current_user.is_authenticated:
        return current_user

    return User.query.order_by(User.id.asc()).first()


def _initials(user):
    if not user:
        return "GU"

    first = (user.first_name or "").strip()
    last = (user.last_name or "").strip()
    if first or last:
        return f"{first[:1]}{last[:1]}".upper()

    return (user.email or "GU")[:2].upper()


def _date(value):
    if not value:
        return None

    return datetime.strptime(value, "%Y-%m-%d").date()


def _amount(value):
    if value in (None, ""):
        return None

    return value


def _trip_days(trip):
    if not trip.start_date or not trip.end_date:
        return 0

    return max((trip.end_date - trip.start_date).days + 1, 1)


def _format_date_range(trip):
    if trip.start_date and trip.end_date:
        return f"{trip.start_date.strftime('%b %d, %Y')} - {trip.end_date.strftime('%b %d, %Y')}"
    if trip.start_date:
        return trip.start_date.strftime("%b %d, %Y")
    return "Dates not set"


def _trip_route(trip):
    names = [region.city or region.name for region in trip.regions]
    return " | ".join(names) if names else "No destinations added"


def _trip_budget(trip):
    total = sum(float(item.budget_amount or 0) for item in trip.itinerary_items)
    return total


def _trips_for(user):
    if not user:
        return []

    return (
        Trip.query.filter_by(user_id=user.id)
        .order_by(Trip.created_at.desc())
        .all()
    )


def _trip_groups(trips):
    return {
        "ongoing": [trip for trip in trips if trip.status == "ongoing"],
        "upcoming": [trip for trip in trips if trip.status in ("draft", "planned", "upcoming")],
        "completed": [trip for trip in trips if trip.status == "completed"],
    }


def _all_cities(trips):
    cities = []
    for trip in trips:
        for region in trip.regions:
            name = region.city or region.name
            if name:
                cities.append(name)
    return sorted(set(cities))


def _profile_context(user):
    trips = _trips_for(user)
    cities = _all_cities(trips)
    completed = [trip for trip in trips if trip.status == "completed"]
    planned = [trip for trip in trips if trip.status != "completed"]

    return {
        "profile_user": user,
        "initials": _initials(user),
        "full_name": f"{(user.first_name or '').strip()} {(user.last_name or '').strip()}".strip() if user else "Guest User",
        "handle": f"@{(user.email or 'guest').split('@')[0]}" if user else "@guest",
        "location": ", ".join(part for part in [getattr(user, "city", None), getattr(user, "country", None)] if part) if user else "Sign in to personalize",
        "bio": user.description if user and user.description else "",
        "stats": {
            "trips": len(trips),
            "cities": len(cities),
            "days": sum(_trip_days(trip) for trip in trips),
        },
        "planned_trips": planned[:3],
        "completed_trips": completed[:3],
        "can_edit": bool(user),
    }


def _selected_trip(user, trip_id=None):
    query = Trip.query
    if user:
        query = query.filter_by(user_id=user.id)

    if trip_id:
        trip = query.filter_by(id=trip_id).first()
        if trip:
            return trip

    return query.order_by(Trip.updated_at.desc()).first()


def _redirect_builder(trip):
    return redirect(url_for("main.itinerary_builder", trip_id=trip.id))


def _first_name(user):
    if user and user.first_name:
        return user.first_name

    return "Traveler"


def _travel_readiness(upcoming_trips):
    if not upcoming_trips:
        return {
            "title": "Travel Readiness",
            "summary": "Create a trip to unlock route-specific planning checks.",
            "checks": ["Add dates", "Add destinations", "Build itinerary", "Review budget"],
        }

    trip = upcoming_trips[0]
    route = _trip_route(trip)
    return {
        "title": f"{trip.trip_name} Checklist",
        "summary": route,
        "checks": ["Confirm stays", "Check local transport", "Review activity bookings", "Share itinerary"],
    }


@main.app_template_filter("trip_days")
def trip_days_filter(trip):
    return _trip_days(trip)


@main.app_template_filter("date_range")
def date_range_filter(trip):
    return _format_date_range(trip)


@main.app_template_filter("trip_route")
def trip_route_filter(trip):
    return _trip_route(trip)


@main.app_template_filter("trip_budget")
def trip_budget_filter(trip):
    return _trip_budget(trip)


@main.route("/")
@main.route("/dashboard")
@main.route("/03-dashboard.html")
def index():
    user = _active_user()
    trips = _trips_for(user)
    groups = _trip_groups(trips)
    cities = _all_cities(trips)
    stats = {
        "trips": len(trips),
        "cities": len(cities),
        "days": sum(_trip_days(trip) for trip in trips),
        "budget": sum(_trip_budget(trip) for trip in trips),
    }
    return render_template(
        "index.html",
        user=user,
        first_name=_first_name(user),
        initials=_initials(user),
        stats=stats,
        curated_destinations=CURATED_DESTINATIONS,
        recent_trips=trips[:3],
        upcoming_trips=(groups["ongoing"] + groups["upcoming"])[:2],
        readiness=_travel_readiness((groups["ongoing"] + groups["upcoming"])[:2]),
    )


@main.route("/registerpage")
@main.route("/register", methods=["GET"])
@main.route("/02-register.html")
def register():
    return render_template("auth/register.html")


@main.route("/profile", methods=["GET", "POST"])
@main.route("/07-user-profile.html", methods=["GET", "POST"])
def profile():
    user = _active_user()

    if request.method == "POST":
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))

        current_user.first_name = request.form.get("first_name", "").strip()
        current_user.last_name = request.form.get("last_name", "").strip()
        current_user.phone_number = request.form.get("phone_number", "").strip()
        current_user.city = request.form.get("city", "").strip()
        current_user.country = request.form.get("country", "").strip()
        current_user.description = request.form.get("description", "").strip()
        db.session.commit()
        return redirect(url_for("main.profile"))

    return render_template("profile/profile.html", **_profile_context(user))


@main.route("/mytrips")
@main.route("/06-my-trips.html")
@main.route("/mytrips.html")
def mytrips():
    user = _active_user()
    trips = _trips_for(user)
    cities = _all_cities(trips)
    return render_template(
        "trips/list.html",
        user=user,
        initials=_initials(user),
        trips=trips,
        trip_groups=_trip_groups(trips),
        stats={
            "trips": len(trips),
            "cities": len(cities),
            "days": sum(_trip_days(trip) for trip in trips),
            "spent": sum(_trip_budget(trip) for trip in trips),
        },
    )


@main.route("/createtrip", methods=["GET", "POST"])
@main.route("/create-trip", methods=["GET", "POST"])
@main.route("/04-create-trip.html", methods=["GET", "POST"])
def createtrip():
    user = _active_user()
    if request.method == "POST":
        if not user:
            return redirect(url_for("auth.login"))

        trip = Trip(
            trip_code=f"TRIP-{uuid4().hex[:8].upper()}",
            user_id=user.id,
            trip_name=request.form.get("trip_name") or "New TravelLoop Trip",
            start_date=_date(request.form.get("start_date")),
            end_date=_date(request.form.get("end_date")),
            description=request.form.get("description"),
            status=request.form.get("status") or "planned",
        )
        db.session.add(trip)
        db.session.flush()

        destinations = request.form.get("destinations", "")
        for raw_name in [item.strip() for item in destinations.split(",") if item.strip()]:
            db.session.add(Region(trip_id=trip.id, name=raw_name, city=raw_name))

        budget = request.form.get("budget")
        if budget:
            db.session.add(
                ItineraryItem(
                    trip_id=trip.id,
                    title="Estimated trip budget",
                    description="Created from trip planning form",
                    budget_amount=budget,
                    currency="INR",
                )
            )

        db.session.commit()
        return redirect(url_for("main.itinerary_builder", trip_id=trip.id))

    return render_template("trips/create.html", user=user, initials=_initials(user))


@main.route("/activities")
@main.route("/08-activity-search.html")
def activities():
    query = request.args.get("q", "India heritage and nature experiences")
    query_text = query.lower()
    catalog = [
        activity for activity in ACTIVITY_CATALOG
        if not query_text
        or query_text in activity["title"].lower()
        or query_text in activity["location"].lower()
        or query_text in activity["category"].lower()
    ]
    if not catalog:
        catalog = ACTIVITY_CATALOG
    return render_template("trips/activity-search.html", query=query, activities=catalog, initials=_initials(_active_user()))


@main.route("/itinerary-builder")
@main.route("/itinerary-builder/<int:trip_id>")
@main.route("/05-itinerary-builder.html")
def itinerary_builder(trip_id=None):
    user = _active_user()
    trip = _selected_trip(user, trip_id)
    return render_template("trips/itinerary-builder.html", trip=trip, initials=_initials(user))


@main.route("/itinerary-builder/<int:trip_id>/sections", methods=["POST"])
def add_itinerary_section(trip_id):
    user = _active_user()
    trip = _selected_trip(user, trip_id)
    if not trip:
        return redirect(url_for("main.createtrip"))

    name = request.form.get("name", "").strip()
    city = request.form.get("city", "").strip()
    db.session.add(
        Region(
            trip_id=trip.id,
            name=name or city or "New destination",
            city=city or name,
            country=request.form.get("country", "").strip(),
            start_date=_date(request.form.get("start_date")),
            end_date=_date(request.form.get("end_date")),
        )
    )
    db.session.commit()
    return _redirect_builder(trip)


@main.route("/itinerary-builder/<int:trip_id>/sections/<int:region_id>", methods=["POST"])
def update_itinerary_section(trip_id, region_id):
    user = _active_user()
    trip = _selected_trip(user, trip_id)
    if not trip:
        return redirect(url_for("main.createtrip"))

    region = Region.query.filter_by(id=region_id, trip_id=trip.id).first()
    if not region:
        return _redirect_builder(trip)

    name = request.form.get("name", "").strip()
    city = request.form.get("city", "").strip()
    region.name = name or city or region.name
    region.city = city or name
    region.country = request.form.get("country", "").strip()
    region.start_date = _date(request.form.get("start_date"))
    region.end_date = _date(request.form.get("end_date"))
    db.session.commit()
    return _redirect_builder(trip)


@main.route("/itinerary-builder/<int:trip_id>/sections/<int:region_id>/delete", methods=["POST"])
def delete_itinerary_section(trip_id, region_id):
    user = _active_user()
    trip = _selected_trip(user, trip_id)
    if not trip:
        return redirect(url_for("main.createtrip"))

    region = Region.query.filter_by(id=region_id, trip_id=trip.id).first()
    if region:
        for item in trip.itinerary_items:
            if item.region_id == region.id:
                item.region_id = None
        db.session.delete(region)
        db.session.commit()
    return _redirect_builder(trip)


@main.route("/itinerary-builder/<int:trip_id>/sections/<int:region_id>/items", methods=["POST"])
def add_itinerary_item(trip_id, region_id):
    user = _active_user()
    trip = _selected_trip(user, trip_id)
    if not trip:
        return redirect(url_for("main.createtrip"))

    region = Region.query.filter_by(id=region_id, trip_id=trip.id).first()
    if not region:
        return _redirect_builder(trip)

    title = request.form.get("title", "").strip()
    db.session.add(
        ItineraryItem(
            trip_id=trip.id,
            region_id=region.id,
            title=title or "New activity",
            description=request.form.get("description", "").strip(),
            start_date=_date(request.form.get("start_date")),
            end_date=_date(request.form.get("end_date")),
            budget_amount=_amount(request.form.get("budget_amount")),
            currency=request.form.get("currency", "INR").strip() or "INR",
        )
    )
    db.session.commit()
    return _redirect_builder(trip)


@main.route("/itinerary-builder/<int:trip_id>/items/<int:item_id>", methods=["POST"])
def update_itinerary_item(trip_id, item_id):
    user = _active_user()
    trip = _selected_trip(user, trip_id)
    if not trip:
        return redirect(url_for("main.createtrip"))

    item = ItineraryItem.query.filter_by(id=item_id, trip_id=trip.id).first()
    if not item:
        return _redirect_builder(trip)

    item.title = request.form.get("title", "").strip() or item.title
    item.description = request.form.get("description", "").strip()
    item.start_date = _date(request.form.get("start_date"))
    item.end_date = _date(request.form.get("end_date"))
    item.budget_amount = _amount(request.form.get("budget_amount"))
    item.currency = request.form.get("currency", item.currency or "INR").strip() or "INR"
    db.session.commit()
    return _redirect_builder(trip)


@main.route("/itinerary-builder/<int:trip_id>/items/<int:item_id>/delete", methods=["POST"])
def delete_itinerary_item(trip_id, item_id):
    user = _active_user()
    trip = _selected_trip(user, trip_id)
    if not trip:
        return redirect(url_for("main.createtrip"))

    item = ItineraryItem.query.filter_by(id=item_id, trip_id=trip.id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
    return _redirect_builder(trip)


@main.route("/itinerary")
@main.route("/itinerary/<int:trip_id>")
@main.route("/09-itinerary-view.html")
def itinerary(trip_id=None):
    user = _active_user()
    trip = _selected_trip(user, trip_id)
    return render_template("trips/itinerary-view.html", trip=trip, initials=_initials(user))


@main.route("/01-login.html")
@main.route("/login.html")
def login_alias():
    return redirect(url_for("auth.login"))


@main.route("/10-community.html")
@main.route("/11-packing.html")
@main.route("/12-admin.html")
@main.route("/13-trip-notes.html")
@main.route("/14-invoice.html")
def missing_static_page_aliases():
    return redirect(url_for("main.index"))


@main.route("/users")
def show_users():
    users = User.query.all()
    lines = [
        f"{user.first_name} {user.last_name} | {user.email} | {user.password_hash}"
        for user in users
    ]

    return "<br>".join(lines) if lines else "No users found"
