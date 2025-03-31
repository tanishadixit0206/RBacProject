from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker,Session,declarative_base
from app.models.user import Base
import os
load_dotenv()

engine=create_engine(os.getenv('DATABASE_URL'))
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base.metadata.create_all(bind=engine)
# engine.connect()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()