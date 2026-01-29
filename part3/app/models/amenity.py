import uuid
from app.extensions import db
from app.models.associations import place_amenity

class Amenity(db.Model):
    __tablename__ = "amenities"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)

    # Relationship (Task 8)
    places = db.relationship(
        "Place",
        secondary=place_amenity,
        back_populates="amenities",
    )

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}
