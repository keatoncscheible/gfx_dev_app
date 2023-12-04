from collections import deque

import numpy as np
from autogen.delay_pedal_variant_base import DelayPedalVariantBase


class DefaultDelayPedal(DelayPedalVariantBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fs = 44100
        self.buffer_size = int(self.time_max * self.fs)
        self.buffer = np.zeros(self.buffer_size)
        self.buffer_index = 0  # Current position in the buffer

    def process_audio(self, data: np.ndarray):
        """Default Delay Pedal Processing"""
        if self.on_off:
            num_samples = len(data)

            # Calculate the current delay time in samples
            current_delay_samples = int(self.time * self.fs)
            read_indices = (np.arange(num_samples) + self.buffer_index - current_delay_samples) % self.buffer_size

            # Read the delayed samples
            delayed_samples = self.buffer[read_indices]

            # Write the new samples to the buffer with feedback
            write_indices = (np.arange(num_samples) + self.buffer_index) % self.buffer_size
            self.buffer[write_indices] = data + self.feedback * delayed_samples

            # Mix the dry and wet signals
            data = (1 - self.dry_wet) * data + self.dry_wet * delayed_samples

            # Update the buffer index
            self.buffer_index = (self.buffer_index + num_samples) % self.buffer_size

            data = data * 1.4

        data = data * self.output

        return data
