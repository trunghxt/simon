from fastapi import APIRouter, HTTPException, Depends, status
from app.models.schemas import UserCreate, UserLogin, AuthResponse, UserResponse
from app.models.user import UserModel
from app.utils.security import verify_password, get_password_hash, create_access_token
from app.utils.deps import get_current_user
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=AuthResponse, status_code=201)
async def register(user_in: UserCreate):
    existing_user = await UserModel.find_by_email(user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    hashed_pw = get_password_hash(user_in.password)
    name = user_in.name or user_in.email.split('@')[0]
    
    user_doc = {
        "email": user_in.email,
        "password": hashed_pw,
        "name": name,
        "created_at": datetime.utcnow(),
        "total_stars": 0,
        "level": 1
    }
    
    user_id = await UserModel.create_user(user_doc)
    
    # Auto login
    token = create_access_token(data={"sub": user_id})
    
    # Needs to match user_doc format but with ID
    user_doc["id"] = user_id
    # remove password before return
    del user_doc["password"]
    user_doc["created_at"] = user_doc["created_at"].isoformat()
    
    return {"msg": "User created successfully", "token": token, "user": user_doc}

@router.post("/login", response_model=AuthResponse)
async def login(user_in: UserLogin):
    user = await UserModel.find_by_email(user_in.email)
    if not user or not verify_password(user_in.password, user['password']):
        raise HTTPException(status_code=401, detail="Bad email or password")
    
    user_id = str(user["_id"])
    token = create_access_token(data={"sub": user_id})
    
    user_resp = {
        "id": user_id,
        "email": user["email"],
        "name": user["name"],
        "total_stars": user.get("total_stars", 0),
        "level": user.get("level", 1),
        "created_at": user.get("created_at").isoformat() if user.get("created_at") else None
    }
    
    return {"msg": "Login successful", "token": token, "user": user_resp}

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user
