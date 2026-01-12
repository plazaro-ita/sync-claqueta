# Claqueta Finder

Claqueta Finder is a Python tool to automatically find the clap sound in a video file and cut the video starting from that point. This is useful for synchronizing video footage from multiple cameras that used a clapperboard for audio-based sync.

## Installation

1.  Clone this repository to your local machine.
2.  Install the required Python packages using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

The main script to use is `main.py`. It takes one or more video files as input and will generate cut versions of them in an output directory.

### Basic Example

To process a single video file and save the output to the default `output/` directory:

```bash
python main.py /path/to/your/video.mp4
```

### Specifying an Output Directory

To specify a different directory for the processed videos, use the `-o` or `--output-dir` flag:

```bash
python main.py /path/to/your/video.mp4 -o /path/to/your/output_folder
```

### Processing Multiple Videos

You can process multiple videos at once by listing them as arguments:

```bash
python main.py video1.mp4 video2.mov video3.mkv --output-dir cut_videos/
```

The script will create a new video file for each input file, with `_cut` appended to the original filename.

## How It Works

The tool uses the `librosa` library to analyze the audio track of the video. It calculates the "onset strength" of the audio signal, which highlights sharp, percussive sounds. The loudest of these sounds is assumed to be the clapperboard. The timestamp of this event is then used to determine the corresponding frame in the video, and a new video is created starting from that frame.
