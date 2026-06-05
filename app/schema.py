# app/schema.py
from pydantic import BaseModel, ValidationError
from typing import Optional

class CommandPayload(BaseModel):
    command:    Optional[str]   = None   # Desktop action name e.g. PREV_TRACK
    eeg_signal: Optional[str]   = None   # Raw EEG e.g. LEFT_HAND
    category:   Optional[str]   = None   # e.g. media, browser, mouse
    confidence: float
    timestamp:  Optional[float] = None
    source:     Optional[str]   = "EEG"

def validate_command(data: dict):
    try:
        payload = CommandPayload(**data)

        # Must have either command OR (eeg_signal + category)
        if not payload.command and not (payload.eeg_signal and payload.category):
            return None, "Provide either 'command' or both 'eeg_signal' and 'category'"

        return payload.dict(), None
    except ValidationError as e:
        errors = e.errors()
        msg    = "; ".join([f'{err["loc"][0]}: {err["msg"]}' for err in errors])
        return None, msg