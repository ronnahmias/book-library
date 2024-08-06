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

def update_book_replica_availability(db: Session, book_replica: BookReplica, is_available: bool):
    book_replica.is_available = is_available
    return book_replica

def get_book_replica_by_id(db: Session, book_replica_id: str):
    return db.query(BookReplica).filter(BookReplica.id == book_replica_id).first()
    