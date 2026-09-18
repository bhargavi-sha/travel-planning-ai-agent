from typing import List, Dict, Any
from datetime import datetime


class DemoProvider:
    """Deterministic demo provider for search/place data."""

    def search_places(self, query: str) -> List[Dict[str, Any]]:
        now = datetime.utcnow().isoformat()
        return [
            {
                "id": "demo-museum-1",
                "name": "Demo Museum",
                "category": "museum",
                "location": {"lat": 48.8566, "lng": 2.3522},
                "source": {"title": "Demo data", "url": "", "retrieved_at": now},
            }
        ]

    def get_place_details(self, place_id: str) -> Dict[str, Any]:
        return {"id": place_id, "description": "A demo place."}
