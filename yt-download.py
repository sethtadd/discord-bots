import yt_dlp
import json

url = "https://youtu.be/caCNxVgirB0"

ydl_opts = {
    "outtmpl": "music/%(title)s.%(ext)s",
    "noplaylist": True,
    }

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=True)
    info = ydl.sanitize_info(info)  # make info json-serializable

with open(f"info/{info['title']}.json", "w") as file:
    json.dump(info, file)
