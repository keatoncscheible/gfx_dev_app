from typing import Optional

from pyfx.exceptions import (
    FootswitchAlreadyExistsException,
    FootswitchDoesNotExistException,
    KnobAlreadyExistsException,
    KnobDoesNotExistException,
)
from pyfx.logging import pyfx_log


class ConfigItem:
    def __init__(self):
        self.modified = True


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

    def set_display_enabled(self, enable: bool):
        if self.display_enabled != enable:
            self.display_enabled = enable
            self.modified = True

    def set_value(self, value):
        if self.value != value:
            pyfx_log.debug(f"{self.name} knob set to {value}")
            self.value = value
            self.modified = True

    """Change Knob Name"""

    def change_knob_name(self, new_name: str):
        if self.name != new_name:
            old_name = self.name
            pyfx_log.debug(f"{old_name} knob name changed to {new_name}")
            self.name = new_name
            self.modified = True
            self.notify_change_knob_name_observers(old_name, new_name)

    def add_change_knob_name_observer(self, observer):
        self._change_knob_name_observers.append(observer)

    def remove_change_knob_name_observer(self, observer):
        self._change_knob_name_observers.remove(observer)

    def notify_change_knob_name_observers(self, old_name: str, new_name: str):
        for observer in self._change_knob_name_observers:
            observer(old_name, new_name)

    """Remove Knob"""

    def remove_knob(self):
        pyfx_log.debug(f"Removing {self.name} Knob")
        self.notify_remove_knob_observers()

    def add_remove_knob_observer(self, observer):
        self._remove_knob_observers.append(observer)

    def remove_remove_knob_observer(self, observer):
        self._remove_knob_observers.remov(observer)

    def notify_remove_knob_observers(self):
        for observer in self._remove_knob_observers:
            observer(self)


