from __future__ import unicode_literals

import logging
import os

from mopidy import config, ext

from .pinconfig import PinConfig

__version__ = "0.0.2"


logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = "Mopidy-Raspberry-GPIO"
    ext_name = "raspberry-gpio"
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), "ext.conf")
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        for pin in range(28):
            schema["bcm{:d}".format(pin)] = PinConfig()
        return schema

    def setup(self, registry):
        from .frontend import RaspberryGPIOFrontend
        registry.add("frontend", RaspberryGPIOFrontend)
