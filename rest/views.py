from django.http import HttpResponse
import json
import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from rest_framework.decorators import api_view
from rest_framework.response import Response


# If modifying these scopes, delete the file token.pkl.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def google_oauth():
    """Shows basic usage of the Google Calendar API and get the user token
    """
    creds = None
    # The file token.pkl stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pkl'):
        credentials_pickle = pickle.load(open("token.pkl", "rb"))
        creds = Credentials.from_authorized_user_file(credentials_pickle, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        pickle.dump(creds, open("token.pkl", "wb"))
    return creds

# get token credentials
@api_view(['GET'])
def GoogleCalendarInitView(request):
    if os.path.exists('token.pkl') == True:
        credentials_pickle = pickle.load(open("token.pkl", "rb"))
        return Response({credentials_pickle.to_json()})
    else:
        creds = google_oauth()
        credentials_pickle = pickle.load(open("token.pkl", "rb"))
        return Response({credentials_pickle.to_json()})

# get user calendar events
@api_view(['GET'])
def GoogleCalendarRedirectView(request):

    if os.path.exists('token.pkl') == True:
        credentials_pickle = pickle.load(open("token.pkl", "rb"))
        service = build("calendar", "v3", credentials=credentials_pickle)
        # Call the Sheets API
        calendar_list = service.calendarList().list().execute()
        calendar_id = calendar_list['items'][0]['id']
        events  = service.events().list(calendarId=calendar_id).execute()

        events_list_append = []
        if not events['items']:
            print('No data found.')
            return Response({"message": "No data found."})
        else:
            for events_list in events['items']:
                events_list_append.append(events_list)
        return Response({"events": events_list_append})
    else:
        return Response({"create token": token})

