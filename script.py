import os
import requests
from ics import Calendar

# Get secrets from GitHub
ICS_URL = os.environ.get("ICS_URL")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# Fetch calendar
response = requests.get(ICS_URL)
calendar = Calendar(response.text)

# Get next event
events = sorted(calendar.events)

if not events:
    message = "No upcoming events found."
else:
    event = list(events)[0]
    message = f"📅 Next Event:\n{event.name}\n🕒 {event.begin}"

# Send message to Telegram
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
data = {
    "chat_id": CHAT_ID,
    "text": message
}

requests.post(url, data=data)
