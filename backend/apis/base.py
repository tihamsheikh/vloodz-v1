from fastapi import APIRouter 
from apis.v1.user import router as user_router  
from apis.v1.blog import router as blog_router 


base_router = APIRouter(prefix="/v1")

# Registered user router 
base_router.include_router(
    router=user_router, 
    prefix="/users", 
    tags=["users"]
)


base_router.include_router(
    router=blog_router,
    prefix="/blogs",
    tags=["blogs"]
)