from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from pydantic_core import core_schema

MONGO_URL = "mongodb+srv://Shreyas:Shreyas123@fasterapi.i2bp8f5.mongodb.net/"
client = AsyncIOMotorClient(MONGO_URL)
database = client.vehicle_brands_db
vehicle_brand_collection = database.vehicle_brands

async def check_connection():
    try:
        await client.admin.command('ping')
        print("Successfully connected to MongoDB")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ]),
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)