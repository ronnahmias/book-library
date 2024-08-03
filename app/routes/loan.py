from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.schemas.loan import LoanCreate
from app.services.loan import LoanService
router = APIRouter()

@router.post("/")
def loan_book(loan: LoanCreate, db: Session = Depends(get_db)):
    return LoanService.loan_book(db, loan)