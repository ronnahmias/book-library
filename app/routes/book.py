from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.book import Book, BookCreate
from app.db.db import get_db
from app.services.book import BookService

router = APIRouter()

@router.get("/", response_model=list[Book])
def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return BookService.get_books(db, skip=skip, limit=limit)

@router.post("/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return BookService.create_book(book, db)