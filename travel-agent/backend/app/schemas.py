from pydantic import BaseModel, Field
from typing import List, Optional


class TripRequest(BaseModel):
    origin: str
    destination: str
    start_date: str
    end_date: str
    travelers: int = Field(..., gt=0)
    currency: str = "USD"
    budget: Optional[float]


class Trip(BaseModel):
    id: str
    request: TripRequest
    status: str
