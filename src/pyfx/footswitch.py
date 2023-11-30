from typing import Optional

from pyfx.component import PyFxComponent
from pyfx.logging import pyfx_log


class PyFxFootswitch(PyFxComponent):
    def __init__(
        self,
        name: str,
        footswitch_type: str = "latching",
        default_state: bool = True,  # noqa: FBT001, FBT002
        state: Optional[bool] = None,
        mode: Optional[str] = None,
        modes: Optional[list[str]] = None,
        display_enabled: bool = False,  # noqa: FBT001, FBT002
    ):
        super().__init__()
        self.name = name
        self.footswitch_type = footswitch_type
        self.default_state = default_state
        self.state = default_state if state is None else state
        self.modes = modes
        if mode is not None and modes is not None and mode in modes:
            self.mode = mode
            self.mode_idx = modes.index(mode)
        else:
            self.mode = None
            self.mode_idx = 0
        self.display_enabled = display_enabled
        self._change_footswitch_name_observers = []
        self._remove_footswitch_observers = []

    def __reduce__(self):
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
        valid_footswitch_types = ["latching", "momentary", "mode"]
        if footswitch_type not in valid_footswitch_types:
            msg = f"{footswitch_type} is an invalid footswitch type. Valid types are {valid_footswitch_types}"
            raise ValueError(msg)
        if self.footswitch_type != footswitch_type:
            pyfx_log.debug(f"Set {self.name} footswitch type to {footswitch_type}")
            self.footswitch_type = footswitch_type
            self.modified = True

    def set_default_state(self, state: bool):  # noqa: FBT001
        if self.default_state != state:
            pyfx_log.debug(f"Set {self.name} footswitch default state to {state}")
            self.default_state = state
            self.modified = True

    def set_state(self, state: bool):  # noqa: FBT001
        if self.state != state:
            pyfx_log.debug(f"Set {self.name} footswitch state to {state}")
            self.state = state
            self.modified = True

    def set_modes(self, modes: list[str]):
        if self.modes != modes:
            pyfx_log.debug(f"Set {self.name} footswitch modes to {modes}")
            self.modes = modes
            try:
                self.mode = self.modes[0]
                pyfx_log.debug(f"Set {self.name} footswitch mode to {self.mode}")
                self.mode_idx = 0
            except TypeError:
                self.mode = None
            self.modified = True

    def set_mode(self, mode: str):
        if self.mode != mode:
            pyfx_log.debug(f"Set {self.name} footswitch mode to {mode}")
            self.mode = mode
            self.modified = True

    def next_mode(self):
        self.mode_idx = (self.mode_idx + 1) % len(self.modes)
        self.set_mode(self.modes[self.mode_idx])

    def set_display_enabled(self):
        if not self.display_enabled:
            pyfx_log.debug(f"Enable {self.name} footswitch display")
            self.display_enabled = True
            self.modified = True

    def set_display_disabled(self):
        if self.display_enabled:
            pyfx_log.debug(f"Disable {self.name} footswitch display")
            self.display_enabled = False
            self.modified = True

    """Change Footswitch Name"""

    def change_footswitch_name(self, new_name: str):
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
        self._change_footswitch_name_observers.append(observer)

    def remove_change_footswitch_name_observer(self, observer):
        pyfx_log.debug(
            f"Removing {self.name} footswitch change footswitch name observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        self._change_footswitch_name_observers.remove(observer)

    def notify_change_footswitch_name_observers(self, old_name: str, new_name: str):
        for observer in self._change_footswitch_name_observers:
            pyfx_log.debug(
                f"Calling {self.name} footswitch change footswitch name observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
            )
            observer(old_name, new_name)

    """Remove Footswitch"""

    def remove_footswitch(self):
        pyfx_log.debug(f"Remove {self.name} footswitch")
        self.notify_remove_footswitch_observers()

    def add_remove_footswitch_observer(self, observer):
        pyfx_log.debug(
            f"Adding {self.name} footswitch remove footswitch observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        self._remove_footswitch_observers.append(observer)

    def remove_remove_footswitch_observer(self, observer):
        pyfx_log.debug(
            f"Removing {self.name} footswitch remove footswitch observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        self._remove_footswitch_observers.remove(observer)

    def notify_remove_footswitch_observers(self):
        for observer in self._remove_footswitch_observers:
            pyfx_log.debug(
                f"Calling {self.name} footswitch remove footswitch observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
            )
            observer(self)
