import numpy as np
from autogen.volume_pedal_variant_base import VolumePedalVariantBase


class DefaultVolumePedal(VolumePedalVariantBase):
    def process_audio(self, data: np.ndarray):
        """Default Volume Pedal Processing"""

        if self.on_off:
            data = self.output * data

        return data
