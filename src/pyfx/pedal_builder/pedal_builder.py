import importlib
import pickle
import re
import shutil
from pathlib import Path

from pyfx.audio_processor import AudioProcessor
from pyfx.config import PedalConfig
from pyfx.exceptions import InvalidPedalConfigException, PedalDoesNotExistException
from pyfx.logging import pyfx_log


# Helper Functions
def property_name(name):
    # Replace all non-letter characters with underscores
    property_name = re.sub(r"[^a-zA-Z0-9]+", "_", name)
    # Remove underscores from the start and end
    property_name = property_name.strip("_")
    return property_name.lower()


def pedal_folder_name(pedal_name: str):
    return pedal_name.lower().replace(" ", "_")


def previous_pedal_file(root_pedal_folder: Path):
    return root_pedal_folder / "previous_pedal"


def pedal_folder(root_pedal_folder: Path, pedal_name: str):
    return root_pedal_folder / pedal_folder_name(pedal_name)


def pedal_config_file(root_pedal_folder: Path, pedal_name: str):
    return pedal_folder(root_pedal_folder, pedal_name) / "pedal_cfg.pkl"


def pedal_module_name(pedal_name: str):
    return f"{pedal_folder_name(pedal_name)}_pedal"


def base_pedal_module_name(pedal_name: str):
    return f"{pedal_module_name(pedal_name)}_base"


def base_pedal_module_filename(pedal_name: str):
    return f"{base_pedal_module_name(pedal_name)}.py"


def base_pedal_module_file(root_pedal_folder: Path, pedal_name: str):
    return pedal_folder(root_pedal_folder, pedal_name) / base_pedal_module_filename(pedal_name)


def base_pedal_class_name(pedal_name: str):
    base_pedal_class_name = "".join([word.capitalize() for word in pedal_module_name(pedal_name).split("_")])
    base_pedal_class_name = f"{base_pedal_class_name}Base"
    return base_pedal_class_name


def variant_module_name(pedal_name: str, variant_name: str):
    variant_part = variant_name.lower().replace(" ", "_")
    return f"{variant_part}_{pedal_module_name(pedal_name)}"


def variant_module_filename(pedal_name: str, variant_name: str):
    return f"{variant_module_name(pedal_name, variant_name)}.py"


def variant_module_file(root_pedal_folder: Path, pedal_name: str, variant_name: str):
    return pedal_folder(root_pedal_folder, pedal_name) / variant_module_filename(pedal_name, variant_name)


def variant_pedal_class_name(pedal_name: str, variant_name: str):
    return "".join([word.capitalize() for word in variant_module_name(pedal_name, variant_name).split("_")])


