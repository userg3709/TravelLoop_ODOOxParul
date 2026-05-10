import os

from flask import Flask
from flask_login import LoginManager

from app.auth import auth_bp
from app.db import db
from app.models import *
from app.routes.routes import main

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "your-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "..", "instance", "travelloop.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app():
    app = Flask(__name__, instance_relative_config=True,
                template_folder="templates",
                static_folder="static")
    app.config.from_object(Config)

    logman = LoginManager()
    logman.init_app(app)
    logman.login_view = "auth.login"

    @logman.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(main)
    app.register_blueprint(auth_bp)

    return app
