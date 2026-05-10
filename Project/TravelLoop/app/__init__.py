from flask import Flask
from app.config import Config
from app import database
from Project.TravelLoop.app.routes.routes import main
from app.auth import auth_bp


def create_app():
    app = Flask(__name__, instance_relative_config=True,
                template_folder="templates",
                static_folder="static")
    app.config.from_object(Config)

    database.init_app(app)
    app.register_blueprint(main)
    app.register_blueprint(auth_bp)

    return app
