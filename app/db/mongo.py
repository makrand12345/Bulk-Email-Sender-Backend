from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class MongoDB:
    client = None
    db = None

db_instance = MongoDB()

async def connect_to_mongo():
    db_instance.client = AsyncIOMotorClient(settings.MONGO_URI)
    db_instance.db = db_instance.client.get_database("bulk_email_db")

    templates = [
        {
            "name": "Offer Letter",
            "subject": "Offer for {{name}}",
            "title": "Congratulations {{name}}!",
            "body": "We are pleased to offer you the role of {{role}} at {{company}}.",
            "footer": "ASP OL Media Hiring Team"
        }
    ]

    if await db_instance.db.templates.count_documents({}) == 0:
        await db_instance.db.templates.insert_many(templates)

async def close_mongo_connection():
    if db_instance.client:
        db_instance.client.close()
