# app/schema.py
from pydantic import BaseModel, ValidationError
from typing import Optional

class CommandPayload(BaseModel):
    command: str
    confidence: float
    timestamp: Optional[float] = None
    source: Optional[str] = "EEG"

def validate_command(data: dict):
    """
    Returns (validated_dict, None) on success.
    Returns (None, error_message) on failure.
    """
    try:
        payload = CommandPayload(**data)
        return payload.dict(), None
    except ValidationError as e:
        errors = e.errors()
        msg = "; ".join([f'{err["loc"][0]}: {err["msg"]}' for err in errors])
        return None, msg