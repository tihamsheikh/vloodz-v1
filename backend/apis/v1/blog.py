from fastapi import APIRouter, Depends, status
from schemas.blog import (
    CreateBlog, 
    ViewSingleBlog, 
    ViewListBlog, 
    ViewPaginatedBlog, 
    ViewPaginatedBlogFilter,
    UpdateBlog, 
    UpdateBlogResponse
)
from db.session import get_db 
from sqlalchemy.orm import Session 
from repositories.blog import provide_blog_repository
from repositories.user import RepositoryUser
from db.models.user import User 

router = APIRouter()


# create a new blog
@router.post("")
async def create_blog(
    payload: CreateBlog,
    db: Session = Depends(get_db),
    current_user: User = Depends(RepositoryUser.get_current_user)
):
    
    repo = provide_blog_repository(db)
    repo.create_blog(data=payload, author_id=current_user.id)

    print(payload)
    return {"message": "blog created successfully"}

# get a single blog
@router.get("/{blog_id}",
    response_model=ViewSingleBlog
)
async def get_single_blog(
    blog_id: int,
    db: Session = Depends(get_db)                          
):
    repo = provide_blog_repository(db)
    print(repo.get_single_blog(blog_id=blog_id))
    blog_data = repo.get_single_blog(blog_id=blog_id)


    return blog_data


# TODO: do sort and search
# get all paginated blogs
@router.get("",
            response_model=ViewPaginatedBlog
        )
async def get_all_blogs(
    filter: ViewPaginatedBlogFilter = Depends(),
    db: Session = Depends(get_db)
):
    
    repo = provide_blog_repository(db)
    result = repo.get_all_blogs(filter=filter)
    total = result[0] if isinstance(result[0], int) else result[1]
    items = result[1] if isinstance(result[0], int) else result[0]
    # print(total, items)
   

    return ViewPaginatedBlog(
        page=filter.page,
        limit=filter.limit,
        total=total,
        items=items
    )


# update a blog 
@router.patch("/{blog_id}",
            response_model=UpdateBlogResponse
        )
async def update_blog(
    blog_id: int,
    payload: UpdateBlog,
    db: Session = Depends(get_db),
    current_user: User = Depends(RepositoryUser.get_current_user)
)-> UpdateBlogResponse:
    
    repo = provide_blog_repository(db)
    updated_blog = repo.update_blog(blog_id=blog_id, payload=payload)

    return UpdateBlogResponse(
        message="Blog updated successfully",
        data=updated_blog
    )


@router.delete("/{blog_id}",
               status_code=status.HTTP_204_NO_CONTENT
            )
async def delete_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(RepositoryUser.get_current_user)
):
    repo = provide_blog_repository(db)
    repo.delete_blog(blog_id=blog_id)






