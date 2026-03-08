import unittest
from src.command_generator import CommandGenerator

class TestCommandGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = CommandGenerator(display=":1.0", fps=60, resolution="1280x720")

    def test_generate_mp4_args(self):
        args = self.generator.generate_args("output.mp4")
        self.assertIn("ffmpeg", args)
        self.assertIn("x11grab", args)
        self.assertIn("1280x720", args)
        self.assertIn("60", args)
        self.assertIn("libx264", args)
        self.assertEqual(args[-1], "output.mp4")

    def test_generate_avi_args(self):
        args = self.generator.generate_args("output.avi")
        self.assertIn("libxvid", args)
        self.assertEqual(args[-1], "output.avi")

    def test_generate_with_timestamp(self):
        self.generator.show_timestamp = True
        args = self.generator.generate_args("output.mp4")
        self.assertIn("-vf", args)
        self.assertTrue(any("drawtext" in arg for arg in args))

    def test_windows_generation(self):
        from unittest.mock import patch
        with patch('platform.system', return_value='Windows'):
            generator = CommandGenerator(fps=60)
            args = generator.generate_args("output.mp4")
            self.assertIn("gdigrab", args)
            self.assertIn("desktop", args)
            self.assertIn("-framerate", args)
            self.assertIn("60", args)

    def test_windows_with_audio(self):
        from unittest.mock import patch
        with patch('platform.system', return_value='Windows'):
            generator = CommandGenerator(use_mic=True)
            args = generator.generate_args("output.mp4")
            self.assertIn("dshow", args)
            self.assertTrue(any("audio=" in arg for arg in args))

    def test_unsupported_format(self):
        with self.assertRaises(ValueError):
            self.generator.generate_args("output.mov")

if __name__ == '__main__':
    unittest.main()
