from ..ai.provider import get_provider
from datetime import datetime, timedelta
import json
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
        prompted_itinerary = await self._plan_with_prompt(trip_request, start, days)
        if prompted_itinerary:
            return {"itinerary": prompted_itinerary, "agent_events": ["planned_with_llm"]}

        itinerary = []
        interests = {interest.lower() for interest in trip_request.interests}
        pace = (trip_request.pace or "balanced").lower()
        activity_limit = {"relaxed": 2, "balanced": 3, "packed": 4}.get(pace, 3)
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

            if "nature" in interests:
                activities.append(Activity(title="Park or waterfront escape", time_of_day="late afternoon", location="Local green space", estimated_duration_minutes=75, cost_estimate=0.0, category="Nature", tip="Bring water and comfortable shoes."))
            elif "shopping" in interests:
                activities.append(Activity(title="Independent shops and local crafts", time_of_day="late afternoon", location="Shopping quarter", estimated_duration_minutes=90, cost_estimate=0.0, category="Shopping", tip="Leave room in your luggage for souvenirs."))
            elif "food" in interests:
                activities.append(Activity(title="Regional tasting stop", time_of_day="late afternoon", location="Neighborhood food hall", estimated_duration_minutes=60, cost_estimate=20.0, category="Food", tip="Share dishes to try more local flavors."))

            selected_activities = activities[:activity_limit]
            for activity in selected_activities:
                activity.category = activity.category or "Experience"
                activity.description = activity.description or f"A hand-picked {activity.category.lower()} experience that fits this day's route and {pace} travel pace."
                activity.tip = activity.tip or "Confirm hours and reservations before setting out."
            itinerary.append(ItineraryDay(
                date=day_date,
                title=f"Day {i+1} - {pace.title()} pace",
                description=f"A {pace} day that balances {', '.join(sorted(interests)) or 'local highlights'} with time to explore at your own pace.",
                activities=selected_activities,
            ))

        return {"itinerary": itinerary, "agent_events": ["planned"]}

    async def _plan_with_prompt(self, request, start, days):
        """Ask the configured LLM for a schema-shaped itinerary; return None on any invalid response."""
        dates = [(start + timedelta(days=index)).date().isoformat() for index in range(days)]
        prompt = self._build_planning_prompt(request, dates)
        try:
            response = await self.llm.call(prompt, temperature=0.65)
            raw_days = response.get("structured", {}).get("itinerary", [])
            if not isinstance(raw_days, list) or len(raw_days) != days:
                return None
            itinerary = [ItineraryDay(**day) for day in raw_days]
            if any(day.date.isoformat() != expected for day, expected in zip(itinerary, dates)):
                return None
            return itinerary
        except Exception:
            # The app remains useful if a key is missing, the provider is unavailable, or JSON is malformed.
            return None

    @staticmethod
    def _build_planning_prompt(request, dates):
        preferences = {
            "origin": request.origin,
            "destination": request.destination,
            "travelers": request.travelers,
            "trip_type": request.trip_type,
            "interests": request.interests,
            "pace": request.pace,
            "accommodation": request.accommodation or "no preference",
            "total_budget": request.budget,
            "currency": request.currency,
            "dates": dates,
        }
        return f"""Create a thoughtful, realistic travel itinerary using the trip brief below.

Trip brief:
{json.dumps(preferences, indent=2)}

Planning requirements:
- Produce exactly one day for each listed date, in the same order.
- Respect the requested pace: relaxed=2 activities, balanced=3, packed=4 maximum activities per day.
- Keep paid activity estimates plausible and make the full plan mindful of the total budget. Costs are for the whole travelling party unless stated otherwise.
- Use specific neighborhoods, landmarks, or venue types when confident; never invent booking confirmations, opening hours, or real-time availability.
- Arrange each day geographically and chronologically. Include meal opportunities where appropriate.
- Make every activity description vivid and useful (one or two sentences), and give a concise practical tip.

Return ONLY this JSON object, with no Markdown or commentary:
{{
  "itinerary": [
    {{
      "date": "YYYY-MM-DD",
      "title": "Short thematic day title",
      "description": "One sentence explaining the flow of the day.",
      "activities": [
        {{
          "title": "Activity name",
          "time_of_day": "morning|afternoon|evening",
          "location": "Specific area or venue type",
          "estimated_duration_minutes": 90,
          "cost_estimate": 25.0,
          "category": "Food|Culture|Nature|Sightseeing|Shopping|Adventure|Nightlife",
          "description": "One or two descriptive, useful sentences.",
          "tip": "A concise practical tip."
        }}
      ]
    }}
  ]
}}"""
