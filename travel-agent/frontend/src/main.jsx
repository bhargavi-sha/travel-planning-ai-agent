import { useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const API_URL = (import.meta.env.VITE_API_URL || "http://localhost:8000").replace(/\/$/, "");
const interests = ["Culture", "Food", "Nature", "Shopping", "Adventure", "Nightlife"];

const initialForm = {
  origin: "",
  destination: "",
  start_date: "",
  end_date: "",
  travelers: 1,
  trip_type: "general",
  interests: [],
  pace: "balanced",
  accommodation: "",
  currency: "USD",
  budget: 1000,
};

function App() {
  const [form, setForm] = useState(initialForm);
  const [trip, setTrip] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const update = (event) => setForm((current) => ({ ...current, [event.target.name]: event.target.value }));
  const toggleInterest = (interest) => setForm((current) => ({
    ...current,
    interests: current.interests.includes(interest)
      ? current.interests.filter((item) => item !== interest)
      : [...current.interests, interest],
  }));

  async function submit(event) {
    event.preventDefault();
    setError("");
    setTrip(null);
    if (form.end_date < form.start_date) {
      setError("Your end date must be on or after your start date.");
      return;
    }
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/trips`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...form, travelers: Number(form.travelers), budget: Number(form.budget) }),
      });
      const body = await response.json();
      if (!response.ok) throw new Error(typeof body.detail === "string" ? body.detail : "Unable to create your trip.");
      setTrip(body);
    } catch (requestError) {
      setError(requestError.message || "Unable to reach the planning service.");
    } finally {
      setLoading(false);
    }
  }

  return <main className="page">
    <section className="hero"><p className="eyebrow">AI-assisted travel planning</p><h1>Build a trip worth remembering.</h1><p>Choose your style and receive a practical day-by-day itinerary in seconds.</p></section>
    <section className="panel">
      <form onSubmit={submit}>
        <div className="grid two">
          <label>From<input required name="origin" value={form.origin} onChange={update} placeholder="Berlin" /></label>
          <label>Destination<input required name="destination" value={form.destination} onChange={update} placeholder="Lisbon" /></label>
          <label>Start date<input required type="date" name="start_date" value={form.start_date} onChange={update} /></label>
          <label>End date<input required type="date" name="end_date" value={form.end_date} onChange={update} /></label>
          <label>Travelers<input min="1" required type="number" name="travelers" value={form.travelers} onChange={update} /></label>
          <label>Trip type<select name="trip_type" value={form.trip_type} onChange={update}>{["general", "friends", "honeymoon", "family", "solo", "business"].map((item) => <option key={item}>{item}</option>)}</select></label>
          <label>Travel pace<select name="pace" value={form.pace} onChange={update}><option value="relaxed">Relaxed</option><option value="balanced">Balanced</option><option value="packed">Packed</option></select></label>
          <label>Accommodation<select name="accommodation" value={form.accommodation} onChange={update}><option value="">No preference</option><option>Hotel</option><option>Boutique hotel</option><option>Apartment</option><option>Hostel</option></select></label>
          <label>Currency<select name="currency" value={form.currency} onChange={update}>{["USD", "EUR", "GBP"].map((item) => <option key={item}>{item}</option>)}</select></label>
          <label>Total budget<input min="0" required type="number" name="budget" value={form.budget} onChange={update} /></label>
        </div>
        <fieldset><legend>What interests you?</legend><div className="chips">{interests.map((interest) => <button type="button" className={form.interests.includes(interest.toLowerCase()) ? "chip selected" : "chip"} onClick={() => toggleInterest(interest.toLowerCase())} key={interest}>{interest}</button>)}</div></fieldset>
        <button className="primary" disabled={loading}>{loading ? "Planning your trip…" : "Plan my trip"}</button>
      </form>
      {error && <p className="error" role="alert">{error}</p>}
    </section>
    {trip && <Itinerary trip={trip} />}
  </main>;
}

function Itinerary({ trip }) {
  const { request, itinerary = [] } = trip;
  const total = itinerary.flatMap((day) => day.activities).reduce((sum, activity) => sum + Number(activity.cost_estimate || 0), 0);
  const download = () => {
    const lines = [`${request.destination} itinerary`, `${request.start_date} to ${request.end_date}`, ""];
    itinerary.forEach((day) => { lines.push(`${day.date} — ${day.title}`); day.activities.forEach((activity) => lines.push(`- ${activity.time_of_day}: ${activity.title} (${request.currency} ${activity.cost_estimate || 0})`)); });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(new Blob([lines.join("\n")], { type: "text/plain" }));
    link.download = "travel-itinerary.txt";
    link.click();
    URL.revokeObjectURL(link.href);
  };
  return <section className="itinerary"><div className="itinerary-heading"><div><p className="eyebrow">Your itinerary</p><h2>{request.destination}</h2><p>{request.start_date} to {request.end_date} · {request.travelers} traveler(s) · {request.pace} pace</p></div><button className="secondary" onClick={download}>Download itinerary</button></div><div className="metrics"><div><span>Days</span><strong>{itinerary.length}</strong></div><div><span>Activity estimate</span><strong>{request.currency} {total.toFixed(2)}</strong></div><div><span>Budget remaining</span><strong>{request.currency} {(request.budget - total).toFixed(2)}</strong></div></div>{request.budget - total < 0 && <p className="error">Planned activity estimates exceed your budget.</p>}<div className="days">{itinerary.map((day) => <article className="day" key={day.date}><h3>{day.title} <small>{day.date}</small></h3>{day.description && <p>{day.description}</p>}{day.activities.map((activity) => <div className="activity" key={`${day.date}-${activity.title}`}><div><span className="tag">{activity.category || "Activity"}</span><h4>{activity.title}</h4><p>{activity.time_of_day} · {activity.location} · {activity.estimated_duration_minutes} min</p>{activity.description && <p>{activity.description}</p>}{activity.tip && <p className="tip">Tip: {activity.tip}</p>}</div><strong>{request.currency} {activity.cost_estimate || 0}</strong></div>)}</article>)}</div></section>;
}

createRoot(document.getElementById("root")).render(<App />);
