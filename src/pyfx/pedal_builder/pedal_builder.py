import importlib
import re
import shutil
import sys
from functools import partial
from pathlib import Path
from typing import Optional

from pyfx.audio_processor import AudioProcessor
from pyfx.exceptions import InvalidPedalConfigError, InvalidRootPedalFolderError, PedalDoesNotExistError
from pyfx.footswitch import PyFxFootswitch
from pyfx.knob import PyFxKnob
from pyfx.logging import pyfx_log
from pyfx.pedal import PyFxPedal, PyFxPedalVariant

# Helper Regexes
knob_dict_pattern = r"( *knobs\s*=\s*{\s*(?:\s*\".*?\"\s*:\s*PyFxKnob\(.*?\),)*\s*})"

footswitch_dict_pattern = r"( *footswitches\s*=\s*{\s*(?:\s*\".*?\"\s*:\s*PyFxFootswitch\(.*?\),)*\s*})"
variants_list_pattern = r"( *variants\s*=\s*\[\s*(?:\s*\w+\(.*?\),?)*\s*\])"
knob_dict_parser = re.compile(knob_dict_pattern, re.DOTALL)
footswitch_dict_parser = re.compile(footswitch_dict_pattern, re.DOTALL)
variants_list_parser = re.compile(variants_list_pattern, re.DOTALL)


def variant_class_body_pattern(pedal_class_name):
    return rf"(class {pedal_class_name}VariantBase\(PyFxPedalVariant\):\s.*?)(?=\n\n\w|$)"


def variant_class_body_parser(pedal_class_name):
    return re.compile(variant_class_body_pattern(pedal_class_name), re.DOTALL)


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


def startup_config_file(root_pedal_folder: Path):
    return root_pedal_folder / "startup.cfg"


def pedal_folder(root_pedal_folder: Path, pedal_name: str):
    return root_pedal_folder / pedal_folder_name(pedal_name)


def pedal_autogen_folder(root_pedal_folder: Path, pedal_name: str):
    return root_pedal_folder / pedal_folder_name(pedal_name) / "autogen"


def pedal_module_name(pedal_name: str):
    return f"{pedal_folder_name(pedal_name)}_pedal"


def pedal_module_filename(pedal_name: str):
    return f"{pedal_module_name(pedal_name)}.py"


def pedal_module_file(root_pedal_folder: Path, pedal_name: str):
    return pedal_autogen_folder(root_pedal_folder, pedal_name) / pedal_module_filename(pedal_name)


def pedal_variant_base_module_name(pedal_name: str):
    return f"{pedal_folder_name(pedal_name)}_pedal_variant_base"


def pedal_variant_base_module_filename(pedal_name: str):
    return f"{pedal_variant_base_module_name(pedal_name)}.py"


def pedal_variant_base_module_file(root_pedal_folder: Path, pedal_name: str):
    return pedal_autogen_folder(root_pedal_folder, pedal_name) / pedal_variant_base_module_filename(pedal_name)


def pedal_variant_base_class_name(pedal_name: str):
    return "".join([word.capitalize() for word in pedal_variant_base_module_name(pedal_name).split("_")])


def pedal_class_name(pedal_name: str):
    return "".join([word.capitalize() for word in pedal_module_name(pedal_name).split("_")])


def pedal_variant_module_name(pedal_name: str, variant_name: str):
    variant_part = variant_name.lower().replace(" ", "_")
    return f"{variant_part}_{pedal_module_name(pedal_name)}"


def pedal_variant_module_filename(pedal_name: str, variant_name: str):
    return f"{pedal_variant_module_name(pedal_name, variant_name)}.py"


def pedal_variant_module_file(root_pedal_folder: Path, pedal_name: str, variant_name: str):
    return pedal_folder(root_pedal_folder, pedal_name) / pedal_variant_module_filename(pedal_name, variant_name)


def pedal_variant_class_name(pedal_name: str, variant_name: str):
    return "".join([word.capitalize() for word in pedal_variant_module_name(pedal_name, variant_name).split("_")])


