"""Facade to simplify communication between API and business/persistence."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from hbnb.persistence.repository import InMemoryRepository
from hbnb.business.models.user import User
from hbnb.business.models.amenity import Amenity
from hbnb.business.models.place import Place
from hbnb.business.models.review import Review


class HBnBFacade:
    def __init__(self) -> None:
        self.repo = InMemoryRepository()

        # Enforce unique fields
        self.repo.register_unique_field("User", "email")
        self.repo.register_unique_field("Amenity", "name")

    # =====================================================
    # Users
    # =====================================================
    def create_user(self, data: Dict) -> User:
        user = User(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            password=data.get("password"),
            is_admin=data.get("is_admin", False),
        )
        return self.repo.add(user)

    def get_user(self, user_id: str) -> Optional[User]:
        return self.repo.get(User, user_id)

    def list_users(self) -> List[User]:
        return self.repo.list(User)

    def update_user(self, user_id: str, data: Dict) -> User:
        user = self.get_user(user_id)
        if user is None:
            raise KeyError("User not found")

        if "first_name" in data:
            user.first_name = User._validate_name(data["first_name"], "first_name")
        if "last_name" in data:
            user.last_name = User._validate_name(data["last_name"], "last_name")
        if "email" in data:
            user.email = User._validate_email(data["email"])

        if "password" in data or "password_hash" in data:
            raise ValueError("Password update is not allowed")

        return self.repo.update(user)

    # =====================================================
    # Amenities
    # =====================================================
    def create_amenity(self, name: str, description: str | None = None) -> Amenity:
        # description موجودة فقط للتوافق لو API عندك يرسلها؛ ما نستخدمها بالموديل.
        if name is None or not str(name).strip():
            raise ValueError("Amenity name is required")

        amenity = Amenity(name=str(name).strip())
        return self.repo.add(amenity)

    def get_amenity(self, amenity_id: str) -> Optional[Amenity]:
        return self.repo.get(Amenity, amenity_id)

    def get_amenities(self) -> List[Amenity]:
        return self.repo.list(Amenity)

    def update_amenity(self, amenity_id: str, data: Dict) -> Optional[Amenity]:
        amenity = self.get_amenity(amenity_id)
        if amenity is None:
            return None

        if "name" in data:
            new_name = data.get("name")
            if new_name is None or not str(new_name).strip():
                raise ValueError("Amenity name cannot be empty")
            amenity.rename(str(new_name))

        return self.repo.update(amenity)

    # =====================================================
    # Helpers (Places/Reviews)
    # =====================================================
    @staticmethod
    def _validate_required_str(value: Any, field: str) -> str:
        if value is None or not str(value).strip():
            raise ValueError(f"{field} is required")
        return str(value).strip()

    @staticmethod
    def _validate_price_per_night(value: Any) -> float:
        if value is None:
            raise ValueError("price_per_night is required")
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError("price_per_night must be a number")
        if value < 0:
            raise ValueError("price_per_night must be >= 0")
        return value

    @staticmethod
    def _validate_rating_any(value: Any) -> int:
        if value is None:
            raise ValueError("rating is required")
        if not isinstance(value, int):
            try:
                value = int(value)
            except (TypeError, ValueError):
                raise ValueError("rating must be an integer")
        if value < 1 or value > 5:
            raise ValueError("rating must be between 1 and 5")
        return value

    @staticmethod
    def _validate_comment(value: Any) -> str:
        if value is None or not isinstance(value, str) or not value.strip():
            raise ValueError("comment must be a non-empty string")
        return value.strip()

    def _resolve_owner(self, owner_id: str) -> User:
        owner = self.repo.get(User, owner_id)
        if owner is None:
            raise KeyError("Owner (user) not found")
        return owner

    def _resolve_amenities(self, amenity_ids: list[str]) -> list[Amenity]:
        amenities: list[Amenity] = []
        for aid in amenity_ids:
            a = self.repo.get(Amenity, aid)
            if a is None:
                raise KeyError(f"Amenity not found: {aid}")
            amenities.append(a)
        return amenities

    def _place_to_dict(self, place: Place, owner: User, amenities: list[Amenity]) -> dict:
        reviews = []
        for rid in getattr(place, "review_ids", []) or []:
            r = self.repo.get(Review, rid)
            if r is not None:
                reviews.append({
                    "id": r.id,
                    "user_id": r.user_id,
                    "place_id": r.place_id,
                    "rating": r.rating,
                    "comment": r.comment,
                })

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price_per_night": place.price_per_night,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": {
                "id": owner.id,
                "first_name": owner.first_name,
                "last_name": owner.last_name,
                "email": owner.email,
            },
            "amenities": [{"id": a.id, "name": a.name} for a in amenities],
            "reviews": reviews,
        }

    # =====================================================
    # Places
    # =====================================================
    def create_place(self, data: Dict) -> dict:
        owner_id = self._validate_required_str(data.get("owner_id"), "owner_id")
        title = self._validate_required_str(data.get("title"), "title")
        description = "" if data.get("description") is None else str(data.get("description"))

        price_per_night = self._validate_price_per_night(data.get("price_per_night"))
        latitude = Place._validate_lat(data.get("latitude"))
        longitude = Place._validate_lng(data.get("longitude"))

        amenity_ids = data.get("amenity_ids") or []
        if not isinstance(amenity_ids, list):
            raise ValueError("amenity_ids must be a list")

        owner = self._resolve_owner(owner_id)
        amenities = self._resolve_amenities([str(x) for x in amenity_ids])

        place = Place(
            owner_id=owner.id,
            title=title,
            description=description,
            price_per_night=price_per_night,
            latitude=latitude,
            longitude=longitude,
        )

        for a in amenities:
            place.add_amenity(a.id)

        saved = self.repo.add(place)
        return self._place_to_dict(saved, owner, amenities)

    def get_place(self, place_id: str) -> Optional[dict]:
        place = self.repo.get(Place, place_id)
        if place is None:
            return None

        owner = self._resolve_owner(place.owner_id)

        amenities: list[Amenity] = []
        for aid in place.amenity_ids:
            a = self.repo.get(Amenity, aid)
            if a is not None:
                amenities.append(a)

        return self._place_to_dict(place, owner, amenities)

    def get_places(self) -> List[dict]:
        return [self.get_place(p.id) for p in self.repo.list(Place)]

    def update_place(self, place_id: str, data: Dict) -> Optional[dict]:
        place = self.repo.get(Place, place_id)
        if place is None:
            return None

        place.update_details(
            title=data.get("title"),
            description=data.get("description"),
            price_per_night=data.get("price_per_night"),
        )

        if "latitude" in data:
            place.latitude = Place._validate_lat(data.get("latitude"))
        if "longitude" in data:
            place.longitude = Place._validate_lng(data.get("longitude"))

        # amenities update
        amenities: list[Amenity] = []
        if "amenity_ids" in data:
            amenity_ids = data.get("amenity_ids") or []
            if not isinstance(amenity_ids, list):
                raise ValueError("amenity_ids must be a list")

            amenities = self._resolve_amenities([str(x) for x in amenity_ids])
            place.amenity_ids = set()
            for a in amenities:
                place.add_amenity(a.id)
        else:
            for aid in place.amenity_ids:
                a = self.repo.get(Amenity, aid)
                if a:
                    amenities.append(a)

        saved = self.repo.update(place)
        owner = self._resolve_owner(saved.owner_id)
        return self._place_to_dict(saved, owner, amenities)

    # =====================================================
    # Reviews
    # =====================================================
    def _review_to_dict(self, review: Review) -> dict:
        return {
            "id": review.id,
            "user_id": review.user_id,
            "place_id": review.place_id,
            "rating": review.rating,
            "comment": review.comment,
        }

    def create_review(self, data: Dict) -> dict:
        user_id = self._validate_required_str(data.get("user_id"), "user_id")
        place_id = self._validate_required_str(data.get("place_id"), "place_id")
        rating = self._validate_rating_any(data.get("rating"))

        comment_in = data.get("comment", data.get("text"))
        comment = self._validate_comment(comment_in)

        user = self.repo.get(User, user_id)
        if user is None:
            raise KeyError("User not found")

        place = self.repo.get(Place, place_id)
        if place is None:
            raise KeyError("Place not found")

        review = Review(user_id=user_id, place_id=place_id, rating=rating, comment=comment)
        saved = self.repo.add(review)

        # link review to place
        if hasattr(place, "link_review"):
            place.link_review(saved.id)
        elif hasattr(place, "review_ids"):
            if saved.id not in place.review_ids:
                place.review_ids.append(saved.id)

        self.repo.update(place)
        return self._review_to_dict(saved)

    def get_review(self, review_id: str) -> Optional[dict]:
        review = self.repo.get(Review, review_id)
        if review is None:
            return None
        return self._review_to_dict(review)

    def get_reviews(self) -> List[dict]:
        return [self._review_to_dict(r) for r in self.repo.list(Review)]

    def update_review(self, review_id: str, data: Dict) -> dict:
        review = self.repo.get(Review, review_id)
        if review is None:
            raise KeyError("Review not found")

        rating = data.get("rating") if "rating" in data else None
        comment = data.get("comment", data.get("text")) if ("comment" in data or "text" in data) else None

        if rating is not None:
            rating = self._validate_rating_any(rating)
        if comment is not None:
            comment = self._validate_comment(comment)

        if hasattr(review, "update_review"):
            review.update_review(rating=rating, comment=comment)
        else:
            if rating is not None:
                review.rating = rating
            if comment is not None:
                review.comment = comment

        saved = self.repo.update(review)
        return self._review_to_dict(saved)

    def delete_review(self, review_id: str) -> None:
        review = self.repo.get(Review, review_id)
        if review is None:
            raise KeyError("Review not found")

        # unlink from place
        place = self.repo.get(Place, review.place_id)
        if place is not None and hasattr(place, "review_ids"):
            if review_id in place.review_ids:
                place.review_ids = [rid for rid in place.review_ids if rid != review_id]
                self.repo.update(place)

        # delete from repository (support different repo implementations)
        if hasattr(self.repo, "delete"):
            self.repo.delete(Review, review_id)
            return
        if hasattr(self.repo, "remove"):
            self.repo.remove(Review, review_id)
            return
        if hasattr(self.repo, "_storage"):
            self.repo._storage.get("Review", {}).pop(review_id, None)
            return

        raise ValueError("Repository does not support delete operation")

    def get_place_reviews(self, place_id: str) -> List[dict]:
        place = self.repo.get(Place, place_id)
        if place is None:
            raise KeyError("Place not found")

        reviews: List[dict] = []
        for rid in getattr(place, "review_ids", []) or []:
            r = self.repo.get(Review, rid)
            if r is not None:
                reviews.append(self._review_to_dict(r))
        return reviews
