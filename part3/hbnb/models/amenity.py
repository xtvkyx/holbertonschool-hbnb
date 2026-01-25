import uuid
from hbnb.extensions import db

class Amenity(db.Model):
    __tablename__ = "amenities"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False, unique=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name}
