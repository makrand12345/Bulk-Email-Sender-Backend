from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime

class CampaignModel(BaseModel):
    name: str
    subject: str
    html_content: str
    status: str = "draft"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TemplateResponse(BaseModel):
    id: str
    name: str
    subject: str
    content: str