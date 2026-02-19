from fastapi import FastAPI, Depends 
from uvicorn import run 

# project file call 
from core.config import settings 
from apis.base import base_router 
from repositories.user import RepositoryUser
from db.models.user import User 

# TODO: completed the /user/token
# TODO: complete the the get all users router
#  
# facebook 13 class / yt 2nd last class -> 44:00 

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION
)
app.include_router(router=base_router)



@app.get("/")
def index():
    return {"message": "Hello, World!"}


@app.get("/protected")
async def protected_router(current_user: User = Depends(RepositoryUser.get_current_user)):
    return {"message": f"Hello, {current_user.email}! You are good to go!"}



if __name__ == "__main__":
    run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True 
    )