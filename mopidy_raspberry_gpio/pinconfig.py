from collections import namedtuple

from mopidy import config


class PinConfig(config.String):
    tuple_pinconfig = namedtuple("PinConfig",
                                 ("event", "active", "bouncetime"))

    valid_events = "play_pause", "prev", "next", "volume_up", "volume_down"

    valid_modes = "active_low", "active_high"

    def __init__(self):
        config.String.__init__(self, optional=True)

    def deserialize(self, value):
        value = config.String.deserialize(self, value)
        event, active, bouncetime = value.split(',')

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
        value = "{:s},{:s},{:d}".format(
            value.event, value.active, value.bouncetime)
        value = config.String.serialize(self, value, display)
        return value
