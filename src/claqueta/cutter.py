import cv2
import os
from moviepy import VideoFileClip
import subprocess

def cut_video_ffmpeg(video_path: str, output_path: str, start_time: float):
    """
    Cuts a video from start_time using FFmpeg stream copy (no re-encoding).
    Preserves original codec, quality, and audio.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    cmd = [
        "ffmpeg",
        "-ss", str(start_time),   # seek to clap timestamp
        "-i", video_path,
        "-c", "copy",             # no re-encoding, preserves H.265 or H.264
        "-avoid_negative_ts", "make_zero",
        "-y",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"Successfully cut video and saved to {output_path}")
    else:
        print(f"Error cutting video: {result.stderr}")
        
def cut_video_ffmpeg_by_frame_fast(video_path: str, output_path: str, start_frame: int):
    """
    Cuts a video from a specific frame ID using FFmpeg stream copy (no re-encoding).
    Preserves original codec, quality, and audio.
    Instead of cutting by frame, I transform to timestamp, thereby losing precision.
    """
    # Get FPS using ffprobe to convert frame -> timestamp
    probe_cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=r_frame_rate",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)

    if probe_result.returncode != 0:
        print(f"Error reading FPS: {probe_result.stderr}")
        return

    # r_frame_rate is returned as a fraction e.g. "30000/1001"
    num, den = map(int, probe_result.stdout.strip().split("/"))
    fps = num / den

    start_time = start_frame / fps

    print(f"FPS: {fps:.4f} | Frame {start_frame} → {start_time:.4f}s")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    cmd = [
        "ffmpeg",
        "-ss", str(start_time),
        "-i", video_path,
        "-c", "copy",
        "-avoid_negative_ts", "make_zero",
        "-y",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"Successfully cut video and saved to {output_path}")
    else:
        print(f"Error cutting video: {result.stderr}")

def cut_video_with_audio(video_path: str, output_path: str, start_time: float):
    """
    Cuts a video from a specified start time and saves the result to a new file,
    including the audio.

    Args:
        video_path: The path to the input video file.
        output_path: The path to save the cut video file.
        start_time: The time in seconds from which to start the cut.
    """
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with VideoFileClip(video_path) as video:
            sub_clip = video.subclipped(start_time)
            sub_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        
        print(f"Successfully cut video with audio and saved to {output_path}")

    except Exception as e:
        print(f"Error cutting video with audio: {e}")


def cut_video_from_frame(video_path: str, output_path: str, start_frame: int):
    """
    Cuts a video from a specified frame and saves the result to a new file.

    Args:
        video_path: The path to the input video file.
        output_path: The path to save the cut video file.
        start_frame: The frame number from which to start the cut.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file: {video_path}")
        return

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Or use the same as the input

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    if not out.isOpened():
        print(f"Error: Could not open video writer for: {output_path}")
        cap.release()
        return
        
    # Set the starting frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    print(f"Successfully cut video and saved to {output_path}")

    # Release everything
    cap.release()
    out.release()
