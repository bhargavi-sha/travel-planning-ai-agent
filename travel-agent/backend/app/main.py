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
    trip_id = str(uuid4())
    trip = Trip(id=trip_id, request=req, status="created")
    TRIPS[trip_id] = trip
    # Start planning in background - simplified synchronous call for scaffold
    itinerary = await planner.plan(req)
    trip.status = "planned"
    return trip


@app.get("/api/trips/{trip_id}")
async def get_trip(trip_id: str):
    trip = TRIPS.get(trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="trip not found")
    return trip
