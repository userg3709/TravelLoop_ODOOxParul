from flask import Blueprint, render_template
from app.models import *

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/registerpage")
def register():
    return render_template("auth/register.html")

@main.route("/profile")
def profile():
    return render_template("profile/profile.html")

@main.route("/mytrips")
def mytrips():
    return render_template("trips/list.html")

@main.route("/createtrip")
def createtrip():
    return render_template("trips/create.html")

@main.route("/users")
def show_users():
    users = User.query.all()

    for user in users:
        # Use correct fields from your model
        print(f"{user.first_name} {user.last_name} | {user.email} | {user.password_hash}")

    return "done"