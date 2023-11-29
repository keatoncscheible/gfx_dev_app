from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton

from pyfx.footswitch import PyFxFootswitch
from pyfx.logging import pyfx_log


class FootswitchWidget(QPushButton):
    footswitch_pressed = Signal()
    footswitch_released = Signal()
    footswitch_clicked = Signal()
    footswitch_toggled = Signal(bool)

    def __init__(self, parent):
        super().__init__(parent)

    def configure_footswitch(self, footswitch: PyFxFootswitch):
        pyfx_log.debug(f"Loading Footswitch config: {footswitch.name}")
        self.footswitch = footswitch
        footswitch_type = footswitch.footswitch_type
        try:
            self.pressed.disconnect()
        except RuntimeError:
            pass
        try:
            self.released.disconnect()
        except RuntimeError:
            pass
        try:
            self.toggled.disconnect()
        except RuntimeError:
            pass
        try:
            self.clicked.disconnect()
        except RuntimeError:
            pass

        if footswitch_type == "latching":
            self.setCheckable(True)
            self.setChecked(footswitch.state)
            self.toggled.connect(self.footswitch_toggled_cb)
        elif footswitch_type == "momentary":
            self.setCheckable(True)
            self.setChecked(footswitch.default_state)
            self.pressed.connect(self.footswitch_pressed_cb)
            self.released.connect(self.footswitch_released_cb)
        elif footswitch_type == "mode":
            self.setCheckable(False)
            self.clicked.connect(self.footswitch_clicked_cb)

    def footswitch_pressed_cb(self):
        pyfx_log.debug(f"{self.footswitch.name} pressed")
        state = not self.footswitch.default_state
        self.footswitch.set_state(state)
        self.setChecked(state)
        self.footswitch_pressed.emit()

    def footswitch_released_cb(self):
        pyfx_log.debug(f"{self.footswitch.name} released")
        state = self.footswitch.default_state
        self.footswitch.set_state(state)
        self.setChecked(state)
        self.footswitch_released.emit()

    def footswitch_toggled_cb(self, state: bool):
        state_str = "on" if state else "off"
        pyfx_log.debug(f"{self.footswitch.name} turned {state_str}")
        self.footswitch.set_state(state)
        self.footswitch_toggled.emit(state)

    def footswitch_clicked_cb(self):
        self.footswitch.next_mode()
        pyfx_log.debug(f"{self.footswitch.name} mode changed to {self.footswitch.mode}")
        self.footswitch_clicked.emit()
