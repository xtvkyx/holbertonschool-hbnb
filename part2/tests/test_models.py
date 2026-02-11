from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# User
user = User("Raneem", "Test", "r@test.com", "StrongPass123")


# Place
place = Place(
    title="Test Place",
    price=100.0,
    latitude=24.7,
    longitude=46.7,
    owner=user
)

# Amenity
amenity = Amenity("WiFi")
place.add_amenity(amenity)

# Review
review = Review(
    text="Great place",
    rating=5,
    user=user,
    place=place
)
place.add_review(review)

print("All model tests passed ✅")
