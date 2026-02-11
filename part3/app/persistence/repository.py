from app.extensions import db

class SQLAlchemyRepository:
    def __init__(self, model):
        self.model = model

    def create(self, **data):
        obj = self.model(**data)
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def list(self):
        return self.model.query.all()

    def update(self, obj, **data):
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.commit()
        return obj

    def delete(self, obj):
        db.session.delete(obj)
        db.session.commit()
