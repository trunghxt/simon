from fastapi import APIRouter, Depends
from typing import List
from app.models.schemas import LeaderboardEntry
from app.models.user import UserModel

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.get("/leaderboard", response_model=List[LeaderboardEntry])
async def get_leaderboard():
    return await UserModel.get_leaderboard()
