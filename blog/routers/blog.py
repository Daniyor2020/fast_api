from fastapi import APIRouter, Depends, status, HTTPException, Response, status
from sqlalchemy.orm import Session
from .. import models, schemas, database


router = APIRouter(
    tags=["Blogs"],
    prefix="/blog"
)



@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(blog:schemas.Blog, db: Session = Depends(database.get_db)):
  new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)
  return new_blog

@router.delete("//{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(database.get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id)
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
  blog.delete(synchronize_session=False)
  db.commit()
  return "deleted"

@router.put("//{id}")
def update_blog(id: int, blog: schemas.Blog, db: Session = Depends(database.get_db)):
  blog_to_update = db.query(models.Blog).filter(models.Blog.id == id)
  if not blog_to_update.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
  blog_to_update.update(blog.dict())
  db.commit()
  return "updated"

@router.get("/", response_model=list[schemas.Blog], status_code=status.HTTP_201_CREATED)
def get_all_blogs(db: Session = Depends(database.get_db)):
  return db.query(models.Blog).all()

@router.get("//{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.showBlog)
def get_blog(id: int, db: Session = Depends(database.get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id).first()
  if not blog:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
  return blog
  
  