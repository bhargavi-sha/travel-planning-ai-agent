from datetime import date
from fastapi import FastAPI, HTTPException
from uuid import uuid4
from .schemas import TripRequest, Trip
from .agents.planner import TripPlanner


planner = TripPlanner()


app = FastAPI(title="Travel Agent")


TRIPS = {}


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.post("/api/trips", response_model=Trip)
async def create_trip(req: TripRequest):
    try:
        start_date = date.fromisoformat(req.start_date)
        end_date = date.fromisoformat(req.end_date)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="Dates must use YYYY-MM-DD format") from exc
    if end_date < start_date:
        raise HTTPException(status_code=422, detail="End date must be on or after the start date")
    if (end_date - start_date).days > 30:
        raise HTTPException(status_code=422, detail="Trips are limited to 31 days")
    trip_id = str(uuid4())
    trip = Trip(id=trip_id, request=req, status="created")
    TRIPS[trip_id] = trip
    # Run planner synchronously for demo scaffold
    result = await planner.plan(req)
    itinerary = result.get("itinerary")
    # attach itinerary to trip
    trip.itinerary = itinerary
    trip.status = "planned"
    TRIPS[trip_id] = trip
    return trip


@app.get("/api/trips", response_model=list[Trip])
async def list_trips():
    return list(TRIPS.values())


@app.get("/api/trips/{trip_id}")
async def get_trip(trip_id: str):
    trip = TRIPS.get(trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="trip not found")
    return trip
