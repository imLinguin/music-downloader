import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="caf7251809ae492a93012c0ccd5fd0d0",
                                                           client_secret="f9032fdb6ddb44a7839ea481492de609"))


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
    return [cover, tracks, album]


def get_spotify_playlist_tracks(playlist_id):
    results = sp.playlist_items(playlist_id=playlist_id, limit=100)
    return results
