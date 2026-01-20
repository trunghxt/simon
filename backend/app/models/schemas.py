from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# --- Auth Schemas ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str | None
    total_stars: int = 0
    level: int = 1
    created_at: str | None

class AuthResponse(BaseModel):
    token: str
    user: Optional[UserResponse] = None
    msg: str = "Success"

# --- Quiz Schemas ---
class QuizSubmission(BaseModel):
    type: str
    score: float
    total: int
    correct: int
    stars: int
    time: int

class QuizHistoryItem(BaseModel):
    id: str
    type: str
    score: float
    total: int
    stars: int
    time: int
    date: str

class LeaderboardEntry(BaseModel):
    name: str | None
    total_stars: int
    level: int
