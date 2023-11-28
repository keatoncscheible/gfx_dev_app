import importlib
import pickle
import re
import shutil
from functools import partial
from pathlib import Path
from typing import Optional

from pyfx.audio_processor import AudioProcessor
from pyfx.exceptions import InvalidPedalConfigException, PedalDoesNotExistException
from pyfx.footswitch import PyFxFootswitch
from pyfx.knob import PyFxKnob
from pyfx.logging import pyfx_log
from pyfx.pedal import PyFxPedal

# Helper Regexes
knob_dict_pattern = r"( *knobs\s*=\s*{\s*(?:\s*\".*?\"\s*:\s*PyFxKnob\(.*?\),)*\s*})"
footswitch_dict_pattern = r"( *footswitches\s*=\s*{\s*(?:\s*\".*?\"\s*:\s*PyFxFootswitch\(.*?\),)*\s*})"
knob_dict_parser = re.compile(knob_dict_pattern, re.DOTALL)
footswitch_dict_parser = re.compile(footswitch_dict_pattern, re.DOTALL)


# Helper Functions
def property_name(name):
    # Replace all non-letter characters with underscores
    property_name = re.sub(r"[^a-zA-Z0-9]+", "_", name)
    # Remove underscores from the start and end
    property_name = property_name.strip("_")
    return property_name.lower()


def generate_pedal_name(root_pedal_folder: Path):
    pedal_idx = 1
    while True:
        pedal_folder_name = f"pedal_{pedal_idx}"
        if not (root_pedal_folder / pedal_folder_name).exists():
            break
        pedal_idx += 1
    return f"Pedal {pedal_idx}"


def pedal_folder_name(pedal_name: str):
    return pedal_name.lower().replace(" ", "_")


def previous_pedal_file(root_pedal_folder: Path):
    return root_pedal_folder / "previous_pedal"


def pedal_folder(root_pedal_folder: Path, pedal_name: str):
    return root_pedal_folder / pedal_folder_name(pedal_name)


def pedal_settings_file(root_pedal_folder: Path, pedal_name: str):
    return pedal_folder(root_pedal_folder, pedal_name) / "pedal_settings.pkl"


def pedal_module_name(pedal_name: str):
    return f"{pedal_folder_name(pedal_name)}_pedal"


def pedal_module_filename(pedal_name: str):
    return f"{pedal_module_name(pedal_name)}.py"


def pedal_module_file(root_pedal_folder: Path, pedal_name: str):
    return pedal_folder(root_pedal_folder, pedal_name) / pedal_module_filename(pedal_name)


def pedal_class_name(pedal_name: str):
    return "".join([word.capitalize() for word in pedal_module_name(pedal_name).split("_")])


def variant_module_name(pedal_name: str, variant_name: str):
    variant_part = variant_name.lower().replace(" ", "_")
    return f"{variant_part}_{pedal_module_name(pedal_name)}"


def variant_module_filename(pedal_name: str, variant_name: str):
    return f"{variant_module_name(pedal_name, variant_name)}.py"


def variant_module_file(root_pedal_folder: Path, pedal_name: str, variant_name: str):
    return pedal_folder(root_pedal_folder, pedal_name) / variant_module_filename(pedal_name, variant_name)


def variant_pedal_class_name(pedal_name: str, variant_name: str):
    return "".join([word.capitalize() for word in variant_module_name(pedal_name, variant_name).split("_")])


def load_pedal_module(root_pedal_folder: Path, pedal_name: str) -> PyFxPedal:
    # Dynamically import pedal class from generated pedal module and return an instance of the class
    spec = importlib.util.spec_from_file_location(
        f"{root_pedal_folder}.{pedal_folder_name(pedal_name)}.{pedal_module_name(pedal_name)}",
        pedal_module_file(root_pedal_folder, pedal_name),
    )
    pedal_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pedal_module)
    pedal_class = getattr(pedal_module, pedal_class_name(pedal_name))
    return pedal_class()


