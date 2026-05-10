from app.models import db


class ItineraryItem(db.Model):
    __tablename__ = "itinerary_items"

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey("regions.id", ondelete="SET NULL"))
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    budget_amount = db.Column(db.Numeric(10, 2))
    currency = db.Column(db.String(10), nullable=False, default="INR")

    trip = db.relationship("Trip", back_populates="itinerary_items")
    region = db.relationship("Region", back_populates="itinerary_items")
