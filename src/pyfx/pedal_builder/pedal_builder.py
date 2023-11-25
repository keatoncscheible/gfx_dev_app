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


class PedalBuilder:
    pedal_config_filename: str = "pedal_cfg.pkl"

    def __init__(self, root_pedal_folder: Path, audio_processor: AudioProcessor):
        self.root_pedal_folder = root_pedal_folder
        self.audio_processor = audio_processor
        try:
            with open(self.previous_pedal_file) as file:
                pedal_name = file.read()
            self.open_pedal(pedal_name)
        except FileNotFoundError:
            self.pedal = None
            self.pedal_name = None
            self.pedal_config = None

    @property
    def pedal_folder_name(self):
        return self.pedal_name.lower().replace(" ", "_")

    @property
    def pedal_folder(self):
        return self.root_pedal_folder / self.pedal_folder_name

    @property
    def pedal_config_file(self):
        return self.pedal_folder / self.pedal_config_filename

    @property
    def pedal_module_name(self):
        return f"{self.pedal_folder_name}_pedal"

    @property
    def pedal_module_filename(self):
        return f"{self.pedal_module_name}.py"

    @property
    def pedal_module_file(self):
        return self.pedal_folder / self.pedal_module_filename

    @property
    def pedal_class_name(self):
        return "".join([word.capitalize() for word in self.pedal_module_name.split("_")])

    @property
    def previous_pedal_file(self):
        return self.root_pedal_folder / "previous_pedal"

    """Create New Pedal"""

    def create_new_pedal(self):
        self.pedal_name = self.generate_pedal_name()
        self.pedal_folder.mkdir()
        self.pedal_config = PedalConfig(name=self.pedal_name)
        self.generate_pedal_module()
        self.pedal = self.load_pedal_module()
        self.temporary = True

    """Open Pedal"""

    def open_pedal(self, name: str):
        self.pedal_name = name
        self.pedal_config = self.load_pedal_config()
        self.pedal = self.load_pedal_module()
        self.update_audio_processor()
        self.update_previous_pedal_file()

    """Close Pedal"""

    def close_pedal(self):
        try:
            if self.temporary:
                shutil.rmtree(self.pedal_folder)
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
        with open(self.pedal_config_file, "wb") as file:
            pickle.dump(self.pedal_config, file)

    def load_pedal_config(self):
        with open(self.pedal_config_file, "rb") as file:
            pedal_config = pickle.load(file)
            if isinstance(pedal_config, PedalConfig):
                return pedal_config
            else:
                raise InvalidPedalConfigException()

    def update_previous_pedal_file(self):
        with open(self.previous_pedal_file, "w") as file:
            file.write(self.pedal_name)

    def remove_previous_pedal_file(self):
        try:
            self.previous_pedal_file.unlink()
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
            file.write("    @classmethod\n")
            file.write("    @property\n")
            file.write(f"    def {property_name(name)}(self):\n")
            file.write(f'        return self.pedal_config.knobs["{name}"].value\n')
            file.write("\n")

        def create_switch_property(file, name):
            file.write("    @classmethod\n")
            file.write("    @property\n")
            file.write(f"    def {property_name(name)}(self):\n")
            file.write(f'        return self.pedal_config.footswitches["{name}"]\n')
            file.write("\n")

        with open(self.pedal_module_file, "w") as file:
            file.write('"""\n')
            file.write("This file is autogenerated and should not be modified manually.\n")
            file.write("Any changes made to this file may be overwritten.\n")
            file.write('"""\n')
            file.write("\n")
            file.write("from pyfx.config import PedalConfig\n")
            file.write("from pyfx.pedal import PyFxPedal\n")
            file.write("\n")
            file.write("\n")
            file.write(f"class {self.pedal_class_name}(PyFxPedal):\n")
            file.write(f'    """{self.pedal_name} Class"""\n')
            file.write("\n")
            file.write("    def __init__(self, pedal_config: PedalConfig):\n")
            file.write("        super().__init__(pedal_config)\n")
            file.write("\n")
            for knob_name in [knob.name for knob in self.pedal_config.knobs.values()]:
                create_knob_property(file, knob_name)
            for footswitch_name in [footswitch.name for footswitch in self.pedal_config.footswitches.values()]:
                create_switch_property(file, footswitch_name)

    def load_pedal_module(self):
        # Dynamically import pedal class from generated pedal module and return an instance of the class
        spec = importlib.util.spec_from_file_location(
            f"pedals.{self.pedal_name}.{self.pedal_module_name}", self.pedal_module_file
        )
        pedal_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pedal_module)
        pedal_class = getattr(pedal_module, self.pedal_class_name)
        return pedal_class(self.pedal_config)

    """Audio Processor Control"""

    def update_audio_processor(self):
        pass
        # TODO: Add this back in
        # self.audio_processor.audio_data_processor(partial(self.pedal.process_audio, self.pedal))
