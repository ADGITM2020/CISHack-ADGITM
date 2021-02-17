from __future__ import print_function

import io
import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
# If modifying these scopes, delete the file token.pickle.
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Saraswati Enterprises Api'


def create_connections(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service


def uploadFile(filename, path, mimetype, folder_id, drive_service):
    file_metadata = {'name': filename, 'parents': [folder_id], 'title': filename}
    media = MediaFileUpload(path,
                            mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    return file.get('id')


def downloadFile(file_id, filepath, drive_service):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath, 'wb') as f:
        fh.seek(0)
        f.write(fh.read())


def createFolder(name, drive_service):
    folder_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
    }
    folder = drive_service.files().create(body=folder_metadata,
                                          fields='id,name').execute()
    return folder


def get_or_create_folder(size, folder_name, drive_service, mimeType="application/vnd.google-apps.folder"):
    results = drive_service.files().list(
        pageSize=size, fields="nextPageToken, files(id, name, kind, mimeType)",
        q=f"mimeType='{mimeType}' and name='{folder_name}'").execute()
    items = results.get('files', [])
    if not items:
        folder = createFolder(folder_name, drive_service)
        return folder
    else:
        return items[0]


def get_or_create_file(size, file_name, folder_id, path, drive_service, mimeType="application/pdf"):
    results = drive_service.files().list(
        pageSize=size, fields="nextPageToken, files(id, name, webViewLink, mimeType)",
        q=f"mimeType='{mimeType}' and name='{file_name}'").execute()
    items = results.get('files', [])
    if not items:
        file = uploadFile(file_name, path, 'application/pdf', folder_id, drive_service)
        file_link = drive_service.files().get(fileId=file,
                                              fields="id, name, webViewLink, mimeType").execute()
        if file_link:
            return file_link.get('webViewLink')
        else:
            return None
    else:
        return items[0].get('webViewLink')


def get_link(invoice_no, year, path):
    service = create_connections(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
    folder = get_or_create_folder(1, year, service)
    file_link = get_or_create_file(1, f"INV{year}-{invoice_no:04d}", folder.get("id"), path, service)
    return file_link