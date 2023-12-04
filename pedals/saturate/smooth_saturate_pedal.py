from collections import deque

import numpy as np
from autogen.saturate_pedal_variant_base import SaturatePedalVariantBase
from scipy.signal import butter, sosfilt, sosfilt_zi

from pyfx.logging import pyfx_log


class SmoothSaturatePedal(SaturatePedalVariantBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fs = 44100
        self.norm_rms_deque = deque([], maxlen=100)
        self.norm_holdoff_frames = 10

        hpf_order = 2
        hpf_cuttoff_freq = 300
        self.hpf_sos = butter(
            hpf_order,
            hpf_cuttoff_freq,
            btype="highpass",
            analog=False,
            fs=fs,
            output="sos",
        )
        self.hpf_zi = sosfilt_zi(self.hpf_sos)

        bsf_order = 4
        bsf_cuttoff_freq_low = 2200
        bsf_cuttoff_freq_high = 2700
        self.bsf_sos = butter(
            bsf_order,
            [bsf_cuttoff_freq_low, bsf_cuttoff_freq_high],
            btype="bandstop",
            analog=False,
            fs=fs,
            output="sos",
        )
        self.bsf_zi = sosfilt_zi(self.bsf_sos)

        lpf_order = 4
        lpf_cuttoff_freq = 8000
        self.lpf_sos = butter(
            lpf_order,
            lpf_cuttoff_freq,
            btype="lowpass",
            analog=False,
            fs=fs,
            output="sos",
        )
        self.lpf_zi = sosfilt_zi(self.lpf_sos)

    def process_audio(self, data: np.ndarray):
        self.norm_rms_deque.append(np.sqrt(np.sum(data**2)))
        if len(self.norm_rms_deque) > self.norm_holdoff_frames:
            scale = np.mean(self.norm_rms_deque)
            scale = max(scale, 0.1)
            data = 2 * data / scale

        """Smooth Saturate Pedal Processing"""
        if self.on_off:
            data = np.clip(self.amount * data, -1, 1)
            data, self.hpf_zi = sosfilt(self.hpf_sos, data, zi=self.hpf_zi)
            data, self.bsf_zi = sosfilt(self.bsf_sos, data, zi=self.bsf_zi)
            data, self.lpf_zi = sosfilt(self.lpf_sos, data, zi=self.lpf_zi)

        data = self.output * data

        return data
