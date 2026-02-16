from fastapi import HTTPException, status
from sqlalchemy.orm import Session 
from sqlalchemy import text
from schemas.blog import (
    CreateBlog, 
    ViewPaginatedBlogFilter, 
    ViewPaginatedBlogResponse,
    ViewListBlog,
    UpdateBlog
)
from slugify import slugify
from db.models.blog import Blog

class RepositoryBlog:

    def __init__(self, 
            db: Session
    )-> None:
        self.db = db 


    def create_blog(
        self,
        data: CreateBlog,
        author_id: int
    )-> None:

        slug = slugify(data.title)
        print(slug)
        
        # sql = text("""
        #     INSERT INTO blogs (title, content, is_active, slug, author_id, created_at)
        #     VALUES (:title, :content, :is_active, :slug, :author_id, datetime('now', 'utc'))
        #     RETURNING *, id, slug 
        # """)
        # params = {
        #     "title": data.title,
        #     "content": data.content,
        #     "is_active": data.is_active,
        #     "slug": slug,
        #     "author_id": author_id,
        # }
        # blog_id = (self.db.execute(sql, params=params)).scalar().first()
        # print(blog_id)

        # db_blog = Blog(
        #     title=data.title,
        #     slug=slug,
        #     content=data.content,
        #     author_id=author_id,
        #     is_active=data.is_active
        # )
        db_blog = Blog(**data.dict(), slug=slug, author_id=author_id)

        try:
            self.db.add(db_blog)
            self.db.commit()
            self.db.refresh(db_blog)
        except Exception as e:
            self.db.rollback()
            print("exception ", e)
            raise e 
        finally:
            self.db.close()

    def get_single_blog(
        self,
        blog_id: int
    ):
        
        # sql = text("""
        #      SELECT * FROM blogs WHERE id = :blog_id
        # """)
        # data = (self.db.execute(sql, {"blog_id": blog_id})).first()

        data = self.db.query(Blog).filter(Blog.id == blog_id).first()


        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Blog not found"
            )
        

        return data 
        # return {
        #     "author_id": data.author_id,
        #     "slug": data.slug,
        #     "title": data.title,
        #     "content": data.content,
        #     "created_at": data.created_at,
        #     "is_active": data.is_active
        # }
    
    def get_all_blogs(
        self,
        filter: ViewPaginatedBlogFilter
    )-> tuple:
        query = self.db.query(Blog)

        if filter.search:
            query = query.filter(Blog.title.ilike(f"%{filter.search}%"))

        # offset = filter.offset
        # stop = filter.stop

        total = query.count()   # total number of blogs
        # items = [
        #     ViewListBlog.from_orm(blog) for blog in query.offset(filter.offset).limit(limit=filter.limit).all()
        # ]
        items = query.offset(filter.offset).limit(limit=filter.limit).all()     # values of blogs
        print(total, items)

        return total, items
    

    def update_blog(
        self,
        blog_id: int,
        payload: UpdateBlog,
    )-> Blog:
        
        blog = self.get_single_blog(blog_id=blog_id)

        if payload.title:
            blog.title = payload.title

        if payload.content:
            blog.content = payload.content

        if payload.is_active:
            blog.is_active = payload.is_active

        self.db.add(blog)
        self.db.commit()
        self.db.refresh(blog)

        return blog
        
    def delete_blog(
        self,
        blog_id: int
    ):
        blog = self.get_single_blog(blog_id=blog_id)
        self.db.delete(blog)
        self.db.commit()
        



def provide_blog_repository(db: Session)-> RepositoryBlog:
    return RepositoryBlog(db)
