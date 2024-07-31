from fastapi import APIRouter
from app.routes import book

api_router = APIRouter()
api_router.include_router(book.router, prefix="/books", tags=["books"])