from pydantic import BaseModel, Field, EmailStr
from email_validator import validate_email, EmailNotValidError
from password_validator import PasswordValidator 
from fastapi import HTTPException, status 



class CreateUser(BaseModel):
    email: str
    password: str = Field(..., min_length=8)

    def __init__(self, **data):
        super().__init__(**data)

        if self.email:
            try: 
                self.email = self.email.strip().lower()
                email_info = validate_email(self.email, check_deliverability=True)
                self.email = email_info.normalized
                
            except EmailNotValidError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid email address. {e}"
                )
            
        if self.password:
            password_schema = PasswordValidator()
            password_schema.min(8).has().uppercase().has().lowercase().has().digits().has().symbols()
         
            
            if not password_schema.validate(self.password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Must have at least 8 characters, uppercase and lowercase letters, digits symbols!"
                )
            
    class Config:
        orm_mode = True 

    
class ViewUser(BaseModel):
    id: int 
    email: EmailStr
    is_active: bool 

    class Config:
        orm_mode = True 


class ViewSingleUser(BaseModel):
    id: int 
    email: EmailStr
    username: str 
    is_active: bool 

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str 
    refresh_token: str 
    token_type: str = "bearer"


