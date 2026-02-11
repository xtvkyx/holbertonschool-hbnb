from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def add(self, obj): ...
    @abstractmethod
    def get(self, obj_id): ...
    @abstractmethod
    def get_all(self): ...
    @abstractmethod
    def update(self, obj_id, data): ...
    @abstractmethod
    def delete(self, obj_id): ...
    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value): ...


class InMemoryRepository(Repository):
    def __init__(self):
        self._data = {}

    def add(self, obj):
        self._data[obj.id] = obj
        return obj

    def get(self, obj_id):
        return self._data.get(obj_id)

    def get_all(self):
        return list(self._data.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if not obj:
            return None
        for k, v in data.items():
            setattr(obj, k, v)
        return obj

    def delete(self, obj_id):
        return self._data.pop(obj_id, None)

    def get_by_attribute(self, attr_name, attr_value):
        for obj in self._data.values():
            if getattr(obj, attr_name, None) == attr_value:
                return obj
        return None
