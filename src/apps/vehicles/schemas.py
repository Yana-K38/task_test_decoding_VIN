from pydantic import BaseModel

class VINRequest(BaseModel):
    vin: str

class VINResponse(BaseModel):
    year: int
    make: str
    model: str
    type_vehicle: str
    color: str
    dimensions: str
    weight: int
