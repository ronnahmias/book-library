from sqlalchemy.orm import Session
from app.schemas.loan import LoanCreate

class LoanService:

    @staticmethod
    def loan_book(db: Session, loan: LoanCreate):
        pass

