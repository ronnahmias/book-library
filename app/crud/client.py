from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate

def get_clients(db: Session, skip: int = 0, limit: int = 10):
    try:
        return db.query(Client).offset(skip).limit(limit).all()
    except:
        raise HTTPException(status_code=500)
    

# TODO: change dynamic filter to use a search query
def get_client(db: Session, client_id: int):
    try:
        return db.query(Client).filter(Client.id == client_id).first()
    except:
        raise HTTPException(status_code=500)

# TODO: change dynamic filter to use a search query
def get_client_by_email(db: Session, email: str):
    try:
        return db.query(Client).filter(Client.email == email).first()
    except:
        raise HTTPException(status_code=500)

def create_client(db: Session, client: ClientCreate):
    db_client = Client(**client.model_dump())
    try:
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
    except:
        db.rollback()
        raise HTTPException(status_code=500)
    return db_client

def update_client(db: Session, client_id: int, client: ClientUpdate):
    db_client = get_client(db, client_id)
    if db_client:
        if client.email:
            existing_client = get_client_by_email(db, client.email)
            if existing_client and existing_client.id != client_id:
                raise HTTPException(status_code=400, detail="Email already exists")

        # Update only the fields that were set
        for key, value in client.model_dump(exclude_unset=True).items():
            setattr(db_client, key, value)
        try:
            db.commit()
            db.refresh(db_client)
            return db_client
        except:
            db.rollback()
            raise HTTPException(status_code=500)
    return None

def delete_client(db: Session, client_id: int):
    db_client = get_client(db, client_id)
    if db_client:
        try:
            db.delete(db_client)
            db.commit()
            return 
        except:
            db.rollback()
            raise HTTPException(status_code=500)
    raise HTTPException(status_code=404, detail="Client not found")