from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session 
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from typing import Optional

from db.models.user import User
from db.session import get_db
from utils.password_manager import PasswordManager 
from utils.jwt_manager import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")



class RepositoryUser:

    def __init__(self, db: Session)-> None:
        self.db = db

    def get_user_by_email(self, email: str)-> User | None:
        
        return self.db.query(User).filter(
            func.lower(User.email) == func.lower(email)
            ).first()
    
    
    def create_user(
        self, 
        email: str, 
        password: str, 
        is_active: bool = True, 
        is_superuser: bool = False
    )-> User:
            
        user_exists = self.get_user_by_email(email=email)
        # print(user_exists.__dict__)
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email already exists"
            )

        _hashed_password = PasswordManager.get_password_hash(password=password)
        db_user = User(
            email=email, 
            password=_hashed_password, 
            is_active=is_active, 
            is_superuser=is_superuser,
            username= email.strip().split("@")[0]
        )


        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email already exists"
            )
        
        return db_user
        
    def get_user_by_id(
        self,
        id: int
    )-> User | None:
        # print(self.db.query(User).filter(User.id == id, User.is_active.is_(True)).first())
        return self.db.query(User).filter(User.id == id, User.is_active.is_(True)).first()
    
    def get_user_for_token(
        self, 
        email: str, 
        password: str
    )-> User | None:
        
        user = self.get_user_by_email(email=email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect credentials"
            )
        
        is_password_matched = PasswordManager.verify_password(plain_password=password, hashed_password=user.password)

        if not is_password_matched:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect credentials"
            )
        
        return user
    
    @staticmethod
    def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db),
    ):
        
        payload = verify_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect credential"
            )
        
        user = db.query(User).filter(User.id == payload.get("sub")).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user 
    
    


