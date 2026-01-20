import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import pprint

load_dotenv()

async def list_users():
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    client = AsyncIOMotorClient(uri)
    db = client["simon_math"]
    
    print(f"Connecting to database: {db.name}")
    print("-" * 30)
    
    cursor = db.users.find({})
    users = await cursor.to_list(length=100)
    
    print(f"Found {len(users)} users:\n")
    for user in users:
        # Convert ObjectId to string for display
        user['_id'] = str(user['_id'])
        pprint.pprint(user)
        print("-" * 30)

if __name__ == "__main__":
    asyncio.run(list_users())
