from pydantic import BaseModel, ConfigDict

# Schema  
class MusicCardCreate(BaseModel):
    author: str = "Unknown author"
    date: str = "Unknown date"
    album: str = "Unknown album"
    song: str = "Unknown song"

# Schema for returning a card (Output to user, includes an ID)
class MusicCard(MusicCardCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)  # Tells Pydantic to read SQLAlchemy database models