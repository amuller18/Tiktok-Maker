import os
import yt_dlp as youtube_dl
import subprocess
import json

def get_video_resolution(video_path):
    command = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'json',
        video_path
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Failed to get video resolution: {result.stderr}")
    video_info = json.loads(result.stdout)
    width = video_info['streams'][0]['width']
    height = video_info['streams'][0]['height']
    return width, height

def get_video_and_prepare(url):
    download_path = '.'
    
    ydl_opts = {
        'format': 'bestvideo[height<=?1080]+bestaudio/best[height<=?1080]',
        'outtmpl': 'video',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


    video_path = os.path.join(download_path, 'video.mp4')
    output_path = os.path.join(download_path, 'edited_video_1080x1920.mp4')
    
    vf_filters = (
        'scale=1080:1920:force_original_aspect_ratio=increase,'
        'crop=1080:1920,'
        'unsharp=5:5:1.0:5:5:0.0,'
        'hqdn3d=1.5:1.5:6:6,'
        'deblock=alpha=0.1:beta=0.1'
    )

    command = [
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-ss', str(1),
        '-t', str(121),
        '-vf', vf_filters,
        '-c:v', 'h264_nvenc',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-f', 'mp4',
        output_path
    ]

    subprocess.run(command, check=True)
    final_width, final_height = get_video_resolution(output_path)
    print(f'Final video width is {final_width} and height is {final_height}')