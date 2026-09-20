from ..ai.provider import get_provider
from datetime import datetime, timedelta
from ..schemas import ItineraryDay, Activity


class TripPlanner:
    def __init__(self):
        self.llm = get_provider()

    async def plan(self, trip_request):
        # Demo deterministic planner: create simple day-by-day activities
        try:
            start = datetime.fromisoformat(trip_request.start_date)
            end = datetime.fromisoformat(trip_request.end_date)
        except Exception:
            # fallback if dates are not iso
            start = datetime.strptime(trip_request.start_date, "%Y-%m-%d")
            end = datetime.strptime(trip_request.end_date, "%Y-%m-%d")

        days = (end.date() - start.date()).days + 1
        itinerary = []
        for i in range(days):
            day_date = (start + timedelta(days=i)).date()
            # tailor activities by trip type
            ttype = (trip_request.trip_type or "general").lower()
            activities = []
            if "honeymoon" in ttype:
                activities.append(Activity(title="Relaxing couples brunch", time_of_day="morning", location="City Center Cafe", estimated_duration_minutes=90, cost_estimate=40.0))
                activities.append(Activity(title="Scenic walk and photoshoot", time_of_day="afternoon", location="Riverfront", estimated_duration_minutes=120, cost_estimate=0.0))
                activities.append(Activity(title="Romantic dinner", time_of_day="evening", location="Top-rated restaurant", estimated_duration_minutes=120, cost_estimate=120.0))
            elif "friends" in ttype:
                activities.append(Activity(title="Local street food crawl", time_of_day="morning", location="Market area", estimated_duration_minutes=120, cost_estimate=30.0))
                activities.append(Activity(title="Group activity (escape room or kayak)", time_of_day="afternoon", location="Activity hub", estimated_duration_minutes=180, cost_estimate=60.0))
                activities.append(Activity(title="Nightlife/bar hop", time_of_day="evening", location="Entertainment district", estimated_duration_minutes=240, cost_estimate=80.0))
            else:
                activities.append(Activity(title="City highlights tour", time_of_day="morning", location="Main attractions", estimated_duration_minutes=180, cost_estimate=25.0))
                activities.append(Activity(title="Museum or cultural visit", time_of_day="afternoon", location="Museum district", estimated_duration_minutes=120, cost_estimate=15.0))
                activities.append(Activity(title="Local dinner", time_of_day="evening", location="Recommended restaurant", estimated_duration_minutes=90, cost_estimate=35.0))

            itinerary.append(ItineraryDay(date=day_date, title=f"Day {i+1}", activities=activities))

        return {"itinerary": itinerary, "agent_events": ["planned"]}
