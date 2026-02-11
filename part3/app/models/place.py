from app.extensions import db
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
import uuid

class Place(db.Model):
    __tablename__ = "places"

    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(100), nullable=False)
    description = Column(String(1024), nullable=True)
    price = Column(Float, nullable=False)
    owner_id = Column(String(60), ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="places")
    reviews = relationship("Review", back_populates="place", cascade="all, delete-orphan")
    amenities = relationship("Amenity", secondary="place_amenity", back_populates="places")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "owner_id": self.owner_id
        }

