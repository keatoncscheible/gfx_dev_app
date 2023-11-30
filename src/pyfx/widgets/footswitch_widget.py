from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton

from pyfx.footswitch import PyFxFootswitch
from pyfx.logging import pyfx_log


class FootswitchWidget(QPushButton):
    """
    A custom widget that extends QPushButton to implement a footswitch-like control.
    It emits custom signals to represent various footswitch actions.
    """

    # Custom signals for different footswitch actions
    footswitch_pressed = Signal()
    footswitch_released = Signal()
    footswitch_clicked = Signal()
    footswitch_toggled = Signal(bool)

    def __init__(self, parent):
        """
        Initializes the footswitch widget.
        :param parent: The parent widget.
        """
        super().__init__(parent)

    def configure_footswitch(self, footswitch: PyFxFootswitch):
        """
        Configures the footswitch widget based on the properties of a PyFxFootswitch object.
        :param footswitch: The PyFxFootswitch instance to configure the widget.
        """
        pyfx_log.debug(f"Loading Footswitch config: {footswitch.name}")
        self.footswitch = footswitch
        footswitch_type = footswitch.footswitch_type

        # Disconnect existing signals to avoid multiple connections
        self._disconnect_signals()

        # Configure based on footswitch type
        if footswitch_type == "latching":
            self._configure_latching(footswitch)
        elif footswitch_type == "momentary":
            self._configure_momentary(footswitch)
        elif footswitch_type == "mode":
            self._configure_mode()

    def _disconnect_signals(self):
        """
        Helper method to disconnect signals to prevent multiple connections.
        """
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

    def _configure_latching(self, footswitch: PyFxFootswitch):
        """
        Configures the widget for latching footswitches.
        :param footswitch: The PyFxFootswitch instance.
        """
        self.setCheckable(True)
        self.setChecked(footswitch.state)
        self.toggled.connect(self.footswitch_toggled_cb)

    def _configure_momentary(self, footswitch: PyFxFootswitch):
        """
        Configures the widget for momentary footswitches.
        :param footswitch: The PyFxFootswitch instance.
        """
        self.setCheckable(True)
        self.setChecked(footswitch.default_state)
        self.pressed.connect(self.footswitch_pressed_cb)
        self.released.connect(self.footswitch_released_cb)

    def _configure_mode(self):
        """
        Configures the widget for mode-switching footswitches.
        :param footswitch: The PyFxFootswitch instance.
        """
        self.setCheckable(False)
        self.clicked.connect(self.footswitch_clicked_cb)

    def footswitch_pressed_cb(self):
        """
        Callback for when the footswitch is pressed.
        """
        pyfx_log.debug(f"{self.footswitch.name} pressed")
        state = not self.footswitch.default_state
        self.footswitch.set_state(state)
        self.setChecked(state)
        self.footswitch_pressed.emit()

    def footswitch_released_cb(self):
        """
        Callback for when the footswitch is released.
        """
        pyfx_log.debug(f"{self.footswitch.name} released")
        state = self.footswitch.default_state
        self.footswitch.set_state(state)
        self.setChecked(state)
        self.footswitch_released.emit()

    def footswitch_toggled_cb(self, state: bool):  # noqa: FBT001
        """
        Callback for when the footswitch state is toggled.
        :param state: The new state of the footswitch.
        """
        state_str = "on" if state else "off"
        pyfx_log.debug(f"{self.footswitch.name} turned {state_str}")
        self.footswitch.set_state(state)
        self.footswitch_toggled.emit(state)

    def footswitch_clicked_cb(self):
        """
        Callback for when the footswitch is clicked.
        """
        self.footswitch.next_mode()
        pyfx_log.debug(f"{self.footswitch.name} mode changed to {self.footswitch.mode}")
        self.footswitch_clicked.emit()
