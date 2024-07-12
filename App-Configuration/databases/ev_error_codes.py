from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://Shreyas:Shreyas123@fasterapi.i2bp8f5.mongodb.net/"
client = AsyncIOMotorClient(MONGO_URL)
database = client.ev_error_codes_db
ev_error_codes_collection = database.ev_error_codes