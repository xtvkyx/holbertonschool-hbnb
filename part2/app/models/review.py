from app.models.base import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, user, place):
        super().__init__()

        if not text:
            raise ValueError("Text is required")

        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

        # user must look like a User object
        if user is None or not hasattr(user, "id") or not hasattr(user, "email"):
            raise ValueError("Invalid user object")

        # place must look like a Place object
        if place is None or not hasattr(place, "id") or not hasattr(place, "title"):
            raise ValueError("Invalid place object")

        self.text = text
        self.rating = rating
        self.user = user
        self.place = place
