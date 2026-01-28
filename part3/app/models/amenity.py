import uuid
from app.extensions import db

class Amenity(db.Model):
    __tablename__ = "amenities"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}
