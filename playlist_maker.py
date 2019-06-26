import os
import re
import sys
import pprint

from config import *
from youtube_client import YoutubePlaylistClient
from spotify_client import SpotifyPlaylistClient

def add_to_spotify(urls):
    spotify_track_urls = []
    spotify_album_urls = []
    for url in urls:
        if "spotify" in url and "/track" in url:
            new_url = url.split("?")[0]
            spotify_track_urls.append(new_url)
        
        if "spotify" in url and "/album" in url:
            new_url = url.split("?")[0]
            spotify_album_urls.append(new_url)

    print(f'Found {len(spotify_track_urls)} Spotify track links. Uploading..')
    spotify_client = SpotifyPlaylistClient()

    # Add standard tracks to the main playlist
    spotify_client.add_tracks_to_playlist(PLAYLIST_ID, spotify_track_urls)

    # Add album tracks to the separate album playlist
    album_track_urls = []
    for url in spotify_album_urls:
        album_tracks = spotify_client.get_tracks_in_album(url)
        album_track_urls.extend(album_tracks)

    print(f'Found {len(spotify_album_urls)} albums with {len(album_track_urls)} tracks. Uploading..')

    spotify_client.add_tracks_to_playlist(ALBUM_PLAYLIST_ID, album_track_urls)

    print("Uploaded successfully to Spotify!")

def add_to_youtube(urls):
    youtube_urls = []
    for url in urls:
        if "youtube" in url and "watch" in url:
            new_url = url.split("?v=")[1].split("&")[0]
            youtube_urls.append(new_url)

        if "youtu.be" in url:
            new_url = url.split("youtu.be/")[1].split("?")[0]
            youtube_urls.append(new_url)

    youtube_client = YoutubePlaylistClient()
    print(f'Found {len(youtube_urls)} YouTube links. Uploading to playlist now..')

    counter = 0
    for url in youtube_urls:
        try:
            counter += 1
            added = youtube_client.add_video_to_playlist(YT_PLAYLIST_ID, url)
            if added:
                print(f'Video {counter} of {len(youtube_urls)} uploaded..')
            else:
                print(f'Video {counter} of {len(youtube_urls)} already exists, skipping..')
        except Exception as e:
            print(f'Video {counter} [{url}] FAILED due to {e}. Continuing..')

    print("Uploaded tracks successfully to YouTube!")

if __name__ == "__main__":
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

    add_to_spotify(urls)
    add_to_youtube(urls)

    print("My work is complete. Happy Listening!")
