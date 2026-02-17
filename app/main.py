from fastapi import FastAPI
from app.api.v1.router import router
from app.core.database import Base, engine
from app.core.config import ENV



app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


app.include_router(router, prefix="/api/v1")
