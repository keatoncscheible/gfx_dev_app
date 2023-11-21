from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDial


class KnobWidget(QDial):
    knob_changed = Signal(float)

    def __init__(self, parent, precision: int = 2):
        """Knob widget that outputs floating point

        Args:
            precision:  number of decimal places to use, ie. precision=2 --> 0.00 to 1.00
        """
        super().__init__()
        self.precision = self.set_precision(precision)
        self.setMinimum(0)
        self.setFixedSize(75, 75)
        self.valueChanged.connect(self.calc_knob_value)

    def set_precision(self, precision: int):
        max_value = 10**precision
        self.scale_fact = 1 / max_value
        self.setMaximum(max_value)

    def set_value(self, value: float):
        if value < 0 or value > 1:
            raise ValueError("The value of KnobWidget must be within the range [0, 1]")
        self.setValue(int(value * self.maximum()))

    def calc_knob_value(self, value):
        float_value = value * self.scale_fact
        self.knob_changed.emit(float_value)
