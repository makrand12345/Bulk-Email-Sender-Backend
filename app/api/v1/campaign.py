import asyncio
from fastapi import APIRouter, UploadFile, File, Form
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
    print(f"DEBUG: Processing {len(recipients)} candidate(s)...")

    success_count = 0

    for user in recipients:
        email = user.get("email")
        if not email:
            continue

        print(f"DEBUG: Sending to {email}")

        designed_html = TemplateService.render_responsive_template(
            campaign_data["html_content"]
        )

        success = await EmailService.send_bulk(
            email,
            campaign_data["subject"],
            designed_html
        )

        if success:
            success_count += 1
            print(f"✅ SENT TO {email}")
        else:
            print(f"❌ FAILED TO SEND {email}")

        await asyncio.sleep(0.5)  # rate safety

    print(f"✅ COMPLETED: {success_count}/{len(recipients)} sent")


@router.post("/send-bulk")
async def create_bulk_campaign(
    name: str = Form(...),
    subject: str = Form(...),
    html_content: str = Form(...),
    csv_file: UploadFile = File(...)
):
    content = await csv_file.read()
    recipients = parse_recipient_csv(content)

    print("\n--- NEW CAMPAIGN RECEIVED ---")
    print(f"Template Name: {name}")
    print(f"Recipients found: {len(recipients)}")

    if not recipients:
        return {"message": "No recipients found in CSV."}

    campaign_data = {
        "name": name,
        "subject": subject,
        "html_content": html_content
    }

    # 🔥 IMPORTANT: synchronous execution
    await process_hiring_campaign(campaign_data, recipients)

    return {
        "message": f"Hiring emails sent to {len(recipients)} recipient(s)."
    }
