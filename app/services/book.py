from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.crud import book as crud_book
from app.crud import book_replicas as crud_book_replicas
from app.crud import client as crud_clients
from app.models.book import Book
from app.models.book_replicas import BookReplica
from app.models.client import Client
from app.schemas.book import BookCreate, BookUpdate

class BookService:
    
    @staticmethod
    def get_books(db: Session, skip: int = 0, limit: int = 10)-> list[Book]:
        try:
            return crud_book.get_books(db, skip=skip, limit=limit)
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while fetching books")
    
    @staticmethod
    def create_book(db: Session, book:BookCreate)-> Book:
        bookEnt = crud_book.create_book(db, book)
        bookEnt.replicas = [crud_book_replicas.create_book_replica(db, bookEnt) for _ in range(book.num_of_copies)]
        return bookEnt
    
    @staticmethod
    def update_book(db: Session, book: BookUpdate, book_id: int)-> Book:
        return crud_book.update_book(db, book, book_id)
    
    @staticmethod
    def delete_book(db: Session, book_id: int)-> bool:
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
        
    @staticmethod
    def get_book_availability(db: Session, book_id: int)-> BookReplica:
        db_book = crud_book.get_book_by_id(db, book_id)
        if not db_book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {book_id} not found")
        return crud_book.get_book_replica_availability(db, db_book)
    
    @staticmethod
    def get_book_holders(db: Session, book_id: int)-> dict:
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

    @staticmethod
    def get_book_replica_holder(db: Session, replica_id: str)-> Client:

        book_replica = crud_book_replicas.get_book_replica_by_id(db, replica_id)
        if not book_replica:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book replica with id {replica_id} not found")
        # the book replica does not have a holder right now
        if bool(book_replica.is_available):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No holder for book replica with id {replica_id}")
        return crud_clients.get_book_replica_holder(db, replica_id)

