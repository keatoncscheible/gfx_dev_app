import numpy as np
from PySide6.QtWidgets import QSpinBox


class FactorOf2SpinBox(QSpinBox):
    def stepBy(self, steps):  # noqa: N802
        current_value = self.value()
        if steps > 0 and current_value == 0:
            new_value = 1
        elif steps < 0 and current_value == 1:
            new_value = 0
        elif steps > 0:
            new_value = 2 ** (np.floor(np.log2(current_value)) + 1)
        else:  # steps < 0:
            new_value = 2 ** (np.ceil(np.log2(current_value)) - 1)

        self.setValue(new_value)
