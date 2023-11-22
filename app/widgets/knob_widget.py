import numpy as np
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QDial, QMenu


class KnobWidget(QDial):
    knob_changed = Signal(float)

    def __init__(
        self,
        parent=None,
        range: list[float, float] = [0, 1],
        precision: float = 0.01,
        sensitivity: float = 1,
        default_value: float = None,
        mode="linear",
    ):
        super().__init__(parent)
        self.min_value, self.max_value = range
        self.precision = precision
        self.sensitivity = sensitivity
        if default_value is None:
            self.default_value = np.mean(range)
        self.mode = mode  # 'linear' or 'logarithmic'
        self.knob_value = self.default_value
        self.update_knob_settings()
        self.last_y = 0
        self.delta_acc = 0
        self.setFixedSize(75, 75)
        self.valueChanged.connect(self.calc_knob_value)

    def set_range(self, range: list[float, float]):
        self.min_value, self.max_value = range
        self.update_knob_settings()

    def set_precision(self, precision: float):
        self.precision = precision
        self.update_knob_settings()

    def set_sensitivity(self, sensitivity: float):
        self.sensitivity = sensitivity
        self.update_knob_settings()

    def set_mode(self, mode):
        if mode not in ["linear", "logarithmic"]:
            raise ValueError("Mode must be either 'linear' or 'logarithmic'")
        self.mode = mode
        self.update_knob_settings()

    def set_knob_value(self, value: float):
        if self.mode == "logarithmic":
            value = 20 * np.log10(value)

        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                "Value must be within the range [{}, {}]".format(
                    self.min_value, self.max_value
                )
            )
        value_int = int(value / self.precision)
        self.setValue(value_int)

    def update_knob_settings(self):
        self.min_value_int = int(self.min_value / self.precision)
        self.max_value_int = int(self.max_value / self.precision)
        single_step = self.sensitivity
        page_step = 10 * self.sensitivity
        self.setMinimum(self.min_value_int)
        self.setMaximum(self.max_value_int)
        self.setSingleStep(single_step)
        self.setPageStep(page_step)
        self.set_knob_value(self.knob_value)

    def calc_knob_value(self, value: int):
        if self.mode == "linear":
            float_value = value * self.precision
        else:  # logarithmic
            float_value = 10 ** (value * self.precision / 20)
        self.knob_changed.emit(float_value)

    def open_context_menu(self, event):
        menu = QMenu(self)
        configure_action = menu.addAction("Configure Knob")
        action = menu.exec_(self.mapToGlobal(event.position().toPoint()))
        if action == configure_action:
            print("Configure Knob clicked")

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.open_context_menu(event)
        else:
            self.last_y = event.position().y()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            step_cnt = self.max_value_int - self.min_value_int
            knob_sensitifity_factor = step_cnt * self.sensitivity / 100
            self.delta_acc += knob_sensitifity_factor * (
                event.position().y() - self.last_y
            )
            self.last_y = event.position().y()
            delta = int(self.delta_acc)
            self.delta_acc -= delta
            current_value = self.value()
            new_value = np.clip(
                current_value - int(delta), self.min_value_int, self.max_value_int
            )
            if current_value == new_value:
                return
            self.setValue(new_value)

    def mouseDoubleClickEvent(self, event):
        self.set_knob_value(self.default_value)

    def mouseReleaseEvent(self, event):
        """Ignore the mouseReleaseEvent"""
