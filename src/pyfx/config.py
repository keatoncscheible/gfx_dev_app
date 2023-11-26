from typing import Optional

from PySide6.QtGui import QColor

from pyfx.exceptions import (
    FootswitchAlreadyExistsException,
    FootswitchDoesNotExistException,
    KnobAlreadyExistsException,
    KnobDoesNotExistException,
)


class ConfigItem:
    def __init__(self):
        self.modified = True
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer()


class KnobConfig(ConfigItem):
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

    def set_name(self, value: str):
        if self.name != value:
            self.name = value
            self.modified = True
            self.notify_observers()

    def set_minimum_value(self, value: float):
        if self.minimum_value != value:
            self.minimum_value = value
            self.modified = True
            self.notify_observers()

    def set_maximum_value(self, value: float):
        if self.maximum_value != value:
            self.maximum_value = value
            self.modified = True
            self.notify_observers()

    def set_default_value(self, value: float):
        if self.default_value != value:
            self.default_value = value
            self.modified = True
            self.notify_observers()

    def set_precision(self, value: float):
        if self.precision != value:
            self.precision = value
            self.modified = True
            self.notify_observers()

    def set_sensitivity(self, value: float):
        if self.sensitivity != value:
            self.sensitivity = value
            self.modified = True
            self.notify_observers()

    def set_mode(self, value: str):
        if self.mode != value:
            self.mode = value
            self.value = self.default_value
            self.modified = True
            self.notify_observers()

    def set_display_enabled(self, value: bool):
        if self.display_enabled != value:
            self.display_enabled = value
            self.modified = True
            self.notify_observers()

    def set_value(self, value):
        if self.value != value:
            self.value = value
            self.modified = True
            self.notify_observers()


class FootswitchConfig(ConfigItem):
    def __init__(
        self,
        name: str,
        footswitch_type: str = "latching",
        default_state: bool = True,
        modes: Optional[list[str]] = None,
        display_enabled: bool = False,
    ):
        super().__init__()
        self.name = name
        self.footswitch_type = footswitch_type
        self.default_state = default_state
        self.state = default_state
        self.modes = modes
        self.mode = modes[0] if modes is not None else None
        self.mode_idx = 0
        self.display_enabled = display_enabled

    def set_name(self, value: str):
        if self.name != value:
            self.name = value
            self.modified = True
            self.notify_observers()

    def set_footswitch_type(self, value: str):
        valid_footswitch_types = ["latching", "momentary", "mode"]
        if value not in valid_footswitch_types:
            msg = f"{value} is an invalid footswitch type. Valid types are {valid_footswitch_types}"
            raise ValueError(msg)
        if self.footswitch_type != value:
            self.footswitch_type = value
            self.modified = True
            self.notify_observers()

    def set_default_state(self, value: bool):
        if self.default_state != value:
            self.default_state = value
            self.modified = True
            self.notify_observers()

    def set_state(self, value: bool):
        if self.state != value:
            self.state = value
            self.modified = True
            self.notify_observers()

    def set_modes(self, value: list[str]):
        if self.modes != value:
            self.modes = value
            try:
                self.mode = self.modes[0]
                self.mode_idx = 0
            except TypeError:
                self.mode = None
            self.modified = True
            self.notify_observers()

    def set_mode(self, value: str):
        if self.mode != value:
            self.mode = value
            self.modified = True
            self.notify_observers()

    def next_mode(self):
        self.mode_idx = (self.mode_idx + 1) % len(self.modes)
        self.set_mode(self.modes[self.mode_idx])

    def set_display_enabled(self, value: bool):
        if self.display_enabled != value:
            self.display_enabled = value
            self.modified = True
            self.notify_observers()


class PedalConfig(ConfigItem):
    def __init__(
        self,
        name: str,
        knobs: Optional[dict[str, KnobConfig]] = None,
        footswitches: Optional[dict[str, FootswitchConfig]] = None,
        variants: Optional[list[str]] = None,
        variant: Optional[str] = None,
        pedal_color: str = "#0000FF",
        text_color: str = "#FFFFFF",
    ):
        super().__init__()
        self.name = name
        self.knobs = knobs if knobs is not None else {}
        self.footswitches = footswitches if footswitches is not None else {}
        self.variants = variants if variants is not None else []
        self.variant = variant
        self.pedal_color = pedal_color
        self.text_color = text_color

    def set_name(self, value: str):
        if self.name != value:
            self.name = value
            self.modified = True
            self.notify_observers()

    def add_knob(self, name: str):
        if name in self.knobs:
            raise KnobAlreadyExistsException()
        self.knobs[name] = KnobConfig(name)
        self.modified = True
        self.notify_observers()

    def remove_knob(self, name: str):
        if name not in self.knobs:
            raise KnobDoesNotExistException()
        del self.knobs[name]
        self.modified = True
        self.notify_observers()

    def change_knob_name(self, old_name: str, new_name: str):
        self.knobs[new_name] = self.knobs[old_name]
        self.knobs[new_name].set_name(new_name)
        del self.knobs[old_name]
        self.modified = True

    def add_footswitch(self, name: str):
        if name in self.footswitches:
            raise FootswitchAlreadyExistsException()
        self.footswitches[name] = FootswitchConfig(name)
        self.modified = True
        self.notify_observers()

    def remove_footswitch(self, name: str):
        if name not in self.footswitches:
            raise FootswitchDoesNotExistException()
        del self.footswitches[name]
        self.modified = True
        self.notify_observers()

    def change_footswitch_name(self, old_name: str, new_name: str):
        self.footswitches[new_name] = self.footswitches[old_name]
        self.footswitches[new_name].set_name(new_name)
        del self.footswitches[old_name]
        self.modified = True

    def set_variant(self, value: str):
        if self.variant != value:
            self.variant = value
            self.modified = True
            self.notify_observers()

    def add_variant(self, value: str):
        if value not in self.variants:
            self.variants.append(value)
            self.variant = value
            self.modified = True
            self.notify_observers()

    def remove_variant(self, value: str):
        if value in self.variants:
            self.variants.remove(value)
            if self.variant == value:
                self.variant = None
            self.modified = True
            self.notify_observers()

    def set_pedal_color(self, value: QColor):
        if self.pedal_color != value:
            self.pedal_color = value
            self.modified = True

    def set_text_color(self, value: QColor):
        if self.text_color != value:
            self.text_color = value
            self.modified = True

    @property
    def config_items(self):
        config_items = [self]
        config_items.extend(list(self.knobs.values()))
        config_items.extend(list(self.footswitches.values()))
        return config_items

    @property
    def is_modified(self):
        return any(config_item.modified for config_item in self.config_items)

    def reset_modified_flags(self):
        if self.is_modified:
            for config_item in self.config_items:
                config_item.modified = False
