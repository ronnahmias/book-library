import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from app.db.base import Base
from sqlalchemy.orm import relationship


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    book_replica_id = Column(String, ForeignKey("books_replicas.id"), nullable=False)
    loan_date = Column(DateTime, default=datetime.datetime.now(datetime.UTC), nullable=False)
    end_loan_date = Column(DateTime, nullable=True)
    
    __table_args__ = (
        UniqueConstraint('client_id', 'book_replica_id', 'loan_date'),
    )

    clients = relationship("Client", back_populates="loans")
    replicas = relationship("BookReplica", back_populates="loans")