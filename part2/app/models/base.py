import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        """Update updated_at timestamp"""
        self.updated_at = datetime.utcnow()

    def update(self, data: dict):
        """Update attributes and save"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
