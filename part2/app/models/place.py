from app.models.base import BaseModel

class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude, owner, description=None):
        super().__init__()

        if not title or len(title) > 100:
            raise ValueError("Invalid title")
        if price <= 0:
            raise ValueError("Price must be positive")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Invalid latitude")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Invalid longitude")

        # ✅ owner must "look like" a User object
        if owner is None or not hasattr(owner, "id") or not hasattr(owner, "email"):
            raise ValueError("Owner must be a valid User object")

        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = latitude
        self.longitude = float(longitude)
        self.owner = owner
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        # ✅ review must look like a Review object and belong to this place
        if review is None or not hasattr(review, "id") or not hasattr(review, "rating"):
            raise ValueError("Invalid review object")
        if not hasattr(review, "place") or review.place is not self:
            raise ValueError("Review.place must reference this Place object")
        self.reviews.append(review)
        self.save()

    def add_amenity(self, amenity):
        # ✅ amenity must look like an Amenity object
        if amenity is None or not hasattr(amenity, "id") or not hasattr(amenity, "name"):
            raise ValueError("Invalid amenity object")
        self.amenities.append(amenity)
        self.save()
