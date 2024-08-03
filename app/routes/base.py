from fastapi import APIRouter
from app.routes import book, client, loan

api_router = APIRouter()
api_router.include_router(book.router, prefix="/books", tags=["books"])
api_router.include_router(client.router, prefix="/clients", tags=["clients"])
api_router.include_router(loan.router, prefix="/loans", tags=["loans"])