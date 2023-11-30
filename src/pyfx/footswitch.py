from typing import Optional

from pyfx.component import PyFxComponent
from pyfx.logging import pyfx_log


class PyFxFootswitch(PyFxComponent):
    """
    Represents a footswitch component in the PyFx system, managing its type, state, modes, and display settings.

    Attributes:
        name (str): The name of the footswitch.
        footswitch_type (str): Type of the footswitch. Defaults to 'latching'.
        default_state (bool): The default state of the footswitch. Defaults to True.
        state (bool): The current state of the footswitch.
        mode (Optional[str]): The current mode of the footswitch, if applicable.
        modes (Optional[list[str]]): A list of available modes for the footswitch.
        display_enabled (bool): Indicates whether the footswitch display is enabled. Defaults to False.
    """

    def __init__(
        self,
        name: str,
        footswitch_type: str = "latching",
        default_state: bool = True,  # noqa: FBT001, FBT002
        state: Optional[bool] = None,
        mode: Optional[str] = None,
        modes: Optional[list[str]] = None,
        display_enabled: bool = False,  # noqa: FBT002, FBT001
    ):
        super().__init__()
        self.name = name
        self.footswitch_type = footswitch_type
        self.default_state = default_state
        self.state = default_state if state is None else state
        self.modes = modes or []
        self.mode = mode if mode in self.modes else None
        self.mode_idx = self.modes.index(mode) if self.mode else 0
        self.display_enabled = display_enabled
        self._change_footswitch_name_observers = []
        self._remove_footswitch_observers = []

    def __reduce__(self):
        """
        Supports the pickle protocol. Returns a tuple with the class and its arguments.
        """
        return (
            self.__class__,
            (
                self.name,
                self.footswitch_type,
                self.default_state,
                self.state,
                self.mode,
                self.modes,
                self.display_enabled,
            ),
        )

    def set_footswitch_type(self, footswitch_type: str):
        """
        Sets the footswitch type.

        Args:
            footswitch_type (str): The new footswitch type to be set.

        Raises:
            ValueError: If an invalid footswitch type is provided.
        """
        valid_footswitch_types = ["latching", "momentary", "mode"]
        if footswitch_type not in valid_footswitch_types:
            msg = f"{footswitch_type} is an invalid footswitch type. Valid types are {valid_footswitch_types}"
            raise ValueError(msg)
        if self.footswitch_type != footswitch_type:
            pyfx_log.debug(f"Set {self.name} footswitch type to {footswitch_type}")
            self.footswitch_type = footswitch_type
            self.modified = True

    def set_default_state(self, state: bool):  # noqa: FBT001
        """
        Sets the default state of the footswitch.

        Args:
            state (bool): The new default state to be set.
        """
        if self.default_state != state:
            pyfx_log.debug(f"Set {self.name} footswitch default state to {state}")
            self.default_state = state
            self.modified = True

    def set_state(self, state: bool):  # noqa: FBT001
        """
        Sets the current state of the footswitch.

        Args:
            state (bool): The new state to be set.
        """
        if self.state != state:
            pyfx_log.debug(f"Set {self.name} footswitch state to {state}")
            self.state = state
            self.modified = True

    def set_modes(self, modes: list[str]):
        """
        Sets the available modes for the footswitch.

        Args:
            modes (list[str]): The list of modes to be set for the footswitch.
        """
        if self.modes != modes:
            pyfx_log.debug(f"Set {self.name} footswitch modes to {modes}")
            self.modes = modes
            try:
                self.mode = self.modes[0]
                pyfx_log.debug(f"Set {self.name} footswitch mode to {self.mode}")
                self.mode_idx = 0
            except IndexError:
                self.mode = None
            self.modified = True

    def set_mode(self, mode: str):
        """
        Sets the current mode of the footswitch.

        Args:
            mode (str): The mode to be set as current.
        """
        if self.mode != mode:
            pyfx_log.debug(f"Set {self.name} footswitch mode to {mode}")
            self.mode = mode
            self.modified = True

    def next_mode(self):
        """
        Advances the footswitch to the next mode in the list of available modes.
        """
        if self.modes:
            self.mode_idx = (self.mode_idx + 1) % len(self.modes)
            self.set_mode(self.modes[self.mode_idx])

    def set_display_enabled(self):
        """
        Enables the display of the footswitch.
        """
        if not self.display_enabled:
            pyfx_log.debug(f"Enable {self.name} footswitch display")
            self.display_enabled = True
            self.modified = True

    def set_display_disabled(self):
        """
        Disables the display of the footswitch.
        """
        if self.display_enabled:
            pyfx_log.debug(f"Disable {self.name} footswitch display")
            self.display_enabled = False
            self.modified = True

    def change_footswitch_name(self, new_name: str):
        """
        Changes the name of the footswitch and notifies the observers.

        Args:
            new_name (str): The new name to be set for the footswitch.
        """
        if self.name != new_name:
            old_name = self.name
            pyfx_log.debug(f"{old_name} footswitch name changed to {new_name}")
            self.name = new_name
            self.modified = True
            self.notify_change_footswitch_name_observers(old_name, new_name)
            pyfx_log.debug(f"Footswitch name changed from {old_name} to {new_name}")

    def add_change_footswitch_name_observer(self, observer):
        pyfx_log.debug(
            f"Adding {self.name} footswitch change footswitch name observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        """
        Adds an observer for the footswitch name change event.

        Args:
            observer: The observer function to be added.
        """
        self._change_footswitch_name_observers.append(observer)

    def remove_change_footswitch_name_observer(self, observer):
        pyfx_log.debug(
            f"Removing {self.name} footswitch change footswitch name observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        """
        Removes an observer for the footswitch name change event.

        Args:
            observer: The observer function to be removed.
        """
        self._change_footswitch_name_observers.remove(observer)

    def notify_change_footswitch_name_observers(self, old_name: str, new_name: str):
        """
        Notifies all observers about the footswitch name change.

        Args:
            old_name (str): The old name of the footswitch.
            new_name (str): The new name of the footswitch.
        """
        for observer in self._change_footswitch_name_observers:
            pyfx_log.debug(
                f"Calling {self.name} footswitch change footswitch name observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
            )
            observer(old_name, new_name)

    def remove_footswitch(self):
        """
        Removes the footswitch and notifies the observers.
        """
        pyfx_log.debug(f"Remove {self.name} footswitch")
        self.notify_remove_footswitch_observers()

    def add_remove_footswitch_observer(self, observer):
        pyfx_log.debug(
            f"Adding {self.name} footswitch remove footswitch observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        """
        Adds an observer for the footswitch removal event.

        Args:
            observer: The observer function to be added.
        """
        self._remove_footswitch_observers.append(observer)

    def remove_remove_footswitch_observer(self, observer):
        pyfx_log.debug(
            f"Removing {self.name} footswitch remove footswitch observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        """
        Removes an observer for the footswitch removal event.

        Args:
            observer: The observer function to be removed.
        """
        self._remove_footswitch_observers.remove(observer)

    def notify_remove_footswitch_observers(self):
        """
        Notifies all observers about the footswitch removal.
        """
        for observer in self._remove_footswitch_observers:
            pyfx_log.debug(
                f"Calling {self.name} footswitch remove footswitch observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
            )
            observer(self)
