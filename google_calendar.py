from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to service account credentials JSON
CREDENTIALS_FILE = "credentials.json"  # Updated from firestore_credentials.json

# Authenticate and initialize the Google Calendar API
def get_calendar_service():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=["https://www.googleapis.com/auth/calendar"]
    )
    service = build("calendar", "v3", credentials=creds)
    return service

# Function to create a calendar event
def create_calendar_event(summary, start_time, end_time):
    """Creates a Google Calendar event."""
    service = get_calendar_service()

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
