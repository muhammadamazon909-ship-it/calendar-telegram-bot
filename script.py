import os
import requests
from datetime import datetime, timedelta
from ics import Calendar
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
ICS_URL = os.environ.get("ICS_URL")  # Your calendar .ics file URL

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    response = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })
    print(response.text)

def fetch_calendar_events():
    response = requests.get(ICS_URL)
    response.raise_for_status()
    c = Calendar(response.text)
    return list(c.events)

def get_todays_events(events):
    today = datetime.now().date()
    today_events = [e for e in events if e.begin.date() == today]
    return sorted(today_events, key=lambda x: x.begin)

def format_event(event):
    start_time = event.begin.to('local').strftime("%H:%M")
    return f"🗓 {event.name}\n⏰ {start_time}\n"

def main():
    events = fetch_calendar_events()
    todays_events = get_todays_events(events)
    
    if not todays_events:
        send_message("📅 You have no events today!")
        return

    message = "🌞 Good morning! Here are your events for today:\n\n"
    for event in todays_events:
        message += format_event(event)

    send_message(message)

if __name__ == "__main__":
    main()
