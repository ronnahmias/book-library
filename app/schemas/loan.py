import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, Field

class LoanBase(BaseModel):
    client_id: int = Field(..., ge=1, description="Client ID must be an integer")
    # if there is loan date it will be today
    loan_date: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.now, description="Loan date must be a valid date")
    # in add loan the end_loan_date is optional
    end_loan_date: Optional[datetime.datetime] = Field(None, description="End loan date must be a valid date")

class LoanCreate(LoanBase):
    book_id: int = Field(..., ge=1, description="Book ID must be an integer")

class LoanReturnBase(BaseModel):
    end_loan_date: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.now, description="End loan date must be a valid date")

class LoanReturn(LoanReturnBase):
    pass

class Loan(LoanBase):
    id: int
    book_replica_id: uuid.UUID
    loan_date: datetime.datetime

    class Config:
        from_attributes = True