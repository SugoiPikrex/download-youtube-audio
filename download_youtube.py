from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api.formatters import SRTFormatter
from urllib.parse import urlparse
import os
import subprocess
import pysrt
import csv


# Input
input_id = str(input("Enter the ID of the video you want to download: \n>> "))

# check for destination to save file
print("Enter the destination (leave blank for current directory)")
destination = str(input(">> ")) or "."


# Pytube to Download the video
# create Pytube instance from the youtube video id
yt = YouTube.from_id(input_id)
vid_title = str(yt.title)

#cleanup vid title from strange characters
vid_title = ''.join(e for e in vid_title if e.isalnum())

# extract only audio from the media stream
video = yt.streams.filter(only_audio=True).first()
# download the file
out_file = video.download(output_path=destination, filename=vid_title)

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
    srt_filename = os.path.join(destination, vid_title + "_subs.srt")
    with open(srt_filename, "w") as f:
        f.write(wanted_subs)
    print("SRT File Generated")
    return srt_filename


srt_filename = download_transcript(vid_id, destination, languages)

# split video into segments based on srt timestamp
video_name = os.path.join(destination   , vid_title + ".mp3")
#subtitle_name = os.path.join(srt_filename)
subprocess.check_call(["./srt-split.sh", video_name, srt_filename, 'wav'])
print("video split to segments based on srt timestamp")


# create video metadata
subs = pysrt.open(srt_filename)
parts = subs.slice()

#determine zfill digit/ add zeroes to front of count based on the length of subtitles
if len(parts) >= 100:
    z_fill_digit = 3
elif len(parts) >=1000:
    z_fill_digit = 4
elif len(parts)>=10:
    z_fill_digit = 2
    
count = 1  
video_location = os.path.join(destination, vid_title + '-clips')
#print(video_location)
with open(os.path.join(video_location, 'metadata.csv'), 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    for part in parts:
        start_time = part.start
        end_time = part.end
        videopart_digit = str(count).zfill(z_fill_digit)
        videopart_name = videopart_digit + '-'  + vid_title + '.wav'
        writer.writerow([video_location + '/{}|{}'.format(videopart_name, part.text)])
        
        
        count +=1