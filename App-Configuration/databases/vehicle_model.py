from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://Shreyas:Shreyas123@fasterapi.i2bp8f5.mongodb.net/"
client = AsyncIOMotorClient(MONGO_URL)
database = client.vehicle_model_db
vehicle_model_collection = database.vehicle_models
