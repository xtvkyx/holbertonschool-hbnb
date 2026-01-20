import re
from hbnb.extensions import bcrypt

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class User:
    """
    Simple in-memory User model for Part 3 Task 1.
    Later you will convert this into a SQLAlchemy model.
    """
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        self.id = None  # can be set by storage later
        self.first_name = self._validate_name(first_name, "first_name")
        self.last_name = self._validate_name(last_name, "last_name")
        self.email = self._validate_email(email)
        self.is_admin = bool(is_admin)

        # Store only hashed password
        self.password_hash = self._hash_password(password)

    @staticmethod
    def _validate_name(value, field):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a non-empty string")
        return value.strip()

    @staticmethod
    def _validate_email(email):
        if not isinstance(email, str) or not _EMAIL_RE.match(email.strip()):
            raise ValueError("email must be a valid email address")
        return email.strip().lower()

    @staticmethod
    def _hash_password(password: str) -> str:
        if not isinstance(password, str) or len(password) < 6:
            raise ValueError("password must be at least 6 characters")
        hashed = bcrypt.generate_password_hash(password)
        return hashed.decode("utf-8")  # store as string

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_public_dict(self):
        """Return user fields WITHOUT password/hash."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
        }
