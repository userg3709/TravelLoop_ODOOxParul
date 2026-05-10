import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    DATABASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "instance", "travelloop.sqlite")
