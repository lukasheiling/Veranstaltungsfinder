import requests
from datetime import datetime

def fetch_events(location, api_key):
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": api_key,
        "locale": "*",
        "city": location,
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return []  # Leere Liste oder Fehlerbehandlung
    data = response.json()
    events = []
    if "_embedded" in data:
        for event in data["_embedded"]["events"]:
            events.append({
                "name": event["name"],
                "date": datetime.strptime(event["dates"]["start"]["dateTime"], "%Y-%m-%dT%H:%M:%SZ"),
                "info": event.get("info", "Keine Informationen verfügbar."),
            })
    return events
