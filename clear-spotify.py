import re
import sys

import json
import spotipy
import spotipy.util as util

from config import *

scope = 'playlist-modify-public'
token = util.prompt_for_user_token(USERNAME, scope, CLIENT_ID, CLIENT_SECRET, REDIRECT_URL)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.user_playlist_tracks(USERNAME, PLAYLIST_ID, fields="items(track(id))")
    track_ids = []

    for item in results["items"]:
        track_ids.append(item["track"]["id"])

    sp.user_playlist_remove_all_occurrences_of_tracks(USERNAME, PLAYLIST_ID, track_ids)

    print("Removed..")
else:
    print("Can't get token for "+ USERNAME)
