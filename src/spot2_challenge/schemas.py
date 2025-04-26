from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class UserMessage(BaseModel):
    session_id: str
    message: str

class BotResponse(BaseModel):
    reply: str
    collected_fields: Dict[str, Any]

class ResponseFields(BaseModel):
    budget: Optional[float] = Field(None, gt=0)
    total_size_requirement: Optional[float] = Field(None, gt=0)
    real_estate_type: Optional[str] = None
    city: Optional[str] = None
    additional_fields: Dict[str, str] = {}

class SessionData(BaseModel):
    fields: ResponseFields
    history: list = Field(default_factory=list)

class OpenAIResponse(BaseModel):
    new_data: ResponseFields
    reply: str