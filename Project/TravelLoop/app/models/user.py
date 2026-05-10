from datetime import datetime

from app.models import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone_number = db.Column(db.String(30))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    description = db.Column(db.Text)
    password_hash = db.Column(db.String(255), nullable=False)
    photo_url = db.Column(db.String(255))
    role = db.Column(db.String(50), nullable=False, default="user")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    trips = db.relationship("Trip", back_populates="user", cascade="all, delete-orphan")
