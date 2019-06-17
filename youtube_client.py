from config import *

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

class YoutubePlaylistClient:
    def __init__(self, playlist_id):
        SCOPES = ['https://www.googleapis.com/auth/youtube']
        API_SERVICE_NAME = 'youtube'
        API_VERSION = 'v3'

        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_console()

        self.client = build(API_SERVICE_NAME, API_VERSION, credentials = credentials)
        self.playlist_id = playlist_id

        # Get existing playlist list

    def add_video_to_playlist(self, video_id):
        request = self.client.playlistItems().insert(
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
        return response

    def remove_video_from_playlist(self, video_id):
        request = self.client.playlistItems().delete(
            id=video_id
        )

        response = request.execute()
        return response

    def get_playlist_items(self, nextPageToken=None):
        params = {
            "part": "id",
            "maxResults": 50,
            "playlistId": self.playlist_id
        }

        if nextPageToken:
            params["pageToken"] = nextPageToken

        request = self.client.playlistItems().list(**params)

        response = request.execute()
        return response

    def get_all_playlist_items(self):
        items = []
        response = self.get_playlist_items(None)
        items.extend(response["items"])
        while "nextPageToken" in response.keys():
            response = self.get_playlist_items(response["nextPageToken"])
            items.extend(response["items"])

        return [item["id"] for item in items]
