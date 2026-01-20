from datetime import datetime
from bson import ObjectId
from app.utils.database import db

class UserModel:
    @staticmethod
    async def create_user(user_data: dict) -> str:
        result = await db.users.insert_one(user_data)
        return str(result.inserted_id)

    @staticmethod
    async def find_by_email(email: str):
        return await db.users.find_one({"email": email})

    @staticmethod
    async def find_by_id(user_id: str):
        try:
            return await db.users.find_one({"_id": ObjectId(user_id)})
        except:
            return None

    @staticmethod
    async def get_leaderboard(limit: int = 10):
        cursor = db.users.find({}, {"name": 1, "total_stars": 1, "level": 1, "_id": 0}).sort("total_stars", -1).limit(limit)
        return await cursor.to_list(length=limit)
