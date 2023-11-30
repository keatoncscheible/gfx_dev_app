from pyfx.component import PyFxComponent
from pyfx.logging import pyfx_log


class PyFxKnob(PyFxComponent):
    def __init__(
        self,
        name: str,
        minimum_value: float = 0,
        maximum_value: float = 1,
        default_value: float = 0.5,
        precision: float = 0.01,
        sensitivity: float = 1,
        mode: str = "linear",
        display_enabled: bool = False,
        value: float = 0.5,
    ):
        super().__init__()
        self.name = name
        self.minimum_value = minimum_value
        self.maximum_value = maximum_value
        self.default_value = default_value
        self.precision = precision
        self.sensitivity = sensitivity
        self.mode = mode
        self.display_enabled = display_enabled
        self.value = value
        self._set_knob_value_observers = []
        self._change_knob_name_observers = []
        self._remove_knob_observers = []

    def __reduce__(self):
        return (
            self.__class__,
            (
                self.name,
                self.minimum_value,
                self.maximum_value,
                self.default_value,
                self.precision,
                self.sensitivity,
                self.mode,
                self.display_enabled,
                self.value,
            ),
        )

    def set_minimum_value(self, value: float):
        if self.minimum_value != value:
            pyfx_log.debug(f"{self.name} knob minimum value set to {value}")
            self.minimum_value = value
            self.modified = True

    def set_maximum_value(self, value: float):
        if self.maximum_value != value:
            pyfx_log.debug(f"{self.name} knob maximum value set to {value}")
            self.maximum_value = value
            self.modified = True

    def set_default_value(self, value: float):
        if self.default_value != value:
            pyfx_log.debug(f"{self.name} knob default value set to {value}")
            self.default_value = value
            self.modified = True

    def set_precision(self, precision: float):
        if self.precision != precision:
            pyfx_log.debug(f"{self.name} knob precision set to {precision}")
            self.precision = precision
            self.modified = True

    def set_sensitivity(self, sensitivity: float):
        if self.sensitivity != sensitivity:
            pyfx_log.debug(f"{self.name} knob sensitivity set to {sensitivity}")
            self.sensitivity = sensitivity
            self.modified = True

    def set_mode(self, mode: str):
        if self.mode != mode:
            pyfx_log.debug(f"{self.name} knob mode set to {mode}")
            self.mode = mode
            self.value = self.default_value
            self.modified = True

    def set_display_enabled(self):
        if not self.display_enabled:
            pyfx_log.debug(f"Enable {self.name} knob display")
            self.display_enabled = True
            self.modified = True

    def set_display_disabled(self):
        if self.display_enabled:
            pyfx_log.debug(f"Disable {self.name} knob display")
            self.display_enabled = False
            self.modified = True

    """Set Knob Value"""

    def set_knob_value(self, value):
        if self.value != value:
            pyfx_log.debug(f"{self.name} knob set to {value}")
            self.value = value
            self.modified = True
            self.notify_set_knob_value_observers(value)

    def add_set_knob_value_observer(self, observer):
        pyfx_log.debug(
            f"Adding {self.name} knob set knob value observer: {observer.__self__.__class__.__name__}.{observer.__name__}"
        )
        self._set_knob_value_observers.append(observer)

    def remove_set_knob_value_observer(self, observer):
        pyfx_log.debug(
            f"Removing {self.name} knob set knob value observer: {observer.__self__.__class__.__name__}.{observer.__name__}"
        )
        self._set_knob_value_observers.remove(observer)

    def notify_set_knob_value_observers(self, value: float):
        for observer in self._set_knob_value_observers:
            pyfx_log.debug(
                f"Calling {self.name} knob set knob value observer: {observer.__self__.__class__.__name__}.{observer.__name__}"
            )
            observer(value)

    """Change Knob Name"""

    def change_knob_name(self, new_name: str):
        if self.name != new_name:
            old_name = self.name
            pyfx_log.debug(f"{old_name} knob name changed to {new_name}")
            self.name = new_name
            self.modified = True
            self.notify_change_knob_name_observers(old_name, new_name)

    def add_change_knob_name_observer(self, observer):
        pyfx_log.debug(
            f"Adding {self.name} knob change knob name observer: {observer.__self__.__class__.__name__}.{observer.__name__}"
        )
        self._change_knob_name_observers.append(observer)

    def remove_change_knob_name_observer(self, observer):
        pyfx_log.debug(
            f"Removing {self.name} knob change knob name observer: {observer.__self__.__class__.__name__}.{observer.__name__}"
        )
        self._change_knob_name_observers.remove(observer)

    def notify_change_knob_name_observers(self, old_name: str, new_name: str):
        for observer in self._change_knob_name_observers:
            pyfx_log.debug(
                f"Calling {self.name} knob change knob name observer: {observer.__self__.__class__.__name__}.{observer.__name__}"
            )
            observer(old_name, new_name)

    """Remove Knob"""

    def remove_knob(self):
        pyfx_log.debug(f"Removing {self.name} Knob")
        self.notify_remove_knob_observers()

    def add_remove_knob_observer(self, observer):
        pyfx_log.debug(
            f"Adding {self.name} knob remove knob observer: {observer.__self__.__class__.__name__}.{observer.__name__}"
        )
        self._remove_knob_observers.append(observer)

    def remove_remove_knob_observer(self, observer):
        pyfx_log.debug(
            f"Removing {self.name} knob remove knob observer: {observer.__self__.__class__.__name__}.{observer.__name__}"
        )
        self._remove_knob_observers.remove(observer)

    def notify_remove_knob_observers(self):
        for observer in self._remove_knob_observers:
            pyfx_log.debug(
                f"Calling {self.name} knob remove knob observer: {observer.__self__.__class__.__name__}.{observer.__name__}"
            )
            observer(self)
