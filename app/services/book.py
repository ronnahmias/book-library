from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.crud import book as crud_book
from app.crud import book_replicas as crud_book_replicas
from app.crud import client as crud_clients
from app.schemas.book import BookCreate, BookUpdate

class BookService:
    
    def get_books(db: Session, skip: int = 0, limit: int = 10):
        try:
            return crud_book.get_books(db, skip=skip, limit=limit)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while fetching books")
    
    def create_book(db: Session, book:BookCreate):
        bookEnt = crud_book.create_book(db, book)
        replicas = []
        for _ in range(book.num_of_copies):
            replica = crud_book_replicas.create_book_replica(db, bookEnt)
            replicas.append(replica)
        bookEnt.replicas = replicas
        return bookEnt
    
    def update_book(db: Session, book: BookUpdate, book_id: int):
        return crud_book.update_book(db, book, book_id)
    
    def delete_book(db: Session, book_id: int):
        # get the book by id
        db_book = crud_book.get_book_by_id(db, book_id)
        if not db_book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {book_id} not found")
        # check if the book is borrowed
        if not crud_book.check_all_replicas_available(db, db_book):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Book with id {book_id} is borrowed")
        try:
            return crud_book.delete_book(db, db_book)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while deleting the book")
    
    def get_book_availability(db: Session, book_id: int):
        db_book = crud_book.get_book_by_id(db, book_id)
        if not db_book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {book_id} not found")
        return crud_book.get_book_replica_availability(db, db_book)
    
    def get_book_holders(db: Session, book_id: int):
        try:
            db_book = crud_book.get_book_by_id(db, book_id)
            if not db_book:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {book_id} not found")
            # get the book holders
            holders = crud_clients.get_book_clients_holders(db, book_id)
            return {
                "book": db_book,
                "book_holders": holders
            }
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while fetching book holders")
        
    def get_book_replica_holder(db: Session, replica_id: str):

        book_replica = crud_book_replicas.get_book_replica_by_id(db, replica_id)
        if not book_replica:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book replica with id {replica_id} not found")
        # the book replica does not have a holder right now
        if book_replica.is_available:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No holder for book replica with id {replica_id}")
        return crud_clients.get_book_replica_holder(db, replica_id)

