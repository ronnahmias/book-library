from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.book import BookCreate, BookResponse, BookUpdate
from app.db.db import get_db
from app.services.book import BookService

router = APIRouter()

@router.get("/", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return BookService.get_books(db, skip=skip, limit=limit)

@router.post("/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return BookService.create_book(db, book)

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book: BookUpdate, db: Session = Depends(get_db), book_id: int = None):
    updated_book = BookService.update_book(db, book, book_id)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found") 
    return updated_book

@router.delete("/{book_id}")
def delete_book(db: Session = Depends(get_db), book_id: int = None):
    if not BookService.delete_book(db, book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}