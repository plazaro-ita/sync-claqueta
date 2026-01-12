import cv2
import os

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
