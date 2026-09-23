import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError
from app.api.v1.router import router
from app.core.database import Base, engine
from app.core.config import APP_NAME, PRODUCTION, CORS_ORIGINS
import app.models.user  # noqa: F401  (registra los modelos en Base.metadata)

logging.basicConfig(level=logging.INFO if PRODUCTION else logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=APP_NAME,
    lifespan=lifespan,
    docs_url=None if PRODUCTION else "/api/docs",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.exception_handler(OperationalError)
async def db_exception_handler(request: Request, exc: OperationalError):
    logging.getLogger(__name__).error("Database error: %s", exc)
    return JSONResponse(status_code=503, content={"detail": "Base de datos no disponible"})


app.include_router(router, prefix="/api/v1")
