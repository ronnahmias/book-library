import datetime
from pydantic import BaseModel, Field

class BookReplicaBase(BaseModel):
    book_id: int = Field(..., example=1)
    is_available: bool = Field(True, example=True)

class BookReplica(BookReplicaBase):
    id: int

    class Config:
        from_attributes = True