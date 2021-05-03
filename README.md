# music-downloader
This is a simple python script that allows you to download music from YouTube and attach Spotify metadata to it.

## Installation
Script requires [ffmpeg](https://ffmpeg.org/) installed and added to your PATH.
```
git clone https://github.com/imLinguin/music-downloader.git
cd music-downloader
pip install -r requirements.txt
```
Rename `.env-sample` to `.env` and fill two variables. You can get them from Spotify's developer dashboard.

## Usage
Script takes one positional argument which could be a Spotify playlist or album URL, or just a song title in quotes.

Template: `python main.py ARG`