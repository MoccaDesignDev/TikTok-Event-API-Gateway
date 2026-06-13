from fastapi import FastAPI, HTTPException, Depends
from typing import Optional, Dict, Any
from datetime import datetime
import uuid
from app.tiktok_client import transform_to_tiktok_payload, send_event_to_tiktok
from sqlalchemy.orm import Session

from app.event_repository import create_event_log, find_event_by_event_id
from app.database import Base, engine, SessionLocal
from app.event_repository import create_event_log
from app.db_models import EventLog

Base.metadata.create_all(bind=engine)

from app.models import EventPayload
from app.validators import (
    validate_event_name,
    validate_purchase_event,
    validate_consent
)

app = FastAPI(title="TikTok Events API Conversion Gateway")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/events/logs")
def get_event_logs(db: Session = Depends(get_db)):
    logs = db.query(EventLog).order_by(EventLog.created_at.desc()).limit(50).all()
    return [
        {
            "id": log.id,
            "event_id": log.event_id,
            "event_name": log.event_name,
            "status": log.status,
            "source_url": log.source_url,
            "created_at": log.created_at
        }
        for log in logs
    ]
def health_check():
    return {
        "status": "ok",
        "service": "TikTok Events API Conversion Gateway"
    }


@app.post("/events")
async def receive_event(payload: EventPayload, db:Session = Depends(get_db)):
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
    existing_event = find_event_by_event_id(db, event_id)
    if existing_event:
        return {
            "status":"duplicate",
            "message": "Event already received. Not forwarded again.",
            "event_id": event_id,
            "event_name": payload.event_name
        }
    
@app.post("/mock-tiktok/event/track")
def mock_tiktok_event_track(payload:dict):
    return {
        "mock_tiktok_status": "success",
        "message": "Event received by mock TikTok API",
        "received_payload":payload
    }

create_event_log(
    db = db,
    event_id=event_id,
    event_name=payload.event_name,
    status="forwarded",
    source_url = payload.url
    request_payload = tiktok_payload,
    destination_response=tiktok_response
)
