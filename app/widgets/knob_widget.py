from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDial


class KnobWidget(QDial):
    knob_changed = Signal(float)

    def __init__(self, parent=None, precision: int = 2, sensitivity: float = 0.5):
        super().__init__(parent)
        self.last_y = 0
        self.sensitivity = sensitivity
        self.set_precision(precision)
        self.setFixedSize(75, 75)
        self.valueChanged.connect(self.calc_knob_value)
        self.original_palette = self.palette()
        self.wrap_around = False

    def mousePressEvent(self, event):
        self.last_y = event.position().y()

    def mouseMoveEvent(self, event):
        delta = self.sensitivity * (event.position().y() - self.last_y)
        self.last_y = event.position().y()
        new_value = self.value() - int(delta)
        if self.wrap_around:
            new_value = new_value % (self.maximum() + 1)
        else:
            new_value = max(min(new_value, self.maximum()), self.minimum())
        self.setValue(new_value)

    def mouseReleaseEvent(self, event):
        self.last_y = 0

    def set_precision(self, precision: int):
        if precision < 0:
            raise ValueError("Precision must be a non-negative integer")
        max_value = 10**precision
        self.scale_fact = 1 / max_value
        self.setMaximum(max_value)

    def set_value(self, value: float):
        if not (0 <= value <= 1):
            raise ValueError("Value must be within the range [0, 1]")
        self.setValue(int(value * self.maximum()))

    def calc_knob_value(self, value):
        float_value = value * self.scale_fact
        self.knob_changed.emit(float_value)

    def setWrapAround(self, enable: bool):
        self.wrap_around = enable