class PedalBuilder:
    def __init__(self, root_pedal_folder: Path, audio_processor: AudioProcessor):
        self.root_pedal_folder = root_pedal_folder
        self.audio_processor = audio_processor
        try:
            with open(previous_pedal_file(self.root_pedal_folder)) as file:
                pedal_name = file.read()
            self.open_pedal(pedal_name)
        except FileNotFoundError:
            self.pedal = None
            self.pedal_name = None
            self.pedal_config = None
            self.variant_name = None

    """Create New Pedal"""

    def create_new_pedal(self):
        self.pedal_name = self.generate_pedal_name()
        pedal_folder(self.root_pedal_folder, self.pedal_name).mkdir()
        self.pedal_config = PedalConfig(name=self.pedal_name)
        self.pedal_config.add_set_variant_observer(self.set_pedal_variant)
        self.pedal_config.add_add_variant_observer(self.create_new_pedal_variant)
        self.pedal_config.add_remove_variant_observer(self.remove_pedal_variant)
        self.pedal_config.add_change_variant_name_observer(self.change_pedal_variant_name)
        self.generate_pedal_module()
        self.pedal = self.load_pedal_module()
        self.temporary = True

    """Open Pedal"""

    def open_pedal(self, name: str):
        self.pedal_name = name
        self.pedal_config = self.load_pedal_config()
        self.pedal_config.add_set_variant_observer(self.set_pedal_variant)
        self.pedal_config.add_add_variant_observer(self.create_new_pedal_variant)
        self.pedal_config.add_remove_variant_observer(self.remove_pedal_variant)
        self.pedal_config.add_change_variant_name_observer(self.change_pedal_variant_name)
        self.pedal = self.load_pedal_module()
        self.update_audio_processor()
        self.update_previous_pedal_file()

    """Close Pedal"""

    def close_pedal(self):
        try:
            if self.temporary:
                shutil.rmtree(pedal_folder(self.root_pedal_folder, self.pedal_name))
        except AttributeError:
            pass
        self.pedal = None
        self.pedal_name = None
        self.pedal_config = None

    """Save Pedal"""

    def save_pedal(self):
        if self.pedal_config is None:
            raise PedalDoesNotExistException()
        self.save_pedal_config()
        self.update_previous_pedal_file()
        self.temporary = False

    def save_pedal_config(self):
        self.pedal_config.reset_modified_flags()
        with open(pedal_config_file(self.root_pedal_folder, self.pedal_name), "wb") as file:
            pickle.dump(self.pedal_config, file)

    def load_pedal_config(self):
        with open(pedal_config_file(self.root_pedal_folder, self.pedal_name), "rb") as file:
            pedal_config = pickle.load(file)
            if isinstance(pedal_config, PedalConfig):
                return pedal_config
            else:
                raise InvalidPedalConfigException()

    def update_previous_pedal_file(self):
        with open(previous_pedal_file(self.root_pedal_folder), "w") as file:
            file.write(self.pedal_name)

    def remove_previous_pedal_file(self):
        try:
            previous_pedal_file(self.root_pedal_folder).unlink()
        except FileNotFoundError:
            pass

    def generate_pedal_name(self):
        pedal_idx = 1
        while True:
            pedal_folder_name = f"pedal_{pedal_idx}"
            if not (self.root_pedal_folder / pedal_folder_name).exists():
                break
            pedal_idx += 1
        return f"Pedal {pedal_idx}"

    def generate_pedal_module(self):
        pyfx_log.debug(f"Generating {self.pedal_name} module")

        def create_knob_property(file, name):
            file.write("    @property\n")
            file.write(f"    def {property_name(name)}(self):\n")
            file.write(f'        return self.knobs["{name}"].value\n')
            file.write("\n")
            file.write("    @property\n")
            file.write(f"    def {property_name(name)}_min(self):\n")
            file.write(f'        return self.knobs["{name}"].minimum_value\n')
            file.write("\n")
            file.write("    @property\n")
            file.write(f"    def {property_name(name)}_max(self):\n")
            file.write(f'        return self.knobs["{name}"].maximum_value\n')
            file.write("\n")
            file.write("    @property\n")
            file.write(f"    def {property_name(name)}_default(self):\n")
            file.write(f'        return self.knobs["{name}"].default_value\n')
            file.write("\n")

        def create_switch_property(file, name):
            file.write("    @property\n")
            file.write(f"    def {property_name(name)}(self):\n")
            footswitch_type = self.pedal_config.footswitches[name].footswitch_type
            if footswitch_type in ["latching", "momentary"]:
                file.write(f'        return self.footswitches["{name}"].state\n')
            elif footswitch_type == "mode":
                file.write(f'        return self.footswitches["{name}"].mode\n')
            file.write("\n")

        with open(base_pedal_module_file(self.root_pedal_folder, self.pedal_name), "w") as file:
            file.write('"""\n')
            file.write("This file is autogenerated and should not be modified manually.\n")
            file.write("Any changes made to this file may be overwritten.\n")
            file.write('"""\n')
            file.write("\n")
            file.write("from pyfx.config import PedalConfig\n")
            file.write("from pyfx.pedal import PyFxPedal\n")
            file.write("\n")
            file.write("\n")
            file.write(f"class {base_pedal_class_name(self.pedal_name)}(PyFxPedal):\n")
            file.write(f'    """{self.pedal_name} Class"""\n')
            file.write("\n")
            file.write("    def __init__(self, pedal_config: PedalConfig):\n")
            file.write("        super().__init__(pedal_config)\n")
            file.write("\n")
            for knob_name in [knob.name for knob in self.pedal_config.knobs.values()]:
                create_knob_property(file, knob_name)
            for footswitch_name in [footswitch.name for footswitch in self.pedal_config.footswitches.values()]:
                create_switch_property(file, footswitch_name)

    def set_pedal_variant(self, variant: str):
        pyfx_log.debug(f"Set pedal variant to {variant}")
        self.variant_name = variant

    def create_new_pedal_variant(self, variant: str):
        pyfx_log.debug(f"Creating pedal variant {variant}")

        with open(variant_module_file(self.root_pedal_folder, self.pedal_name, variant), "w") as file:
            file.write("import numpy as np\n")
            file.write(
                f"from {base_pedal_module_name(self.pedal_name)} import {base_pedal_class_name(self.pedal_name)}\n"
            )
            file.write("\n")
            file.write("\n")
            file.write(
                f"class {variant_pedal_class_name(self.pedal_name, variant)}({base_pedal_class_name(self.pedal_name)}):\n"
            )
            file.write("    def process_audio(self, data: np.ndarray):\n")
            file.write(f'        """{variant} {self.pedal_name} Processing"""\n')
            file.write("\n")
            file.write("        # TODO: Replace this line with your processing code\n")
            file.write("        processed_data = data\n")
            file.write("\n")
            file.write("        return processed_data\n")
            file.write("\n")

    def update_pedal_variant(self, variant: str):
        pyfx_log.debug(f"Updating pedal variant {variant}")

    def remove_pedal_variant(self, variant: str):
        pyfx_log.debug(f"Removing pedal variant {variant}")

    def change_pedal_variant_name(self, old_variant_name: str, new_variant_name: str):
        pyfx_log.debug(f"Changing {old_variant_name} pedal variant to {new_variant_name}")

    def change_pedal_name(self, new_pedal_name: str):
        old_pedal_name = self.pedal_name
        pyfx_log.debug(f"Changing pedal name from {old_pedal_name} to {new_pedal_name}")

    def change_knob_name(self, old_knob_name: str, new_knob_name: str):
        pyfx_log.debug(f"Changing {old_knob_name} knob name to {new_knob_name}")

    def change_footswitch_name(self, old_footswitch_name: str, new_footswitch_name: str):
        pyfx_log.debug(f"Changing {old_footswitch_name} footswitch name to {new_footswitch_name}")

    def load_pedal_module(self):
        # Dynamically import pedal class from generated pedal module and return an instance of the class
        spec = importlib.util.spec_from_file_location(
            f"pedals.{self.pedal_name}.{pedal_module_name(self.pedal_name)}",
            base_pedal_module_file(self.root_pedal_folder, self.pedal_name),
        )
        pedal_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pedal_module)
        pedal_class = getattr(pedal_module, base_pedal_class_name(self.pedal_name))
        return pedal_class(self.pedal_config)

    """Audio Processor Control"""

    def update_audio_processor(self):
        pass
        # TODO: Add this back in
        # self.audio_processor.audio_data_processor(partial(self.pedal.process_audio, self.pedal))