def generate_pedal_module(root_pedal_folder: Path, pedal_name: str, default_variant_name: str = "Default"):
    pyfx_log.debug(f"Generating {pedal_name} module")

    with open(pedal_module_file(root_pedal_folder, pedal_name), "w") as file:
        file.write("from __future__ import annotations\n")
        file.write("\n")
        file.write("import numpy as np\n")
        file.write("\n")
        file.write("from pyfx.footswitch import PyFxFootswitch\n")
        file.write("from pyfx.knob import PyFxKnob\n")
        file.write("from pyfx.pedal import PyFxPedal, PyFxPedalVariant\n")
        file.write("\n")
        file.write("\n")
        file.write(f"class {pedal_class_name(pedal_name)}(PyFxPedal):\n")
        file.write(f'    """{pedal_name} Class"""\n')
        file.write("\n")
        file.write("    def __init__(self):\n")
        file.write(f'        name = "{pedal_name}"\n')
        file.write("        knobs = {}\n")
        file.write("        footswitches = {}\n")

        file.write("        variants = [\n")
        file.write(f"            {variant_pedal_class_name(pedal_name, default_variant_name)}(\n")
        file.write(f'                name="{default_variant_name} {pedal_name}",\n')
        file.write("                knobs=knobs,\n")
        file.write("                footswitches=footswitches,\n")
        file.write("            )\n")
        file.write("        ]\n")
        file.write("        variant = variants[0]\n")
        file.write('        pedal_color = "#0000FF"\n')
        file.write('        text_color = "#FFFFFF"\n')
        file.write("        super().__init__(\n")
        file.write("            name=name,\n")
        file.write("            knobs=knobs,\n")
        file.write("            footswitches=footswitches,\n")
        file.write("            variant=variant,\n")
        file.write("            variants=variants,\n")
        file.write("            pedal_color=pedal_color,\n")
        file.write("            text_color=text_color,\n")
        file.write("        )\n")
        file.write("\n")
        file.write("\n")
        file.write(f"class {variant_pedal_class_name(pedal_name, default_variant_name)}(PyFxPedalVariant):\n")
        file.write("    def process_audio(self, data: np.ndarray):\n")
        file.write(f'        """{default_variant_name} {pedal_name} Processing"""\n')
        file.write("\n")
        file.write("        # TODO: Replace this line with your processing code\n")
        file.write("        processed_data = data\n")
        file.write("\n")
        file.write("        return processed_data\n")
        file.write("\n")


def update_pedal_module(root_pedal_folder: Path, pedal_name: str, pedal: PyFxPedal):
    with open(pedal_module_file(root_pedal_folder, pedal_name)) as file:
        pedal_module_contents = file.read()

    current_knob_dict = knob_dict_parser.findall(pedal_module_contents)[0]
    current_footswitch_dict = footswitch_dict_parser.findall(pedal_module_contents)[0]

    if pedal.knobs:
        updated_knob_dict = "        knobs = {\n"
        for knob in pedal.knobs.values():
            updated_knob_dict += f'            "{knob.name}": PyFxKnob(\n'
            updated_knob_dict += f'                name="{knob.name}",\n'
            updated_knob_dict += f"                minimum_value={knob.minimum_value},\n"
            updated_knob_dict += f"                maximum_value={knob.maximum_value},\n"
            updated_knob_dict += f"                default_value={knob.default_value},\n"
            updated_knob_dict += f"                precision={knob.precision},\n"
            updated_knob_dict += f"                sensitivity={knob.sensitivity},\n"
            updated_knob_dict += f'                mode="{knob.mode}",\n'
            updated_knob_dict += f"                display_enabled={knob.display_enabled},\n"
            updated_knob_dict += f"                value={knob.value},\n"
            updated_knob_dict += "            ),\n"
        updated_knob_dict += "        }"
        pedal_module_contents = pedal_module_contents.replace(current_knob_dict, updated_knob_dict)

    if pedal.footswitches:
        updated_footswitch_dict = "        footswitches = {\n"
        for footswitch in pedal.footswitches.values():
            updated_footswitch_dict += f'            "{footswitch.name}": PyFxFootswitch(\n'
            updated_footswitch_dict += f'                name="{footswitch.name}",\n'
            updated_footswitch_dict += f'                footswitch_type="{footswitch.footswitch_type}",\n'
            updated_footswitch_dict += f"                default_state={footswitch.default_state},\n"
            updated_footswitch_dict += f"                state={footswitch.state},\n"
            if footswitch.modes:
                updated_footswitch_dict += f'                mode="{footswitch.mode}",\n'
                updated_footswitch_dict += "                modes=[\n"
                for mode in footswitch.modes:
                    updated_footswitch_dict += f'                    "{mode}",\n'
                updated_footswitch_dict += "                ],\n"
            else:
                updated_footswitch_dict += "                mode=None,\n"
                updated_footswitch_dict += "                modes=None,\n"
            updated_footswitch_dict += f"                display_enabled={footswitch.display_enabled},\n"
            updated_footswitch_dict += "            ),\n"
        updated_footswitch_dict += "        }"
        pedal_module_contents = pedal_module_contents.replace(current_footswitch_dict, updated_footswitch_dict)

    with open(pedal_module_file(root_pedal_folder, pedal_name), "w") as file:
        file.write(pedal_module_contents)


