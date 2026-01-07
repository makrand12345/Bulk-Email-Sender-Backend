import asyncio
from fastapi import APIRouter, BackgroundTasks, UploadFile, File, Form
from app.db.mongo import db_instance
from app.services.email_service import EmailService
from app.services.template_service import TemplateService
from app.utils.csv_parser import parse_recipient_csv

router = APIRouter()

@router.get("/templates")
async def get_templates():
    templates = []
    if db_instance.db is not None:
        cursor = db_instance.db.templates.find()
        async for doc in cursor:
            templates.append({
                "id": str(doc["_id"]),
                "name": doc["name"],
                "subject": doc["subject"],
                "content": doc["content"]
            })
    print(f"DEBUG: Fetched {len(templates)} templates from DB")
    return templates

async def process_hiring_campaign(campaign_data: dict, recipients: list):
    print(f"DEBUG: Starting background loop for {len(recipients)} candidates...")
    for user in recipients:
        email = user.get('email')
        if not email:
            print("DEBUG: Skipping record - No email found")
            continue
            
        print(f"DEBUG: Processing email: {email}")
        designed_html = TemplateService.render_responsive_template(campaign_data['html_content'])
        
        # Await the sending service
        success = await EmailService.send_bulk(email, campaign_data['subject'], designed_html)
        
        if success:
            print(f"✅ FINAL STATUS: Sent to {email}")
        else:
            print(f"❌ FINAL STATUS: Failed to send to {email}")
            
        await asyncio.sleep(1)

@router.post("/send-bulk")
async def create_bulk_campaign(
    background_tasks: BackgroundTasks,
    name: str = Form(...),
    subject: str = Form(...),
    html_content: str = Form(...),
    csv_file: UploadFile = File(...)
):
    # READ CSV
    content = await csv_file.read()
    recipients = parse_recipient_csv(content)
    
    print(f"\n--- NEW CAMPAIGN RECEIVED ---")
    print(f"Template Name: {name}")
    print(f"Recipients found: {len(recipients)}")
    
    if len(recipients) == 0:
        print("ERROR: CSV parsing resulted in 0 recipients. Check CSV format!")

    campaign_data = {"name": name, "subject": subject, "html_content": html_content}
    background_tasks.add_task(process_hiring_campaign, campaign_data, recipients)
    
    return {"message": "Hiring batch started successfully!"}