import numpy as np
from autogen.saturate_pedal_variant_base import SaturatePedalVariantBase
from scipy.signal import butter, lfilter, lfilter_zi


class SmoothSaturatePedal(SaturatePedalVariantBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        order = 4
        low_cutoff_freq = 200
        high_cutoff_freq = 5000
        fs = 44100
        b, a = butter(order, [low_cutoff_freq, high_cutoff_freq], btype="bandpass", analog=False, fs=fs)
        self.zi = lfilter_zi(b, a)
        self.b = b
        self.a = a

    def process_audio(self, data: np.ndarray):
        """Smooth Saturate Pedal Processing"""

        if self.on_off:
            data = np.clip(self.amount * data, -1, 1)
            data = self.output * data
            data, self.zi = lfilter(self.b, self.a, data, zi=self.zi)

        return data
