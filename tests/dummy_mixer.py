import pykka

from mopidy import mixer


def create_proxy(config=None):
    return DummyMixer.start(config=None).proxy()


class DummyMixer(pykka.ThreadingActor, mixer.Mixer):
    def __init__(self, config):
        super().__init__()
        self._volume = 50   # Had to be initialised to avoid none type error in tests
        self._mute = False  # Ditto

    def get_volume(self):
        return self._volume

    def set_volume(self, volume):
        self._volume = volume
        self.trigger_volume_changed(volume=volume)
        return True

    def get_mute(self):
        return self._mute

    def set_mute(self, mute):
        self._mute = mute
        self.trigger_mute_changed(mute=mute)
        return True
