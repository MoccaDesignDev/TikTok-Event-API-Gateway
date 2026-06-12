from pydantic import BaseModel
from typing import Optional, Dict, Any

class EventPayload(BaseModel):
    event_name: str
    event_id:Optional[str] = None
    timestamp: Optional[str] = None
    url: Optional[str] = None
    user_data: Optional[Dict[str, Any]] = {}
    custom_data: Optional[Dict[str, Any]] = {}
    consent: Optional[bool] = True

