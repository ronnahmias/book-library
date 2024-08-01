import datetime
from pydantic import BaseModel, Field

from app.schemas.book_replica import BookReplica

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Title must be between 1 and 100 characters")
    year: int =Field(..., ge=1900, le=datetime.datetime.now().year, description=f"Year must be between 1900 and {datetime.datetime.now().year}")
    rating: float = Field(..., ge=0, le=10, description="Rating must be between 0 and 10")

class BookCreate(BookBase):
    num_of_copies: int = Field(..., ge=1, description="Number of copies must be greater than 0")

class BookUpdate(BookBase):
    pass

# return a list of BookReplica objects inside the book object
class BookResponse(BookBase):
    id: int
    replicas: list[BookReplica]

class Book(BookBase):
    id: int

    class Config:
        from_attributes = True