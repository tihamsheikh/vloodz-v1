from fastapi import APIRouter, Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 

from db.session import get_db 
from schemas.user import CreateUser, Token, ViewUser, ViewSingleUser
from repositories.user import RepositoryUser 
from utils.jwt_manager import (
    create_refresh_token, 
    create_access_token, 
    verify_token
)


router = APIRouter() 

@router.post("", 
             response_model=ViewUser
)
def create_user(
    payload: CreateUser, 
    db: Session = Depends(get_db)
):
    
    repo = RepositoryUser(db)
    new_user = repo.create_user(email=payload.email, password=payload.password)

    return new_user
    # return ViewUser(
    #     id= new_user.id,
    #     email= new_user.email,
    #     is_active= new_user.is_active
    # )
    


@router.get("/{user_id}", response_model=ViewSingleUser)
def get_users(user_id: int,db: Session = Depends(get_db)):   
    
    repo = RepositoryUser(db=db)
    user =repo.get_user_by_id(user_id)

    return ViewSingleUser(
        id= user_id,
        email= user.email,
        username= user.username,
        is_active= user.is_active 
    )

# day 9 2 previews vid left fastapi: 13:30-> make the tokens uniqe to themself, for access for token api and refresh for refresh api
@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = RepositoryUser(db=db).get_user_for_token(
        email=form_data.username,
        password=form_data.password
    )

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/refresh", response_model=Token)
async def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    
    payload = verify_token(refresh_token)
    print("payload: ", payload)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    payload_subject = payload.get("sub")
    user = RepositoryUser(db=db).get_user_by_id(id=payload_subject)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token
    )
















        
