"""In-memory repository for storing and validating objects."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Type, TypeVar

T = TypeVar("T")


class InMemoryRepository:
    """
    Generic in-memory repository.

    Storage structure:
      self._data["User"][id] = user_object
    """

    def __init__(self) -> None:
        self._data: Dict[str, Dict[str, Any]] = {}
        # Indexes for uniqueness checks (example: email)
        self._unique_indexes: Dict[str, Dict[str, Dict[str, str]]] = {}
        # Example:
        # self._unique_indexes["User"]["email"][email_value] = user_id

    def _bucket(self, cls_name: str) -> Dict[str, Any]:
        if cls_name not in self._data:
            self._data[cls_name] = {}
        return self._data[cls_name]

    def register_unique_field(self, cls_name: str, field_name: str) -> None:
        self._unique_indexes.setdefault(cls_name, {})
        self._unique_indexes[cls_name].setdefault(field_name, {})

    def _check_unique(self, cls_name: str, obj: Any, obj_id: Optional[str] = None) -> None:
        """
        Enforce uniqueness for registered fields.
        obj_id is used for updates (ignore the same object).
        """
        if cls_name not in self._unique_indexes:
            return

        for field_name, index_map in self._unique_indexes[cls_name].items():
            value = getattr(obj, field_name, None)
            if value is None:
                continue
            existing_id = index_map.get(str(value))
            if existing_id and existing_id != obj_id:
                raise ValueError(f"{cls_name}.{field_name} must be unique")

    def add(self, obj: Any) -> Any:
        cls_name = obj.__class__.__name__
        bucket = self._bucket(cls_name)

        self._check_unique(cls_name, obj)
        bucket[obj.id] = obj

        # update unique indexes
        if cls_name in self._unique_indexes:
            for field_name, index_map in self._unique_indexes[cls_name].items():
                value = getattr(obj, field_name, None)
                if value is not None:
                    index_map[str(value)] = obj.id

        return obj

    def get(self, cls: Type[T], obj_id: str) -> Optional[T]:
        cls_name = cls.__name__
        bucket = self._bucket(cls_name)
        return bucket.get(obj_id)

    def list(self, cls: Type[T]) -> List[T]:
        cls_name = cls.__name__
        bucket = self._bucket(cls_name)
        return list(bucket.values())

    def delete(self, cls: Type[T], obj_id: str) -> bool:
        cls_name = cls.__name__
        bucket = self._bucket(cls_name)
        obj = bucket.get(obj_id)
        if not obj:
            return False

        # clean unique indexes
        if cls_name in self._unique_indexes:
            for field_name, index_map in self._unique_indexes[cls_name].items():
                value = getattr(obj, field_name, None)
                if value is not None:
                    index_map.pop(str(value), None)

        del bucket[obj_id]
        return True

    def update(self, obj: Any) -> Any:
        cls_name = obj.__class__.__name__
        bucket = self._bucket(cls_name)
        if obj.id not in bucket:
            raise KeyError(f"{cls_name} not found")

        # uniqueness check considering same id
        self._check_unique(cls_name, obj, obj_id=obj.id)

        bucket[obj.id] = obj
        if hasattr(obj, "touch"):
            obj.touch()

        # rebuild indexes for that object (simple way)
        if cls_name in self._unique_indexes:
            for field_name, index_map in self._unique_indexes[cls_name].items():
                value = getattr(obj, field_name, None)
                if value is not None:
                    index_map[str(value)] = obj.id

        return obj
