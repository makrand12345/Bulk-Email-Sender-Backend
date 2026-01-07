from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

db_instance = MongoDB()

async def connect_to_mongo():
    db_instance.client = AsyncIOMotorClient(settings.MONGO_URI)
    db_instance.db = db_instance.client.get_database("bulk_email_db")
    
    # Predefined Hiring Templates for ASP OL Media
    templates = [
        {
            "name": "Application Received",
            "subject": "Resume Received - ASP OL Media",
            "content": "<h1>Thank you for applying!</h1><p>We have received your resume and our team is currently reviewing your profile.</p>"
        },
        {
            "name": "Not Selected",
            "subject": "Application Update - ASP OL Media",
            "content": "<h1>Status Update</h1><p>Thank you for your interest. At this time, we have decided to move forward with other candidates.</p>"
        },
        {
            "name": "Interview Invitation",
            "subject": "Interview Selection - ASP OL Media",
            "content": "<h1>Congratulations!</h1><p>You have been selected for a personal interview. Please reply with your availability.</p>"
        },
        {
            "name": "Offer Letter",
            "subject": "Offer of Employment - ASP OL Media",
            "content": "<h1>Welcome to the Team!</h1><p>We are pleased to offer you full-time employment at ASP OL Media Pvt. Ltd.</p>"
        }
    ]
    
    # Auto-seed templates if collection is empty
    count = await db_instance.db.templates.count_documents({})
    if count == 0:
        await db_instance.db.templates.insert_many(templates)

async def close_mongo_connection():
    if db_instance.client:
        db_instance.client.close()