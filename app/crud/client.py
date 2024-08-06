from sqlalchemy.orm import Session
from app.models.book_replicas import BookReplica
from app.models.client import Client
from app.models.loan import Loan
from app.schemas.client import ClientCreate, ClientUpdate

def get_clients(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Client).offset(skip).limit(limit).all()
    
def get_client(db: Session, client_id: int):
    return db.query(Client).filter(Client.id == client_id).first()

def get_client_by_email(db: Session, email: str):
    return db.query(Client).filter(Client.email == email).first()

def create_client(db: Session, client: ClientCreate):
    db_client = Client(**client.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def update_client(db: Session, db_client: Client, client: ClientUpdate):
    # Update only the fields that were set
    for key, value in client.model_dump(exclude_unset=True).items():
        setattr(db_client, key, value)
    
        db.commit()
        db.refresh(db_client)
        return db_client
       

def delete_client(db: Session, db_client: Client):
    db.delete(db_client)
    db.commit()

def get_book_clients_holders(db: Session, book_id: int):
    return db.query(Client).join(Loan, Client.id == Loan.client_id).join(BookReplica, Loan.book_replica_id == BookReplica.id).filter(BookReplica.book_id == book_id,
                                                                                                                                BookReplica.is_available == False).all()
    
def get_book_replica_holder(db: Session, replica_id: int):
    return db.query(Client).join(Loan, Client.id == Loan.client_id).join(BookReplica, Loan.book_replica_id == BookReplica.id).filter(BookReplica.id == replica_id).first()