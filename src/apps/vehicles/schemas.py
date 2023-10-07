from pydantic import BaseModel
from typing import Optional

class VINResponse(BaseModel):
    year: int
    make: str
    model: str
    type_vehicle: Optional[str] = None
    color: Optional[str] = None
    dimensions: Optional[str] = None
    weight: Optional[int] = None


class VINRequest(VINResponse):
    vin: str