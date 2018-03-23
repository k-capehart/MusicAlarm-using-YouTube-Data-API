import webbrowser
import random
import os

from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools
from time import localtime, strftime, sleep, strptime
from threading import Thread

# The CLIENT_SECRETS_FILE contains client_id and client_secret
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope asks for permission for full read/write access to account
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
musicId = 'UC-9-kyTW8ZkZNDHQJ6FgpwQ'

class ClockUpdater(Thread):

  def __init__(self, clock_func):
    Thread.__init__(self)
    self.runnable = clock_func

  def run(self):
    self.runnable()

# End of Class

def cls():
  os.system('cls' if os.name == 'nt' else 'clear')

def clock():
  print(strftime("%I:%M %p", localtime()))
  sleep(.5)
  cls()
  clock()

def get_authenticated_service():
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=SCOPES)
  storage = Storage("oath2.json")
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    flags = tools.argparser.parse_args(args=[])
    credentials = tools.run_flow(flow, storage, flags)

  return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def get_playlist_id(service, **kwargs):
  list = service.playlists().list(**kwargs).execute()

  # Selects a random playlist
  length = len(list)
  index = random.randint(0, length - 1)
  playlistId = list['items'][index]['id']

  return playlistId


def get_video_id(service, **kwargs):
  playListItems = service.playlistItems().list(**kwargs).execute()

  length = len(playListItems)
  index = random.randint(0, length - 1)

  videoId = playListItems['items'][index]['contentDetails']['videoId']
  return videoId


if __name__ == '__main__':
  my_time = strptime(input("When do you want to wake up? (HH:MM AM/PM)  "), "%I:%M %p")

  # Multithreading
  thread = ClockUpdater(clock)
  thread.start()

  # Program pauses here until the time is reached
  while(strftime("%I:%M %p", localtime()) != strftime("%I:%M %p", my_time)):
    sleep(.5)

  # Ask for permission to use account
  service = get_authenticated_service()

  # Returns a list of all playlists for the Music Channel and then selects a random video
  playlistId = get_playlist_id(service, part='snippet, contentDetails', channelId=musicId)
  videoId = get_video_id(service, part='snippet, contentDetails', playlistId=playlistId)

  link = ("https://www.youtube.com/watch?v=%s" % str(videoId))
  webbrowser.open(link)

  # Join the threads
  thread.join()