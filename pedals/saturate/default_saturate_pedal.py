import numpy as np
from autogen.saturate_pedal_variant_base import SaturatePedalVariantBase


class DefaultSaturatePedal(SaturatePedalVariantBase):
    def process_audio(self, data: np.ndarray):
        """Default Saturate Pedal Processing"""

        if self.on_off:
            data = np.clip(self.amount * data, -1, 1)
            data = self.output * data

        return data
