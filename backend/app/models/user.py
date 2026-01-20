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
