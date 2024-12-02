from fastapi import APIRouter, Depends, status, HTTPException, Response, status
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..hashing import Hash
from ..database import get_db


router = APIRouter(tags = ["User"], prefix = "/user")


@router.post("/", status_code=status.HTTP_201_CREATED, tags = ["User"], response_model=schemas.ShowUser)
def create_user(user:schemas.User, db: Session = Depends(get_db)):
  hashed_password = Hash.bcrypt(user.password)
  new_user = models.User(name=user.name, email=user.email, password=hashed_password)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user
@router.get("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
  return user