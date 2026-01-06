"""Facade to simplify communication between API and business/persistence."""
from __future__ import annotations

from typing import Dict, List

from hbnb.persistence.repository import InMemoryRepository
from hbnb.business.models.user import User
from hbnb.business.models.amenity import Amenity


class HBnBFacade:
    def __init__(self) -> None:
        self.repo = InMemoryRepository()
        # Enforce unique email for users
        self.repo.register_unique_field("User", "email")
        # Enforce unique name for amenities
        self.repo.register_unique_field("Amenity", "name")

    # -------- Users --------
    def create_user(self, data: Dict) -> User:
        user = User(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            password=data.get("password"),
            is_admin=data.get("is_admin", False),
        )
        return self.repo.add(user)

    def get_user(self, user_id: str) -> User | None:
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
            raise ValueError("Password update is not allowed here")

        return self.repo.update(user)

    # -------- Amenities --------
    def create_amenity(self, name: str, description: str | None = None) -> Amenity:
        if name is None or not str(name).strip():
            raise ValueError("Amenity name is required")

        amenity = Amenity(name=str(name).strip())

        if description is not None and hasattr(amenity, "description"):
            amenity.description = str(description).strip()

        return self.repo.add(amenity)

    def get_amenity(self, amenity_id: str) -> Amenity | None:
        return self.repo.get(Amenity, amenity_id)

    def get_amenities(self) -> List[Amenity]:
        return self.repo.list(Amenity)

    def update_amenity(self, amenity_id: str, data: Dict) -> Amenity | None:
        amenity = self.get_amenity(amenity_id)
        if amenity is None:
            return None

        if "name" in data:
            new_name = data.get("name")
            if new_name is None or not str(new_name).strip():
                raise ValueError("Amenity name cannot be empty")
            amenity.name = str(new_name).strip()

        if "description" in data and hasattr(amenity, "description"):
            desc = data.get("description")
            amenity.description = "" if desc is None else str(desc).strip()

        return self.repo.update(amenity)
