from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.book import BookCreate

def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Book).offset(skip).limit(limit).all()

def create_book(book: BookCreate, db: Session):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book