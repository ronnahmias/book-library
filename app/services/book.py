from sqlalchemy.orm import Session
from app.crud import book as crud_book
from app.crud import book_replicas as crud_book_replicas
from app.schemas.book import BookCreate

class BookService:
    
    @staticmethod
    def get_books(db: Session, skip: int = 0, limit: int = 10):
        return crud_book.get_books(db, skip=skip, limit=limit)
    
    @staticmethod
    def create_book(book:BookCreate ,db: Session):
        book = crud_book.create_book(book, db)
        replicas = []
        for _ in range(book.replicas):
            replica = crud_book_replicas.create_book_replica(book, db)
            replicas.append(replica)
        book.replicas = replicas
        return book
