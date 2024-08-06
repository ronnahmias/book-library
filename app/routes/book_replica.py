from fastapi import APIRouter, Depends
from app.db.db import get_db
from app.services.book import BookService
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/{replica_id}")
async def check_who_has_specific_book(replica_id: str, db: Session = Depends(get_db)):
    return BookService.get_book_replica_holder(db, replica_id)