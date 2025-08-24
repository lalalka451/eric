import subprocess

import praw
import requests
import os
import re
import ffmpeg

# Replace these with the values from your Reddit app
reddit = praw.Reddit(
    client_id='AJ8IpOAc2yFLdn2R5SbhuA',
    client_secret='g3c0y22tSigQhyIMCyflFpsOfrgLEg',
    username='Left-Effort-7573',
    password='a13579246810A@',
    user_agent='testscript by u/Left-Effort-7573'
)

# Select subreddit
subreddit = reddit.subreddit('asmongold')

# Create a directory to save media files
MEDIA_DIR = 'media'
if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)


def download_file(url, path):
    """
    Downloads a file from a URL and saves it to the specified path.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad status codes
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"Downloaded: {path}")
        return True
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return False


def merge_audio_video(video_path, audio_path, output_path):
    """
    Merges video and audio files into a single output file using FFmpeg.
    """
    try:
        # FFmpeg command to merge without re-encoding
        command = [
            r"C:\Users\fueqq\Downloads\eric\qq chat export 0.2.0\lib\ffmpeg-lgpl\ffmpeg.exe",
            '-i', video_path,
            '-i', audio_path,
            '-c', 'copy',
            output_path
        ]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Merged video and audio into: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg failed: {e.stderr.decode()}")
        return False


# Fetch the top 100 hot posts and get media (videos with audio)
for post in subreddit.hot(limit=100):
    permalink = post.permalink
    print(f"Title: {post.title}")
    if post.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):

        print(f"Image URL: {post.url}")

        # Download the image
        response = requests.get(post.url)
        if response.status_code == 200:
            file_name = os.path.join('media', os.path.basename(post.url))
            with open(file_name, 'wb') as f:
                f.write(response.content)
            print(f"Image saved as {file_name}")
    elif post.is_video and post.media and 'reddit_video' in post.media:
        video_url = post.media['reddit_video'].get('fallback_url')
        if video_url:
            print(f"Video URL: {video_url}")

            # Derive audio URL from video URL
            # Example video URL: https://v.redd.it/ku7fb2wyucsd1/DASH_1080.mp4?source=fallback
            # Corresponding audio URL: https://v.redd.it/ku7fb2wyucsd1/HLS_AUDIO_128.aac
            reddit_id = re.findall(r'https://v.redd.it/(.*?)/DASH', video_url)[0]
            audio_url = f'https://v.redd.it/{reddit_id}/HLS_AUDIO_128.aac'
            print(f"Audio URL: {audio_url}")

            # Define file paths
            video_filename = f"{post.id}_video.mp4"
            audio_filename = f"{post.id}_audio.aac"
            output_filename = f"{post.id}_final.mp4"

            video_path = os.path.join(MEDIA_DIR, video_filename)
            audio_path = os.path.join(MEDIA_DIR, audio_filename)
            output_path = os.path.join(MEDIA_DIR, output_filename)

            # Download video
            if download_file(video_url, video_path):
                # Download audio
                if download_file(audio_url, audio_path):
                    # Merge video and audio
                    if merge_audio_video(video_path, audio_path, output_path):
                        print(f"Final video with audio saved as {output_filename}")
                    else:
                        print("Failed to merge audio and video.")
                else:
                    print("Failed to download audio.")
            else:
                print("Failed to download video.")
    else:
        print("No media content or unsupported media type.")

    print('-' * 40)