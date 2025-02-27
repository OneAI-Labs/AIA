from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
import datetime
from googleapiclient.discovery import build

# Define the required API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def authenticate_google_calendar():
    creds = None
    # Check if token.pickle exists (to store user session)
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If no valid credentials, prompt user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for future use
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return creds

def create_calendar_event(summary, start_time, end_time):
    """Creates a calendar event."""
    creds = authenticate_google_calendar()
    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": summary,
        "start": {"dateTime": start_time, "timeZone": "America/New_York"},
        "end": {"dateTime": end_time, "timeZone": "America/New_York"},
    }

    event = service.events().insert(calendarId="primary", body=event).execute()
    print(f"✅ Event created: {event.get('htmlLink')}")

# Example Usage
if __name__ == "__main__":
    create_calendar_event(
        summary="AI Test Event",
        start_time="2025-02-28T10:00:00",
        end_time="2025-02-28T11:00:00"
    )
