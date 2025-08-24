import requests
from tqdm import tqdm

def download_file(url, filename):
    # Send a GET request to the URL to stream content
    response = requests.get(url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the total file size from the response headers
        total_size = int(response.headers.get('content-length', 0))

        # Open the file in write-binary mode and download with a progress bar
        with open(filename, 'wb') as file, tqdm(
            desc=filename,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                # Write data to file and update the progress bar
                size = file.write(data)
                bar.update(size)

        print(f"Download complete: {filename}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

# URLs for video and audio files
audio_url = 'https://v.redd.it/wllt1cn5wgsd1/HLS_AUDIO_128.aac'
video_url = 'https://v.redd.it/wllt1cn5wgsd1/DASH_720.mp4'

# File names for saving locally
audio_filename = 'audio.aac'
video_filename = 'video.mp4'

# Download the audio and video
download_file(video_url, video_filename)
download_file(audio_url, audio_filename)

import subprocess


def merge_audio_video(video_file, audio_file, output_file, ffmpeg_path):
    # Command to merge the audio and video files
    command = [
        ffmpeg_path,  # Path to your ffmpeg executable
        '-i', video_file,  # Input video
        '-i', audio_file,  # Input audio
        '-c:v', 'copy',  # Copy video without re-encoding
        '-c:a', 'aac',  # Encode audio using AAC codec
        '-strict', 'experimental',  # Ensure compatibility for some builds
        output_file  # Output file
    ]

    # Run the command
    subprocess.run(command)
    print(f"Merge complete: {output_file}")


# Example usage
ffmpeg_path = r"C:\Users\fueqq\Downloads\eric\work\python\ffmpeg.exe"  # Path to your ffmpeg
video_file = 'video.mp4'
audio_file = 'audio.aac'
output_file = 'output_with_audio.mp4'

merge_audio_video(video_file, audio_file, output_file, ffmpeg_path)
