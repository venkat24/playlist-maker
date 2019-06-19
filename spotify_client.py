import spotipy
import spotipy.util as util

from config import *

class SpotifyPlaylistClient:
    def __init__(self):
        scope = 'playlist-modify-public'
        token = util.prompt_for_user_token(USERNAME, scope, CLIENT_ID, CLIENT_SECRET, REDIRECT_URL)

        if token:
            self.sp = spotipy.Spotify(auth=token)
            self.sp.trace = False
        else:
            print(f'Can\'t get token for {USERNAME}')
            return None

    def add_tracks_to_playlist(self, playlist_id, track_urls):
        return self.sp.user_playlist_add_tracks(USERNAME, playlist_id, track_urls)

    def replace_tracks_in_playlist(self, playlist_id, track_urls):
        return self.sp.user_playlist_replace_tracks(USERNAME, playlist_id, track_urls)

    def get_tracks_in_album(self, album_id):
        tracks = self.sp.album_tracks(album_id)
        return [track["id"] for track in tracks["items"]]
