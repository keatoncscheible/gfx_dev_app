from abc import ABC, abstractmethod

from pyfx.config import PedalConfig


class PyFxPedal(ABC):
    def __init__(self, pedal_config: PedalConfig):
        self.pedal_config = pedal_config

    @property
    def name(self):
        return self.pedal_config.name

    @property
    def knobs(self):
        return self.pedal_config.knobs

    @property
    def footswitches(self):
        return self.pedal_config.footswitches

    # @abstractmethod
    # def process_audio(self, data):
    #     """Abstract Process Audio Callback"""
