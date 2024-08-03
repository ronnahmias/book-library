from fastapi import APIRouter
from app.routes import book, client

api_router = APIRouter()
api_router.include_router(book.router, prefix="/books", tags=["books"])
api_router.include_router(client.router, prefix="/clients", tags=["clients"])