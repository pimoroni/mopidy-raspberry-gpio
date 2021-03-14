import sys
from unittest import mock

import pykka
from mopidy import core

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
        "bcm4": deserialize("volume_down,active_high,250,rotenc_id=vol"),
        "bcm5": deserialize("volume_up,active_high,250,rotenc_id=vol"),
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

    ext = Extension()
    schema = ext.get_config_schema()
    settings = schema["bcm1"].deserialize("play_pause,active_low,30")

    frontend.dispatch_input(settings.event, settings.options)

    stop_mopidy_core()


def test_frontend_handler_dispatch_play_stop():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    frontend = frontend_lib.RaspberryGPIOFrontend(
        dummy_config, dummy_mopidy_core()
    )

    ext = Extension()
    schema = ext.get_config_schema()
    settings = schema["bcm1"].deserialize("play_stop,active_low,30")

    frontend.dispatch_input(settings.event, settings.options)

    stop_mopidy_core()


def test_frontend_handler_dispatch_next():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    frontend = frontend_lib.RaspberryGPIOFrontend(
        dummy_config, dummy_mopidy_core()
    )

    ext = Extension()
    schema = ext.get_config_schema()
    settings = schema["bcm1"].deserialize("next,active_low,30")

    frontend.dispatch_input(settings.event, settings.options)

    stop_mopidy_core()


def test_frontend_handler_dispatch_prev():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    frontend = frontend_lib.RaspberryGPIOFrontend(
        dummy_config, dummy_mopidy_core()
    )

    ext = Extension()
    schema = ext.get_config_schema()
    settings = schema["bcm1"].deserialize("prev,active_low,30")

    frontend.dispatch_input(settings.event, settings.options)

    stop_mopidy_core()


def test_frontend_handler_dispatch_volume_up():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    frontend = frontend_lib.RaspberryGPIOFrontend(
        dummy_config, dummy_mopidy_core()
    )

    ext = Extension()
    schema = ext.get_config_schema()
    settings = schema["bcm1"].deserialize("volume_up,active_low,30")

    frontend.dispatch_input(settings.event, settings.options)

    stop_mopidy_core()


def test_frontend_handler_dispatch_volume_down():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    frontend = frontend_lib.RaspberryGPIOFrontend(
        dummy_config, dummy_mopidy_core()
    )

    ext = Extension()
    schema = ext.get_config_schema()
    settings = schema["bcm1"].deserialize("volume_down,active_low,30")

    frontend.dispatch_input(settings.event, settings.options)

    stop_mopidy_core()


def test_frontend_handler_dispatch_volume_up_custom_step():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    frontend = frontend_lib.RaspberryGPIOFrontend(
        dummy_config, dummy_mopidy_core()
    )

    ext = Extension()
    schema = ext.get_config_schema()
    settings = schema["bcm1"].deserialize("volume_up,active_low,30,step=1")

    frontend.dispatch_input(settings.event, settings.options)

    stop_mopidy_core()


def test_frontend_handler_dispatch_volume_down_custom_step():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    frontend = frontend_lib.RaspberryGPIOFrontend(
        dummy_config, dummy_mopidy_core()
    )

    ext = Extension()
    schema = ext.get_config_schema()
    settings = schema["bcm1"].deserialize("volume_down,active_low,30,step=1")

    frontend.dispatch_input(settings.event, settings.options)

    stop_mopidy_core()


def test_frontend_gpio_event():
    sys.modules["RPi"] = mock.Mock()
    sys.modules["RPi.GPIO"] = mock.Mock()

    frontend = frontend_lib.RaspberryGPIOFrontend(
        dummy_config, dummy_mopidy_core()
    )

    frontend.gpio_event(3)

    stop_mopidy_core()


@mock.patch("RPi.GPIO.input")
def test_frontend_rot_encoder_event(patched_input):
    patched_input.return_value = False

    frontend = frontend_lib.RaspberryGPIOFrontend(
        dummy_config, dummy_mopidy_core()
    )

    # Check that transition (False, True) -> (False, False) triggers volume_up
    encoder = frontend.rot_encoders["vol"]
    encoder.state = (False, True)

    dispatch_input = mock.Mock()
    frontend.dispatch_input = dispatch_input

    frontend.gpio_event(4)
    assert dispatch_input.call_args[0][0] == "volume_up"
    assert encoder.state == (False, False)

    # Check that we do not submit an event for the invalid transition
    # (False, False) -> (False, False)
    dispatch_input.reset_mock()
    frontend.gpio_event(4)
    dispatch_input.assert_not_called()

    stop_mopidy_core()
