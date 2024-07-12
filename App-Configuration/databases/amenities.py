from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from pydantic_core import core_schema

MONGO_URL = "mongodb+srv://Shreyas:Shreyas123@fasterapi.i2bp8f5.mongodb.net/"
client = AsyncIOMotorClient(MONGO_URL)
database = client.amenities_db
amenities_collection = database.amenities