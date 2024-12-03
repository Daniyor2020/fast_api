from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .. import models, schemas, database, token
from ..hashing import Hash
from sqlalchemy.orm import Session



router = APIRouter(
    tags=["Authentication"],
    prefix="/login"
)

@router.post("/")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {request.username} not found")
    
    if(not Hash.verify(user.password, request.password)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")
    
    access_token = token.create_access_token(data={"sub": user.email})

    response = {"access_token": access_token, "token_type": "bearer"}
    return response
   