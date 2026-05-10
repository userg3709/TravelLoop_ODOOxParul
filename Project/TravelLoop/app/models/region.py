from app.models import db

class Region(db.Model):
    __tablename__ = "regions"

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    trip = db.relationship("Trip", back_populates="regions")
    itinerary_items = db.relationship("ItineraryItem", back_populates="region")
