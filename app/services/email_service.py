import resend
from app.core.config import settings

class EmailService:
    @staticmethod
    async def send_bulk(to_email: str, subject: str, html_content: str):
        try:
            resend.api_key = settings.RESEND_API_KEY

            response = resend.Emails.send({
                "from": settings.FROM_EMAIL,
                "to": to_email,
                "subject": subject,
                "html": html_content
            })

            print(f"✅ SUCCESSFULLY SENT TO: {to_email}")
            print(f"DEBUG: Resend response id = {response.get('id')}")
            return True

        except Exception as e:
            print(f"❌ RESEND ERROR: {str(e)}")
            return False
