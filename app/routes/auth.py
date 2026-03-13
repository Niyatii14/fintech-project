from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import create_user
from app.schemas.user import UserLogin
from app.services.auth_service import authenticate_user
from app.core.security import create_access_token
from app.schemas.user import UserLogin
from app.services.auth_service import authenticate_user
from app.core.dependencies import get_current_user



router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register",response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    try:
        authenticate_user(db, user.email, user.password)
        return {"message":"Login successful"}
    
    except ValueError as e:
        raise HTTPException(status_code = 400, detail=str(e))
    
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = authenticate_user(db, user.email, user.password)
        token = create_access_token({"sub": db_user.email})
        return {
            "access_token": token,
            "token_type": "bearer"
        }
    except ValueError as e:
        raise HTTPException(status_code = 400, detail=str(e))
    
    

@router.get("/me")

def get_me(user: str = Depends(get_current_user)):
    return {
        "message" : "Authorized",
        "user": user
    }
    