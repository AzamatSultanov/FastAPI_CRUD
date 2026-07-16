from sqlalchemy.orm import Session #for type-hinting
from app.repositories.repository import MusicRepository
import app.schemas.schemas as schemas
from fastapi import HTTPException #to generated a formatted HTTP error response
from redis_client import get_cache, delete_cache, set_cache
from redis import Redis

ALL_CARDS_KEYS = "music_cards:all"

class MusicService:
    def __init__(self, db: Session, redis_client: Redis):
        #DB session into the service -> passes it to the repository.
        self.repo = MusicRepository(db) #repo writes it (new ID) and returns here
        self.redis = redis_client

    def create_new_card(self, card: schemas.MusicCardCreate):
        existing_card = self.repo.get_card_by_author_and_song(card.author, card.song) #None if the card doesn't exist yet

        if existing_card:
            raise HTTPException(
                status_code=409, #conflict (dublicate)
                detail=f"'{card.song}' by '{card.author}' already exists"
            )
        new_card = self.repo.create_card(card)
        delete_cache(self.redis, ALL_CARDS_KEYS) #a full list is already outdated
        return new_card

    def get_cards(self):
        cache = get_cache(self.redis, ALL_CARDS_KEYS)
        if cache is not None:
            return [schemas.MusicCard.model_validate(item) for item in cache]
        
        #if cache miss:
        cards = self.repo.get_all_cards()
        response = [schemas.MusicCard.model_validate(card) for card in cards] #to pydantic schema
        set_cache(self.redis, ALL_CARDS_KEYS, [item.model_dump() for item in response], ttl = 50) #model_dump: Pydantic object -> Py dict
        return response

    def get_card(self, card_id: int):
        key = f"music_cards:{card_id}"
        cache = get_cache(self.redis, key)

        if cache is not None:
            return schemas.MusicCard.model_validate(cache)
        
        #if cache miss:
        card = self.repo.get_card_by_id(card_id)
        if not card:
            raise HTTPException(
                status_code=404, #not found
                detail="Music card not found"
            )
        response = schemas.MusicCard.model_validate(card)
        set_cache(self.redis, key, response.model_dump())
        return response
    
    def update_card(self, card_id:int, updated_card: schemas.MusicCardCreate):
        db_card = self.repo.get_card_by_id(card_id) #returns an ORM object
        if not db_card:
            raise HTTPException(
                status_code=404,
                detail="Music card not found"
            )
        updated = self.repo.update(db_card, updated_card) 

        response = schemas.MusicCard.model_validate(updated)
        set_cache(self.redis, f"music_cards:{card_id}", response.model_dump())
        delete_cache(self.redis, ALL_CARDS_KEYS)
        return response
    
    def delete_card(self, card_id: int):
        db_card = self.repo.get_card_by_id(card_id)
        if not db_card:
            raise HTTPException(
                status_code=404,
                detail="Music card not found"
            )
        self.repo.delete(db_card) #first db and then cache delete
        delete_cache(self.redis, f"music_cards:{card_id}")
