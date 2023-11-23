import importlib.util
import pickle
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from gfx.exceptions import (
    GfxPedalDoesNotExistException,
    GfxPedalVariantAlreadyExistsException,
)
from gfx_dev_logging import gfx_dev_log
from PySide6.QtGui import QColor
from widgets.knob import KnobConfig


# Helper Functions
def property_name(name):
    # Replace all non-letter characters with underscores
    property_name = re.sub(r"[^a-zA-Z0-9]+", "_", name)
    # Remove underscores from the start and end
    property_name = property_name.strip("_")
    return property_name.lower()


@dataclass
class GfxPedalConfig:
    name: str
    knobs: dict[str, KnobConfig]
    switches: dict[str, bool]
    pedal_color: QColor
    text_color: QColor
    modified: bool = False
    config_file: Path = None

    def set_name(self, value: str):
        if self.name != value:
            self.name = value
            self.modified = True

    def set_knobs(self, value: dict[str, KnobConfig]):
        if self.knobs != value:
            self.knobs = value
            self.modified = True

    def set_switches(self, value: dict[str, bool]):
        if self.switches != value:
            self.switches = value
            self.modified = True

    def set_pedal_color(self, value: QColor):
        if self.pedal_color != value:
            self.pedal_color = value
            self.modified = True

    def set_text_color(self, value: QColor):
        if self.text_color != value:
            self.text_color = value
            self.modified = True

    @property
    def is_modified(self):
        return self.modified or any(
            config_item.modified for config_item in self.config_items
        )

    @property
    def config_items(self):
        # TODO: Need to add the other config items to this list as we add modified flags
        config_items = [self]
        config_items.extend([knob for knob in self.knobs.values()])
        return config_items

    def load(self, config_file: Path):
        if self.is_modified:
            raise ValueError("Cant load when modified. Fix this")
        with open(self.config_file, "rb") as file:
            config: KnobConfig = pickle.load(file)
            self.minimum_value = config.minimum_value
            self.maximum_value = config.maximum_value
            self.default_value = config.default_value
            self.precision = config.precision
            self.sensitivity = config.sensitivity
            self.mode = config.mode
            self.display_value = config.display_value
            self.value = config.value
            self.modified = False

    def save(self):
        if self.config_file is None:
            # TODO: Replace with custom exception
            raise ValueError("Config file does not exist")
        if self.is_modified:
            with open(self.config_file, "wb") as file:
                pickle.dump(self, file)
            for config_item in self.config_items:
                config_item.modified = False


class GfxPedalUpdateInfo:
    def __init__(self):
        self.name: tuple[str, str] = tuple()
        self.knobs: dict[str, str] = {}
        self.switches: dict[str, str] = {}

    @property
    def update_needed(self):
        return bool(self.name or self.knobs or self.switches)

    def reset(self):
        self.name = tuple()
        self.knobs = {}
        self.switches = {}


