import sys
from unittest import mock

import pytest
from mopidy_raspberry_gpio import Extension
from mopidy_raspberry_gpio import frontend as frontend_lib
from mopidy_raspberry_gpio import pinconfig

deserialize = pinconfig.PinConfig().deserialize

dummy_config = {
    "raspberry-gpio": {
        # Plugins expect settings to be deserialized
        "bcm1": deserialize("play_pause,active_low,30"),
        "bcm2": deserialize("volume_up,active_high,30"),
        "bcm3": deserialize("volume_down,active_high,30")
    }
}


def test_get_frontend_classes():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    ext = Extension()
    registry = mock.Mock()

    ext.setup(registry)

    registry.add.assert_called_once_with(
        "frontend", frontend_lib.RaspberryGPIOFrontend
    )


def test_frontend_handler_dispatch_play_pause():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    frontend = frontend_lib.RaspberryGPIOFrontend(dummy_config, mock.Mock())

    frontend.dispatch_input("play_pause")


def test_frontend_handler_dispatch_next():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    frontend = frontend_lib.RaspberryGPIOFrontend(dummy_config, mock.Mock())

    frontend.dispatch_input("next")


def test_frontend_handler_dispatch_prev():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    frontend = frontend_lib.RaspberryGPIOFrontend(dummy_config, mock.Mock())

    frontend.dispatch_input("prev")


def test_frontend_handler_dispatch_volume_up():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    frontend = frontend_lib.RaspberryGPIOFrontend(dummy_config, mock.Mock())

    frontend.dispatch_input("volume_up")


def test_frontend_handler_dispatch_volume_down():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    frontend = frontend_lib.RaspberryGPIOFrontend(dummy_config, mock.Mock())

    frontend.dispatch_input("volume_down")


def test_frontend_handler_dispatch_invalid_event():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    frontend = frontend_lib.RaspberryGPIOFrontend(dummy_config, mock.Mock())

    with pytest.raises(RuntimeError):
        frontend.dispatch_input("tomato")


def test_frontend_gpio_event():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    frontend = frontend_lib.RaspberryGPIOFrontend(dummy_config, mock.Mock())

    frontend.gpio_event(3)
