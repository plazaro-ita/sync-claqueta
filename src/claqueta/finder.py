import cv2
import numpy as np
import librosa

def find_clap_frame_from_audio(video_path: str) -> tuple[int, float]:
    """
    Finds the video frame corresponding to the loudest sound event (clap) in a video file.

    This function loads the audio from the video, calculates the onset strength to
    identify sharp transient sounds, and finds the point of maximum change. It then
    converts this point in time to a video frame number.

    Args:
        video_path: The path to the video file.

    Returns:
        A tuple containing:
        - The frame number of the clap.
        - The timestamp of the clap in seconds.
    """
    try:
        y, sr = librosa.load(video_path)
    except Exception as e:
        print(f"Error loading audio from {video_path}: {e}")
        return -1, -1.0

    # Calculate the onset strength envelope
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)

    # Find the frame with the maximum onset strength
    clap_onset_frame = np.argmax(onset_env)

    # Convert the onset frame to time
    clap_timestamp = librosa.frames_to_time([clap_onset_frame], sr=sr)[0]

    # Get video FPS to convert the timestamp to a video frame number
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file: {video_path}")
        return -1, -1.0
        
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    clap_video_frame = int(clap_timestamp * fps)

    return clap_video_frame, clap_timestamp

def _show_onset_frames(video_path: str, onset_frames: list[int]):
    """
    Reads a video and displays the frames specified by onset_frames.
    Internal use for debugging.

    Args:
        video_path: The path to the video file.
        onset_frames: A list of frame numbers to display.
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video file: {video_path}")
        return

    for frame_number in onset_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()

        if ret:
            cv2.imshow(f'Frame {frame_number}', frame)
            cv2.waitKey(0)
        else:
            print(f"Warning: Could not read frame {frame_number}")

    cap.release()
    cv2.destroyAllWindows()
