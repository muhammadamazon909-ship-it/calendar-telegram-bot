import os
from datetime import datetime, timedelta
from ics import Calendar
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
ICS_URL = os.environ.get("ICS_URL")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def fetch_events():
    response = requests.get(ICS_URL)
    response.raise_for_status()
    c = Calendar(response.text)
    return list(c.events)

def format_event(event):
    start_time = event.begin.to('local').strftime("%H:%M")
    return f"🗓 {event.name}\n⏰ {start_time}\n"

def daily_summary(events):
    today = datetime.now().date()
    today_events = [e for e in events if e.begin.date() == today]
    if not today_events:
        send_message("📅 You have no events today!")
        return
    message = "🌞 Good morning! Here are your events for today:\n\n"
    for e in sorted(today_events, key=lambda x: x.begin):
        message += format_event(e)
    send_message(message)

def weekly_summary(events):
    now = datetime.now()
    week_later = now + timedelta(days=7)
    week_events = [e for e in events if now <= e.begin.datetime <= week_later]
    if not week_events:
        send_message("📅 No events in the next 7 days!")
        return
    message = "📆 Upcoming events for the next 7 days:\n\n"
    for e in sorted(week_events, key=lambda x: x.begin):
        message += format_event(e)
    send_message(message)

def main():
    events = fetch_events()
    daily_summary(events)   # Daily summary for today
    weekly_summary(events)  # Weekly summary for next 7 days

if __name__ == "__main__":
    main()
