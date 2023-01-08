from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api.formatters import SRTFormatter
from urllib.parse import urlparse
import os
import subprocess

input_id = str(input("Enter the ID of the video you want to download: \n>> "))
yt = YouTube.from_id(input_id)
vid_title = yt.title

# print(yt.metadata)

# extract transcript of the video
vid_id = input_id
base_lang = "en-US"
wanted_lang = "en"


transcripts = YouTubeTranscriptApi.list_transcripts(vid_id)

transcript = transcripts.find_manually_created_transcript([base_lang])
english_transcript = transcript.fetch()


# extract only audio
video = yt.streams.filter(only_audio=True).first()

# check for destination to save file
print("Enter the destination (leave blank for current directory)")
destination = str(input(">> ")) or "."

# download the file
out_file = video.download(output_path=destination)

# save the file
base, ext = os.path.splitext(out_file)
new_file = base + ".mp3"
os.rename(out_file, new_file)

srt_formatter = SRTFormatter()
wanted_subs = srt_formatter.format_transcript(english_transcript)
print("Writing {} Subtitles ...".format(base_lang), end="")
with open(destination + "/" + vid_title + "_{}_subs.srt".format(base_lang), "w") as f:
    f.write(wanted_subs)
print("SRT File Generated")


# result of success
print(vid_title + " has been successfully downloaded.")

# split video into segments based on srt timestamp
arg1 = vid_title + ".mp3"
arg2 = vid_title + "_{}_subs.srt".format(base_lang)
subprocess.check_call(["./srt-split.sh", arg1, arg2])
print("video split to segments based on srt timestamp")
