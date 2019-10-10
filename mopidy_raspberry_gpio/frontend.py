from __future__ import unicode_literals

import logging
import os

from mopidy import core


import pykka


logger = logging.getLogger(__name__)


class RaspberryGPIO(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        pass
