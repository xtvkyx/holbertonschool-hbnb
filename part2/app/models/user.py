#!/usr/bin/python3
"""User model."""

import re
import hashlib
from .base import BaseModel

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class User(BaseModel):
    """Represents a system user."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        is_admin: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.first_name = self._validate_name(first_name, "first_name")
        self.last_name = self._validate_name(last_name, "last_name")
        self.email = self._validate_email(email)
        self.password_hash = self._hash_password(password)
        self.is_admin = bool(is_admin)

        # Relationships (store IDs to keep it simple)
        self.place_ids = []
        self.review_ids = []

    @staticmethod
    def _validate_name(value: str, field: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a non-empty string")
        return value.strip()

    @staticmethod
    def _validate_email(email: str) -> str:
        if not isinstance(email, str) or not _EMAIL_RE.match(email.strip()):
            raise ValueError("email must be a valid email address")
        return email.strip().lower()

    @staticmethod
    def _hash_password(password: str) -> str:
        if not isinstance(password, str) or len(password) < 6:
            raise ValueError("password must be at least 6 characters")
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def verify_password(self, password: str) -> bool:
        return self.password_hash == hashlib.sha256(password.encode("utf-8")).hexdigest()

    def update_profile(self, first_name=None, last_name=None, email=None) -> None:
        if first_name is not None:
            self.first_name = self._validate_name(first_name, "first_name")
        if last_name is not None:
            self.last_name = self._validate_name(last_name, "last_name")
        if email is not None:
            self.email = self._validate_email(email)
        self.updated_at = self._now() if hasattr(self, "_now") else self.updated_at

    def link_place(self, place_id: str) -> None:
        if place_id and place_id not in self.place_ids:
            self.place_ids.append(place_id)

    def link_review(self, review_id: str) -> None:
        if review_id and review_id not in self.review_ids:
            self.review_ids.append(review_id)
