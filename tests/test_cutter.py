import unittest
import os
import numpy as np
from moviepy import VideoFileClip, AudioArrayClip, ColorClip

from claqueta.cutter import cut_video_with_audio, cut_video_from_frame


class TestCutter(unittest.TestCase):

    def setUp(self):
        """Set up a dummy video file for testing."""
        self.test_dir = "test_videos"
        os.makedirs(self.test_dir, exist_ok=True)
        
        self.video_path = os.path.join(self.test_dir, "test_video.mp4")
        self.output_path_audio = os.path.join(self.test_dir, "test_video_cut_audio.mp4")
        self.output_path_no_audio = os.path.join(self.test_dir, "test_video_cut_no_audio.mp4")

        # Create a silent audio clip
        sr = 44100  # sample rate
        duration = 5  # seconds
        frequency = 440  # Hz
        t = np.linspace(0, duration, int(sr * duration), False)
        audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)
        audio_clip = AudioArrayClip(np.vstack((audio_data, audio_data)).T, fps=sr)

        # Create a simple color video clip
        video_clip = ColorClip(size=(640, 480), color=(0, 255, 0), duration=duration)
        video_clip.audio = audio_clip
        video_clip.write_videofile(self.video_path, codec="libx264", audio_codec="aac", fps=24)

    def tearDown(self):
        """Clean up the created files."""
        for f in [self.video_path, self.output_path_audio, self.output_path_no_audio]:
            if os.path.exists(f):
                os.remove(f)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def test_cut_video_with_audio(self):
        """Test that cut_video_with_audio produces a video with an audio track."""
        start_time = 2  # seconds
        cut_video_with_audio(self.video_path, self.output_path_audio, start_time)
        
        # Check if the output file exists
        self.assertTrue(os.path.exists(self.output_path_audio))
        
        # Check if the output video has audio
        with VideoFileClip(self.output_path_audio) as video:
            self.assertIsNotNone(video.audio)
            self.assertAlmostEqual(video.duration, 3, delta=0.1)

    def test_cut_video_from_frame_no_audio(self):
        """Test that cut_video_from_frame produces a video without an audio track."""
        start_frame = 48
        cut_video_from_frame(self.video_path, self.output_path_no_audio, start_frame)

        # Check if the output file exists
        self.assertTrue(os.path.exists(self.output_path_no_audio))

        # Check if the output video has no audio
        with VideoFileClip(self.output_path_no_audio) as video:
            self.assertIsNone(video.audio)
            self.assertAlmostEqual(video.duration, 3, delta=0.1)

if __name__ == '__main__':
    unittest.main()
