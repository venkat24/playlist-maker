# What Are U Listening To

This is a quick script to upload all YouTube and Spotify links that you may be sharing with your friends into neat playlists. Simply save your chat that contains any Spotify or YouTube links (such as your WhatsApp group export). The script automatically parses all links, and uploads them to playlists of your choice.

## Usage

You will need Spotify API credentials and Google API credentials (with OAuth access to YouTube Data API v3)

1. Copy `config.py.example` to `config.py` and fill in the API information

2. `pip install -r requirements.txt` (preferably after creating a virtual env first)

3. `python playlist_maker.py ~/path/to/chats.txt`

Happy listening!
