# app/services/hbnb_facade.py

from app.extensions import db


class HBnBFacade:
    """
    Facade layer that centralizes DB operations for the API.
    IMPORTANT: Models must NOT import this file (avoid circular imports).
    """

    # -------------------------
    # Helpers
    # -------------------------
    def _commit(self):
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    # -------------------------
    # Users
    # -------------------------
    def create_user(self, **data):
        from app.models.user import User  # local import avoids circular imports
        user = User(**data)
        db.session.add(user)
        self._commit()
        return user

    def get_user(self, user_id):
        from app.models.user import User
        return User.query.get(user_id)

    def get_user_by_email(self, email):
        from app.models.user import User
        return User.query.filter_by(email=email).first()

    def get_users(self):
        from app.models.user import User
        return User.query.all()

    def update_user(self, user_id, **data):
        user = self.get_user(user_id)
        if not user:
            return None
        for k, v in data.items():
            setattr(user, k, v)
        self._commit()
        return user

    def delete_user(self, user_id):
        user = self.get_user(user_id)
        if not user:
            return False
        db.session.delete(user)
        self._commit()
        return True

    # -------------------------
    # Places
    # -------------------------
    def create_place(self, **data):
        from app.models.place import Place
        place = Place(**data)
        db.session.add(place)
        self._commit()
        return place

    def get_place(self, place_id):
        from app.models.place import Place
        return Place.query.get(place_id)

    def get_places(self):
        from app.models.place import Place
        return Place.query.all()

    def update_place(self, place_id, **data):
        place = self.get_place(place_id)
        if not place:
            return None
        for k, v in data.items():
            setattr(place, k, v)
        self._commit()
        return place

    def delete_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return False
        db.session.delete(place)
        self._commit()
        return True

    # -------------------------
    # Reviews
    # -------------------------
    def create_review(self, **data):
        from app.models.review import Review
        review = Review(**data)
        db.session.add(review)
        self._commit()
        return review

    def get_review(self, review_id):
        from app.models.review import Review
        return Review.query.get(review_id)

    def get_reviews(self):
        from app.models.review import Review
        return Review.query.all()

    def get_reviews_by_place(self, place_id):
        from app.models.review import Review
        return Review.query.filter_by(place_id=place_id).all()

    def update_review(self, review_id, **data):
        review = self.get_review(review_id)
        if not review:
            return None
        for k, v in data.items():
            setattr(review, k, v)
        self._commit()
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return False
        db.session.delete(review)
        self._commit()
        return True

    # -------------------------
    # Amenities
    # -------------------------
    def create_amenity(self, **data):
        from app.models.amenity import Amenity
        amenity = Amenity(**data)
        db.session.add(amenity)
        self._commit()
        return amenity

    def get_amenity(self, amenity_id):
        from app.models.amenity import Amenity
        return Amenity.query.get(amenity_id)

    def get_amenities(self):
        from app.models.amenity import Amenity
        return Amenity.query.all()

    def update_amenity(self, amenity_id, **data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        for k, v in data.items():
            setattr(amenity, k, v)
        self._commit()
        return amenity

    def delete_amenity(self, amenity_id):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return False
        db.session.delete(amenity)
        self._commit()
        return True

    # -------------------------
    # Place <-> Amenities (Many-to-Many)
    # -------------------------
    def add_amenity_to_place(self, place_id, amenity_id):
        place = self.get_place(place_id)
        amenity = self.get_amenity(amenity_id)
        if not place or not amenity:
            return None

        # assuming Place.amenities relationship exists
        if amenity not in place.amenities:
            place.amenities.append(amenity)
            self._commit()
        return place

    def remove_amenity_from_place(self, place_id, amenity_id):
        place = self.get_place(place_id)
        amenity = self.get_amenity(amenity_id)
        if not place or not amenity:
            return None

        if amenity in place.amenities:
            place.amenities.remove(amenity)
            self._commit()
        return place

