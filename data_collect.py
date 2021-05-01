import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="SPOTIFY_CLIENT_ID",
                                                           client_secret="SPOTIFY_CLIENT_SECRET"))


def get_spotify_title_data(args):
    results = sp.search(q=args.title, limit=1, type="track")
    return results


def get_spotify_album_data(args):
    results = sp.search(q=args.album, limit=1, type="album")
    cover = results["albums"]["items"][0]["images"][0]["url"]
    album = results["albums"]["items"][0]["name"]
    tracks = sp.album_tracks(results["albums"]["items"][0]["id"])
    return [cover, tracks, album]


def get_spotify_playlist_tracks(playlist_id):
    results = sp.playlist_items(playlist_id=playlist_id, limit=100)
    return results
