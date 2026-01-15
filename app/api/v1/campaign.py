import asyncio
from fastapi import APIRouter, UploadFile, File, Form
from app.services.email_service import EmailService
from app.services.template_service import TemplateService
from app.utils.csv_parser import parse_recipient_csv

router = APIRouter()


@router.post("/preview")
async def preview_email(
    company_name: str = Form(...),
    header_title: str = Form(...),
    title: str = Form(...),
    body: str = Form(...),
    footer: str = Form(...)
):
    dummy_user = {
        "name": "John Doe",
        "role": "Frontend Developer",
        "company": company_name
    }

    html = TemplateService.render_template(
        {
            "company_name": company_name,
            "header_title": header_title,
            "title": title,
            "body": body,
            "footer": footer
        },
        dummy_user
    )

    return {"html": html}


@router.post("/send-bulk")
async def send_bulk(
    company_name: str = Form(...),
    header_title: str = Form(...),
    subject: str = Form(...),
    title: str = Form(...),
    body: str = Form(...),
    footer: str = Form(...),
    csv_file: UploadFile = File(...)
):
    recipients = parse_recipient_csv(await csv_file.read())

    for user in recipients:
        html = TemplateService.render_template(
            {
                "company_name": company_name,
                "header_title": header_title,
                "title": title,
                "body": body,
                "footer": footer
            },
            user
        )

        await EmailService.send_bulk(user["email"], subject, html)
        await asyncio.sleep(0.5)

    return {"message": f"Campaign emails sent to {len(recipients)} recipients"}
