from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.crud import client as crud_client
from app.schemas.client import ClientCreate, ClientUpdate

class ClientService:

    @staticmethod
    def get_clients(db: Session, skip: int = 0, limit: int = 10):
        try:
            return crud_client.get_clients(db, skip=skip, limit=limit)
        except:
            raise HTTPException(status_code=500, detail="There was an error while trying to get clients")
    
    @staticmethod
    def create_client(db: Session, client: ClientCreate):
        try:
            # Check if client already exists by email
            if not crud_client.get_client_by_email(db, client.email):
                return crud_client.create_client(db, client)
            return None
        except:
            db.rollback()
            raise HTTPException(status_code=500, detail="There was an error while trying to create client")
    
    @staticmethod
    def get_client(db: Session, client_id: int):
        try:
            return crud_client.get_client(db, client_id)
        except:
            raise HTTPException(status_code=500, detail="There was an error while trying to get client")
    
    @staticmethod
    def update_client(db: Session, client_id: int, client: ClientUpdate):
        db_client = crud_client.get_client(db, client_id)
        if db_client:
            if client.email:
                existing_client = crud_client.get_client_by_email(db, client.email)
                if existing_client and existing_client.id != client_id:
                    raise HTTPException(status_code=400, detail="Email already exists")
            try:
                return crud_client.update_client(db, db_client, client)
            except: 
                db.rollback()
                raise HTTPException(status_code=500, detail="There was an error while trying to update client")
    
    @staticmethod
    def delete_client(db: Session, client_id: int):
        db_client = crud_client.get_client(db, client_id)
        if not db_client:
            raise HTTPException(status_code=404, detail="Client not found")
        try:
            return crud_client.delete_client(db, client_id)
        except:
            db.rollback()
            raise HTTPException(status_code=500, detail="There was an error while trying to delete client")
    