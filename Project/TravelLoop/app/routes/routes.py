from flask import Blueprint, render_template


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/registerpage")
def register():
    return render_template("auth/register.html")

@main.route("/profile")
def register():
    return render_template("profile/profile.html")

@main.route("/mytrips")
def mytrips():
    return render_template("trips/list.html")

@main.route("/createtrip")
def createtrip():
    return render_template("trips/create.html")

