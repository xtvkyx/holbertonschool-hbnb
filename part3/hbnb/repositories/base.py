from abc import ABC, abstractmethod
from typing import Any, List, Optional


class BaseRepository(ABC):
    """Repository interface (backend-agnostic)."""

    @abstractmethod
    def add(self, obj: Any) -> Any:
        pass

    @abstractmethod
    def get(self, model: Any, obj_id: str) -> Optional[Any]:
        pass

    @abstractmethod
    def get_all(self, model: Any) -> List[Any]:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def delete(self, obj: Any) -> None:
        pass
