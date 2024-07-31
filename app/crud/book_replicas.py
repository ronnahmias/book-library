from sqlalchemy.orm import Session
from app.schemas.book import Book
from app.schemas.book_replica import BookReplica

def create_book_replica(book:Book, db: Session):
    db_book_rep = BookReplica(book_id=book.id)
    db.add(db_book_rep)
    db.commit()
    db.refresh(db_book_rep)
    return db_book_rep