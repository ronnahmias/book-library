from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.schemas.loan import LoanCreate, LoanReturn
from app.services.loan import LoanService

router = APIRouter()

@router.post("/")
def loan_book(loan: LoanCreate, db: Session = Depends(get_db)):
    return LoanService.loan_book(db, loan)

@router.put("/{loan_id}/return")
def return_book(loan: LoanReturn, loan_id: int, db: Session = Depends(get_db)):
    db_loan = LoanService.return_book(db, loan, loan_id)
    if db_loan.end_loan_date:
        return {"message": "Book returned successfully"}
    raise HTTPException(status_code=400, detail="An error occurred while returning the book")

@router.get("/overdue")
def get_overdue_loans(db: Session = Depends(get_db), days: int = Query(45)):
    return LoanService.get_overdue_loans(db, days)
