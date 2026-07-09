from sqlalchemy.orm import Session #for type-hinting
from app.repositories.repository import MusicRepository
import app.schemas.schemas as schemas
from fastapi import HTTPException #to generated a formatted HTTP error response

class MusicService:
    def __init__(self, db: Session):
        #DB session into the service -> passes it to the repository.
        self.repo = MusicRepository(db) #repo writes it (new ID) and returns here

    def create_new_card(self, card: schemas.MusicCardCreate):
        existing_card = self.repo.get_card_by_author_and_song(card.author, card.song) #None if the card doesn't exist yet

        if existing_card:
            raise HTTPException(
                status_code=409, #conflict (dublicate)
                detail=f"'{card.song}' by '{card.author}' already exists"
            )
        return self.repo.create_card(card)

    def get_cards(self):
        return self.repo.get_all_cards()
    
    def get_card(self, card_id: int):
        card = self.repo.get_card_by_id(card_id)

        if not card:
            raise HTTPException(
                status_code=404, #not found
                detail="Music card not found"
            )
        return card

    
    def update_card(self, card_id:int, updated_card: schemas.MusicCardCreate):
        db_card = self.get_card(card_id) #service method
        return self.repo.update(db_card, updated_card)
    
    def delete_card(self, card_id: int):
        db_card = self.get_card(card_id)
        self.repo.delete(db_card)