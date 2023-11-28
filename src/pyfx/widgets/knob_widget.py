import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QContextMenuEvent
from PySide6.QtWidgets import QDial

from pyfx.config import KnobConfig
from pyfx.logging import pyfx_log


class KnobWidget(QDial):
    def __init__(self, parent):
        super().__init__(parent)
        self.minimum_value = None
        self.maximum_value = None
        self.precision = None
        self.sensitivity = None
        self.default_value = None
        self.mode = None
        self.knob_value = None
        self.last_y = 0
        self.delta_acc = 0
        self.setFixedSize(75, 75)
        self.valueChanged.connect(self.calc_knob_value)

    def load_knob_config(self, knob_config: KnobConfig):
        pyfx_log.debug(f"Loading knob config: {knob_config.name}")
        self.knob_config = knob_config
        self.minimum_value = knob_config.minimum_value
        self.maximum_value = knob_config.maximum_value
        self.precision = knob_config.precision
        self.sensitivity = knob_config.sensitivity
        self.default_value = knob_config.default_value
        self.mode = knob_config.mode
        self.knob_value = np.clip(knob_config.value, self.minimum_value, self.maximum_value)
        self.update_knob_settings()

    def set_knob_value(self, value: float):
        value_int = int(value / self.precision)
        self.setValue(value_int)

    def update_knob_settings(self):
        self.minimum_value_int = int(self.minimum_value / self.precision)
        self.maximum_value_int = int(self.maximum_value / self.precision)
        single_step = self.sensitivity
        page_step = 10 * self.sensitivity
        self.setMinimum(self.minimum_value_int)
        self.setMaximum(self.maximum_value_int)
        self.setSingleStep(single_step)
        self.setPageStep(page_step)
        self.set_knob_value(self.knob_value)

    def calc_knob_value(self, value: int):
        if self.mode == "linear":
            float_value = value * self.precision
        else:  # logarithmic
            float_value = 10 ** (value * self.precision / 20)
        self.knob_config.set_value(float_value)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            context_event = QContextMenuEvent(QContextMenuEvent.Mouse, event.pos())
            super().contextMenuEvent(context_event)
        else:
            self.last_y = event.position().y()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            step_cnt = self.maximum_value_int - self.minimum_value_int
            knob_sensitifity_factor = step_cnt * self.sensitivity / 100
            self.delta_acc += knob_sensitifity_factor * (event.position().y() - self.last_y)
            self.last_y = event.position().y()
            delta = int(self.delta_acc)
            self.delta_acc -= delta
            current_value = self.value()
            new_value = np.clip(
                current_value - int(delta),
                self.minimum_value_int,
                self.maximum_value_int,
            )
            if current_value == new_value:
                return
            self.setValue(new_value)

    def mouseDoubleClickEvent(self, event):
        self.set_knob_value(self.default_value)

    def mouseReleaseEvent(self, event):
        """Ignore the mouseReleaseEvent"""