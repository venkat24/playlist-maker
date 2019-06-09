import os
import re
import sys
import pprint

import spotipy
import spotipy.util as util

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

from config import *

if len(sys.argv) > 1:
    track_id_file = sys.argv[1]
else:
    print("Usage: {} chat.txt".format((sys.argv[0])))
    sys.exit()

f = open(track_id_file, 'r')
s = f.read()

urls = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+', s)
spotify_urls = []
for url in urls:
    if "spotify" in url and "track" in url:
        new_url = url.split("?")[0]
        spotify_urls.append(new_url)

print("Found " + str(len(spotify_urls)) + " Spotify links. Uploading to playlist now..")

scope = 'playlist-modify-public'
token = util.prompt_for_user_token(USERNAME, scope, CLIENT_ID, CLIENT_SECRET, REDIRECT_URL)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.user_playlist_add_tracks(USERNAME, PLAYLIST_ID, spotify_urls)
    print(results)
else:
    print("Can't get token for "+ USERNAME)

print("Uploaded successfully to Spotify..")

# YouTube
youtube_urls = []
for url in urls:
    if "youtube" in url and "watch" in url:
        new_url = url.split("?v=")[1]
        youtube_urls.append(new_url)

print("Found " + str(len(youtube_urls)) + " YouTube links. Uploading to playlist now..")

SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
credentials = flow.run_console()
youtube = build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def add_video_to_playlist(youtube, video_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body = {
            "snippet" : {
                "playlistId" : YT_PLAYLIST_ID,
                "position" : 0,
                "resourceId" : {
                    "kind" : "youtube#video",
                    "videoId" : video_id
                }
            }
        }
    )

    response = request.execute()

for url in youtube_urls:
    add_video_to_playlist(youtube, url)

print ("Uploaded successfully to YouTube..")
print("My work is complete! Happy Listening!")
