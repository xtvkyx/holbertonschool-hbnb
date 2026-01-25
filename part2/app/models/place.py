#!/usr/bin/python3
"""Place model."""

from .base import BaseModel


class Place(BaseModel):
    """Represents a place listing."""

    def __init__(
        self,
        owner_id: str,
        title: str,
        description: str = "",
        price_per_night: float = 0.0,
        latitude: float = 0.0,
        longitude: float = 0.0,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.owner_id = self._validate_id(owner_id, "owner_id")
        self.title = self._validate_text(title, "title")
        self.description = self._validate_text(description, "description", allow_empty=True)
        self.price_per_night = self._validate_price(price_per_night)
        self.latitude = self._validate_lat(latitude)
        self.longitude = self._validate_lng(longitude)

        # Relationships (IDs)
        self.amenity_ids = set()
        self.review_ids = []

    @staticmethod
    def _validate_id(value: str, field: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a non-empty string")
        return value.strip()

    @staticmethod
    def _validate_text(value: str, field: str, allow_empty: bool = False) -> str:
        if not isinstance(value, str):
            raise ValueError(f"{field} must be a string")
        val = value.strip()
        if not allow_empty and not val:
            raise ValueError(f"{field} must be a non-empty string")
        return val

    @staticmethod
    def _validate_price(value) -> float:
        if not isinstance(value, (int, float)):
            raise ValueError("price_per_night must be a number")
        value = float(value)
        if value < 0:
            raise ValueError("price_per_night must be >= 0")
        return value

    @staticmethod
    def _validate_lat(value) -> float:
        if not isinstance(value, (int, float)):
            raise ValueError("latitude must be a number")
        value = float(value)
        if value < -90 or value > 90:
            raise ValueError("latitude must be between -90 and 90")
        return value

    @staticmethod
    def _validate_lng(value) -> float:
        if not isinstance(value, (int, float)):
            raise ValueError("longitude must be a number")
        value = float(value)
        if value < -180 or value > 180:
            raise ValueError("longitude must be between -180 and 180")
        return value

    def update_details(self, title=None, description=None, price_per_night=None) -> None:
        if title is not None:
            self.title = self._validate_text(title, "title")
        if description is not None:
            self.description = self._validate_text(description, "description", allow_empty=True)
        if price_per_night is not None:
            self.price_per_night = self._validate_price(price_per_night)
        self.updated_at = self._now() if hasattr(self, "_now") else self.updated_at

    def add_amenity(self, amenity_id: str) -> None:
        amenity_id = self._validate_id(amenity_id, "amenity_id")
        self.amenity_ids.add(amenity_id)
        self.updated_at = self._now() if hasattr(self, "_now") else self.updated_at

    def remove_amenity(self, amenity_id: str) -> None:
        if amenity_id in self.amenity_ids:
            self.amenity_ids.remove(amenity_id)
            self.updated_at = self._now() if hasattr(self, "_now") else self.updated_at

    def link_review(self, review_id: str) -> None:
        if review_id and review_id not in self.review_ids:
            self.review_ids.append(review_id)
