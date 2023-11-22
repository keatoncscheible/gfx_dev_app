import numpy as np
from pedals.saturate.saturate_pedal import SaturatePedal


def process_audio(pedal: SaturatePedal, data: np.ndarray):
    if pedal.on_off:
        saturation_factor = 15
        scale = saturation_factor * pedal.amount + 1
        data = np.clip(data * scale, -32768, 32767).astype(np.int16)

    return data
