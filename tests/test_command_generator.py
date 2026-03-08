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

    def test_generate_mp4_with_audio_args(self):
        self.generator.use_mic = True
        args = self.generator.generate_args("output.mp4")
        self.assertIn("pulse", args)
        self.assertIn("default", args)
        self.assertIn("aac", args)
        self.assertIn("aresample=async=1", args)

    def test_generate_with_timestamp(self):
        self.generator.show_timestamp = True
        args = self.generator.generate_args("output.mp4")
        self.assertIn("-vf", args)
        self.assertTrue(any("drawtext" in arg for arg in args))
        self.assertTrue(any("localtime" in arg for arg in args))

    def test_unsupported_format(self):
        with self.assertRaises(ValueError):
            self.generator.generate_args("output.mov")

if __name__ == '__main__':
    unittest.main()