class GfxPedal:
    pedal_config_filename = "pedal_cfg.pkl"

    def __new__(cls, pedal_folder: Path = None, pedal_config: GfxPedalConfig = None):
        if pedal_folder is None and pedal_config is None:
            return cls

        cls.pedal_folder = pedal_folder
        cls.variants_folder = pedal_folder / "variants"
        cls.variants = [
            variant_file.stem for variant_file in cls.variants_folder.glob("*.py")
        ]
        cls.pedal_updated_observers = []
        cls.variant_updated_observers = []
        cls.pedal_update_info = GfxPedalUpdateInfo()

        # # If configuration is provided, we are creating a new pedal
        if pedal_config:
            pedal_config.config_file = cls.pedal_config_file
            cls.pedal_config = pedal_config
            if not pedal_folder.exists():
                cls.pedal_folder.mkdir(exist_ok=True)
                cls.generate_pedal_module()
                cls.generate_pedal_variant()
                cls.save_pedal()
        # If no configuration is provided, we are loading a pedal
        else:
            cls.pedal_config = cls._load_pedal_config()

        cls.load_variant(cls.variants[0])

        # Dynamically import pedal class from generated pedal module and return an instance of the class
        spec = importlib.util.spec_from_file_location(
            f"pedals.{cls.name}.{cls.pedal_module_name}", cls.pedal_module_file
        )
        pedal_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pedal_module)
        pedal_class = getattr(pedal_module, cls.pedal_class_name)
        return pedal_class()

    @classmethod
    def generate_pedal_module(cls):
        gfx_dev_log.debug(f"Generating {cls.name} module")

        def create_knob_property(file, name):
            file.write("    @classmethod\n")
            file.write("    @property\n")
            file.write(f"    def {property_name(name)}(self):\n")
            file.write(f'        return self.knobs["{name}"].value\n')
            file.write("\n")

        def create_switch_property(file, name):
            file.write("    @classmethod\n")
            file.write("    @property\n")
            file.write(f"    def {property_name(name)}(self):\n")
            file.write(f'        return self.switches["{name}"]\n')
            file.write("\n")

        with open(cls.pedal_module_file, "w") as file:
            file.write('"""\n')
            file.write(
                "This file is autogenerated and should not be modified manually.\n"
            )
            file.write("Any changes made to this file may be overwritten.\n")
            file.write('"""\n')
            file.write("\n")
            file.write("from gfx.pedal import GfxPedal\n")
            file.write("\n")
            file.write("\n")
            file.write(f"class {cls.pedal_class_name}(GfxPedal):\n")
            for knob_name in cls.knob_names:
                create_knob_property(file, knob_name)
            for switch_name in cls.switch_names:
                create_switch_property(file, switch_name)

    @classmethod
    def generate_pedal_variant(cls, variant_name: str = "default"):
        if variant_name not in cls.variants:
            cls.variants.append(variant_name)
        gfx_dev_log.debug(f"Generating {variant_name} {cls.name} variant")
        cls.variants_folder.mkdir(exist_ok=True)
        variant_file = cls.variants_folder / f"{variant_name}.py"
        if variant_file.exists():
            raise GfxPedalVariantAlreadyExistsException()
        with open(variant_file, "w") as file:
            file.write("import numpy as np\n")
            file.write(
                f"from pedals.{cls.name.lower().replace(' ', '_')}.{cls.pedal_module_name} import {cls.pedal_class_name}\n"
            )
            file.write("\n")
            file.write("\n")
            file.write(
                f"def process_audio(pedal: {cls.pedal_class_name}, data: np.ndarray):\n"
            )
            file.write("\n")
            file.write("    # TODO: Add audio processing code here\n")
            file.write("\n")
            file.write("    return data\n")

    @classmethod
    def update_pedal_module(cls):
        gfx_dev_log.debug(f"Updating {cls.name} Pedal module")

        with open(cls.pedal_module_file, "r") as file:
            pedal_module_contents = file.read()

        # Update pedal name if necessary
        if cls.pedal_update_info.name:
            old_pedal_name, new_pedal_name = cls.pedal_update_info.name
            old_pedal_name_snake_case = old_pedal_name.lower().replace(" ", "_")
            new_pedal_name_snake_case = new_pedal_name.lower().replace(" ", "_")
            old_pedal_module_name = f"{old_pedal_name_snake_case}_pedal"
            new_pedal_module_name = f"{new_pedal_name_snake_case}_pedal"
            old_pedal_class_name = "".join(
                [word.capitalize() for word in old_pedal_module_name.split("_")]
            )
            new_pedal_class_name = "".join(
                [word.capitalize() for word in new_pedal_module_name.split("_")]
            )

            class_name_pattern = rf"class {old_pedal_class_name}"
            pedal_module_contents = re.sub(
                class_name_pattern,
                f"class {new_pedal_class_name}",
                pedal_module_contents,
            )

        # Update pedal knob names if necessary
        if cls.pedal_update_info.knobs:
            for old_knob_name, new_knob_name in cls.pedal_update_info.knobs.items():
                knob_def_pattern = rf"def {property_name(old_knob_name)}"
                pedal_module_contents = re.sub(
                    knob_def_pattern,
                    f"def {property_name(new_knob_name)}",
                    pedal_module_contents,
                )

                knob_assignmet_pattern = rf'\["\b{old_knob_name}\b"\]'
                pedal_module_contents = re.sub(
                    knob_assignmet_pattern,
                    f'["{new_knob_name}"]',
                    pedal_module_contents,
                )

        # Update pedal switch names if necessary
        if cls.pedal_update_info.switches:
            for (
                old_switch_name,
                new_switch_name,
            ) in cls.pedal_update_info.switches.items():
                switch_def_pattern = rf"def {property_name(old_switch_name)}"
                pedal_module_contents = re.sub(
                    switch_def_pattern,
                    f"def {property_name(new_switch_name)}",
                    pedal_module_contents,
                )

                switch_assignmet_pattern = rf'\["\b{old_switch_name}\b"\]'
                pedal_module_contents = re.sub(
                    switch_assignmet_pattern,
                    f'["{new_switch_name}"]',
                    pedal_module_contents,
                )

        with open(cls.pedal_module_file, "w") as file:
            file.write(pedal_module_contents)

    @classmethod
    def update_pedal_variants(cls):
        for variant_file in cls.variants_folder.glob("*.py"):
            gfx_dev_log.debug(f"Updating {cls.name} Pedal Variant: {variant_file.stem}")

            with open(variant_file, "r") as file:
                variant_file_contents = file.read()

            # Update pedal import and pedal typehint if necessary
            if cls.pedal_update_info.name:
                old_pedal_name, new_pedal_name = cls.pedal_update_info.name
                old_pedal_folder_name = old_pedal_name.lower().replace(" ", "_")
                new_pedal_folder_name = new_pedal_name.lower().replace(" ", "_")
                old_pedal_name_snake_case = old_pedal_name.lower().replace(" ", "_")
                new_pedal_name_snake_case = new_pedal_name.lower().replace(" ", "_")
                old_pedal_module_name = f"{old_pedal_name_snake_case}_pedal"
                new_pedal_module_name = f"{new_pedal_name_snake_case}_pedal"
                old_pedal_class_name = "".join(
                    [word.capitalize() for word in old_pedal_module_name.split("_")]
                )
                new_pedal_class_name = "".join(
                    [word.capitalize() for word in new_pedal_module_name.split("_")]
                )

                # Update import
                pedal_import_pattern = rf"from pedals.{old_pedal_folder_name}.{old_pedal_module_name} import {old_pedal_class_name}"
                variant_file_contents = re.sub(
                    pedal_import_pattern,
                    f"from pedals.{new_pedal_folder_name}.{new_pedal_module_name} import {new_pedal_class_name}",
                    variant_file_contents,
                )

                # Update pedal typehint
                pedal_typehint_pattern = rf"pedal: {old_pedal_class_name}"
                variant_file_contents = re.sub(
                    pedal_typehint_pattern,
                    f"pedal: {new_pedal_class_name}",
                    variant_file_contents,
                )

            # Update pedal knob names if necessary
            if cls.pedal_update_info.knobs:
                for old_knob_name, new_knob_name in cls.pedal_update_info.knobs.items():
                    knob_pattern = rf"pedal.{property_name(old_knob_name)}"
                    variant_file_contents = re.sub(
                        knob_pattern,
                        f"pedal.{property_name(new_knob_name)}",
                        variant_file_contents,
                    )

            # Update pedal switch names if necessary
            if cls.pedal_update_info.switches:
                for (
                    old_switch_name,
                    new_switch_name,
                ) in cls.pedal_update_info.switches.items():
                    switch_pattern = rf"pedal.{property_name(old_switch_name)}"
                    variant_file_contents = re.sub(
                        switch_pattern,
                        f"pedal.{property_name(new_switch_name)}",
                        variant_file_contents,
                    )

            with open(variant_file, "w") as file:
                variant_file_contents = file.write(variant_file_contents)

    @classmethod
    @property
    def pedal_config_file(cls):
        return cls.pedal_folder / cls.pedal_config_filename

    @classmethod
    @property
    def pedal_module_name(cls):
        pedal_name_snake_case = cls.pedal_config.name.lower().replace(" ", "_")
        return f"{pedal_name_snake_case}_pedal"

    @classmethod
    @property
    def pedal_module_filename(cls):
        return f"{cls.pedal_module_name}.py"

    @classmethod
    @property
    def pedal_module_file(cls):
        return cls.pedal_folder / cls.pedal_module_filename

    @classmethod
    @property
    def pedal_class_name(cls):
        return "".join([word.capitalize() for word in cls.pedal_module_name.split("_")])

    @classmethod
    @property
    def name(cls):
        return cls.pedal_config.name

    @classmethod
    def set_name(cls, name: str):
        old_pedal_folder = cls.pedal_folder
        cls.pedal_folder = cls.pedal_folder.parent / name.lower().replace(" ", "_")
        cls.variants_folder = cls.pedal_folder / "variants"
        old_pedal_module_file = cls.pedal_module_file
        old_name = cls.pedal_config.name
        cls.pedal_config.set_name(name)
        old_pedal_folder.rename(cls.pedal_folder)
        old_pedal_module_file.rename(cls.pedal_module_file)
        cls.pedal_update_info.name = (old_name, name)
        cls.update_pedal_info()

    @classmethod
    @property
    def knobs(cls):
        return cls.pedal_config.knobs

    @classmethod
    @property
    def switches(cls):
        return cls.pedal_config.switches

    @classmethod
    @property
    def knob_names(cls):
        return [knob_name for knob_name in cls.pedal_config.knobs.keys()]

    @classmethod
    @property
    def switch_names(cls):
        return [switch_name for switch_name in cls.pedal_config.switches.keys()]

    @classmethod
    def change_knob_value(cls, knob_name, knob_value):
        cls.pedal_config.knobs[knob_name].set_value(knob_value)

    @classmethod
    def change_knob_name(cls, old_name, new_name):
        cls.pedal_config.knobs[new_name] = cls.pedal_config.knobs[old_name]
        del cls.pedal_config.knobs[old_name]
        cls.pedal_update_info.knobs[old_name] = new_name
        cls.update_pedal_info()

    @classmethod
    def change_knob_config(cls, knob_name: str, knob_config: KnobConfig):
        gfx_dev_log.debug("Knob config changing")
        cls.pedal_config.knobs[knob_name] = knob_config
        cls.update_pedal_info()

    @classmethod
    def change_switch_state(cls, switch_name, switch_state):
        cls.pedal_config.switches[switch_name] = switch_state

    @classmethod
    def change_switch_name(cls, old_name, new_name):
        cls.pedal_config.switches[new_name] = cls.pedal_config.switches[old_name]
        del cls.pedal_config.switches[old_name]
        cls.pedal_update_info.switches[old_name] = new_name
        cls.update_pedal_info()

    @classmethod
    @property
    def pedal_color(cls):
        return cls.pedal_config.pedal_color

    @classmethod
    def set_pedal_color(cls, pedal_color):
        cls.pedal_config.set_pedal_color(pedal_color)
        cls.update_pedal_info()

    @classmethod
    @property
    def text_color(cls):
        return cls.pedal_config.text_color

    @classmethod
    def set_text_color(cls, text_color):
        cls.pedal_config.set_text_color(text_color)
        cls.update_pedal_info()

    @classmethod
    def _load_pedal_config(cls):
        if not cls.pedal_folder.exists() or not cls.pedal_config_file.exists():
            raise GfxPedalDoesNotExistException()
        with open(cls.pedal_config_file, "rb") as file:
            return pickle.load(file)

    @classmethod
    def save_pedal(cls):
        cls.pedal_config.save()

    @classmethod
    def update_pedal_info(cls):
        cls.update_pedal_module()
        cls.update_pedal_variants()
        cls.load_variant(cls.variant)
        cls.pedal_update_info.reset()
        cls.save_pedal()
        for observer in cls.pedal_updated_observers:
            observer()

    @classmethod
    def add_pedal_updated_observer(cls, observer):
        cls.pedal_updated_observers.append(observer)

    @classmethod
    def remove_pedal_updated_observer(cls, observer):
        try:
            cls.pedal_updated_observers.remove(observer)
        except ValueError:
            gfx_dev_log.debug("Pedal updated observer not found")

    @classmethod
    def load_variant(cls, variant: str):
        gfx_dev_log.debug(f"Loading the {cls.name} {variant} variant")
        cls.variant = variant
        variant_filename = f"{variant}.py"
        variant_module_file = cls.variants_folder / variant_filename

        # Import the module dynamically
        spec = importlib.util.spec_from_file_location("", variant_module_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Get a reference to the variants process_audio function
        cls.process_audio: callable[
            [GfxPedal, np.ndarray], np.ndarray
        ] = module.process_audio

        for observer in cls.variant_updated_observers:
            observer()

    @classmethod
    def add_variant_updated_observer(cls, observer):
        cls.variant_updated_observers.append(observer)

    @classmethod
    def remove_variant_updated_observer(cls, observer):
        try:
            cls.variant_updated_observers.remove(observer)
        except ValueError:
            gfx_dev_log.debug("Variant updated observer not found")
