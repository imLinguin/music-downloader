import youtube_dl

ytdl_opts = {
    "format": "bestaudio/best",
    "default_search": "ytsearch",
    "outtmpl": "Tmp/%(title)s.%(ext)s",
    "noprogress": True,
    "noplaylist": True,
    "postprocessors": [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}

ytdl = youtube_dl.YoutubeDL(ytdl_opts)


def download(query):
    downloaded = ytdl.extract_info(query, download=True)
    if downloaded["entries"]:
        downloaded = downloaded['entries'][0]
    filename = ytdl.prepare_filename(downloaded)
    dot = filename.rindex(".")
    name = filename[4:dot]
    print(name)
    return name
