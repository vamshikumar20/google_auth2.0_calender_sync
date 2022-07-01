from django.http import HttpResponse
import json
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from rest_framework.decorators import api_view
from rest_framework.response import Response


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def google_oauth():
    """Shows basic usage of the Google Calendar API and get the user token
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


@api_view(['GET'])
def GoogleCalendarInitView(request):

    if os.path.exists('token.json') == True:
        with open('token.json', 'r') as token:
            token_private = json.load(token)
        return Response({"token": token_private})
    else:
        creds = google_oauth()
        with open('token.json', 'r') as token:
            token_private = json.load(token)
        return Response({"token": token_private})


@api_view(['GET'])
def GoogleCalendarRedirectView(request):

    credentials = google_oauth()
    service = build("calendar", "v3", credentials=credentials)
    # Call the Sheets API
    calendar_list = service.calendarList().list().execute()
    calendar_id = calendar_list['items'][0]['id']
    events  = service.events().list(calendarId=calendar_id).execute()

    events_list_append = []
    if not events ['items']:
        print('No data found.')
        return Response({"Error": "No data found."})
    else:
        for events_list in events['items']:
            events_list_append.append(events_list)
    return Response({"events": events_list_append})
