from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from pyfx.logging import pyfx_log
from pyfx.ui.transport_control_widget_ui import Ui_TransportControlWidget


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
        audio_files = [filepath.name for filepath in audio_folder.iterdir() if filepath.is_file()]
        for audio_file in audio_files:
            self.audio_file_combobox.addItem(audio_file)

    def audio_file_changed(self, audio_file: str):
        audio_file_w_path = self.audio_folder / audio_file
        pyfx_log.debug(f"Audio file changed to {audio_file_w_path}")
        self.set_audio_file.emit(str(audio_file_w_path))

    def play_button_pressed(self):
        pyfx_log.debug("Play button pressed")
        self.play.emit()

    def pause_button_pressed(self):
        pyfx_log.debug("Pause button pressed")
        self.pause.emit()

    def stop_button_pressed(self):
        pyfx_log.debug("Stop button pressed")
        self.stop.emit()

    def loop_button_toggled(self, state: bool):
        state_str = "on" if state else "off"
        pyfx_log.debug(f"Looping set to {state_str}")
        self.loop.emit(state)
