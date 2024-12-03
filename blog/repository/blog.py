
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models



def get_all_blogs(db: Session ):
  return db.query(models.Blog).all()

def create(blog ,db):
  new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)
  return new_blog

def delete(id, db):
  blog = db.query(models.Blog).filter(models.Blog.id == id)
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
  blog.delete(synchronize_session=False)
  db.commit()
  return "deleted"

def update(id, blog, db):
  blog_to_update = db.query(models.Blog).filter(models.Blog.id == id)
  if not blog_to_update.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
  blog_to_update.update(blog.dict())
  db.commit()
  return "updated"

def get_blog_by_id(id ,db):
  blog = db.query(models.Blog).filter(models.Blog.id == id).first()
  if not blog:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
  return blog