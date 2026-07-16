from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session #type: ignore
from database import get_db
import app.schemas.schemas as schemas
from app.services.service import MusicService
from redis import Redis
from redis_client import get_redis

router = APIRouter()

# Create endpoint
@router.post("/cards/", response_model=schemas.MusicCard)
def create_card(card: schemas.MusicCardCreate, db: Session = Depends(get_db), redis_client: Redis = Depends(get_redis)):
    service = MusicService(db, redis_client)
    return service.create_new_card(card)

# Read all
@router.get("/cards/", response_model=list[schemas.MusicCard])
def read_cards(db: Session = Depends(get_db), redis_client: Redis = Depends(get_redis)):
    service = MusicService(db, redis_client)
    return service.get_cards()

#Read one
@router.get("/cards/{card_id}", response_model=schemas.MusicCard)
def read_card(card_id: int, db: Session = Depends(get_db), redis_client: Redis = Depends(get_redis)):
    service = MusicService(db, redis_client)
    return service.get_card(card_id)

# Update
@router.put("/cards/{card_id}", response_model=schemas.MusicCard)
def update_card(card_id: int, card: schemas.MusicCard, db: Session = Depends(get_db), redis_client: Redis = Depends(get_redis)):
    service = MusicService(db, redis_client)
    return service.update_card(card_id, card)

# Delete 
@router.delete("/cards/{card_id}")
def delete_card(card_id: int, db: Session = Depends(get_db), redis_client: Redis = Depends(get_redis)):
    service = MusicService(db, redis_client)
    service.delete_card(card_id)
    return {"message": f"Card {card_id} successfully deleted"}   
