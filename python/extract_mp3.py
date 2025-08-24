import os
import subprocess

# Define paths
input_dir = r"C:\baidunetdiskdownload\MAOimagine灯光班-第4期等多个文件\MAOimagine灯光班-第4期"
ffmpeg_path = r"C:\Users\fueqq\Downloads\eric\work\python\ffmpeg.exe"

def extract_mp3(input_file, output_file):
    # Skip if output file already exists
    if os.path.exists(output_file):
        print(f"Skipping {input_file} - output file already exists")
        return
        
    try:
        # Command optimized for speed
        command = [
            ffmpeg_path,
            '-i', input_file,
            '-vn',  # Disable video
            '-acodec', 'libmp3lame',  # Use MP3 codec
            '-q:a', '2',  # Audio quality (2 is high quality, lower number = higher quality)
            '-threads', '4',  # Use 4 threads for faster processing (adjust based on your CPU)
            '-preset', 'ultrafast',  # Use the fastest encoding preset
            output_file
        ]
        subprocess.run(command, check=True)
        print(f"Successfully extracted audio from: {input_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing {input_file}: {str(e)}")

def main():
    # Create output directory if it doesn't exist
    output_dir = os.path.join(input_dir, "extracted_mp3")
    os.makedirs(output_dir, exist_ok=True)

    # Process all MP4 files in the directory
    processed_files = set()
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.mp4'):
            # Skip if file was already processed
            if filename in processed_files:
                continue
                
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.mp3")
            extract_mp3(input_file, output_file)
            processed_files.add(filename)

if __name__ == "__main__":
    main()
