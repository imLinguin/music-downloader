import youtube_dl
import sys

ytdl_opts = {
    "format": "bestaudio/best",
    "default_search": "ytsearch",
    "outtmpl": "Tmp/%(title)s.%(ext)s",
    "noprogress": True,
    "noplaylist": True,
    "quiet":True,
}

ytdl = youtube_dl.YoutubeDL(ytdl_opts)


def progress(data):
    if data.get("status") == "downloading":
        downloaded_bytes = data.get("downloaded_bytes")
        total_bytes = data.get("total_bytes")
        if downloaded_bytes and total_bytes:
            procentage = round((downloaded_bytes / total_bytes) * 100, 2)
            # Calculate minutes and create easly readable string
            eta = ""
            seconds = data.get("eta")
            if seconds:
                minutes = round(seconds / 60)
                seconds = seconds - 60 * minutes
                eta = "{0}:{1}".format(minutes, seconds)
            else:
                eta = "0:0"

            sys.stdout.write("\r{0}% ETA {1}".format(procentage, eta))

ytdl.add_progress_hook(progress)


def download(query):
    sys.stdout.write("\rDownloading")
    downloaded = ytdl.extract_info(query, download=True)
    if len(downloaded.get("entries")) > 0:
        downloaded = downloaded['entries'][0]
    filename = ytdl.prepare_filename(downloaded)
    #dot = filename.rindex(".")
    name = filename[4:]
    return [name, downloaded.get("id")]