class FootswitchConfig(ConfigItem):
    def __init__(
        self,
        name: str,
        footswitch_type: str = "latching",
        default_state: bool = True,
        state: bool = None,
        mode: Optional[str] = None,
        modes: Optional[list[str]] = None,
        display_enabled: bool = False,
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

    def set_default_state(self, state: bool):
        if self.default_state != state:
            pyfx_log.debug(f"Set {self.name} footswitch default state to {state}")
            self.default_state = state
            self.modified = True

    def set_state(self, state: bool):
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

    def set_display_enabled(self, enable: bool):
        if self.display_enabled != enable:
            pyfx_log.debug(f"{'Enable' if enable else 'Disable'} {self.name} footswitch display")
            self.display_enabled = enable
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
        self._change_footswitch_name_observers.append(observer)

    def remove_change_footswitch_name_observer(self, observer):
        self._change_footswitch_name_observers.remove(observer)

    def notify_change_footswitch_name_observers(self, old_name: str, new_name: str):
        for observer in self._change_footswitch_name_observers:
            observer(old_name, new_name)

    """Remove Footswitch"""

    def remove_footswitch(self):
        pyfx_log.debug(f"Remove {self.name} footswitch")
        self.notify_remove_footswitch_observers()

    def add_remove_footswitch_observer(self, observer):
        self._remove_footswitch_observers.append(observer)

    def remove_remove_footswitch_observer(self, observer):
        self._remove_footswitch_observers.remov(observer)

    def notify_remove_footswitch_observers(self):
        for observer in self._remove_footswitch_observers:
            observer(self)


class PedalConfig(ConfigItem):
    def __init__(
        self,
        name: str,
        knobs: Optional[dict[str, KnobConfig]] = None,
        footswitches: Optional[dict[str, FootswitchConfig]] = None,
        variant: Optional[str] = None,
        variants: Optional[list[str]] = None,
        pedal_color: str = "#0000FF",
        text_color: str = "#FFFFFF",
    ):
        super().__init__()
        self.name = name
        self.knobs = knobs if knobs is not None else {}
        self.footswitches = footswitches if footswitches is not None else {}
        self.variant = variant
        self.variants = variants if variants is not None else []
        self.pedal_color = pedal_color
        self.text_color = text_color
        self._change_pedal_name_observers = []
        self._add_knob_observers = []
        self._remove_knob_observers = []
        self._change_knob_name_observers = []
        self._add_footswitch_observers = []
        self._remove_footswitch_observers = []
        self._change_footswitch_name_observers = []
        self._set_variant_observers = []
        self._add_variant_observers = []
        self._remove_variant_observers = []
        self._change_variant_name_observers = []
        self._set_pedal_color_observers = []
        self._set_text_color_observers = []

    def __reduce__(self):
        return (
            self.__class__,
            (
                self.name,
                self.knobs,
                self.footswitches,
                self.variant,
                self.variants,
                self.pedal_color,
                self.text_color,
            ),
        )

    """Change Name"""

    def change_pedal_name(self, new_name: str):
        if self.name != new_name:
            old_name = self.name
            pyfx_log.debug(f"{old_name} pedal name changed to {new_name}")
            self.name = new_name
            self.modified = True
            self.notify_change_pedal_name_observers(old_name, new_name)

    def add_change_pedal_name_observer(self, observer):
        self._change_pedal_name_observers.append(observer)

    def remove_change_pedal_name_observer(self, observer):
        self._change_pedal_name_observers.remove(observer)

    def notify_change_pedal_name_observers(self, old_name: str, new_name: str):
        for observer in self._change_pedal_name_observers:
            observer(old_name, new_name)

    """Add Knob"""

    def add_knob(self, name: str):
        if name in self.knobs:
            raise KnobAlreadyExistsException()
        pyfx_log.debug(f"Add {name} knob to {self.name} pedal")
        knob_config = KnobConfig(name)
        knob_config.add_remove_knob_observer(self.remove_knob)
        self.knobs[name] = knob_config
        self.modified = True
        self.notify_add_knob_observers(knob_config)

    def add_add_knob_observer(self, observer):
        self._add_knob_observers.append(observer)

    def remove_add_knob_observer(self, observer):
        self._add_knob_observers.remove(observer)

    def notify_add_knob_observers(self, knob_config: KnobConfig):
        for observer in self._add_knob_observers:
            observer(knob_config)

    """Remove Knob"""

    def remove_knob(self, knob_config: KnobConfig):
        try:
            del self.knobs[knob_config.name]
        except KeyError as err:
            raise KnobDoesNotExistException() from err
        pyfx_log.debug(f"Remove {knob_config.name} knob from {self.name} pedal")
        self.modified = True
        self.notify_remove_knob_observers(knob_config)

    def add_remove_knob_observer(self, observer):
        self._remove_knob_observers.append(observer)

    def remove_remove_knob_observer(self, observer):
        self._remove_knob_observers.remove(observer)

    def notify_remove_knob_observers(self, knob_config: KnobConfig):
        for observer in self._remove_knob_observers:
            observer(knob_config)

    """Change Knob Name"""

    def change_knob_name(self, old_name: str, new_name: str):
        self.knobs[new_name] = self.knobs[old_name]
        self.knobs[new_name].change_knob_name(new_name)
        del self.knobs[old_name]
        self.modified = True
        self.notify_change_knob_name_observers(old_name, new_name)

    def add_change_knob_name_observer(self, observer):
        self._change_knob_name_observers.append(observer)

    def remove_change_knob_name_observer(self, observer):
        self._change_knob_name_observers.remove(observer)

    def notify_change_knob_name_observers(self, old_name: str, new_name: str):
        for observer in self._change_knob_name_observers:
            observer(old_name, new_name)

    """Add Footswitch"""

    def add_footswitch(self, name: str):
        if name in self.footswitches:
            raise FootswitchAlreadyExistsException()
        pyfx_log.debug(f"Add {name} footswitch to {self.name} pedal")
        footswitch_config = FootswitchConfig(name)
        footswitch_config.add_remove_footswitch_observer(self.remove_footswitch)
        self.footswitches[name] = footswitch_config
        self.modified = True
        self.notify_add_footswitch_observers(footswitch_config)

    def add_add_footswitch_observer(self, observer):
        self._add_footswitch_observers.append(observer)

    def remove_add_footswitch_observer(self, observer):
        self._add_footswitch_observers.remove(observer)

    def notify_add_footswitch_observers(self, footswitch_config: FootswitchConfig):
        for observer in self._add_footswitch_observers:
            observer(footswitch_config)

    """Remove Footswitch"""

    def remove_footswitch(self, footswitch_config: FootswitchConfig):
        try:
            del self.footswitches[footswitch_config.name]
        except KeyError as err:
            raise FootswitchDoesNotExistException() from err
        pyfx_log.debug(f"Remove {footswitch_config.name} footswitch from {self.name} pedal")
        self.modified = True
        self.notify_remove_footswitch_observers(footswitch_config)

    def add_remove_footswitch_observer(self, observer):
        self._remove_footswitch_observers.append(observer)

    def remove_remove_footswitch_observer(self, observer):
        self._remove_footswitch_observers.remove(observer)

    def notify_remove_footswitch_observers(self, footswitch_config: FootswitchConfig):
        for observer in self._remove_footswitch_observers:
            observer(footswitch_config)

    """Change Footswitch Name"""

    def change_footswitch_name(self, old_name: str, new_name: str):
        self.footswitches[new_name] = self.footswitches[old_name]
        self.footswitches[new_name].change_footswitch_name(old_name, new_name)
        del self.footswitches[old_name]
        self.modified = True
        self.notify_change_footswitch_name_observers(old_name, new_name)

    def add_change_footswitch_name_observer(self, observer):
        self._change_footswitch_name_observers.append(observer)

    def remove_change_footswitch_name_observer(self, observer):
        self._change_footswitch_name_observers.remove(observer)

    def notify_change_footswitch_name_observers(self, old_name: str, new_name: str):
        for observer in self._change_footswitch_name_observers:
            observer(old_name, new_name)

    """Set Variant"""

    def set_variant(self, name: str):
        if self.variant != name:
            pyfx_log.debug(f"Set {self.name} pedal variant to {name}")
            self.variant = name
            self.modified = True
            self.notify_set_variant_observers(name)

    def add_set_variant_observer(self, observer):
        self._set_variant_observers.append(observer)

    def remove_set_variant_observer(self, observer):
        self._set_variant_observers.remove(observer)

    def notify_set_variant_observers(self, name: str):
        for observer in self._set_variant_observers:
            observer(name)

    """Add Variant"""

    def add_variant(self, name: str):
        if name not in self.variants:
            pyfx_log.debug(f"Add {name} {self.name} pedal variant")
            self.variants.append(name)
            self.notify_add_variant_observers(name)
            self.set_variant(name)
            self.modified = True

    def add_add_variant_observer(self, observer):
        self._add_variant_observers.append(observer)

    def remove_add_variant_observer(self, observer):
        self._add_variant_observers.remove(observer)

    def notify_add_variant_observers(self, name: str):
        for observer in self._add_variant_observers:
            observer(name)

    """Remove Variant"""

    def remove_variant(self, name: str):
        if name in self.variants:
            pyfx_log.debug(f"Remove {name} {self.name} pedal variant")
            self.variants.remove(name)
            if self.variant == name:
                self.variant = None
            self.modified = True
            self.notify_remove_variant_observers(name)

    def add_remove_variant_observer(self, observer):
        self._remove_variant_observers.append(observer)

    def remove_remove_variant_observer(self, observer):
        self._remove_variant_observers.remove(observer)

    def notify_remove_variant_observers(self, name: str):
        for observer in self._remove_variant_observers:
            observer(name)

    """Change Variant Name"""

    def change_variant_name(self, old_name, new_name: str):
        if old_name in self.variants:
            pyfx_log.debug(f"Change {old_name} {self.name} pedal variant to {new_name}")
            self.variants = [new_name if variant == old_name else variant for variant in self.variants]
            if self.variant == old_name:
                self.variant = new_name
            self.notify_change_variant_name_observers(old_name, new_name)

    def add_change_variant_name_observer(self, observer):
        self._change_variant_name_observers.append(observer)

    def remove_change_variant_name_observer(self, observer):
        self._change_variant_name_observers.remove(observer)

    def notify_change_variant_name_observers(self, old_name: str, new_name: str):
        for observer in self._change_variant_name_observers:
            observer(old_name, new_name)

    """Set Pedal Color"""

    def set_pedal_color(self, pedal_color: str):
        if self.pedal_color != pedal_color:
            pyfx_log.debug(f"Set {self.name} pedal color to {pedal_color}")
            self.pedal_color = pedal_color
            self.modified = True
            self.notify_set_pedal_color_observers(pedal_color)

    def add_set_pedal_color_observer(self, observer):
        self._set_pedal_color_observers.append(observer)

    def remove_set_pedal_color_observer(self, observer):
        self._set_pedal_color_observers.remove(observer)

    def notify_set_pedal_color_observers(self, pedal_color: str):
        for observer in self._set_pedal_color_observers:
            observer(pedal_color)

    """Set Text Color"""

    def set_text_color(self, text_color: str):
        if self.text_color != text_color:
            pyfx_log.debug(f"Set {self.name} pedal text color to {text_color}")
            self.text_color = text_color
            self.modified = True
            self.notify_set_text_color_observers(text_color)

    def add_set_text_color_observer(self, observer):
        self._set_text_color_observers.append(observer)

    def remove_set_text_color_observer(self, observer):
        self._set_text_color_observers.remove(observer)

    def notify_set_text_color_observers(self, text_color: str):
        for observer in self._set_text_color_observers:
            observer(text_color)

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
