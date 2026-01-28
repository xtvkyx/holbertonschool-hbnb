import uuid
from app.extensions import db

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=True)

    # No relationships / No foreign keys in Task 7
    user_id = db.Column(db.String(36), nullable=True)
    place_id = db.Column(db.String(36), nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
