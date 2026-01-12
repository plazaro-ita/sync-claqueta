import argparse
import os
import sys
from pathlib import Path

# Add src to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent / 'src'))

from claqueta.finder import find_clap_frame_from_audio
from claqueta.cutter import cut_video_from_frame

def main():
    """
    Main function to process videos to find a clap and cut them.
    """
    parser = argparse.ArgumentParser(
        description="A tool to find a clap sound in videos and cut them from that point."
    )
    parser.add_argument(
        "input_files",
        metavar="VIDEO",
        type=str,
        nargs="+",
        help="One or more video files to process.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default="output",
        help="The directory to save the processed videos. Defaults to 'output'.",
    )
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    for video_path in args.input_files:
        if not os.path.isfile(video_path):
            print(f"Error: Input file not found: {video_path}")
            continue

        print(f"Processing {video_path}...")
        
        # 1. Find the clap frame
        clap_frame, clap_timestamp = find_clap_frame_from_audio(video_path)

        if clap_frame == -1:
            print(f"Could not find clap in {video_path}. Skipping.")
            continue
            
        print(f"  - Found clap at frame {clap_frame} ({clap_timestamp:.2f}s)")

        # 2. Cut the video
        input_filename = Path(video_path).name
        output_filename = f"{Path(input_filename).stem}_cut.mp4"
        output_path = os.path.join(args.output_dir, output_filename)
        
        print(f"  - Cutting video and saving to {output_path}")
        cut_video_from_frame(video_path, output_path, clap_frame)

if __name__ == "__main__":
    main()
