import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, Field

class LoanBase(BaseModel):
    client_id: int = Field(..., ge=1, description="Client ID must be an integer")
    book_replica_id: uuid.UUID = Field(..., description="Book replica ID must be a valid UUID")
    # if there is loan date it will be today
    loan_date: Optional[datetime.datetime] = Field(..., description="Loan date must be a valid date")
    # in add loan the end_loan_date is optional
    end_loan_date: Optional[datetime.datetime] = Field(None, description="End loan date must be a valid date")

class LoanCreate(LoanBase):
    pass

class LoanUpdate(LoanBase):
    end_loan_date: datetime.datetime = Field(None, description="End loan date must be a valid date")

class Loan(LoanBase):
    id: int
    loan_date: datetime.datetime

    class Config:
        from_attributes = True