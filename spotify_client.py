import spotipy
import spotipy.util as util

from utils import *
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
        # Spotify has a max upload limit of 100 songs per request, so we chunk them up
        for i, track_chunk in enumerate(chunks(track_urls, 100)):
            # Replace all tracks on the first chunk, append them on subsequent chunks
            if i == 0:
                self.replace_track_chunk_in_playlist(playlist_id, track_chunk)
            else:
                self.add_track_chunk_to_playlist(playlist_id, track_chunk)

    def add_track_chunk_to_playlist(self, playlist_id, track_urls):
        return self.sp.user_playlist_add_tracks(USERNAME, playlist_id, track_urls)

    def replace_track_chunk_in_playlist(self, playlist_id, track_urls):
        return self.sp.user_playlist_replace_tracks(USERNAME, playlist_id, track_urls)

    def get_tracks_in_album(self, album_id):
        tracks = self.sp.album_tracks(album_id)
        return [track["id"] for track in tracks["items"]]
