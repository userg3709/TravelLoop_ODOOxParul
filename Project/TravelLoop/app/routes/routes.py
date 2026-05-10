from flask import Blueprint, redirect, render_template, url_for

from app.models import User


main = Blueprint("main", __name__)


@main.route("/")
@main.route("/dashboard")
@main.route("/03-dashboard.html")
def index():
    return render_template("index.html")


@main.route("/registerpage")
@main.route("/register", methods=["GET"])
@main.route("/02-register.html")
def register():
    return render_template("auth/register.html")


@main.route("/profile")
@main.route("/07-user-profile.html")
def profile():
    return render_template("profile/profile.html")


@main.route("/mytrips")
@main.route("/06-my-trips.html")
@main.route("/mytrips.html")
def mytrips():
    return render_template("trips/list.html")


@main.route("/createtrip")
@main.route("/create-trip")
@main.route("/04-create-trip.html")
def createtrip():
    return render_template("trips/create.html")


@main.route("/activities")
@main.route("/08-activity-search.html")
def activities():
    return render_template("trips/activity-search.html")


@main.route("/itinerary-builder")
@main.route("/05-itinerary-builder.html")
def itinerary_builder():
    return render_template("trips/itinerary-builder.html")


@main.route("/itinerary")
@main.route("/09-itinerary-view.html")
def itinerary():
    return render_template("trips/itinerary-view.html")


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
