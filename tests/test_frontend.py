from __future__ import unicode_literals

import sys

import mock

import pytest

from mopidy_raspberry_gpio import Extension, pinconfig
from mopidy_raspberry_gpio import frontend as frontend_lib


deserialize = pinconfig.PinConfig().deserialize

dummy_config = {
    "raspberry-gpio": {
        # Plugins expect settings to be deserialized
        "bcm1": deserialize("play_pause,active_low,30")
    }
}


def test_get_frontend_classes():
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi.GPIO'] = mock.Mock()

    ext = Extension()
    registry = mock.Mock()

    ext.setup(registry)

    registry.add.assert_called_once_with(
        'frontend', frontend_lib.RaspberryGPIOFrontend)


def test_frontend_handler_dispatch():
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi.GPIO'] = mock.Mock()

    frontend = frontend_lib.RaspberryGPIOFrontend(dummy_config, mock.Mock())

    with pytest.raises(RuntimeError):
        frontend.dispatch_input('tomato')
