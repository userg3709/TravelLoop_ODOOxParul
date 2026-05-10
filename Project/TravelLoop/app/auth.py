from flask import render_template,Blueprint
from flask_login import login_required,logout_user,login_user,current_user

auth_bp=Blueprint("auth",__name__)

@auth_bp.route("/login",methods=['GET','POST'])
def login():
    return render_template("auth/login.html")