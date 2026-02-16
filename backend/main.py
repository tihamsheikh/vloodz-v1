from fastapi import FastAPI 
from uvicorn import run 

# project file call 
from core.config import settings 
from apis.base import base_router 

# class 12 facebook 


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION
)
app.include_router(router=base_router)



@app.get("/")
def index():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True 
    )