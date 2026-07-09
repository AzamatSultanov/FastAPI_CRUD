from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./music.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DB_MusicCard(Base):
    __tablename__ = "music_cards"

    id = Column(Integer, primary_key=True, index=True) #primary key = 100% unique, index - searching optimization with the B-tree
    author = Column(String, index=True)
    date = Column(String)
    album = Column(String)
    song = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db #hands the connection over to the router and waits
    finally: #close when done
        db.close()