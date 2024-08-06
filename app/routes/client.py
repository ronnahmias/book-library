from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.schemas.client import Client, ClientCreate, ClientUpdate
from app.services.client import ClientService

router = APIRouter()

@router.get("/", response_model=list[Client])
def get_clients(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return ClientService.get_clients(db, skip=skip, limit=limit)

@router.post("/")
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    new_client = ClientService.create_client(db, client)
    if not new_client:
        raise HTTPException(status_code=409, detail="Client already exists")
    return new_client

@router.get("/{client_id}", response_model=Client)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = ClientService.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/{client_id}")
def update_client(client_id: int, client: ClientUpdate, db: Session = Depends(get_db)):
    updated_client = ClientService.update_client(db, client_id, client)
    if not updated_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated_client

@router.delete("/{client_id}", status_code=204)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    return ClientService.delete_client(db, client_id)
    