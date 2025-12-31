"""Facade to simplify communication between API and business/persistence."""
from __future__ import annotations
from hbnb.persistence.repository import InMemoryRepository


class HBnBFacade:
    def __init__(self) -> None:
        self.repo = InMemoryRepository()

        # Example for future: enforce unique email for User
        # (When you create User model, uncomment/register it)
        # self.repo.register_unique_field("User", "email")

    # Later you will add:
    # create_user, get_user, list_users...
    # create_place, create_review, etc.
