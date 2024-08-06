from fastapi import FastAPI
from app.models.base import Base
from app.db.session import engine
from app.routes.base import api_router
from fastapi.middleware.cors import CORSMiddleware
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Library API", version="1.0")

app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"Book Library API": "Welcome to the Book Library API!"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# TODO: Add Api key middleware
