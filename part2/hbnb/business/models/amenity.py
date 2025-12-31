#!/usr/bin/python3
"""Amenity model."""

from .base import BaseModel


class Amenity(BaseModel):
    """Represents an amenity (e.g., Wi-Fi, Parking)."""

    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name = self._validate_name(name)

    @staticmethod
    def _validate_name(name: str) -> str:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        return name.strip()

    def rename(self, new_name: str) -> None:
        self.name = self._validate_name(new_name)
        self.updated_at = self._now() if hasattr(self, "_now") else self.updated_at
