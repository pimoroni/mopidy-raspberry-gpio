import logging
import pathlib

from mopidy import config, ext

from .pinconfig import PinConfig

__version__ = "0.0.2"


logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = "Mopidy-Raspberry-GPIO"
    ext_name = "raspberry-gpio"
    version = __version__

    def get_default_config(self):
        return config.read(pathlib.Path(__file__).parent / "ext.conf")

    def get_config_schema(self):
        schema = super().get_config_schema()
        for pin in range(28):
            schema[f"bcm{pin:d}"] = PinConfig()
        return schema

    def setup(self, registry):
        from .frontend import RaspberryGPIOFrontend

        registry.add("frontend", RaspberryGPIOFrontend)
