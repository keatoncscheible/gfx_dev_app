from functools import partial
from pathlib import Path

from gfx.audio_processor import AudioProcessor
from gfx.exceptions import GfxPedalAlreadyExistsException, GfxPedalDoesNotExistException
from gfx.pedal import GfxPedal, GfxPedalConfig
from gfx_dev_logging import gfx_dev_log


class GfxDevBackend:
    root_pedal_folder = Path("app/pedals")

    def __init__(self):
        self.root_pedal_folder.mkdir(exist_ok=True)
        self._new_pedal_created_observers = []

        self.pedal = None
        self.audio_processor = AudioProcessor()

    """Create New Pedal"""

    def create_new_pedal(self, pedal_config: GfxPedalConfig):
        pedal_folder_name = pedal_config.name.lower().replace(" ", "_")
        pedal_folder = self.root_pedal_folder / pedal_folder_name

        try:
            self.pedal = GfxPedal(
                pedal_folder=pedal_folder,
                pedal_config=pedal_config,
            )
            self.update_audio_processor()
            self.pedal.add_variant_updated_observer(self.update_audio_processor)
        except GfxPedalAlreadyExistsException:
            gfx_dev_log.debug(f"{pedal_config.name} already exists")
            return

    """Open Pedal"""

    def open_pedal(self, name: str):
        pedal_folder_name = name.lower().replace(" ", "_")
        pedal_folder = self.root_pedal_folder / pedal_folder_name
        self.pedal = GfxPedal(pedal_folder)
        self.update_audio_processor()
        self.pedal.add_variant_updated_observer(self.update_audio_processor)

    """Save Pedal"""

    def save_pedal(self):
        if self.pedal is None:
            raise GfxPedalDoesNotExistException()
        self.pedal.save_pedal()

    """Audio Processor Control"""

    def update_audio_processor(self):
        self.audio_processor.audio_data_processor(
            partial(self.pedal.process_audio, self.pedal)
        )
