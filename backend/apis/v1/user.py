from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session 
from db.session import get_db 
from schemas.user import CreateUser, ViewUser
from repositories.user import RepositoryUser 



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
    


@router.get("")
def get_users(db: Session = Depends(get_db)):   
    
    return {"message": "List of users"}