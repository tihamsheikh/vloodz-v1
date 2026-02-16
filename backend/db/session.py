from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker 

from core.config import settings 

# Create the database engine
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)#, echo=True)

# initialize the session 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db 
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
        