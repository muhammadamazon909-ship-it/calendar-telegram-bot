import requests
import datetime
from ics import Calendar
import os

ICS_URL = os.environ['https://outlook.office365.com/owa/calendar/b1d8e10321234c0099743ee75eaaf2a6@ulaval.ca/567e88c0dd24451f9a648230fc845e8b14931969559727039684/calendar.ics']
BOT_TOKEN = os.environ['8548811509:AAEpWt0jmSJ0CyIy4E0dLLPwjVtwT8-Y42c']
CHAT_ID = os.environ['8548811509']

def get_events():
    c = Calendar(requests.get(ICS_URL).text)
    today = datetime.date.today()
    events_today = []

    for e in c.events:
        if e.begin.date() == today:
            time = e.begin.strftime('%H:%M')
            events_today.append(f"• {e.name} at {time}")

    return events_today

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

events = get_events()

if events:
    msg = "📅 Your tasks today:\n\n" + "\n".join(events)
else:
    msg = "✅ No tasks today!"

send_message(msg)