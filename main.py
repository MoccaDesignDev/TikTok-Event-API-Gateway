from fastapi import FastAPI, HTTPException
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

from app.models import EventPayload
from app.validators import (
    validate_event_name,
    validate_purchase_event,
    validate_consent
)

app = FastAPI(title="TikTok Events API Conversion Gateway")




@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "TikTok Events API Conversion Gateway"
    }


@app.post("/events")
def receive_event(payload: EventPayload):
    is_valid, error = app.validators.validate_event_name(payload.event_name)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)
    
    is_valid, error = app.validators.validate_purchase_event(payload)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)
    
    is_valid, error = app.validators.validate_consent(payload)
    if not is_valid:
        return {
            "status": "blocked",
            "reason": error
        }
    event_id = payload.event_id or str(uuid.uuid4())
    timestamp = payload.timestamp or datetime.utcnow().isoformat()

    return {
        "message": "Event received",
        "event_id": event_id,
        "event_name": payload.event_name,
        "timestamp": timestamp,
        "consent": payload.consent,
        "status": "accepted"
    }