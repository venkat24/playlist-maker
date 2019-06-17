import spotipy
import spotipy.util as util

from config import *

class SpotifyPlaylistClient:
    def __init__(self, playlist_id):
        scope = 'playlist-modify-public'
        token = util.prompt_for_user_token(USERNAME, scope, CLIENT_ID, CLIENT_SECRET, REDIRECT_URL)
        self.playlist_id = playlist_id

        if token:
            self.sp = spotipy.Spotify(auth=token)
            self.sp.trace = False
        else:
            print(f'Can\'t get token for {USERNAME}')
            return None

    def add_tracks_to_playlist(self, track_urls):
        return self.sp.user_playlist_replace_tracks(USERNAME, self.playlist_id, track_urls)
