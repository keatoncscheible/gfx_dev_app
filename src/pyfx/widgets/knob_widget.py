import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QContextMenuEvent
from PySide6.QtWidgets import QDial

from pyfx.knob import PyFxKnob
from pyfx.logging import pyfx_log


class KnobWidget(QDial):
    """
    A custom widget that extends QDial to implement a knob-like control.
    It is configurable for different behaviors and sensitivity settings.
    """

    def __init__(self, parent):
        """
        Initializes the knob widget with default properties and connects the valueChanged signal.
        :param parent: The parent widget.
        """
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

    def configure_knob(self, knob: PyFxKnob):
        """
        Configures the knob widget based on the properties of a PyFxKnob object.
        :param knob: The PyFxKnob instance to configure the widget.
        """
        pyfx_log.debug(f"Loading knob config: {knob.name}")
        self.knob = knob
        self.minimum_value = knob.minimum_value
        self.maximum_value = knob.maximum_value
        self.precision = knob.precision
        self.sensitivity = knob.sensitivity
        self.default_value = knob.default_value
        self.mode = knob.mode
        if self.mode == "linear":
            self.knob_value = np.clip(knob.value, self.minimum_value, self.maximum_value)
        elif self.mode == "logarithmic":
            self.knob_value = np.clip(20 * np.log10(knob.value), self.minimum_value, self.maximum_value)
        self.update_knob_settings()

    def set_knob_value(self, value: float):
        """
        Sets the knob value.
        :param value: The float value to set the knob to.
        """
        value_int = int(value / self.precision)
        self.setValue(value_int)

    def update_knob_settings(self):
        """
        Updates the knob settings like minimum, maximum values, and steps based on the current configuration.
        """
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
        """
        Calculates the float value of the knob based on the integer value from the dial.
        :param value: The integer value from the dial.
        """
        if self.mode == "linear":
            float_value = value * self.precision
        else:  # logarithmic
            float_value = 10 ** (value * self.precision / 20)
        self.knob.set_knob_value(float_value)

    def mousePressEvent(self, event):
        """
        Handles mouse press events. Right-clicks are treated as context menu events.
        :param event: The mouse event.
        """
        if event.button() == Qt.RightButton:
            context_event = QContextMenuEvent(QContextMenuEvent.Mouse, event.pos())
            super().contextMenuEvent(context_event)
        else:
            self.last_y = event.position().y()

    def mouseMoveEvent(self, event):
        """
        Handles mouse move events to adjust the knob value.
        :param event: The mouse event.
        """
        if event.buttons() & Qt.LeftButton:
            step_cnt = self.maximum_value_int - self.minimum_value_int
            knob_sensitivity_factor = step_cnt * self.sensitivity / 100
            self.delta_acc += knob_sensitivity_factor * (event.position().y() - self.last_y)
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
        """
        Handles mouse double-click events to reset the knob to its default value.
        :param event: The mouse event.
        """
        self.set_knob_value(self.default_value)

    def mouseReleaseEvent(self, event):
        """
        Handles mouse release events. Currently, this method does not perform any action.
        :param event: The mouse event.
        """
        pass
