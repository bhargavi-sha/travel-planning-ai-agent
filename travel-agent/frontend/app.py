import os
import streamlit as st
import requests
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


st.set_page_config(page_title="Travel Agent", layout="wide")


class TripForm(BaseModel):
    origin: str
    destination: str
    start_date: str
    end_date: str
    travelers: int
    currency: str
    budget: float


def main():
    st.title("Agentic Travel Planner")
    with st.form("trip_form"):
        origin = st.text_input("From")
        destination = st.text_input("Destination")
        start = st.date_input("Start date")
        end = st.date_input("End date")
        travelers = st.number_input("Travelers", min_value=1, value=1)
        trip_type = st.selectbox("Trip type", ["General", "Friends", "Honeymoon", "Family", "Solo", "Business"], index=0)
        interests = st.multiselect("Interests", ["Culture", "Food", "Nature", "Shopping", "Adventure", "Nightlife"])
        pace = st.select_slider("Travel pace", options=["Relaxed", "Balanced", "Packed"], value="Balanced")
        accommodation = st.selectbox("Accommodation preference", ["No preference", "Hotel", "Boutique hotel", "Apartment", "Hostel"])
        currency = st.selectbox("Currency", ["USD", "EUR", "GBP"])
        budget = st.number_input("Total budget", min_value=0.0, value=1000.0)
        submitted = st.form_submit_button("Plan My Trip")

    if submitted:
        payload = {
            "origin": origin,
            "destination": destination,
            "start_date": str(start),
            "end_date": str(end),
            "travelers": travelers,
            "trip_type": trip_type.lower(),
            "interests": [interest.lower() for interest in interests],
            "pace": pace.lower(),
            "accommodation": None if accommodation == "No preference" else accommodation,
            "currency": currency,
            "budget": budget,
        }
        backend_url = os.environ.get("BACKEND_URL", "http://localhost:8000").rstrip("/")
        api_url = f"{backend_url}/api/trips"
        try:
            r = requests.post(api_url, json=payload, timeout=10)
            r.raise_for_status()
            data = r.json()
            st.success(f"Trip created (id={data.get('id')}).")
            # Render a human-friendly itinerary
            def render_itinerary(trip: dict):
                req = trip.get("request", {})
                st.header(f"Itinerary — {req.get('destination')}")
                st.markdown(f"**Dates:** {req.get('start_date')} → {req.get('end_date')}  \n**Travelers:** {req.get('travelers')}  \n**Trip type:** {req.get('trip_type', 'general').title()}")

                # Short descriptive summary
                days = trip.get("itinerary") or []
                total_est = 0.0
                for d in days:
                    for a in d.get("activities", []):
                        cost = a.get("cost_estimate") or 0.0
                        try:
                            total_est += float(cost)
                        except Exception:
                            pass

                st.markdown(f"**Overview:** This {req.get('trip_type', 'general')} trip to {req.get('destination')} includes {len(days)} day(s) of curated activities tailored to your preferences. Estimated activity costs: {req.get('currency','USD')} {total_est:.2f}. These are estimates and may vary.")
                budget = req.get("budget") or 0
                remaining = budget - total_est
                metric_cols = st.columns(3)
                metric_cols[0].metric("Days", len(days))
                metric_cols[1].metric("Activity estimate", f"{req.get('currency', 'USD')} {total_est:.2f}")
                metric_cols[2].metric("Budget remaining", f"{req.get('currency', 'USD')} {remaining:.2f}")
                if remaining < 0:
                    st.warning("Planned activity estimates exceed your total budget. Consider a relaxed pace or fewer paid activities.")

                for day in days:
                    with st.expander(f"{day.get('date')} — {day.get('title')}"):
                        for act in day.get('activities', []):
                            st.subheader(act.get('title'))
                            cols = st.columns([3,1,1])
                            cols[0].markdown(f"**Location:** {act.get('location') or '—'}\n\n**When:** {act.get('time_of_day') or '—'}\n\n**Duration:** {act.get('estimated_duration_minutes') or '—'} minutes")
                            cols[1].metric("Est. Cost", f"{req.get('currency','USD')} {act.get('cost_estimate') or 0.0}")
                            cols[2].button(f"Remove", key=f"remove-{day.get('date')}-{act.get('title')}")

                st.markdown("---")
                itinerary_text = [
                    f"{req.get('destination')} itinerary",
                    f"{req.get('start_date')} to {req.get('end_date')}",
                    "",
                ]
                for day in days:
                    itinerary_text.append(f"{day.get('date')} - {day.get('title')}")
                    itinerary_text.extend(
                        f"- {act.get('time_of_day')}: {act.get('title')} ({req.get('currency', 'USD')} {act.get('cost_estimate') or 0})"
                        for act in day.get("activities", [])
                    )
                st.download_button(
                    "Download itinerary",
                    "\n".join(itinerary_text),
                    file_name="travel-itinerary.txt",
                    mime="text/plain",
                )

            render_itinerary(data)
        except requests.exceptions.RequestException as e:
            # If name resolution failed for a Docker-style hostname, try localhost fallback once
            fallback_base = "http://localhost:8000"
            if api_url.startswith("http://localhost"):
                st.error(f"Failed to create trip: {e}")
            else:
                try:
                    fallback = f"{fallback_base}/api/trips"
                    r2 = requests.post(fallback, json=payload, timeout=10)
                    r2.raise_for_status()
                    data = r2.json()
                    st.warning(f"Backend host unreachable; fell back to {fallback_base}.")
                    st.success(f"Trip created (id={data.get('id')}).")
                    st.json(data)
                except Exception as e2:
                    st.error(f"Failed to create trip: {e}; fallback also failed: {e2}")
        except Exception as e:
            st.error(f"Failed to create trip: {e}")


if __name__ == "__main__":
    main()
