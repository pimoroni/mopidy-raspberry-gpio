import pytest
from mopidy_raspberry_gpio import Extension, PinConfig


def test_get_default_config():
    ext = Extension()

    config = ext.get_default_config()

    assert "[raspberry-gpio]" in config
    assert "enabled = false" in config


def test_get_config_schema():
    ext = Extension()

    schema = ext.get_config_schema()

    # Test the content of config schema
    assert "bcm0" in schema
    assert "bcm27" in schema


def test_pinconfig():
    ext = Extension()

    schema = ext.get_config_schema()
    bcm0 = schema["bcm0"].deserialize("play_pause,active_low,30")

    assert type(bcm0) == PinConfig.tuple_pinconfig
    assert type(bcm0.bouncetime) == int


def test_pinconfig_invalid_event_raises_valueerror():
    ext = Extension()

    schema = ext.get_config_schema()

    with pytest.raises(ValueError):
        bcm1 = schema["bcm1"].deserialize("tomato,active_low,30")
        del bcm1


def test_pinconfig_invalid_mode_raises_valueerror():
    ext = Extension()

    schema = ext.get_config_schema()

    with pytest.raises(ValueError):
        bcm1 = schema["bcm1"].deserialize("play_pause,tomato,30")
        del bcm1


def test_pinconfig_invalid_bouncetime_raises_valueerror():
    ext = Extension()

    schema = ext.get_config_schema()

    with pytest.raises(ValueError):
        bcm1 = schema["bcm1"].deserialize("play_pause,active_low,tomato")
        del bcm1


def test_pinconfig_additional_options():
    ext = Extension()

    schema = ext.get_config_schema()

    bcm1 = schema["bcm1"].deserialize("volume_up,active_low,30,steps=1")
    del bcm1


def test_pinconfig_serialize():
    ext = Extension()

    schema = ext.get_config_schema()

    bcm1 = schema["bcm1"].deserialize("volume_up,active_low,30,steps=1")
    assert schema["bcm1"].serialize(bcm1) == "volume_up,active_low,30,steps=1"
