from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api.formatters import SRTFormatter
from urllib.parse import urlparse
import os
import subprocess


# Input
input_id = str(input("Enter the ID of the video you want to download: \n>> "))

# check for destination to save file
print("Enter the destination (leave blank for current directory)")
destination = str(input(">> ")) or "."


# Pytube to Download the video
# create Pytube instance from the youtube video id
yt = YouTube.from_id(input_id)
vid_title = yt.title
# extract only audio from the media stream
video = yt.streams.filter(only_audio=True).first()
# download the file
out_file = video.download(output_path=destination)
# save the file
base, ext = os.path.splitext(out_file)
new_file = base + ".mp3"
os.rename(out_file, new_file)


# extract transcript of the video
vid_id = input_id
languages = ["en-US", "en"]


def download_transcript(video_id, destination, language_list):
    transcripts = YouTubeTranscriptApi.list_transcripts(video_id)

    transcript = transcripts.find_manually_created_transcript(language_list)
    english_transcript = transcript.fetch()
    srt_formatter = SRTFormatter()
    wanted_subs = srt_formatter.format_transcript(english_transcript)
    print("Writing {} Subtitles ...".format("english"), end="")
    with open(destination + "/" + vid_title + "_subs.srt", "w") as f:
        f.write(wanted_subs)
    print("SRT File Generated")


download_transcript(vid_id, destination, languages)

# split video into segments based on srt timestamp
video_name = vid_title + ".mp3"
subtitle_name = vid_title + "_subs.srt"
subprocess.check_call(["./srt-split.sh", video_name, subtitle_name])
print("video split to segments based on srt timestamp")

