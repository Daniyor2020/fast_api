from fastapi import APIRouter, Depends, status, HTTPException, Response, status
from sqlalchemy.orm import Session

from blog import oauth2
from blog.repository.blog import *
from .. import models, schemas, database


router = APIRouter(
    tags=["Blogs"],
    prefix="/blog"
)

@router.get("/", response_model=list[schemas.Blog], status_code=status.HTTP_201_CREATED)
def get_blogs(db: Session = Depends(database.get_db) , current_user: schemas.User = Depends(oauth2.get_current_user)):
    return get_all_blogs(db)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(blog:schemas.Blog, db: Session = Depends(database.get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
  return create(blog, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(database.get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return delete(id, db)

@router.put("/{id}")
def update_blog(id: int, blog: schemas.Blog, db: Session = Depends(database.get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
  return update(id, blog, db)



@router.get("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.showBlog)
def get_blog(id: int, db: Session = Depends(database.get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
  blog = db.query(models.Blog).filter(models.Blog.id == id).first()
  if not blog:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
  return blog
  
  