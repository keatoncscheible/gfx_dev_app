import numpy as np
from pedals.volume.volume_pedal import VolumePedal


def process_audio(pedal: VolumePedal, data: np.ndarray):
    if pedal.on_off:
        data = (data * pedal.volume).astype(np.int16)

    return data
