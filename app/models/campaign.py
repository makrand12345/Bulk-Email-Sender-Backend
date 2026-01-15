from pydantic import BaseModel, Field
from datetime import datetime

class CampaignModel(BaseModel):
    name: str
    subject: str
    title: str
    body: str
    footer: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TemplateResponse(BaseModel):
    id: str
    name: str
    subject: str
    title: str
    body: str
    footer: str
