from flask import Flask,render_template,request,redirect,session,flash,url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash,generate_password_hash
import json
import os
from datetime import datetime
from enum import Enum


local_server=True

with open('config.json','r') as f:
    parames = json.load(f)["params"]


app = Flask(__name__)
app.secret_key='super-secret-key'
app.config['upload']=parames['upload']
if(local_server==True):
    app.config['SQLALCHEMY_DATABASE_URI'] = parames['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = parames['online_uri']
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(20), nullable = False)
    phone_num=db.Column(db.String(12), nullable = False)
    companyName=db.Column(db.String(12), nullable = False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    year_of_joining = db.Column(db.Integer, nullable=False)
    role=db.Column(db.String(12),nullable=False)
    password = db.Column(db.String(200), nullable=False)  
    login_id = db.Column(db.String(50), unique=True, nullable=False)

ALLOWED_ROLES = ["Admin", "Employee"]



def generate_login_id(first_name, last_name, year_of_joining):
    initials = first_name[0].upper() + last_name[0].upper()
    count = Employee.query.filter_by(
        year_of_joining=year_of_joining
    ).count()
    serial_number = count + 1
    serial_str = str(serial_number).zfill(3)
    login_id = f"OI{initials}{year_of_joining}{serial_str}"

    return login_id




@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for("dashboard"))

    if request.method == 'POST':
        email = request.form.get("username")
        password = request.form.get("password")

        employee = Employee.query.filter_by(email=email).first()

        if employee and check_password_hash(employee.password, password):
            session['user'] = employee.id
            session['role'] = employee.role
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials", "error")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if 'user' not in session:
        return redirect(url_for("login"))
    employee = Employee.query.get(session['user'])
    return render_template("dashboard.html", employee=employee)




@app.route("/signup",methods=['GET','POST'])
def signup():
    userRole = request.form.get("role", "Employee")
    if request.method == 'POST' and userRole=="Admin":
                first_name = request.form.get('slug')
                last_name = request.form.get('slug')
                email = request.form.get('title')
                companyName = request.form.get('content')
                phone = request.form.get('image')
                password = request.form.get('image')
                confirmPassword = request.form.get('image')
                year_of_joining = int(request.form['year_of_joining'])
                
                login_id = generate_login_id(first_name, last_name, year_of_joining)
                hashed_password = generate_password_hash(password)

                if role not in ALLOWED_ROLES:
                    role = "Employee"
                if password!=confirmPassword:
                    flash("Passwords do not match", "error") 
                    return render_template("signup.html")
                

                employee = Employee(first_name=first_name,last_name=last_name, email=email,companyName=companyName, phone=phone,password=password, role=role,login_id=login_id)
                db.session.add(employee)
                db.session.commit()

    return render_template("login.html")


@app.route("/logout")
def out():
    session.pop('user')
    return render_template("logout.html")

if __name__ == "__main__":
    app.run(debug=True,host='127.0.0.1',port=5555)