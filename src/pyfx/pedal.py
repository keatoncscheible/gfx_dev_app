from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from pyfx.component import PyFxComponent
from pyfx.exceptions import (
    FootswitchAlreadyExistsError,
    FootswitchDoesNotExistError,
    KnobAlreadyExistsError,
    KnobDoesNotExistError,
    PedalVariantAlreadyExistsError,
    PedalVariantDoesNotExistError,
)
from pyfx.footswitch import PyFxFootswitch
from pyfx.knob import PyFxKnob
from pyfx.logging import pyfx_log


class PyFxPedal(ABC, PyFxComponent):
    def __init__(
        self,
        name: str,
        knobs: dict[str, PyFxKnob] | None = None,
        footswitches: dict[str, PyFxFootswitch] | None = None,
        variant: PyFxPedalVariant | None = None,
        variants: list[PyFxPedalVariant] | None = None,
        pedal_color: str = "#0000FF",
        text_color: str = "#FFFFFF",
    ):
        super().__init__()
        self.name = name
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

        self.knobs: dict[str, PyFxKnob] = {}
        if knobs:
            for knob in knobs.values():
                self.add_knob(knob)

        self.footswitches: dict[str, PyFxFootswitch] = {}
        if footswitches:
            for footswitch in footswitches.values():
                self.add_footswitch(footswitch)

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
        pyfx_log.debug(
            f"""Adding {self.name} pedal change pedal name observer: {observer.__self__.__class__.__name__}.{observer.__name__}"""  # noqa: E501
        )
        self._change_pedal_name_observers.append(observer)

    def remove_change_pedal_name_observer(self, observer):
        pyfx_log.debug(
            f"Removing {self.name} pedal change pedal name observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        self._change_pedal_name_observers.remove(observer)

    def notify_change_pedal_name_observers(self, old_name: str, new_name: str):
        for observer in self._change_pedal_name_observers:
            pyfx_log.debug(
                f"Calling {self.name} pedal change pedal name observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
            )
            observer(old_name, new_name)

    """Add Knob"""

    def add_knob(self, knob: PyFxKnob = None):
        if knob is None:
            knob_idx = 1
            while True:
                knob_name = f"Knob {knob_idx}"
                if knob_name not in self.knobs:
                    break
                knob_idx += 1
            knob = PyFxKnob(knob_name)
        elif knob.name in self.knobs:
            raise KnobAlreadyExistsError()
        pyfx_log.debug(f"Add {knob.name} knob to {self.name} pedal")
        knob.add_remove_knob_observer(self.remove_knob)
        self.knobs[knob.name] = knob
        self.modified = True
        self.notify_add_knob_observers(knob)

    def add_add_knob_observer(self, observer):
        pyfx_log.debug(
            f"Adding {self.name} pedal add knob observer: {observer.__self__.__class__.__name__}.{observer.__name__}"
        )
        self._add_knob_observers.append(observer)

    def remove_add_knob_observer(self, observer):
        pyfx_log.debug(
            f"Removing {self.name} pedal add knob observer: {observer.__self__.__class__.__name__}.{observer.__name__}"
        )
        self._add_knob_observers.remove(observer)

    def notify_add_knob_observers(self, knob: PyFxKnob):
        for observer in self._add_knob_observers:
            pyfx_log.debug(
                f"Calling {self.name} pedal add knob observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
            )
            observer(knob)

    """Remove Knob"""

    def remove_knob(self, knob: PyFxKnob):
        try:
            del self.knobs[knob.name]
        except KeyError as err:
            raise KnobDoesNotExistError() from err
        pyfx_log.debug(f"Remove {knob.name} knob from {self.name} pedal")
        self.modified = True
        self.notify_remove_knob_observers(knob)

    def add_remove_knob_observer(self, observer):
        pyfx_log.debug(
            f"Adding {self.name} pedal remove knob observer: {observer.__self__.__class__.__name__}.{observer.__name__}"
        )
        self._remove_knob_observers.append(observer)

    def remove_remove_knob_observer(self, observer):
        pyfx_log.debug(
            f"Removing {self.name} pedal remove knob observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        self._remove_knob_observers.remove(observer)

    def notify_remove_knob_observers(self, knob: PyFxKnob):
        for observer in self._remove_knob_observers:
            pyfx_log.debug(
                f"Calling {self.name} pedal remove knob observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
            )
            observer(knob)

    """Change Knob Name"""

    def change_knob_name(self, old_name: str, new_name: str):
        self.knobs[new_name] = self.knobs[old_name]
        self.knobs[new_name].change_knob_name(new_name)
        del self.knobs[old_name]
        self.modified = True
        self.notify_change_knob_name_observers(old_name, new_name)

    def add_change_knob_name_observer(self, observer):
        pyfx_log.debug(
            f"Adding {self.name} pedal change knob name observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        self._change_knob_name_observers.append(observer)

    def remove_change_knob_name_observer(self, observer):
        pyfx_log.debug(
            f"Removing {self.name} pedal change knob name observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        self._change_knob_name_observers.remove(observer)

    def notify_change_knob_name_observers(self, old_name: str, new_name: str):
        for observer in self._change_knob_name_observers:
            pyfx_log.debug(
                f"Calling {self.name} pedal change knob name observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
            )
            observer(old_name, new_name)

    """Add Footswitch"""

    def add_footswitch(self, footswitch: PyFxFootswitch = None):
        if footswitch is None:
            footswitch_idx = 1
            while True:
                footswitch_name = f"Footswitch {footswitch_idx}"
                if footswitch_name not in self.footswitches:
                    break
                footswitch_idx += 1
            footswitch = PyFxFootswitch(footswitch_name)
        elif footswitch.name in self.footswitches:
            raise FootswitchAlreadyExistsError()
        pyfx_log.debug(f"Add {footswitch.name} footswitch to {self.name} pedal")
        footswitch.add_remove_footswitch_observer(self.remove_footswitch)
        self.footswitches[footswitch.name] = footswitch
        self.modified = True
        self.notify_add_footswitch_observers(footswitch)

    def add_add_footswitch_observer(self, observer):
        pyfx_log.debug(
            f"Adding {self.name} pedal add footswitch observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        self._add_footswitch_observers.append(observer)

    def remove_add_footswitch_observer(self, observer):
        pyfx_log.debug(
            f"Removing {self.name} pedal add footswitch observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        self._add_footswitch_observers.remove(observer)

    def notify_add_footswitch_observers(self, footswitch: PyFxFootswitch):
        for observer in self._add_footswitch_observers:
            pyfx_log.debug(
                f"Calling {self.name} pedal add footswitch observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
            )
            observer(footswitch)

    """Remove Footswitch"""

    def remove_footswitch(self, footswitch: PyFxFootswitch):
        try:
            del self.footswitches[footswitch.name]
        except KeyError as err:
            raise FootswitchDoesNotExistError() from err
        pyfx_log.debug(f"Remove {footswitch.name} footswitch from {self.name} pedal")
        self.modified = True
        self.notify_remove_footswitch_observers(footswitch)

    def add_remove_footswitch_observer(self, observer):
        pyfx_log.debug(
            f"Adding {self.name} pedal remove footswitch observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        self._remove_footswitch_observers.append(observer)

    def remove_remove_footswitch_observer(self, observer):
        pyfx_log.debug(
            f"Removing {self.name} pedal remove footswitch observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        self._remove_footswitch_observers.remove(observer)

    def notify_remove_footswitch_observers(self, footswitch: PyFxFootswitch):
        for observer in self._remove_footswitch_observers:
            pyfx_log.debug(
                f"Calling {self.name} pedal remove footswitch observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
            )
            observer(footswitch)

    """Change Footswitch Name"""

    def change_footswitch_name(self, old_name: str, new_name: str):
        self.footswitches[new_name] = self.footswitches[old_name]
        self.footswitches[new_name].change_footswitch_name(old_name, new_name)
        del self.footswitches[old_name]
        self.modified = True
        self.notify_change_footswitch_name_observers(old_name, new_name)

    def add_change_footswitch_name_observer(self, observer):
        pyfx_log.debug(
            f"Adding {self.name} pedal change footswitch name observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        self._change_footswitch_name_observers.append(observer)

    def remove_change_footswitch_name_observer(self, observer):
        pyfx_log.debug(
            f"Removing {self.name} pedal change footswitch name observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        self._change_footswitch_name_observers.remove(observer)

    def notify_change_footswitch_name_observers(self, old_name: str, new_name: str):
        for observer in self._change_footswitch_name_observers:
            pyfx_log.debug(
                f"Calling {self.name} pedal change footswitch name observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
            )
            observer(old_name, new_name)

    """Set Variant"""

    def set_variant(self, variant_name: str):
        try:
            variant = next(variant for variant in self.variants if variant.name == variant_name)
        except StopIteration as err:
            raise PedalVariantDoesNotExistError() from err

        if self.variant != variant:
            pyfx_log.debug(f"Set {self.name} pedal variant to {variant.name}")
            self.variant = variant
            self.modified = True
            self.notify_set_variant_observers(variant)

    def add_set_variant_observer(self, observer):
        pyfx_log.debug(
            f"Adding {self.name} pedal set variant observer: {observer.__self__.__class__.__name__}.{observer.__name__}"
        )
        self._set_variant_observers.append(observer)

    def remove_set_variant_observer(self, observer):
        pyfx_log.debug(
            f"Removing {self.name} pedal set variant observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        self._set_variant_observers.remove(observer)

    def notify_set_variant_observers(self, variant: PyFxPedalVariant):
        for observer in self._set_variant_observers:
            pyfx_log.debug(
                f"Calling {self.name} pedal set variant observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
            )
            observer(variant)

    """Add Variant"""

    def add_variant(self, variant_name: str):
        if variant_name not in [variant.name for variant in self.variants]:
            pyfx_log.debug(f"Add {variant_name} {self.name} pedal variant")
            variant = PyFxPedalVariant(name=variant_name, knobs=self.knobs, footswitches=self.footswitches)
            self.variants.append(variant)
            self.notify_add_variant_observers(variant)
            self.set_variant(variant.name)
            self.modified = True

    def add_add_variant_observer(self, observer):
        pyfx_log.debug(
            f"Adding {self.name} pedal add variant observer: {observer.__self__.__class__.__name__}.{observer.__name__}"
        )
        self._add_variant_observers.append(observer)

    def remove_add_variant_observer(self, observer):
        pyfx_log.debug(
            f"Removing {self.name} pedal add variant observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        self._add_variant_observers.remove(observer)

    def notify_add_variant_observers(self, variant: PyFxPedalVariant):
        for observer in self._add_variant_observers:
            pyfx_log.debug(
                f"Calling {self.name} pedal add variant observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
            )
            observer(variant)

    """Remove Variant"""

    def remove_variant(self, variant_name: str):
        if variant_name in [variant.name for variant in self.variants]:
            pyfx_log.debug(f"Remove {variant_name} {self.name} pedal variant")
            variant = next(variant for variant in self.variants if variant.name == variant_name)
            self.variants.remove(variant)
            if self.variant == variant:
                self.variant = None
            self.modified = True
            self.notify_remove_variant_observers(variant)

    def add_remove_variant_observer(self, observer):
        pyfx_log.debug(
            f"Adding {self.name} pedal remove variant observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        self._remove_variant_observers.append(observer)

    def remove_remove_variant_observer(self, observer):
        pyfx_log.debug(
            f"Removing {self.name} pedal remove variant observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        self._remove_variant_observers.remove(observer)

    def notify_remove_variant_observers(self, variant: PyFxPedalVariant):
        for observer in self._remove_variant_observers:
            pyfx_log.debug(
                f"Calling {self.name} pedal remove variant observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
            )
            observer(variant)

    """Change Variant Name"""

    def change_variant_name(self, old_name, new_name: str):
        if old_name in [variant.name for variant in self.variants]:
            pyfx_log.debug(f"Change {old_name} {self.name} pedal variant to {new_name}")
            for variant in self.variants:
                if variant.name == old_name:
                    variant.name = new_name
            self.notify_change_variant_name_observers(old_name, new_name)

    def add_change_variant_name_observer(self, observer):
        pyfx_log.debug(
            f"Adding {self.name} pedal change variant name observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        self._change_variant_name_observers.append(observer)

    def remove_change_variant_name_observer(self, observer):
        pyfx_log.debug(
            f"Removing {self.name} pedal change variant name observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        self._change_variant_name_observers.remove(observer)

    def notify_change_variant_name_observers(self, old_name: str, new_name: str):
        for observer in self._change_variant_name_observers:
            pyfx_log.debug(
                f"Calling {self.name} pedal change variant name observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
            )
            observer(old_name, new_name)

    """Set Pedal Color"""

    def set_pedal_color(self, pedal_color: str):
        if self.pedal_color != pedal_color:
            pyfx_log.debug(f"Set {self.name} pedal color to {pedal_color}")
            self.pedal_color = pedal_color
            self.modified = True
            self.notify_set_pedal_color_observers(pedal_color)

    def add_set_pedal_color_observer(self, observer):
        pyfx_log.debug(
            f"Adding {self.name} pedal set pedal color observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        self._set_pedal_color_observers.append(observer)

    def remove_set_pedal_color_observer(self, observer):
        pyfx_log.debug(
            f"Removing {self.name} pedal set pedal color observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        self._set_pedal_color_observers.remove(observer)

    def notify_set_pedal_color_observers(self, pedal_color: str):
        for observer in self._set_pedal_color_observers:
            pyfx_log.debug(
                f"Calling {self.name} pedal set pedal color observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
            )
            observer(pedal_color)

    """Set Text Color"""

    def set_text_color(self, text_color: str):
        if self.text_color != text_color:
            pyfx_log.debug(f"Set {self.name} pedal text color to {text_color}")
            self.text_color = text_color
            self.modified = True
            self.notify_set_text_color_observers(text_color)

    def add_set_text_color_observer(self, observer):
        pyfx_log.debug(
            f"Adding {self.name} pedal set text color observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        self._set_text_color_observers.append(observer)

    def remove_set_text_color_observer(self, observer):
        pyfx_log.debug(
            f"Removing {self.name} pedal set text color observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
        )
        self._set_text_color_observers.remove(observer)

    def notify_set_text_color_observers(self, text_color: str):
        for observer in self._set_text_color_observers:
            pyfx_log.debug(
                f"Calling {self.name} pedal set text color observer: {observer.__self__.__class__.__name__}.{observer.__name__}"  # noqa: E501
            )
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

    # @abstractmethod
    # def process_audio(self, data):
    #     """Abstract Process Audio Callback"""


class PyFxPedalVariant(PyFxComponent):
    def __init__(
        self,
        name: str,
        knobs: dict[str, PyFxKnob],
        footswitches: dict[str, PyFxFootswitch],
    ):
        self.name = name
        self.knobs = knobs
        self.footswiches = footswitches
