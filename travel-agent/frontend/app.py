import streamlit as st
import requests
from pydantic import BaseModel


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
            "currency": currency,
            "budget": budget,
        }
        try:
            r = requests.post("http://backend:8000/api/trips", json=payload, timeout=10)
            st.success("Trip created. Open the itinerary page soon.")
        except Exception as e:
            st.error(f"Failed to create trip: {e}")


if __name__ == "__main__":
    main()
