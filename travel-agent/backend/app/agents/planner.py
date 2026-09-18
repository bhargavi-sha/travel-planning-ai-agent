from ..ai.provider import get_provider


class TripPlanner:
    def __init__(self):
        self.llm = get_provider()

    async def plan(self, trip_request):
        # Simple demo planning flow
        prompt = f"Plan a trip to {trip_request.destination}"
        res = await self.llm.call(prompt)
        return {"itinerary": "demo", "agent_events": ["planned"]}
