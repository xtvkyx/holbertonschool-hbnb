import uuid
from app.extensions import db
from app.models.associations import place_amenity

class Place(db.Model):
    __tablename__ = "places"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # FK (Task 8)
    owner_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Relationships (Task 8)
    owner = db.relationship("User", back_populates="places")
    reviews = db.relationship("Review", back_populates="place", cascade="all, delete-orphan")

    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        back_populates="places",
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id
        }
