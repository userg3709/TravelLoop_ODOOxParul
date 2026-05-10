from flask import render_template,Blueprint,request,url_for,redirect
from flask_login import login_required,logout_user,login_user,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from app.models import User
from app.db import db
auth_bp=Blueprint("auth",__name__)





@auth_bp.route("/register", methods=['POST'])
def register():

    first_name = request.form.get("firstName")
    last_name = request.form.get("lastName")
    email = request.form.get("email")
    phone_number = request.form.get("phone_number")
    city = request.form.get("city")
    country = request.form.get("country")
    password = request.form.get("password")
    description = request.form.get("description")

    # validation
    if not email or not password:
        return "Email and password required", 400
    
    if User.query.filter_by(email=email).first():
        return "User already exists", 400

    # hash password
    hashed_password = generate_password_hash(password)

    
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        city=city,
        country=country,
        password_hash=hashed_password,
        description=description
    )
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            return "Invalid credentials", 401

        login_user(user)

        return redirect("/")

    return render_template("auth/login.html")