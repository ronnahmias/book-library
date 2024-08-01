from sqlalchemy.orm import Session
from app.models.book_replicas import BookReplica
from app.schemas.book import Book

def create_book_replica(db: Session, book:Book):
    db_book_rep = BookReplica(book_id=book.id, is_available=True)
    db.add(db_book_rep)
    db.commit()
    db.refresh(db_book_rep)
    return db_book_rep

def delete_book_replica(db: Session, book_replica: BookReplica):
    db.delete(book_replica)
    db.commit()
    return True
    