from pydantic import BaseModel, Field 
from datetime import datetime


class CreateBlog(BaseModel):
    title: str = Field("untitled blog", min_length=1, max_length=80) 
    content: str 
    is_active: bool 

    class Config:
        orm_mode = True 


class ViewSingleBlog(BaseModel):
    author_id: int 
    title: str 
    content: str  
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True 

class ViewListBlog(BaseModel):
    id: int
    author_id: int 
    title: str 
    
    class Config:
        orm_mode = True

class ViewPaginatedBlog(BaseModel):
    page: int 
    limit: int 
    total: int
    items: list[ViewListBlog] = Field(default_factory=list)

    class Config: 
        orm_mode = True 


class ViewPaginatedBlogFilter(BaseModel):
    page: int = Field(default=1, gt=0)
    limit: int = Field(default=5, gt=0, le=5)
    search: str = Field(default=None, max_length=50)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit

    @property
    def stop(self) -> int:
        return self.offset + self.limit

    class Config: 
        orm_mode = True 

class ViewPaginatedBlogResponse(BaseModel):
    total: int 
    items: list[ViewListBlog]

    class Config: 
        orm_mode = True


class UpdateBlog(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=80)
    content: str | None = Field(None, min_length=5)
    is_active: bool | None = None 

    class Config:
        orm_mode = True

class UpdateBlogResponse(BaseModel):
    message: str 
    data: ViewSingleBlog

    class Config:
        orm_mode = True