from config import *

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

class YoutubePlaylistClient:
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/youtube']
        API_SERVICE_NAME = 'youtube'
        API_VERSION = 'v3'

        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_console()

        self.client = build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

        # Cache to stored already fetched playlist members
        self.playlist_cache = {}
        # Get existing playlist list

    def add_video_to_playlist(self, playlist_id, video_id):
        playlist_items = self.get_all_playlist_items(playlist_id)
        playlist_video_ids = [item["snippet"]["resourceId"]["videoId"] for item in playlist_items]

        if video_id in playlist_video_ids:
            return False

        request = self.client.playlistItems().insert(
            part="snippet",
            body = {
                "snippet" : {
                    "playlistId" : playlist_id,
                    "position" : 0,
                    "resourceId" : {
                        "kind" : "youtube#video",
                        "videoId" : video_id
                    }
                }
            }
        )

        request.execute()
        return True

    def remove_video_from_playlist(self, playlist_id, video_id):
        request = self.client.playlistItems().delete(
            id=video_id
        )

        response = request.execute()
        return response

    def get_playlist_items(self, playlist_id, nextPageToken=None):
        params = {
            "part": "id, snippet",
            "maxResults": 50,
            "playlistId": playlist_id
        }

        if nextPageToken:
            params["pageToken"] = nextPageToken

        request = self.client.playlistItems().list(**params)

        response = request.execute()
        return response

    def get_all_playlist_items(self, playlist_id):
        if playlist_id in self.playlist_cache.keys():
            return self.playlist_cache[playlist_id]

        items = []
        response = self.get_playlist_items(playlist_id, None)
        items.extend(response["items"])
        while "nextPageToken" in response.keys():
            response = self.get_playlist_items(playlist_id, response["nextPageToken"])
            items.extend(response["items"])

        self.playlist_cache[playlist_id] = items

        return items
