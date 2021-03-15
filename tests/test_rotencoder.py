import unittest

from unittest.mock import patch
from mopidy_raspberry_gpio.rotencoder import RotEncoder


class RotEncoderTests(unittest.TestCase):
    def test_rotenc_init(self):
        rot_enc = RotEncoder("vol")
        self.assertTrue(rot_enc.id == "vol")
        self.assertTrue(((False, False), (False, True)) in rot_enc.state_map)

    def test_get_direction(self):
        rot_enc = RotEncoder("vol")
        rot_enc.add_pin(123, "vol_up")
        rot_enc.add_pin(124, "vol_down")

        dir_down = rot_enc.get_direction((False, False), (False, True))
        dir_up = rot_enc.get_direction((False, False), (True, False))

        self.assertEqual(dir_up, 1)
        self.assertEqual(dir_down, 0)

    def test_add_pin_invalid(self):
        rot_enc = RotEncoder("vol")
        rot_enc.add_pin(123, "vol_up")
        rot_enc.add_pin(124, "vol_down")

        with self.assertRaises(RuntimeError):
            rot_enc.add_pin(124, "vol_down")

    @patch("RPi.GPIO.input")
    def test_get_event(self, patched_input):
        # Always return False for GPIO.input
        patched_input.return_value = False

        rot_enc = RotEncoder("vol")
        rot_enc.add_pin(123, "vol_down")  # dir 0 => vol_down
        rot_enc.add_pin(124, "vol_up")  # dir 1 => vol_up

        # from False,True to False,False => dir 1
        rot_enc.state = (False, True)
        event = rot_enc.get_event()
        self.assertEqual(event, "vol_up")

        # from True,False to False,False => dir 0
        rot_enc.state = (True, False)
        event = rot_enc.get_event()
        self.assertEqual(event, "vol_down")

        # from True,True to False,False => None
        rot_enc.state = (True, True)
        event = rot_enc.get_event()
        self.assertEqual(event, None)