def load_pedal_module(root_pedal_folder: Path, pedal_name: str) -> PyFxPedal:
    pedal_folder_path = pedal_folder(root_pedal_folder, pedal_name).resolve().as_posix()
    sys.path.append(pedal_folder_path)
    # Dynamically import pedal class from generated pedal module and return an instance of the class
    spec = importlib.util.spec_from_file_location(
        f"{root_pedal_folder}.{pedal_folder_name(pedal_name)}.{pedal_module_name(pedal_name)}",
        pedal_module_file(root_pedal_folder, pedal_name),
    )
    pedal_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pedal_module)
    pedal_class = getattr(pedal_module, pedal_class_name(pedal_name))
    sys.path.remove(pedal_folder_path)
    return pedal_class()


class PedalBuilder:
    def __init__(self, root_pedal_folder: Path | str, audio_processor: AudioProcessor):
        if isinstance(root_pedal_folder, Path):
            pass
        elif isinstance(root_pedal_folder, str):
            root_pedal_folder = Path(root_pedal_folder)
        else:
            raise InvalidRootPedalFolderError()
        root_pedal_folder.mkdir(parents=True, exist_ok=True)

        self.root_pedal_folder = root_pedal_folder
        self.audio_processor = audio_processor
        try:
            with open(startup_config_file(self.root_pedal_folder)) as file:
                pedal_name = file.read()
            self.open_pedal(pedal_name)
        except FileNotFoundError:
            self.pedal = None

        # Used to know when pedal parameters have changed between saves
        self.prev_pedal_name = None
        self.new_variants: list[PyFxPedalVariant] = []
        self.variants_to_remove: set[str] = set()
        self.knob_name_changes: dict[str, str] = {}
        self.footswitch_name_changes: dict[str, str] = {}
        self.variant_name_changes: dict[str, str] = {}

    """Create New Pedal"""

    def create_new_pedal(self, pedal_name: Optional[str] = None):
        if pedal_name is None:
            pedal_name = generate_pedal_name(self.root_pedal_folder)
        pedal_folder(self.root_pedal_folder, pedal_name).mkdir()
        pedal_autogen_folder(self.root_pedal_folder, pedal_name).mkdir()
        default_variant_name = "Default"
        self.generate_pedal_module(pedal_name, [default_variant_name])
        self.generate_pedal_variant_base_module(pedal_name)
        self.generate_pedal_variant_module(pedal_name, default_variant_name)
        self.pedal = load_pedal_module(self.root_pedal_folder, pedal_name)
        self.pedal.add_set_variant_observer(self.set_pedal_variant)
        self.pedal.add_add_variant_observer(self.add_pedal_variant)
        self.pedal.add_remove_variant_observer(self.remove_pedal_variant)
        self.pedal.add_change_variant_name_observer(self.change_pedal_variant_name)
        self.pedal.add_change_pedal_name_observer(self.change_pedal_name)
        self.pedal.add_change_knob_name_observer(self.change_knob_name)
        self.pedal.add_change_footswitch_name_observer(self.change_footswitch_name)
        self.temporary = True

    """Open Pedal"""

    def open_pedal(self, pedal_name: str):
        self.pedal = load_pedal_module(self.root_pedal_folder, pedal_name)
        self.pedal.add_set_variant_observer(self.set_pedal_variant)
        self.pedal.add_add_variant_observer(self.add_pedal_variant)
        self.pedal.add_remove_variant_observer(self.remove_pedal_variant)
        self.pedal.add_change_variant_name_observer(self.change_pedal_variant_name)
        self.pedal.add_change_pedal_name_observer(self.change_pedal_name)
        self.pedal.add_change_knob_name_observer(self.change_knob_name)
        self.pedal.add_change_footswitch_name_observer(self.change_footswitch_name)
        self.pedal.reset_modified_flags()
        self.update_audio_processor()
        self.update_startup_config_file()

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
            raise PedalDoesNotExistError()

        if self.prev_pedal_name is not None and self.prev_pedal_name != self.pedal.name:
            # Remove pedal module file and variant base module file. They will be regenerated below
            pedal_module_file(self.root_pedal_folder, self.prev_pedal_name).unlink()
            pedal_variant_base_module_file(self.root_pedal_folder, self.prev_pedal_name).unlink()
            # Rename the pedal folder to use the updated pedal name
            pedal_folder(self.root_pedal_folder, self.prev_pedal_name).rename(
                pedal_folder(self.root_pedal_folder, self.pedal.name)
            )
            # Rename pedal variants in updated folder to have the new pedal name
            for variant in self.pedal.variants.values():
                pedal_variant_module_to_update = pedal_folder(
                    self.root_pedal_folder, self.pedal.name
                ) / pedal_variant_module_filename(self.prev_pedal_name, variant.name)
                if pedal_variant_module_to_update.exists():
                    pedal_variant_module_to_update.rename(
                        pedal_variant_module_file(self.root_pedal_folder, self.pedal.name, variant.name)
                    )

        # Rename any variant modules whose name has changed
        for old_variant_name, new_variant_name in self.variant_name_changes.items():
            pedal_variant_module_file(self.root_pedal_folder, self.pedal.name, old_variant_name).rename(
                pedal_variant_module_file(self.root_pedal_folder, self.pedal.name, new_variant_name)
            )

        # Remove variants that have been deleted
        for variant_name in self.variants_to_remove:
            variant_module = pedal_variant_module_file(self.root_pedal_folder, self.pedal.name, variant_name)
            if variant_module.exists():
                variant_module.unlink()

        # Add any new variants
        for variant in self.new_variants:
            self.generate_pedal_variant_module(self.pedal.name, variant.name)

        # Update pedal variant files
        for variant in self.pedal.variants.values():
            self.update_pedal_variant(variant)

        # Regenerate pedal module and pedal variant base module
        self.generate_pedal_module(self.pedal.name, [variant.name for variant in self.pedal.variants.values()])
        self.generate_pedal_variant_base_module(self.pedal.name)

        self.update_startup_config_file()
        self.pedal.reset_modified_flags()
        self.temporary = False
        self.prev_pedal_name = None
        self.new_variants = []
        self.variants_to_remove = set()
        self.knob_name_changes = {}
        self.footswitch_name_changes = {}
        self.variant_name_changes = {}

    def generate_pedal_module(self, pedal_name: str, variant_names: str):
        pyfx_log.debug(f"Generating {pedal_name} module")

        with open(pedal_module_file(self.root_pedal_folder, pedal_name), "w") as file:
            file.write('"""\n')
            file.write("DO NOT MODIFY THIS FILE\n")
            file.write("This file was generated using the Pedal Builder App.\n")
            file.write("Use the Pedal Builder App to make changes to this file.\n")
            file.write('"""\n')
            file.write("\n")
            for variant_name in sorted(variant_names):
                file.write(
                    f"from {pedal_variant_module_name(pedal_name, variant_name)} import {pedal_variant_class_name(pedal_name, variant_name)}\n"  # noqa: E501
                )
            file.write("\n")
            file.write("from pyfx.footswitch import PyFxFootswitch\n")
            file.write("from pyfx.knob import PyFxKnob\n")
            file.write("from pyfx.pedal import PyFxPedal\n")

            file.write("\n")
            file.write("\n")
            file.write(f"class {pedal_class_name(pedal_name)}(PyFxPedal):\n")
            file.write(f'    """{pedal_name} Class"""\n')
            file.write("\n")
            file.write("    def __init__(self):\n")
            file.write(f'        name = "{pedal_name}"\n')
            if self.pedal and self.pedal.knobs:
                file.write("        knobs = {\n")
                for knob in self.pedal.knobs.values():
                    file.write(f'            "{knob.name}": PyFxKnob(\n')
                    file.write(f'                name="{knob.name}",\n')
                    file.write(f"                minimum_value={knob.minimum_value},\n")
                    file.write(f"                maximum_value={knob.maximum_value},\n")
                    file.write(f"                default_value={knob.default_value},\n")
                    file.write(f"                precision={knob.precision},\n")
                    file.write(f"                sensitivity={knob.sensitivity},\n")
                    file.write(f'                mode="{knob.mode}",\n')
                    file.write(f"                display_enabled={knob.display_enabled},\n")
                    file.write(f"                value={knob.value},\n")
                    file.write("            ),\n")
                file.write("        }\n")
            else:
                file.write("        knobs = {}\n")

            if self.pedal and self.pedal.footswitches:
                file.write("        footswitches = {\n")
                for footswitch in self.pedal.footswitches.values():
                    footswitch_type = footswitch.footswitch_type
                    file.write(f'            "{footswitch.name}": PyFxFootswitch(\n')
                    file.write(f'                name="{footswitch.name}",\n')
                    file.write(f'                footswitch_type="{footswitch_type}",\n')
                    file.write(f"                default_state={footswitch.default_state},\n")
                    file.write(f"                state={footswitch.state},\n")
                    if footswitch_type == "mode":
                        file.write(f'                mode="{footswitch.mode}",\n')
                        file.write("                modes=[\n")
                        for mode in footswitch.modes:
                            file.write(f'                    "{mode}",\n')
                        file.write("                ],\n")
                    else:
                        file.write("                mode=None,\n")
                        file.write("                modes=None,\n")
                    file.write(f"                display_enabled={footswitch.display_enabled},\n")

                    file.write("            ),\n")
                file.write("        }\n")
            else:
                file.write("        footswitches = {}\n")

            if variant_names:
                file.write("        variants = {\n")
                for variant_name in variant_names:
                    file.write(f'            "{variant_name}": {pedal_variant_class_name(pedal_name, variant_name)}(\n')
                    file.write(f'                name="{variant_name}",\n')
                    file.write("                knobs=knobs,\n")
                    file.write("                footswitches=footswitches,\n")
                    file.write("            ),\n")
                file.write("        }\n")
            else:
                file.write("        variants = {}\n")
            if self.pedal is not None and self.pedal.variant is not None:
                file.write(f'        variant = variants["{self.pedal.variant.name}"]\n')
            elif len(variant_names) > 0:
                file.write(f'        variant = variants["{variant_names[0]}"]\n')
            else:
                file.write("        variant = None\n")
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

    def generate_pedal_variant_module(self, pedal_name: str, variant_name: str):
        with open(pedal_variant_module_file(self.root_pedal_folder, pedal_name, variant_name), "w") as file:
            file.write("import numpy as np\n")
            file.write(
                f"from autogen.{pedal_variant_base_module_name(pedal_name)} import {pedal_variant_base_class_name(pedal_name)}\n"  # noqa: E501
            )
            file.write("\n")
            file.write("\n")
            file.write(
                f"class {pedal_variant_class_name(pedal_name, variant_name)}({pedal_variant_base_class_name(pedal_name)}):\n"  # noqa: E501
            )
            file.write("    def process_audio(self, data: np.ndarray):\n")
            file.write(f'        """{variant_name} {pedal_name} Pedal Processing"""\n')
            file.write("\n")
            file.write("        # TODO: Add data processing code here\n")
            file.write("\n")
            file.write("        return data\n")

    def generate_pedal_variant_base_module(self, pedal_name: str):
        with open(pedal_variant_base_module_file(self.root_pedal_folder, pedal_name), "w") as file:
            file.write('"""\n')
            file.write("DO NOT MODIFY THIS FILE\n")
            file.write("This file was generated using the Pedal Builder App.\n")
            file.write("Use the Pedal Builder App to make changes to this file.\n")
            file.write('"""\n')
            file.write("\n")
            file.write("from pyfx.pedal import PyFxPedalVariant\n")
            file.write("\n")
            file.write("\n")
            file.write(f"class {pedal_variant_base_class_name(pedal_name)}(PyFxPedalVariant):\n")
            file.write(f'    """{pedal_name} Pedal Variant Base Class"""\n')
            if self.pedal is not None:
                for knob in self.pedal.knobs.values():
                    file.write("\n")
                    file.write(f'    """{knob.name} Knob Parameters"""\n')
                    file.write("\n")
                    file.write("    @property\n")
                    file.write(f"    def {property_name(knob.name)}(self):\n")
                    file.write(f'        return self.knobs["{knob.name}"].value\n')
                    file.write("\n")
                    file.write("    @property\n")
                    file.write(f"    def {property_name(knob.name)}_min(self):\n")
                    file.write(f'        return self.knobs["{knob.name}"].minimum_value\n')
                    file.write("\n")
                    file.write("    @property\n")
                    file.write(f"    def {property_name(knob.name)}_max(self):\n")
                    file.write(f'        return self.knobs["{knob.name}"].maximum_value\n')
                    file.write("\n")
                    file.write("    @property\n")
                    file.write(f"    def {property_name(knob.name)}_default(self):\n")
                    file.write(f'        return self.knobs["{knob.name}"].default_value\n')

                for footswitch in self.pedal.footswitches.values():
                    file.write("\n")
                    file.write(f'    """{footswitch.name} Footswitch Parameters"""\n')
                    file.write("\n")
                    if footswitch.footswitch_type == "latching":
                        file.write("    @property\n")
                        file.write(f"    def {property_name(footswitch.name)}(self):\n")
                        file.write(f'        return self.footswitches["{footswitch.name}"].state\n')
                        file.write("\n")
                        file.write("    @property\n")
                        file.write(f"    def {property_name(footswitch.name)}_default(self):\n")
                        file.write(f'        return self.footswitches["{footswitch.name}"].default_state\n')
                    elif footswitch.footswitch_type == "momentary":
                        file.write("    @property\n")
                        file.write(f"    def {property_name(footswitch.name)}(self):\n")
                        file.write(f'        return self.footswitches["{footswitch.name}"].state\n')
                        file.write("\n")
                        file.write("    @property\n")
                        file.write(f"    def {property_name(footswitch.name)}_default(self):\n")
                        file.write(f'        return self.footswitches["{footswitch.name}"].default_state\n')
                    elif footswitch.footswitch_type == "mode":
                        file.write("    @property\n")
                        file.write(f"    def {property_name(footswitch.name)}(self):\n")
                        file.write(f'        return self.footswitches["{footswitch.name}"].mode\n')
                        file.write("\n")
                        file.write("    @property\n")
                        file.write(f"    def {property_name(footswitch.name)}_modes(self):\n")
                        file.write(f'        return self.footswitches["{footswitch.name}"].modes\n')

    def update_pedal_variant(self, variant: PyFxPedalVariant):
        pyfx_log.debug(f"Updating pedal variant {variant.name}")

        with open(pedal_variant_module_file(self.root_pedal_folder, self.pedal.name, variant.name)) as file:
            pedal_variant_file_contents = file.read()

        if self.prev_pedal_name is not None:
            pedal_variant_file_contents = pedal_variant_file_contents.replace(
                pedal_variant_base_class_name(self.prev_pedal_name),
                pedal_variant_base_class_name(self.pedal.name),
            )
            pedal_variant_file_contents = pedal_variant_file_contents.replace(
                pedal_variant_base_module_name(self.prev_pedal_name),
                pedal_variant_base_module_name(self.pedal.name),
            )
            pedal_variant_file_contents = pedal_variant_file_contents.replace(
                pedal_variant_class_name(self.prev_pedal_name, variant.name),
                pedal_variant_class_name(self.pedal.name, variant.name),
            )
            pedal_variant_file_contents = pedal_variant_file_contents.replace(
                f'"""{variant.name} {self.prev_pedal_name} Pedal Processing"""',
                f'"""{variant.name} {self.pedal.name} Pedal Processing"""',
            )

        for old_knob_name, new_knob_name in self.knob_name_changes.items():
            pedal_variant_file_contents = pedal_variant_file_contents.replace(
                f"self.{property_name(old_knob_name)}",
                f"self.{property_name(new_knob_name)}",
            )
            pedal_variant_file_contents = pedal_variant_file_contents.replace(
                f"self.{property_name(old_knob_name)}_min",
                f"self.{property_name(new_knob_name)}_min",
            )
            pedal_variant_file_contents = pedal_variant_file_contents.replace(
                f"self.{property_name(old_knob_name)}_max",
                f"self.{property_name(new_knob_name)}_max",
            )
            pedal_variant_file_contents = pedal_variant_file_contents.replace(
                f"self.{property_name(old_knob_name)}_default",
                f"self.{property_name(new_knob_name)}_default",
            )

        for old_footswitch_name, new_footswitch_name in self.footswitch_name_changes.items():
            pedal_variant_file_contents = pedal_variant_file_contents.replace(
                f"self.{property_name(old_footswitch_name)}",
                f"self.{property_name(new_footswitch_name)}",
            )
            pedal_variant_file_contents = pedal_variant_file_contents.replace(
                f"self.{property_name(old_footswitch_name)}_default",
                f"self.{property_name(new_footswitch_name)}_default",
            )
            pedal_variant_file_contents = pedal_variant_file_contents.replace(
                f"self.{property_name(old_footswitch_name)}_modes",
                f"self.{property_name(new_footswitch_name)}_modes",
            )

        for old_variant_name, new_variant_name in self.variant_name_changes.items():
            pedal_variant_file_contents = pedal_variant_file_contents.replace(
                pedal_variant_class_name(self.pedal.name, old_variant_name),
                pedal_variant_class_name(self.pedal.name, new_variant_name),
            )

            pedal_variant_file_contents = pedal_variant_file_contents.replace(
                f'"""{old_variant_name} {self.pedal.name} Pedal Processing"""',
                f'"""{new_variant_name} {self.pedal.name} Pedal Processing"""',
            )

        with open(pedal_variant_module_file(self.root_pedal_folder, self.pedal.name, variant.name), "w") as file:
            file.write(pedal_variant_file_contents)

    def update_startup_config_file(self):
        with open(startup_config_file(self.root_pedal_folder), "w") as file:
            file.write(self.pedal.name)

    def remove_startup_config_file(self):
        try:
            startup_config_file(self.root_pedal_folder).unlink()
        except FileNotFoundError:
            pass

    def set_pedal_variant(self, variant: PyFxPedalVariant):
        pyfx_log.debug(f"Set pedal variant to {variant.name}")

    def add_pedal_variant(self, variant: PyFxPedalVariant):
        if variant not in self.new_variants:
            self.new_variants.append(variant)

    def remove_pedal_variant(self, variant: PyFxPedalVariant):
        pyfx_log.debug(f"Removing pedal variant {variant.name}")
        self.variants_to_remove.add(variant.name)
        for new_variant in self.new_variants.copy():
            if variant.name == new_variant.name:
                self.new_variants.remove(variant)

    def change_pedal_variant_name(self, old_variant_name: str, new_variant_name: str):
        pyfx_log.debug(f"Changing {old_variant_name} pedal variant to {new_variant_name}")
        for old_variant_name_in_dict, new_variant_name_in_dict in self.variant_name_changes.copy().items():
            if old_variant_name == new_variant_name_in_dict:
                self.variant_name_changes[old_variant_name_in_dict] = new_variant_name
                return
        self.variant_name_changes[old_variant_name] = new_variant_name

    def change_pedal_name(self, old_pedal_name: str, new_pedal_name: str):
        pyfx_log.debug(f"Changing pedal name from {old_pedal_name} to {new_pedal_name}")
        if self.prev_pedal_name is None:
            self.prev_pedal_name = old_pedal_name

    def change_knob_name(self, old_knob_name: str, new_knob_name: str):
        pyfx_log.debug(f"Changing {old_knob_name} knob name to {new_knob_name}")
        for old_knob_name_in_dict, new_knob_name_in_dict in self.knob_name_changes.copy().items():
            if old_knob_name == new_knob_name_in_dict:
                self.knob_name_changes[old_knob_name_in_dict] = new_knob_name
                return
        self.knob_name_changes[old_knob_name] = new_knob_name

    def change_footswitch_name(self, old_footswitch_name: str, new_footswitch_name: str):
        pyfx_log.debug(f"Changing {old_footswitch_name} footswitch name to {new_footswitch_name}")
        for old_footswitch_name_in_dict, new_footswitch_name_in_dict in self.footswitch_name_changes.copy().items():
            if old_footswitch_name == new_footswitch_name_in_dict:
                self.footswitch_name_changes[old_footswitch_name_in_dict] = new_footswitch_name
                return
        self.footswitch_name_changes[old_footswitch_name] = new_footswitch_name

    """Audio Processor Control"""

    def update_audio_processor(self):
        pass
        # TODO: Add this back in
        # self.audio_processor.audio_data_processor(partial(self.pedal.process_audio, self.pedal))
