import httpx
import os

TIKTOK_API_MODE = os.getenv("TIKTOK_API_MODE", "mock")
MOCK_TIKTOK_URL = os.getenv(
    "MOCK_TIKTOK_URL",
    "http://127.0.0.1:8000/mock-tiktok/event/track"
)

def transform_to_tiktok_payload(payload, event_id, timestamp):
    return {
        "event_source": "web",
        "event_source_id": os.getenv("TIKTOK_PIXEL_CODE", "TEST_PIXEL_CODE"),
        "data":[
            {
                "event": payload.event_name,
                "event_id": event_id,
                "timestamp": timestamp,
                "page":{
                    "url":payload.url
                },
                "user": payload.user_data,
                "properties": payload.custom_data
            }
        ]
    }

async def send_event_to_tiktok(tiktok_payload):
     async with httpx.AsyncClient() as client:
        response = await client.post(MOCK_TIKTOK_URL, json=tiktok_payload)
        return response.status_code, response.json()
    