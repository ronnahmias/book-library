from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.book import Book
from app.models.loan import Loan
from app.schemas.loan import LoanCreate, LoanReturn
from app.crud import book as crud_book
from app.crud import client as crud_client
from app.crud import loan as crud_loan
from app.crud import book_replicas as crud_book_replicas
import pytz

class LoanService:

    @staticmethod
    def loan_book(db: Session, loan: LoanCreate)-> Loan:
        try:
            # ensure that all operations are done in a single transaction for validation of the loan
            with db.begin():
                # find book by id
                db_book = crud_book.get_book_by_id(db, loan.book_id)
                if not db_book:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {loan.book_id} not found")
                # find book replica
                db_replica = crud_book.get_book_replica_availability(db, db_book)
                if not db_replica:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No available book with id {loan.book_id} for loan")
                # find client
                if not crud_client.get_client(db, loan.client_id):
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Client with id {loan.client_id} not found")
                # create loan and update book replica is_available
                crud_book_replicas.update_book_replica_availability(db_replica, False)
                db_loan = crud_loan.loan_book(db, loan, db_replica)
                db.flush()
                db.refresh(db_loan)
                return db_loan
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while processing the request")
    
    @staticmethod    
    def return_book(db: Session, loan_dto:LoanReturn, loan_id: int)-> Loan:
        try:
            with db.begin():
                # find loan by id
                db_loan = crud_loan.get_loan_by_id(db, loan_id)
                if not db_loan:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Loan with id {loan_id} not found")
                if db_loan.end_loan_date is not None:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Loan with id {loan_id} has already been returned")
                loan_date = db_loan.loan_date
                loan_date = pytz.timezone('UTC').localize(loan_date) # type: ignore
                    
                if loan_dto.end_loan_date is not None and loan_dto.end_loan_date < loan_date:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"End loan date must be greater than loan date")
                
                # find the book replica
                db_book_replica = crud_book_replicas.get_book_replica_by_id(db, str(db_loan.book_replica_id))
                
                if not db_book_replica:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book replica with id {db_loan.book_replica_id} not found")
                
                # return book and update book replica is_available for next loan
                db_loan = crud_loan.return_book(db_loan, loan_dto.end_loan_date)
                
                # update availability of book replica - set it to True
                crud_book_replicas.update_book_replica_availability(db_book_replica, True)
                
                db.flush()
                db.refresh(db_loan)
                return db_loan
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while processing the request")
    
    @staticmethod    
    def get_overdue_loans(db: Session, days: int)-> list[Book]:
        try:
            return crud_book.get_overdue_book_loans(db, days)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while processing the request")
            

