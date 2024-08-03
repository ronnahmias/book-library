from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from app.crud.book_replicas import delete_book_replica
from app.models.book import Book
from app.schemas.book import BookCreate

def get_books(db: Session, skip: int = 0, limit: int = 10):
    # TODO - fix the handling of exceptions
    try:
        return db.query(Book).options(joinedload(Book.replicas)).offset(skip).limit(limit).all()
    except:
        raise HTTPException(status_code=500)

def get_book_by_id(db: Session, book_id: int):
    return db.query(Book).options(joinedload(Book.replicas)).filter(Book.id == book_id).first()

def create_book(db: Session, book: BookCreate):
    # create a new book - exclude num_of_copies from the model dump as it is not a column in the database
    db_book = Book(**book.model_dump(exclude={'num_of_copies'}))
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book: BookCreate, book_id: int):
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        # book not found by the given id
        return None
    for key, value in book.model_dump().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    # TODO: add a check if the book is borrowed by any user to prevent deletion
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        # book not found by the given id
        return None
    
    # Delete book replicas
    for replica in db_book.replicas:
        delete_book_replica(db, replica)

    # Delete the book
    db.delete(db_book)
    db.commit()
    return True