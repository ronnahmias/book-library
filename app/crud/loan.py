from sqlalchemy.orm import Session
from app.models.book_replicas import BookReplica
from app.schemas.loan import LoanCreate
from app.models.loan import Loan


def loan_book(db: Session, loan_dto: LoanCreate, db_replica: BookReplica)-> Loan:
    # we store book replica not the book id
    loan = Loan(**loan_dto.model_dump(exclude={'book_id'}), book_replica_id=db_replica.id)
    db.add(loan)
    db.flush()
    db.refresh(loan)
    return loan

def get_loan_by_id(db: Session, loan_id: int)-> Loan:
    return db.query(Loan).filter(Loan.id == loan_id).first()

def return_book(loan: Loan, end_loan_date)-> Loan:
    loan.end_loan_date = end_loan_date
    return loan