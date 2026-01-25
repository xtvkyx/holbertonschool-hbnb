#!/usr/bin/python3
"""Review model."""

from .base import BaseModel


class Review(BaseModel):
    """Represents a review written by a user about a place."""

    def __init__(
        self,
        user_id: str,
        place_id: str,
        rating: int,
        comment: str = "",
        **kwargs
    ):
        super().__init__(**kwargs)

        self.user_id = self._validate_id(user_id, "user_id")
        self.place_id = self._validate_id(place_id, "place_id")
        self.rating = self._validate_rating(rating)
        self.comment = self._validate_comment(comment)

    @staticmethod
    def _validate_id(value: str, field: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a non-empty string")
        return value.strip()

    @staticmethod
    def _validate_rating(rating: int) -> int:
        if not isinstance(rating, int):
            raise ValueError("rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("rating must be between 1 and 5")
        return rating

    @staticmethod
    def _validate_comment(comment: str) -> str:
        if not isinstance(comment, str):
            raise ValueError("comment must be a string")
        return comment.strip()

    def update_review(self, rating=None, comment=None) -> None:
        if rating is not None:
            self.rating = self._validate_rating(rating)
        if comment is not None:
            self.comment = self._validate_comment(comment)
        self.updated_at = self._now() if hasattr(self, "_now") else self.updated_at
