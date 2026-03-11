import unittest
import numpy as np
from unittest.mock import patch
from claqueta.finder import find_clap_frame_from_audio

class TestFinder(unittest.TestCase):
    @patch('claqueta.finder.librosa.load')
    @patch('claqueta.finder.cv2.VideoCapture')
    def test_find_clap_frame_from_audio(self, mock_cv2, mock_librosa):
        """Test finding a clap using mocked audio signal."""
        sr = 44100
        duration = 5
        # Create a silent audio array
        y = np.zeros(int(sr * duration))
        
        # Add a "clap" spike at exactly 2.5 seconds
        clap_index = int(2.5 * sr)
        y[clap_index:clap_index + 100] = 1.0  # Loud sound spike
        
        mock_librosa.return_value = (y, sr)
        
        # Mock cv2.VideoCapture return values
        mock_cap = mock_cv2.return_value
        mock_cap.isOpened.return_value = True
        mock_cap.get.return_value = 24.0  # 24 fps
        
        frame, timestamp = find_clap_frame_from_audio("dummy_video.mp4")
        
        # Verify the findings
        self.assertAlmostEqual(timestamp, 2.5, places=1)
        # Expected frame at 2.5s and 24fps is 60
        self.assertEqual(frame, int(timestamp * 24.0))

if __name__ == '__main__':
    unittest.main()
