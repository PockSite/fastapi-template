from typing import Type, TypeVar, Generic
from sqlalchemy.orm import Session

T = TypeVar("T")

class Repository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def create(self, data: dict) -> T:
        obj = self.model(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def read_all(self) -> list[T]:
        return self.db.query(self.model).all()

    def read_by_id(self, id: int) -> T | None:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def update(self, id: int, data: dict) -> T | None:
        obj = self.read_by_id(id)
        if not obj:
            return None

        for key, value in data.items():
            setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, id: int) -> bool:
        obj = self.read_by_id(id)
        if not obj:
            return False

        self.db.delete(obj)
        self.db.commit()
        return True
