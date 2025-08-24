from faster_whisper import WhisperModel

model = WhisperModel("deepdml/faster-whisper-large-v3-turbo-ct2")

segments, info = model.transcribe(r"C:\Users\fueqq\Downloads\Video\Ученик. Восхождение Трампа (2024).mp4")

# Open a file to write the subtitles
with open("subtitles.srt", "w", encoding="utf-8") as srt_file:
    for i, segment in enumerate(segments, start=1):
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        # Format start and end times
        start_time = f"{int(segment.start // 3600):02d}:{int(segment.start % 3600 // 60):02d}:{int(segment.start % 60):02d},{int(segment.start % 1 * 1000):03d}"
        end_time = f"{int(segment.end // 3600):02d}:{int(segment.end % 3600 // 60):02d}:{int(segment.end % 60):02d},{int(segment.end % 1 * 1000):03d}"
        
        # Write subtitle entry
        srt_file.write(f"{i}\n")
        srt_file.write(f"{start_time} --> {end_time}\n")
        srt_file.write(f"{segment.text}\n\n")

print("Subtitles saved to subtitles.srt")
