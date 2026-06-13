import json
from app.db_models import EventLog

def create_event_log(
        db,
        event_id,
        event_name,
        status,
        source_url,
        request_payload,
        destination_response
):
    
    event_log = EventLog(
        event_id = event_id,
        event_name = event_name,
        status = status,
        source_url = source_url,
        request_payload = json.dumps(request_payload),
        destination_response = json.dumps(destination_response)
    )

    db.add(event_log)
    db.commit()
    db.refresh(event_log)

    return event_log

def find_event_by_event_id(db, event_id):
    return db.query(EventLog).filter(EventLog.event_id == event_id).first()

