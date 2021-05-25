import argparse
import data_collect
import youtube
import os
import sys
import re

illegal_chars = ["/", "\\", "|", "*", "?", "<", ">", ":"]
chars_to_escape = ["$", "&", "#", "'", " ", "(", ")"]

# Ensures that there are no illegal characters in song name
def make_save_name(name):
    output = name
    for char in illegal_chars:
        output = output.replace(char, "_")
    output = escape_chars(output)
    return output

# Escapes sh specific characters
def escape_chars(name):
    if sys.platform != "win32":
        for char in chars_to_escape:
            name = name.replace(char, "\{0}".format(char))
    return name


def classify_query(query):
    if not query:
        return None
    
    if re.search("spotify.com[\/:]playlist[\/:](.+)[\s?]",query):
        return "playlist"
    elif re.search("spotify.com[\/:]album[\/:](.+)[\s?]",query):
        return "album"
    else:
        return "custom"


def attach_metadata(filename, artist, album, cover, name):
    sys.stdout.write("\rAdding metadata...")
    os.system('ffmpeg -i Tmp/{0}.mp3 -i {3} -map 0 -map 1:0 -y -loglevel error -hide_banner -codec copy '
              '-metadata "artist={1}" -metadata "album={2}" Out/{4}.mp3'.format(escape_chars(filename),
                                                                                  artist,
                                                                                  album,
                                                                                  cover,
                                                                                  make_save_name(name)))
    print("✅")
    #os.remove("./Tmp/{0}.mp3".format(filename))


def main():
    parser = argparse.ArgumentParser(description='Download desired song with metadata. Please put values in quotes')
    parser.add_argument("query", type=str, help="Title or url of the song, url of playlist, url of album")

    args = parser.parse_args()

    classified = classify_query(args.query)
    # Check if Out folder exists
    if not os.path.isdir("./Out"):
        os.makedirs("./Out")
        print("Creating Output directory in {0}".format(os.path.join(os.getcwd(),"Out")))

    # Execute if title is provided
    if classified == "custom":
        results = data_collect.get_spotify_title_data(args.query)
        data = results["tracks"]["items"][0]

        name = data["name"]
        album = data["album"]["name"]
        artists = data["album"]["artists"]
        cover = data["album"]["images"][0]["url"]

        print("{0} - {1}".format(name, artists[0]["name"]))
        [filename, videoid] = youtube.download(("{1} {0}".format(name, artists[0]["name"])))
        attach_metadata(filename, artists[0]["name"], album, cover, name)

    # Else do same thing but with album
    elif classified == "album":
        results = data_collect.get_spotify_album_data(args.query)
        cover = results[0]
        data = results[1]
        album = results[2]

        for track in data["items"]:
            name = track['name']
            artists = track["artists"]
            print("\r{1} {0}".format(name, artists[0]["name"]))
            [filename, videoid] = youtube.download(("{1} {0}".format(name, artists[0]["name"])))

            attach_metadata(filename, artists[0]["name"], album, cover, name)

    elif classified == "playlist":        
        # Extract playlist ID from URL
        question_mark_pos = args.query.index("?")
        playlist_id = args.query[34:question_mark_pos]
        tracks = data_collect.get_spotify_playlist_tracks(playlist_id)

        for track in tracks["items"][:100]:
            name = track["track"]["name"]
            artists = track["track"]["artists"]
            album = track["track"]["album"]["name"]
            cover = track["track"]["album"]["images"][0]["url"]
            print("{0} - {1}".format(name, artists[0]["name"]))
            [filename, videoid] = youtube.download(("{1} {0}".format(name, artists[0]["name"])))

            attach_metadata(filename, artists[0]["name"], album, cover, name)
    print("Done")

if __name__ == '__main__':
    main()
