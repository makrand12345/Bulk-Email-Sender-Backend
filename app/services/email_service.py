import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

class EmailService:
    @staticmethod
    async def send_bulk(to_email: str, subject: str, html_content: str):
        try:
            msg = MIMEMultipart()
            msg['From'] = f"ASP OL Media Hiring <{settings.SMTP_USER}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(html_content, 'html'))

            # Using with statement to ensure connection closes
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=15) as server:
                server.set_debuglevel(1) # This forces the SMTP conversation to show in terminal
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            
            print(f"✅ SUCCESSFULLY SENT TO: {to_email}")
            return True
        except smtplib.SMTPAuthenticationError:
            print(f"❌ AUTH ERROR: Gmail rejected your credentials. Check App Password.")
            return False
        except Exception as e:
            print(f"❌ DETAILED SMTP ERROR: {str(e)}")
            return False