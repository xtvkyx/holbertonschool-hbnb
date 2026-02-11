from typing import Any, List, Optional
from hbnb.extensions import db
from hbnb.repositories.base import BaseRepository


class SQLAlchemyRepository(BaseRepository):
    """SQLAlchemy repository for CRUD operations.
    NOTE: No DB initialization is done here.
    """

    def add(self, obj: Any) -> Any:
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, model: Any, obj_id: str) -> Optional[Any]:
        return model.query.get(obj_id)

    def get_all(self, model: Any) -> List[Any]:
        return model.query.all()

    def update(self) -> None:
        db.session.commit()

    def delete(self, obj: Any) -> None:
        db.session.delete(obj)
        db.session.commit()
