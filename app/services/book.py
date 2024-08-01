from sqlalchemy.orm import Session
from app.crud import book as crud_book
from app.crud import book_replicas as crud_book_replicas
from app.schemas.book import BookCreate, BookUpdate

class BookService:
    
    @staticmethod
    def get_books(db: Session, skip: int = 0, limit: int = 10):
        return crud_book.get_books(db, skip=skip, limit=limit)
    
    @staticmethod
    def create_book(db: Session, book:BookCreate):
        bookEnt = crud_book.create_book(db, book)
        replicas = []
        for _ in range(book.num_of_copies):
            replica = crud_book_replicas.create_book_replica(db, bookEnt)
            replicas.append(replica)
        bookEnt.replicas = replicas
        print(bookEnt.replicas[0].id)
        return bookEnt
    
    @staticmethod
    def update_book(db: Session, book: BookUpdate, book_id: int):
        return crud_book.update_book(db, book, book_id)
    
    @staticmethod
    def delete_book(db: Session, book_id: int):
        return crud_book.delete_book(db, book_id)
