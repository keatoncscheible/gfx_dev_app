from pyfx.component import PyFxComponent
from pyfx.logging import pyfx_log


class PyFxKnob(PyFxComponent):
    """
    Represents a knob component in the PyFx system, managing its value, range, sensitivity, mode, and display settings.

    Attributes:
        name (str): The name of the knob.
        minimum_value (float): The minimum value the knob can hold. Defaults to 0.
        maximum_value (float): The maximum value the knob can hold. Defaults to 1.
        default_value (float): The default value of the knob. Defaults to 0.5.
        precision (float): The precision of the knob value changes. Defaults to 0.01.
        sensitivity (float): The sensitivity of the knob. Defaults to 1.
        mode (str): The mode of the knob operation ('linear' by default).
        display_enabled (bool): Flag indicating if the display is enabled. Defaults to False.
        value (float): The current value of the knob. Defaults to 0.5.
    """

    def __init__(
        self,
        name: str,
        minimum_value: float = 0,
        maximum_value: float = 1,
        default_value: float = 0.5,
        precision: float = 0.01,
        sensitivity: float = 1,
        mode: str = "linear",
        display_enabled: bool = False,  # noqa: FBT001, FBT002
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
        """
        Supports the pickle protocol. Returns a tuple with the class and its arguments.
        """
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
        """
        Sets the minimum value of the knob.

        Args:
            value (float): The new minimum value to be set.
        """
        if self.minimum_value != value:
            pyfx_log.debug(f"{self.name} knob minimum value set to {value}")
            self.minimum_value = value
            self.modified = True

    def set_maximum_value(self, value: float):
        """
        Sets the maximum value of the knob.

        Args:
            value (float): The new maximum value to be set.
        """
        if self.maximum_value != value:
            pyfx_log.debug(f"{self.name} knob maximum value set to {value}")
            self.maximum_value = value
            self.modified = True

    def set_default_value(self, value: float):
        """
        Sets the default value of the knob.

        Args:
            value (float): The new default value to be set.
        """
        if self.default_value != value:
            pyfx_log.debug(f"{self.name} knob default value set to {value}")
            self.default_value = value
            self.modified = True

    def set_precision(self, precision: float):
        """
        Sets the precision of the knob.

        Args:
            precision (float): The new precision value to be set.
        """
        if self.precision != precision:
            pyfx_log.debug(f"{self.name} knob precision set to {precision}")
            self.precision = precision
            self.modified = True

    def set_sensitivity(self, sensitivity: float):
        """
        Sets the sensitivity of the knob.

        Args:
            sensitivity (float): The new sensitivity value to be set.
        """
        if self.sensitivity != sensitivity:
            pyfx_log.debug(f"{self.name} knob sensitivity set to {sensitivity}")
            self.sensitivity = sensitivity
            self.modified = True

    def set_mode(self, mode: str):
        """
        Sets the mode of the knob.

        Args:
            mode (str): The new mode to be set.
        """
        if self.mode != mode:
            pyfx_log.debug(f"{self.name} knob mode set to {mode}")
            self.mode = mode
            self.value = self.default_value
            self.modified = True

    def set_display_enabled(self):
        """
        Enables the display for the knob.
        """
        if not self.display_enabled:
            pyfx_log.debug(f"Enable {self.name} knob display")
            self.display_enabled = True
            self.modified = True

    def set_display_disabled(self):
        """
        Disables the display for the knob.
        """
        if self.display_enabled:
            pyfx_log.debug(f"Disable {self.name} knob display")
            self.display_enabled = False
            self.modified = True

    def set_knob_value(self, value: float):
        """
        Sets the value of the knob.

        Args:
            value (float): The new value to be set for the knob.
        """
        if self.value != value:
            pyfx_log.debug(f"{self.name} knob set to {value}")
            self.value = value
            self.modified = True
            self.notify_set_knob_value_observers(value)

    def add_set_knob_value_observer(self, observer):
        pyfx_log.debug(
            f"Adding {self.name} knob set knob value observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        """
        Adds an observer for the knob value set event.

        Args:
            observer: The observer function to be added.
        """
        self._set_knob_value_observers.append(observer)

    def remove_set_knob_value_observer(self, observer):
        pyfx_log.debug(
            f"Removing {self.name} knob set knob value observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        """
        Removes an observer for the knob value set event.

        Args:
            observer: The observer function to be removed.
        """
        self._set_knob_value_observers.remove(observer)

    def notify_set_knob_value_observers(self, value: float):
        """
        Notifies all observers about the knob value set event.

        Args:
            value (float): The value that has been set.
        """
        for observer in self._set_knob_value_observers:
            pyfx_log.debug(
                f"Calling {self.name} knob set knob value observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
            )
            observer(value)

    def change_knob_name(self, new_name: str):
        """
        Changes the name of the knob and notifies the observers.

        Args:
            new_name (str): The new name to be set for the knob.
        """
        if self.name != new_name:
            old_name = self.name
            pyfx_log.debug(f"{old_name} knob name changed to {new_name}")
            self.name = new_name
            self.modified = True
            self.notify_change_knob_name_observers(old_name, new_name)

    def add_change_knob_name_observer(self, observer):
        pyfx_log.debug(
            f"Adding {self.name} knob change knob name observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        """
        Adds an observer for the knob name change event.

        Args:
            observer: The observer function to be added.
        """
        self._change_knob_name_observers.append(observer)

    def remove_change_knob_name_observer(self, observer):
        pyfx_log.debug(
            f"Removing {self.name} knob change knob name observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        """
        Removes an observer for the knob name change event.

        Args:
            observer: The observer function to be removed.
        """
        self._change_knob_name_observers.remove(observer)

    def notify_change_knob_name_observers(self, old_name: str, new_name: str):
        """
        Notifies all observers about the knob name change event.

        Args:
            old_name (str): The old name of the knob.
            new_name (str): The new name of the knob.
        """
        for observer in self._change_knob_name_observers:
            pyfx_log.debug(
                f"Calling {self.name} knob change knob name observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
            )
            observer(old_name, new_name)

    def remove_knob(self):
        """
        Removes the knob and notifies the observers.
        """
        pyfx_log.debug(f"Removing {self.name} Knob")
        self.notify_remove_knob_observers()

    def add_remove_knob_observer(self, observer):
        pyfx_log.debug(
            f"Adding {self.name} knob remove knob observer: {observer.__self__.__class__.__name__}.{observer.__name__}"
        )
        """
        Adds an observer for the knob removal event.

        Args:
            observer: The observer function to be added.
        """
        self._remove_knob_observers.append(observer)

    def remove_remove_knob_observer(self, observer):
        pyfx_log.debug(
            f"Removing {self.name} knob remove knob observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        """
        Removes an observer for the knob removal event.

        Args:
            observer: The observer function to be removed.
        """
        self._remove_knob_observers.remove(observer)

    def notify_remove_knob_observers(self):
        """
        Notifies all observers about the knob removal.

        Args:
            observer: The observer function that was notified.
        """
        for observer in self._remove_knob_observers:
            pyfx_log.debug(
                f"Calling {self.name} knob remove knob observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
            )
            observer(self)
