from pydantic import BaseModel, Field

class TelemetryLogInput(BaseModel):
    """
    Strict data validation contract for incoming client traffic frames.
    Enforces structure at the web door before allowing data to hit the AI model.
    """
    raw_log: str = Field(..., min_length=5, description="The unstructured raw computer error string.")
