import uuid
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship

class BookReplica(Base):
    __tablename__ = "books_replicas"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    is_available = Column(Boolean, default=True)
    book_id = Column(Integer, ForeignKey("books.id"))

    book = relationship("Book", back_populates="replicas")
    loans = relationship("Loan", back_populates="replicas")