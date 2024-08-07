from fastapi import APIRouter, Depends
from app.routes import book, client, loan, book_replica
from app.core.credentials import check_api_key

api_router = APIRouter(dependencies=[Depends(check_api_key)])
api_router.include_router(book.router, prefix="/books", tags=["books"])
api_router.include_router(book_replica.router, prefix="/books_replicas", tags=["books replicas"])
api_router.include_router(client.router, prefix="/clients", tags=["clients"])
api_router.include_router(loan.router, prefix="/loans", tags=["loans"])