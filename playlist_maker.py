import os
import re
import sys
import pprint

from config import *
from youtube_client import YoutubePlaylistClient
from spotify_client import SpotifyPlaylistClient

# Open up the chats file
if len(sys.argv) > 1:
    chats_file_name = sys.argv[1]
else:
    print(f'Usage: {sys.argv[0]} chats.txt')
    sys.exit()

chats_file = open(chats_file_name, 'r')
content = chats_file.read()

# Magic regex that extracts all URLs from the string
urls = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+', content)

# Spotify
spotify_urls = []
for url in urls:
    if "spotify" in url and "track" in url:
        new_url = url.split("?")[0]
        spotify_urls.append(new_url)

print(f'Found {len(spotify_urls)} Spotify links. Uploading to playlist now..')

spotify_client = SpotifyPlaylistClient(PLAYLIST_ID)
spotify_client.add_tracks_to_playlist(spotify_urls)

print("Uploaded successfully to Spotify!")

# YouTube
youtube_urls = []
for url in urls:
    if "youtube" in url and "watch" in url:
        new_url = url.split("?v=")[1]
        youtube_urls.append(new_url)

youtube_client = YoutubePlaylistClient(YT_PLAYLIST_ID)

print("Clearing existing playlist..")
video_ids = youtube_client.get_all_playlist_items()
for video in video_ids:
    youtube_client.remove_video_from_playlist(video)
print("Cleared existing playlist")

print(f'Found {len(youtube_urls)} YouTube links. Uploading to playlist now..')

counter = 0
for url in youtube_urls:
    youtube_client.add_video_to_playlist(url)
    counter += 1
    print(f'Uploaded video {counter} of {len(youtube_urls)}..')

print("Uploaded successfully to YouTube!")
print("My work is complete. Happy Listening!")
