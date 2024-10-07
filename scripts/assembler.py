import PIL.Image
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import subprocess
import stt
from youtube_ripper import get_video_resolution
import PIL 
from PIL import Image
import json


class editor:
    def __init__(self):
        pass
    
    def add_subtitles(self, subtitle_file, video):
        
        video_clip = VideoFileClip(video)
        audio = video_clip.audio
        audio.write_audiofile('output_audio.wav')
        
        stt.speech_to_text_func('TTS.wav')

        mix_command = [
        'ffmpeg',
        '-y',
        '-i', video,
        '-i', 'TTS.wav',
        '-filter_complex', '[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=3',
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-f', 'mp4',
        'temp_video.mp4'
        ]

        subprocess.run(mix_command, check=True)

        subtitle_command = [
            'ffmpeg',
            '-y',
            '-i', 'temp_video.mp4',
            '-vf', f"subtitles={subtitle_file}:force_style='Alignment=10,Fontsize=24,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&'",
            '-c:v', 'h264_nvenc',
            '-cq:', '18',
            '-c:a', 'copy',
            '-f', 'mp4',
            'subtitled_video.mp4'
        ]

        subprocess.run(subtitle_command, check=True)

    def create_thumbnail(self):

        width, height = get_video_resolution('subtitled_video.mp4')

    
        img = PIL.Image.open('post_pic.png')
        image_width, image_height = img.size

        x = 0
        y = 960 - (image_height/2)

        print(f'Height is {height} and width is {width}')
        thumbnail_command = [
            "ffmpeg",
            '-y',
            "-i", 'subtitled_video.mp4',
            "-i", 'post_pic.png',
            "-filter_complex", f"[1:v]scale=1080:800[scaled];[0:v][scaled]overlay={x}:{y}:enable='between(t,0,0.01)'",
            "-c:v", "h264_nvenc",
            "-c:a", "copy",
            'thumbnailed_video.mp4'
        ]
        subprocess.run(thumbnail_command)

    def trim_video_to_audio_length(self, audio_path):
        result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', audio_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
        )
        
        probe = json.loads(result.stdout)
        duration = float(probe['format']['duration'])
        
        command = [
        'ffmpeg', 
        '-i', 'thumbnailed_video.mp4',
        '-ss', str(0),
        '-t', str(duration),
        '-c', 'copy',
        'trimmed_video.mp4'
        ]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
