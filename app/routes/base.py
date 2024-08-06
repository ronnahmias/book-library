from fastapi import APIRouter
from app.routes import book, client, loan, book_replica

api_router = APIRouter()
api_router.include_router(book.router, prefix="/books", tags=["books"])
api_router.include_router(book_replica.router, prefix="/books_replicas", tags=["books replicas"])
api_router.include_router(client.router, prefix="/clients", tags=["clients"])
api_router.include_router(loan.router, prefix="/loans", tags=["loans"])