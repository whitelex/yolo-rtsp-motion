from ffmpeg import FFmpeg
import time

def start_ffmpeg(rtsp_stream, filename):
    ffmpeg_copy = (
        FFmpeg()
        .option("y")
        .input(
            rtsp_stream,
            rtsp_transport="tcp",
            rtsp_flags="prefer_tcp",
        )
        .output(filename, vcodec="copy", acodec="copy")
    )
    try:
        ffmpeg_copy.execute()
    except:
        print("Issue recording the stream. Trying again.")
        time.sleep(1)
        ffmpeg_copy.execute()
    return ffmpeg_copy

def stop_ffmpeg(ffmpeg_copy):
    ffmpeg_copy.terminate()

def create_thumbnail(video_file):
    thumbnail_file = video_file.replace(".mkv", ".jpg")
    print(f"Creating thumbnail for {video_file}")
    ffmpeg_cmd = (
        FFmpeg()
        .input(video_file, ss="00:00:01")
        .output(thumbnail_file, vframes=1)
    )
    ffmpeg_cmd.execute()
    print(f"Thumbnail created: {thumbnail_file}")