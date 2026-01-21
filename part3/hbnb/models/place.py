import uuid
from hbnb.extensions import db

class Place(db.Model):
    __tablename__ = "places"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)

    # owner of the place
    owner_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "owner_id": self.owner_id
        }

