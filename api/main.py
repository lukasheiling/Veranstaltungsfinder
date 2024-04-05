import requests
from datetime import datetime

def fetch_events(location):
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": "DEIN_API_SCHLÜSSEL",
        "locale": "*",
        "city": location,
    }
    response = requests.get(url, params=params)
    data = response.json()
    events = []
    for event in data["_embedded"]["events"]:
        events.append({
            "name": event["name"],
            "date": datetime.strptime(event["dates"]["start"]["dateTime"], "%Y-%m-%dT%H:%M:%SZ"),
            "info": event.get("info", "Keine Informationen verfügbar."),
        })
    return events
