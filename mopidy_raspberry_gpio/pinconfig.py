from collections import namedtuple

from mopidy import config
from mopidy.config import types


class ValidList(list):
    def __format__(self, format_string=None):
        if format_string is None:
            format_string = ", "
        return format_string.join(self)


class PinConfig(config.ConfigValue):
    tuple_pinconfig = namedtuple("PinConfig", ("event", "active", "bouncetime"))

    valid_events = ValidList(
        ["play_pause", "prev", "next", "volume_up", "volume_down"]
    )

    valid_modes = ValidList(["active_low", "active_high"])

    def __init__(self):
        pass

    def deserialize(self, value):
        if value is None:
            return None

        value = types.decode(value).strip()

        try:
            event, active, bouncetime = value.split(",")
        except ValueError:
            return None

        if event not in self.valid_events:
            raise ValueError(
                f"invalid event for pin config {event} (Must be {self.valid_events})"
            )

        if active not in self.valid_modes:
            raise ValueError(
                f"invalid event for pin config {active} (Must be one of {self.valid_modes})"
            )

        try:
            bouncetime = int(bouncetime)
        except ValueError:
            raise ValueError(
                f"invalid bouncetime value for pin config {bouncetime}"
            )

        return self.tuple_pinconfig(event, active, bouncetime)

    def serialize(self, value, display=False):
        if value is None:
            return ""
        value = f"{value.event},{value.active},{value.bouncetime}"
        return types.encode(value)
