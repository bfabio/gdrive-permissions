#!/usr/bin/env python

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token: pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    drives = []

    params = {
        'fields': 'nextPageToken, drives(id, name, restrictions)',
        'useDomainAdminAccess': True,
    }
    while True:
        results = service.drives().list(**params).execute()

        drives += results.get('drives', [])

        params['pageToken'] = results.get('nextPageToken', None)
        if params['pageToken'] is None:
            break

    print(f"Found {len(drives)} drives")
    for drive in drives:
        params = {
            'fileId': drive['id'],
            'fields': 'nextPageToken, permissions',
            'useDomainAdminAccess': True,
            'supportsAllDrives': True,
        }
        while True:
            perms_res = service.permissions().list(**params).execute()

            print(f"{drive['name']}: " +
                f"domainUsersOnly: {drive['restrictions']['domainUsersOnly']} " +
                f"driveMembersOnly: {drive['restrictions']['driveMembersOnly']}")
            for permission in perms_res.get('permissions', []):
                print(f"{drive['name']},{permission['emailAddress']},{permission['role']},{permission['type']}")

            params['pageToken'] = perms_res.get('nextPageToken', None)
            if params['pageToken'] is None:
                break

if __name__ == '__main__':
    main()
