import webbrowser
import random

from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=SCOPES)
  storage = Storage("oath2.json")
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    flags = tools.argparser.parse_args(args=[])
    credentials = tools.run_flow(flow, storage, flags)
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def get_playlist_list(service, **kwargs):
  list = service.playlists().list(**kwargs).execute()
  return list

def get_video_id(service, **kwargs):
  video = service.playlistItems().list(**kwargs).execute()
  videoId = video['items'][0]['id']
  return videoId

if __name__ == '__main__':
  service = get_authenticated_service()

  # Returns a list of all playlists for the Music Channel
  musicId = 'UC-9-kyTW8ZkZNDHQJ6FgpwQ'
  list = get_playlist_list(service, part = 'snippet, contentDetails', channelId = musicId)

  # Selects a random playlist
  length = len(list)
  index = random.randint(0, length)
  playlistId = list['items'][index]['id']

  videoId = get_video_id(service, part = 'snippet, contentDetails', playlistId = playlistId)
  webbrowser.open('https://www.youtube.com/watch?v=%s' % videoId)