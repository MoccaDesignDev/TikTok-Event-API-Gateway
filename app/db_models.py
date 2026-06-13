from sqlalchemy import Column, Integer, String, DataTime, Text
from datatime import datatime
from app.database import Base

class EventLog(Base):
    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, index=True)
    event_name = Column(String, index=True)
    status = Column(String, index=True)
    source_url = Column(String)
    request_payload = Column(Text)
    destination_response = Column(Text)
    created_at = Column(DataTime, default=datetime.utcnow)

    