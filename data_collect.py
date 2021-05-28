import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                                                           client_secret=os.getenv("SPOTIFY_SECRET")))


def get_spotify_title_data(query):
    results = sp.search(q=query, limit=1, type="track")
    return results


def get_spotify_album_data(args):
    question_mark_pos = args.index("?")
    album_id = args[31:question_mark_pos]

    album_data = sp.album(album_id)
    tracks = sp.album_tracks(album_id, limit=50)
    cover = album_data["images"][0]["url"]
    album = album_data["name"]
    year = album_data["release_date"]
    return [cover, tracks, album, year]


def get_spotify_playlist_tracks(playlist_id):
    results = sp.playlist_items(playlist_id=playlist_id, limit=100)
    return results
