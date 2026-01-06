"""Facade to simplify communication between API and business/persistence."""
from __future__ import annotations

from typing import Dict, List, Optional, Any

from hbnb.persistence.repository import InMemoryRepository
from hbnb.business.models.user import User
from hbnb.business.models.amenity import Amenity
from hbnb.business.models.place import Place


class HBnBFacade:
    def __init__(self) -> None:
        self.repo = InMemoryRepository()

        # Enforce unique email for users
        self.repo.register_unique_field("User", "email")

        # Enforce unique name for amenities
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
    def create_amenity(self, name: str) -> Amenity:
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
    # Helpers (Places)
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
