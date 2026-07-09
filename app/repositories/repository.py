from sqlalchemy.orm import Session
from database import DB_MusicCard
import app.schemas.schemas as schemas

class MusicRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_card(self, card: schemas.MusicCardCreate):
        db_card = DB_MusicCard(**card.model_dump()) #Pydantic schema -> Python dictionary -> unpacks into the SQLAlchemy model
        self.db.add(db_card)
        self.db.commit() #INSERT command (also generates an ID)
        self.db.refresh(db_card) #Fetching it back before returning
        return db_card

    def get_all_cards(self):
        return self.db.query(DB_MusicCard).all() #SELECT * FROM music_cards, returns all records as a list
    
    def get_card_by_id(self, card_id: int):
        return self.db.query(DB_MusicCard).filter(DB_MusicCard.id == card_id).first() #without first() returns just a query, not data
    
    def update(self, db_card: DB_MusicCard, updated_data: schemas.MusicCardCreate):
        for key, value in updated_data.model_dump().items(): #-> Py dict -> divides into several items to loop through
            setattr(db_card, key, value)
        self.db.commit()
        self.db.refresh(db_card)
        return db_card

    def delete(self, db_card: DB_MusicCard): #deletes and returns the card
        self.db.delete(db_card)
        self.db.commit()
        return db_card

    def get_card_by_author_and_song(self, author: str, song: str):
        return self.db.query(DB_MusicCard).filter(
            DB_MusicCard.author == author,
            DB_MusicCard.song == song
        ).first()