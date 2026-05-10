from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import db
from app.models import User


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    first_name = request.form.get("firstName")
    last_name = request.form.get("lastName")
    email = request.form.get("email")
    phone_number = request.form.get("phone_number") or request.form.get("phone")
    city = request.form.get("city")
    country = request.form.get("country")
    password = request.form.get("password")
    description = request.form.get("description") or request.form.get("about")

    if not email or not password:
        return "Email and password required", 400

    if User.query.filter_by(email=email).first():
        return "User already exists", 400

    new_user = User(
        first_name=first_name or "",
        last_name=last_name or "",
        email=email,
        phone_number=phone_number,
        city=city,
        country=country,
        password_hash=generate_password_hash(password),
        description=description,
    )
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            return "Invalid credentials", 401

        login_user(user)

        return redirect(url_for("main.index"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
