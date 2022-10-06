

import os.path
import requests

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1qm9W1j2s8HjLFMzDHv-YLILMjRdyw9HC0o7mby_UNu0'
SAMPLE_RANGE_NAME = 'Sheet1'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)


def add_data(data):
    try:
        print(SAMPLE_SPREADSHEET_ID)
        request = service.spreadsheets().values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                        range=SAMPLE_RANGE_NAME,valueInputOption='USER_ENTERED',
                                                        body={'values':data}).execute()
                                                        

    except HttpError as err:
        print(err)


def main():
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'keys2.json'
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    # The ID and range of a sample spreadsheet.
    service = build('sheets', 'v4', credentials=creds)
    try:
        request = service.spreadsheets().values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME,valueInputOption='USER_ENTERED',
                                    body={'values': [['FALSE','maybe'],['True']]}

        ).execute()
        request = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()