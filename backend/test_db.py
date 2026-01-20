import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def test_connection():
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    print(f"Connecting to {uri}...")
    try:
        client = AsyncIOMotorClient(uri)
        # Force a connection check
        await client.admin.command('ping')
        print("MongoDB connection successful!")
        
        db = client["test_db"]
        res = await db.test_col.insert_one({"test": "data"})
        print(f"Insert successful: {res.inserted_id}")
        
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
