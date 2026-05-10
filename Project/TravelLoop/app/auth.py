from flask import render_template,Blueprint,request,url_for,redirect
from flask_login import login_required,logout_user,login_user,current_user
from werkzeug.security import generate_password_hash
auth_bp=Blueprint("auth",__name__)





@auth_bp.route("/register", methods=['POST'])
def register():

    first_name = request.form.get("firstName")
    last_name = request.form.get("lastName")
    email = request.form.get("email")
    phone = request.form.get("phone")
    city = request.form.get("city")
    country = request.form.get("country")
    password = request.form.get("password")
    about = request.form.get("about")

    # validation
    if not email or not password:
        return "Email and password required", 400

    # hash password
    hashed_password = generate_password_hash(password)

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        city=city,
        country=country,
        password=hashed_password,
        about=about
    )
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))

@auth_bp.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form.get("username")
        password = request.form.get("password")
    return render_template("auth/login.html")