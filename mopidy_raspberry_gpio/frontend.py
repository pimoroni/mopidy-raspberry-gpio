import logging

import pykka
from mopidy import core

from .rotencoder import RotEncoder

logger = logging.getLogger(__name__)


class RaspberryGPIOFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super().__init__()
        import RPi.GPIO as GPIO

        self.core = core
        self.config = config["raspberry-gpio"]
        self.pin_settings = {}
        self.rot_encoders = {}

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        # Iterate through any bcmN pins in the config
        # and set them up as inputs with edge detection
        for key in self.config:
            if key.startswith("bcm"):
                pin = int(key.replace("bcm", ""))
                settings = self.config[key]
                if settings is None:
                    continue

                pull = GPIO.PUD_UP
                edge = GPIO.FALLING
                if settings.active == "active_high":
                    pull = GPIO.PUD_DOWN
                    edge = GPIO.RISING

                if "rotenc_id" in settings.options:
                    edge = GPIO.BOTH
                    rotenc_id = settings.options["rotenc_id"]
                    encoder = None
                    if rotenc_id in self.rot_encoders.keys():
                        encoder = self.rot_encoders[rotenc_id]
                    else:
                        encoder = RotEncoder(rotenc_id)
                        self.rot_encoders[rotenc_id] = encoder
                    encoder.add_pin(pin, settings.event)

                GPIO.setup(pin, GPIO.IN, pull_up_down=pull)

                GPIO.add_event_detect(
                    pin,
                    edge,
                    callback=self.gpio_event,
                    bouncetime=settings.bouncetime,
                )

                self.pin_settings[pin] = settings

        # TODO validate all self.rot_encoders have two pins

    def find_pin_rotenc(self, pin):
        for encoder in self.rot_encoders.values():
            if pin in encoder.pins:
                return encoder

    def gpio_event(self, pin):
        settings = self.pin_settings[pin]
        event = settings.event
        encoder = self.find_pin_rotenc(pin)
        if encoder:
            event = encoder.get_event()

        if event:
            self.dispatch_input(event, settings.options)

    def dispatch_input(self, event, options):
        handler_name = f"handle_{event}"
        try:
            getattr(self, handler_name)(options)
        except AttributeError:
            raise RuntimeError(
                f"Could not find input handler for event: {event}"
            )

    def handle_play_pause(self, config):
        if self.core.playback.get_state().get() == core.PlaybackState.PLAYING:
            self.core.playback.pause()
        else:
            self.core.playback.play()

    def handle_play_stop(self, config):
        if self.core.playback.get_state().get() == core.PlaybackState.PLAYING:
            self.core.playback.stop()
        else:
            self.core.playback.play()

    def handle_next(self, config):
        self.core.playback.next()

    def handle_prev(self, config):
        self.core.playback.previous()

    def handle_volume_up(self, config):
        step = int(config.get("step", 5))
        volume = self.core.mixer.get_volume().get()
        volume += step
        volume = min(volume, 100)
        self.core.mixer.set_volume(volume)

    def handle_volume_down(self, config):
        step = int(config.get("step", 5))
        volume = self.core.mixer.get_volume().get()
        volume -= step
        volume = max(volume, 0)
        self.core.mixer.set_volume(volume)