def generate_pedal_variant(root_pedal_folder: Path, pedal_name: str, variant_name: str):
    pyfx_log.debug(f"Creating pedal variant {variant_name}")

    with open(variant_module_file(root_pedal_folder, pedal_name, variant_name), "w") as file:
        file.write(f"class {variant_pedal_class_name(pedal_name, variant_name)}({pedal_class_name(pedal_name)}):\n")
        file.write("    def process_audio(self, data: np.ndarray):\n")
        file.write(f'        """{variant_name} {pedal_name} Processing"""\n')
        file.write("\n")
        file.write("        # TODO: Replace this line with your processing code\n")
        file.write("        processed_data = data\n")
        file.write("\n")
        file.write("        return processed_data\n")
        file.write("\n")


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

    """Create New Pedal"""

    def create_new_pedal(self, pedal_name: Optional[str] = None):
        if pedal_name is None:
            pedal_name = generate_pedal_name(self.root_pedal_folder)
        pedal_folder(self.root_pedal_folder, pedal_name).mkdir()
        generate_pedal_module(self.root_pedal_folder, pedal_name)
        self.pedal = load_pedal_module(self.root_pedal_folder, pedal_name)
        self.pedal.add_set_variant_observer(self.set_pedal_variant)
        self.pedal.add_add_variant_observer(self.add_pedal_variant)
        self.pedal.add_remove_variant_observer(self.remove_pedal_variant)
        self.pedal.add_change_variant_name_observer(self.change_pedal_variant_name)
        self.temporary = True

    """Open Pedal"""

    def open_pedal(self, pedal_name: str):
        self.pedal = load_pedal_module(self.root_pedal_folder, pedal_name)
        self.pedal.add_set_variant_observer(self.set_pedal_variant)
        self.pedal.add_add_variant_observer(self.add_pedal_variant)
        self.pedal.add_remove_variant_observer(self.remove_pedal_variant)
        self.pedal.add_change_variant_name_observer(self.change_pedal_variant_name)

        self.update_audio_processor()
        self.update_previous_pedal_file()

    """Close Pedal"""

    def close_pedal(self):
        try:
            if self.temporary:
                shutil.rmtree(pedal_folder(self.root_pedal_folder, self.pedal.name))
        except AttributeError:
            pass
        self.pedal = None

    """Save Pedal"""

    def save_pedal(self):
        if self.pedal is None:
            raise PedalDoesNotExistException()

        update_pedal_module(self.root_pedal_folder, self.pedal.name, self.pedal)

        self.pedal.reset_modified_flags()

        # with open(pedal_settings_file(self.root_pedal_folder, self.pedal.name), "wb") as file:
        #     pickle.dump(self.pedal, file)
        self.update_previous_pedal_file()
        self.temporary = False

    def load_pedal(self):
        with open(pedal_settings_file(self.root_pedal_folder, self.pedal.name), "rb") as file:
            pedal = pickle.load(file)
            if isinstance(pedal, PyFxPedal):
                return pedal
            else:
                raise InvalidPedalConfigException()

    def update_previous_pedal_file(self):
        with open(previous_pedal_file(self.root_pedal_folder), "w") as file:
            file.write(self.pedal.name)

    def remove_previous_pedal_file(self):
        try:
            previous_pedal_file(self.root_pedal_folder).unlink()
        except FileNotFoundError:
            pass

    def set_pedal_variant(self, variant: str):
        pyfx_log.debug(f"Set pedal variant to {variant}")

    def add_pedal_variant(self, variant_name: str):
        generate_pedal_variant(self.root_pedal_folder, self.pedal.name, variant_name)

    def update_pedal_variant(self, variant: str):
        pyfx_log.debug(f"Updating pedal variant {variant}")

    def remove_pedal_variant(self, variant: str):
        pyfx_log.debug(f"Removing pedal variant {variant}")

    def change_pedal_variant_name(self, old_variant_name: str, new_variant_name: str):
        pyfx_log.debug(f"Changing {old_variant_name} pedal variant to {new_variant_name}")

    def change_pedal_name(self, new_pedal_name: str):
        old_pedal_name = self.pedal.name
        pyfx_log.debug(f"Changing pedal name from {old_pedal_name} to {new_pedal_name}")

    def change_knob_name(self, old_knob_name: str, new_knob_name: str):
        pyfx_log.debug(f"Changing {old_knob_name} knob name to {new_knob_name}")

    def change_footswitch_name(self, old_footswitch_name: str, new_footswitch_name: str):
        pyfx_log.debug(f"Changing {old_footswitch_name} footswitch name to {new_footswitch_name}")

    """Audio Processor Control"""

    def update_audio_processor(self):
        pass
        # TODO: Add this back in
        # self.audio_processor.audio_data_processor(partial(self.pedal.process_audio, self.pedal))
