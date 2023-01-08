import pysrt
import os
import ffmpeg
import subprocess as sp
from datetime import datetime 



# def trim(in_file, out_file, start, end):
#     if os.path.exists(out_file):
#         os.remove(out_file)

#     in_file_probe_result = ffmpeg.probe(in_file)
#     in_file_duration = in_file_probe_result.get(
#         "format", {}).get("duration", None)
#     print(in_file_duration)

#     input_stream = ffmpeg.input(in_file)

#     pts = "PTS-STARTPTS"
#     #video = input_stream.trim(start=start, end=end).setpts(pts)
#     audio = (input_stream
#              .filter_("atrim", start=start, end=end)
#              .filter_("asetpts", pts))
#     #video_and_audio = ffmpeg.concat(video, audio, v=1, a=1)
#     output = ffmpeg.output(audio, out_file, format="mp3")
#     output.run()

#     out_file_probe_result = ffmpeg.probe(out_file)
#     out_file_duration = out_file_probe_result.get(
#         "format", {}).get("duration", None)
#     print(out_file_duration)

def trim_video(input_file, output_file, start,end):
    input_stream = ffmpeg.input(input_file)
    #pts = "PTS-STARTPTS"
    audio = ffmpeg.trim(input_stream, start_pts=start, end_pts=end)
    output = ffmpeg.output(audio, out_file, format="mp3")
    output.run()
    out_file_probe_result = ffmpeg.probe(output_file)
    out_file_duration = out_file_probe_result.get(
        "format", {}).get("duration", None)
    print(out_file_duration)


subs = pysrt.open('./Samsung is Hiding This Monitor’s Best Feature – Odyssey OLED G8_en-US_subs.srt')
parts = subs.slice()
input_vid = "./Samsung is Hiding This Monitor’s Best Feature – Odyssey OLED G8.mp3"
folder_output = './linus_clips/'
#os.mkdir(folder_output)
count = 1   
for part in parts:
    start_time = part.start
    end_time = part.end
    
    out_file = folder_output + str(count) + '.mp3'
    start_obj = datetime.strptime(str(start_time),
                           '%H:%M:%S,%f')
    end_obj = datetime.strptime(str(end_time),
                           '%H:%M:%S,%f')
    trim_video(input_vid, folder_output + str(count) + '.mp3', start_obj, end_obj)
    # ffmpeg -ss 00:00:30.0 -i input.wmv -c copy -t 00:00:10.0 output.wmv
    #sp.Popen("ffmpeg -ss {start} -i {input_dir} -to {end} -c copy {output_name}".format(start=start_time, input_dir=input_vid, end=end_time, output_name=out_file)).wait()
    count +=1