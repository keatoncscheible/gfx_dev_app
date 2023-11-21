from pathlib import Path

from gfx_dev_logging import gfx_dev_log
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from ui.transport_control_widget_ui import Ui_TransportControlWidget


class TransportControlWidget(QWidget, Ui_TransportControlWidget):
    play = Signal()
    pause = Signal()
    stop = Signal()
    loop = Signal(bool)
    set_audio_file = Signal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.audio_folder = None

    def set_audio_folder(self, audio_folder: Path):
        self.audio_folder = audio_folder
        self.populate_audio_file_combobox(audio_folder)

    def populate_audio_file_combobox(self, audio_folder: Path):
        for filepath in audio_folder.iterdir():
            if filepath.is_file():
                self.audio_file_combobox.addItem(filepath.name)

    def audio_file_changed(self, audio_file: str):
        audio_file_w_path = self.audio_folder / audio_file
        gfx_dev_log.debug(f"Audio file changed to {audio_file_w_path}")
        self.set_audio_file.emit(str(audio_file_w_path))

    def play_button_pressed(self):
        gfx_dev_log.debug("Play button pressed")
        self.play.emit()

    def pause_button_pressed(self):
        gfx_dev_log.debug("Pause button pressed")
        self.pause.emit()

    def stop_button_pressed(self):
        gfx_dev_log.debug("Stop button pressed")
        self.stop.emit()

    def loop_button_toggled(self, state: bool):
        state_str = "on" if state else "off"
        gfx_dev_log.debug(f"Looping set to {state_str}")
        self.loop.emit(state)
