from fastapi import HTTPException, status
from sqlalchemy.orm import Session 
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from typing import Optional
from db.models.user import User
from utils.password_manager import PasswordManager 



class RepositoryUser:

    def __init__(self, db: Session)-> None:
        self.db = db

    def get_user_by_email(
        self, 
        email: str
    )-> Optional[User]:
        
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
        
