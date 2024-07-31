from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base
from sqlalchemy.orm import relationship

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    year = Column(Integer)
    rating = Column(Float)

    replicas = relationship("BookReplica", back_populates="book")