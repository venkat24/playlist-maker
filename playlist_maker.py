import os
import re
import sys
import pprint

from utils import *
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
    spotify_client.replace_tracks_in_playlist(PLAYLIST_ID, spotify_track_urls)

    # Add album tracks to the separate album playlist
    all_album_tracks = []
    for url in spotify_album_urls:
        album_tracks = spotify_client.get_tracks_in_album(url)
        all_album_tracks.extend(album_tracks)

    print(f'Found {len(spotify_album_urls)} albums with {len(all_album_tracks)} tracks. Uploading..')

    # Spotify has an upload limit of 100 tracks per request, so upload in chunks
    for i, track_chunk in enumerate(chunks(all_album_tracks, 100)):
        # Replace all tracks on the first chunk, append them on subsequent chunks
        if i == 0:
            spotify_client.replace_tracks_in_playlist(ALBUM_PLAYLIST_ID, track_chunk)
        else:
            spotify_client.add_tracks_to_playlist(ALBUM_PLAYLIST_ID, track_chunk)

    print("Uploaded successfully to Spotify!")

def add_to_youtube(urls):
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
        try:
            youtube_client.add_video_to_playlist(url)
            counter += 1
            print(f'Uploaded video {counter} of {len(youtube_urls)}..')
        except Exception as e:
            print(f'Video {url} FAILED due to {e}. Continuing..')

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
