import sys
from unittest import mock

import pykka
from mopidy import core

import pytest
from mopidy_raspberry_gpio import Extension
from mopidy_raspberry_gpio import frontend as frontend_lib
from mopidy_raspberry_gpio import pinconfig

from . import dummy_audio, dummy_backend, dummy_mixer

deserialize = pinconfig.PinConfig().deserialize

dummy_config = {
    "raspberry-gpio": {
        # Plugins expect settings to be deserialized
        "bcm1": deserialize("play_pause,active_low,30"),
        "bcm2": deserialize("volume_up,active_high,30"),
        "bcm3": deserialize("volume_down,active_high,30"),
    }
}


def stop_mopidy_core():
    pykka.ActorRegistry.stop_all()


def dummy_mopidy_core():
    mixer = dummy_mixer.create_proxy()
    audio = dummy_audio.create_proxy()
    backend = dummy_backend.create_proxy(audio=audio)
    return core.Core.start(audio=audio, mixer=mixer, backends=[backend]).proxy()


def test_get_frontend_classes():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    ext = Extension()
    registry = mock.Mock()

    ext.setup(registry)

    registry.add.assert_called_once_with(
        "frontend", frontend_lib.RaspberryGPIOFrontend
    )

    stop_mopidy_core()


def test_frontend_handler_dispatch_play_pause():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    frontend = frontend_lib.RaspberryGPIOFrontend(
        dummy_config, dummy_mopidy_core()
    )

    frontend.dispatch_input("play_pause")

    stop_mopidy_core()


def test_frontend_handler_dispatch_next():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    frontend = frontend_lib.RaspberryGPIOFrontend(
        dummy_config, dummy_mopidy_core()
    )

    frontend.dispatch_input("next")

    stop_mopidy_core()


def test_frontend_handler_dispatch_prev():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    frontend = frontend_lib.RaspberryGPIOFrontend(
        dummy_config, dummy_mopidy_core()
    )

    frontend.dispatch_input("prev")

    stop_mopidy_core()


def test_frontend_handler_dispatch_volume_up():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    frontend = frontend_lib.RaspberryGPIOFrontend(
        dummy_config, dummy_mopidy_core()
    )

    frontend.dispatch_input("volume_up")

    stop_mopidy_core()


def test_frontend_handler_dispatch_volume_down():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    frontend = frontend_lib.RaspberryGPIOFrontend(
        dummy_config, dummy_mopidy_core()
    )

    frontend.dispatch_input("volume_down")

    stop_mopidy_core()


def test_frontend_handler_dispatch_invalid_event():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    frontend = frontend_lib.RaspberryGPIOFrontend(
        dummy_config, dummy_mopidy_core()
    )

    with pytest.raises(RuntimeError):
        frontend.dispatch_input("tomato")

    stop_mopidy_core()


def test_frontend_gpio_event():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    frontend = frontend_lib.RaspberryGPIOFrontend(
        dummy_config, dummy_mopidy_core()
    )

    frontend.gpio_event(3)

    stop_mopidy_core()
