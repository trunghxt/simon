from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.schemas import QuizSubmission, QuizHistoryItem
from app.models.quiz import QuizModel
from app.utils.deps import get_current_user

router = APIRouter(prefix="/quiz", tags=["Quiz"])

@router.post("/submit", status_code=201)
async def submit_quiz(submission: QuizSubmission, current_user: dict = Depends(get_current_user)):
    user_id = current_user['id']
    success = await QuizModel.save_result(user_id, submission.dict())
    if success:
        return {"msg": "Result saved successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to save result")

@router.get("/history", response_model=List[QuizHistoryItem])
async def get_history(current_user: dict = Depends(get_current_user)):
    user_id = current_user['id']
    history = await QuizModel.get_user_history(user_id)
    return history

@router.delete("/history")
async def clear_history(current_user: dict = Depends(get_current_user)):
    user_id = current_user['id']
    await QuizModel.clear_history(user_id)
    return {"msg": "History cleared"}
