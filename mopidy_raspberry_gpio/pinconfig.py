from collections import namedtuple

from mopidy import config


class PinConfig(config.ConfigValue):
    tuple_pinconfig = namedtuple("PinConfig",
                                 ("event", "active", "bouncetime"))

    valid_events = "play_pause", "prev", "next", "volume_up", "volume_down"

    valid_modes = "active_low", "active_high"

    def __init__(self):
        pass

    def deserialize(self, value):
        if value is None:
            return None

        value = config.decode(value).strip()

        try:
            event, active, bouncetime = value.split(',')
        except ValueError:
            return None

        if event not in self.valid_events:
            raise ValueError(
                "invalid event for pin config {:s} (Must be {})".format(
                    event, ", ".join(self.valid_events)
                )
            )

        if active not in self.valid_modes:
            raise ValueError(
                "invalid mode for pin config {:s} (Must be {})".format(
                    event, ", ".join(self.valid_events)
                )
            )

        try:
            bouncetime = int(bouncetime)
        except ValueError:
            raise ValueError(
                "invalid bouncetime value for pin config {}".format(bouncetime)
            )

        return self.tuple_pinconfig(event, active, bouncetime)

    def serialize(self, value, display=False):
        if value is None:
            return ""
        value = "{:s},{:s},{:d}".format(
            value.event, value.active, value.bouncetime)
        return config.encode(value)
