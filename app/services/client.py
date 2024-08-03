from sqlalchemy.orm import Session
from app.crud import client as crud_client
from app.schemas.client import ClientCreate, ClientUpdate

class ClientService:

    @staticmethod
    def get_clients(db: Session, skip: int = 0, limit: int = 10):
        return crud_client.get_clients(db, skip=skip, limit=limit)
    
    @staticmethod
    def create_client(db: Session, client: ClientCreate):
        # Check if client already exists by email
        if not crud_client.get_client_by_email(db, client.email):
            return crud_client.create_client(db, client)
        return None
    
    @staticmethod
    def get_client(db: Session, client_id: int):
        return crud_client.get_client(db, client_id)
    
    @staticmethod
    def update_client(db: Session, client_id: int, client: ClientUpdate):
        return crud_client.update_client(db, client_id, client)
    
    @staticmethod
    def delete_client(db: Session, client_id: int):
        return crud_client.delete_client(db, client_id)
    