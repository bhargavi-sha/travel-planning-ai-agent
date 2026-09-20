from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class Activity(BaseModel):
    title: str
    time_of_day: str
    location: Optional[str]
    estimated_duration_minutes: Optional[int]
    cost_estimate: Optional[float]
    category: Optional[str] = None
    tip: Optional[str] = None


class ItineraryDay(BaseModel):
    date: date
    title: Optional[str]
    activities: List[Activity]


class TripRequest(BaseModel):
    origin: str
    destination: str
    start_date: str
    end_date: str
    travelers: int = Field(..., gt=0)
    currency: str = "USD"
    budget: Optional[float]
    trip_type: Optional[str] = "general"
    interests: List[str] = Field(default_factory=list)
    pace: str = "balanced"
    accommodation: Optional[str] = None


class Trip(BaseModel):
    id: str
    request: TripRequest
    status: str
    itinerary: Optional[List[ItineraryDay]] = None
