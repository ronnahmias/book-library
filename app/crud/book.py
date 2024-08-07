from sqlalchemy.orm import Session, joinedload
from app.crud.book_replicas import delete_book_replica
from app.models.book import Book
from app.models.book_replicas import BookReplica
from app.models.loan import Loan
from app.schemas.book import BookCreate, BookUpdate
from datetime import datetime, timedelta

def get_books(db: Session, skip: int = 0, limit: int = 10)-> list[Book]:
    return db.query(Book).options(joinedload(Book.replicas)).offset(skip).limit(limit).all()

def get_book_by_id(db: Session, book_id: int)-> Book:
    return db.query(Book).options(joinedload(Book.replicas)).filter(Book.id == book_id).first()

def create_book(db: Session, book: BookCreate)-> Book:
    # create a new book - exclude num_of_copies from the model dump as it is not a column in the database
    db_book = Book(**book.model_dump(exclude={'num_of_copies'}))
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book: BookUpdate, book_id: int)-> Book|None:
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        # book not found by the given id
        return None
    for key, value in book.model_dump().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, db_book: Book)-> bool:
    # Delete book replicas first
    for replica in db_book.replicas:
        delete_book_replica(db, replica)

    # Delete the book row in the database
    db.delete(db_book)
    db.commit()
    return True

def get_book_replica_availability(db: Session, db_book: Book)-> BookReplica|None:
    # we need to check in the replicas if there is any available book
    available_replica = next((replica for replica in db_book.replicas if replica.is_available), None)
    return available_replica

def check_all_replicas_available(db: Session, db_book: Book):
    # check if all the book replicas are available
    return all(replica.is_available for replica in db_book.replicas)

def get_overdue_book_loans(db: Session, days: int):
    # gets all the books that are overdue by the given number of days
    delta_days = datetime.now() - timedelta(days=days)
    active_loans = db.query(Book).join(BookReplica).join(Loan).filter(
        Loan.loan_date < delta_days,
        Loan.end_loan_date == None
    ).all()
    
    completed_loans = db.query(Book).join(BookReplica).join(Loan).filter(
        (Loan.end_loan_date - Loan.loan_date) > timedelta(days=days)
    ).all()
    
    return list(set(active_loans + completed_loans))
