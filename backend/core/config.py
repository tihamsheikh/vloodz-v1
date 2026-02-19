import os 
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Project settings 
    PROJECT_NAME: str = "VLOODZ"
    PROJECT_VERSION: str = "0.1.0"
    PROJECT_DESCRIPTION: str = "A new generation communication website"

    # DB settings
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")

    SECRET_KEY = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

    

    DB_MODE: str = os.getenv("DB_MODE", "sqlite")  # Default to SQLITE if not set

    @property 
    def DATABASE_URL(self):
        if self.DB_MODE == "sqlite":
            return "sqlite:///./db.sqlite3"
        
        else:
            return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        


settings = Settings()
