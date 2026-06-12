from fastapi import FastAPI, HTTPException
from typing import Optional, Dict, Any
from datetime import datetime
import uuid
from app.tiktok_client import transform_to_tiktok_payload, send_event_to_tiktok

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
async def receive_event(payload: EventPayload):
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
    tiktok_payload = transform_to_tiktok_payload(payload, event_id, timestamp)
    status_code, tiktok_response = await send_event_to_tiktok(tiktok_payload)

    return {
        "message": "Event validated and forwarded",
        "event_id": event_id,
        "event_name": payload.event_name,
        "timestamp": timestamp,
        "gateway_status":"forwarded",
        "desitnation_status_code":status_code,
        "destination_response": tiktok_response
        
    }
@app.post("/mock-tiktok/event/track")
def mock_tiktok_event_track(payload:dict):
    return {
        "mock_tiktok_status": "success",
        "message": "Event received by mock TikTok API",
        "received_payload":payload
    }

