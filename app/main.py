from fastapi import FastAPI
from app.models.base import Base
from app.db.session import engine
from app.routes.base import api_router
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"Hello": "World1"}