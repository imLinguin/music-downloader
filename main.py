import argparse
import data_collect
import youtube
import os
import re

illegalChars = ["/", "\\", "|", "\'", "*", "?", "<", ">", ":"]


# Ensures that there are no illegal characters in song name
def make_save_name(name):
    output = name
    for char in illegalChars:
        output = output.replace(char, "_")
    return output


def attach_metadata(filename, artist, album, cover, name):
    os.system('ffmpeg -i Tmp/"{0}.mp3" -i {3} -map 0 -map 1:0 -y -hide_banner -codec copy '
              '-metadata "artist={1}" -metadata "album={2}" Out/"{4}.mp3"'.format(filename, artist,
                                                                                  album,
                                                                                  cover,
                                                                                  make_save_name(name)))
    os.remove("./Tmp/{0}.mp3".format(filename))


def main():
    parser = argparse.ArgumentParser(description='Download desired song with metadata. Please put names in quotes')
    parser.add_argument("--title", type=str, help="Title of the song we are looking for")
    parser.add_argument("--album", type=str, help="Title of the album")
    parser.add_argument("--playlist", type=str, help="Spotify playlist url")

    args = parser.parse_args()

    # Execute if title is provided
    if args.title:
        results = data_collect.get_spotify_title_data(args)
        data = results["tracks"]["items"][0]

        name = data["name"]
        album = data["album"]["name"]
        artists = data["album"]["artists"]
        cover = data["album"]["images"][0]["url"]

        print("{0} - {1}".format(name, artists[0]["name"]))
        print(cover)
        filename = youtube.download(("{1} {0}".format(name, artists[0]["name"])))
        attach_metadata(filename, artists[0]["name"], album, cover, name)

    # Else do same thing but with album
    elif args.album:
        results = data_collect.get_spotify_album_data(args)
        cover = results[0]
        data = results[1]
        album = results[2]

        for track in data["items"]:
            name = track['name']
            artists = track["artists"]
            print("{1} {0}".format(name, artists[0]["name"]))
            print(cover)
            filename = youtube.download(("{1} {0}".format(name, artists[0]["name"])))

            attach_metadata(filename, artists[0]["name"], album, cover, name)

    elif args.playlist:
        if not re.match("https://(open.spotify.com)/playlist/", args.playlist):
            print("Invalid playlist URL provided")
            return
        else:
            # Extract playlist ID from URL
            question_mark_pos = args.playlist.index("?")
            playlist_id = args.playlist[34:question_mark_pos]
            tracks = data_collect.get_spotify_playlist_tracks(playlist_id)

            for track in tracks["items"][:100]:
                name = track["track"]["name"]
                artists = track["track"]["artists"]
                album = track["track"]["album"]["name"]
                cover = track["track"]["album"]["images"][0]["url"]
                print("{0} - {1}".format(name, artists[0]["name"]))
                print(cover)
                filename = youtube.download(("{1} {0}".format(name, artists[0]["name"])))

                attach_metadata(filename, artists[0]["name"], album, cover, name)


if __name__ == '__main__':
    main()
