SUPPORTED_EVENTS ={
    "ViewContent",
    "AddToCart",
    "InitiateCheckOut",
    "Purchase",
    "SubmitForm",
    "CompleteRegistration",
    "Contact"
}


def validate_event_name(event_name: str):
    if event_name not in SUPPORTED_EVENTS: 
        return False, f"Unsupported event_name:{event_name}"
    return True, None

def validate_purchase_event(payload):
    if payload.event_name == "Purchase":
        value = payload.custom_data.get("value")
        currency = payload.custom_data.get("currency")

        if value is None:
            return False, "Purchase event requires custom_data.value"

        if currency is None:
            return False, "Purchase event requires custom.data.curency"
    
    return True, None

def validate_consent(payload):
    if payload.consent is not True:
        return False, "User consent is false. Event should be forwarded."
    return True, None

