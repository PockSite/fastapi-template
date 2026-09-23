import logging
from typing import Type, TypeVar, Generic
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

T = TypeVar("T")  # modelo
K = TypeVar("K")  # tipo de la clave primaria (int, uuid.UUID, ...)


class Repository(Generic[T, K]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def create(self, data: dict) -> T:
        obj = self.model(**data)
        self.db.add(obj)
        try:
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            logger.warning("Integrity error on create: %s", e.orig)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El registro ya existe o viola una restricción de integridad",
            )
        self.db.refresh(obj)
        return obj

    def read_all(self) -> list[T]:
        return self.db.query(self.model).all()

    def read_by_id(self, id: K) -> T | None:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def update(self, id: K, data: dict) -> T | None:
        obj = self.read_by_id(id)
        if not obj:
            return None

        for key, value in data.items():
            setattr(obj, key, value)

        try:
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            logger.warning("Integrity error on update: %s", e.orig)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="La actualización viola una restricción de integridad",
            )
        self.db.refresh(obj)
        return obj

    def delete(self, id: K) -> bool:
        obj = self.read_by_id(id)
        if not obj:
            return False

        try:
            self.db.delete(obj)
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            logger.warning("Integrity error on delete: %s", e.orig)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar: hay registros que dependen de este",
            )
        return True
