import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.exc import OperationalError
from sqlalchemy.pool import StaticPool, NullPool
from app.core.config import DB_URL

logger = logging.getLogger(__name__)

if DB_URL.startswith("sqlite"):
    # SQLite (desarrollo / tests): comparte una única conexión en memoria.
    engine = create_engine(
        DB_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    # Postgres / Supabase: NullPool + pre_ping evita conexiones muertas detrás de pgbouncer.
    engine = create_engine(DB_URL, poolclass=NullPool, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    except OperationalError as e:
        logger.error("Database connection error: %s", e)
        raise
    finally:
        db.close()
