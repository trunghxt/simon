from datetime import datetime
from bson import ObjectId
from app.utils.database import db

class QuizModel:
    @staticmethod
    async def save_result(user_id: str, quiz_data: dict):
        result_doc = {
            "user_id": ObjectId(user_id),
            "quiz_type": quiz_data['type'], 
            "score": quiz_data['score'],
            "total_questions": quiz_data['total'],
            "correct_answers": quiz_data['correct'],
            "stars_earned": quiz_data['stars'],
            "time_taken": quiz_data['time'],
            "completed_at": datetime.utcnow()
        }
        
        await db.quiz_history.insert_one(result_doc)
        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$inc": {"total_stars": quiz_data['stars']}}
        )
        return True

    @staticmethod
    async def get_user_history(user_id: str, limit=20):
        cursor = db.quiz_history.find({"user_id": ObjectId(user_id)}).sort("completed_at", -1).limit(limit)
        results = []
        async for doc in cursor:
            results.append({
                "id": str(doc["_id"]),
                "type": doc.get("quiz_type"),
                "score": doc.get("score"),
                "total": doc.get("total_questions"),
                "stars": doc.get("stars_earned"),
                "time": doc.get("time_taken"),
                "date": doc.get("completed_at").isoformat()
            })
        return results

    @staticmethod
    async def clear_history(user_id: str):
        await db.quiz_history.delete_many({"user_id": ObjectId(user_id)})
        return True
