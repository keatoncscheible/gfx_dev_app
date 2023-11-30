from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from pyfx.logging import pyfx_log
from pyfx.ui.transport_control_widget_ui import Ui_TransportControlWidget


class TransportControlWidget(QWidget, Ui_TransportControlWidget):
    """
    A widget for transport control in a media or audio application. It includes controls for play, pause, stop, loop,
    and selecting audio files.
    """

    play = Signal()
    pause = Signal()
    stop = Signal()
    loop = Signal(bool)
    set_audio_file = Signal(str)

    def __init__(self, parent):
        """
        Initialize the TransportControlWidget with a given parent.
        :param parent: The parent widget.
        """
        super().__init__(parent)
        self.setupUi(self)
        self.audio_folder = None

    def set_audio_folder(self, audio_folder: Path):
        """
        Sets the audio folder and populates the audio file combobox with audio files from the folder.
        :param audio_folder: A Path object representing the directory containing audio files.
        """
        self.audio_folder = audio_folder
        self.populate_audio_file_combobox(audio_folder)

    def populate_audio_file_combobox(self, audio_folder: Path):
        """
        Populates the audio file combobox with audio files from the specified folder.
        :param audio_folder: A Path object representing the directory containing audio files.
        """
        audio_files = [filepath.name for filepath in audio_folder.iterdir() if filepath.is_file()]
        self.audio_file_combobox.clear()
        for audio_file in audio_files:
            self.audio_file_combobox.addItem(audio_file)

    def audio_file_changed(self, audio_file: str):
        """
        Handler for when the selected audio file is changed.
        :param audio_file: The name of the selected audio file.
        """
        audio_file_w_path = self.audio_folder / audio_file
        pyfx_log.debug(f"Audio file changed to {audio_file_w_path}")
        self.set_audio_file.emit(str(audio_file_w_path))

    def play_button_pressed(self):
        """
        Handler for when the play button is pressed.
        """
        pyfx_log.debug("Play button pressed")
        self.play.emit()

    def pause_button_pressed(self):
        """
        Handler for when the pause button is pressed.
        """
        pyfx_log.debug("Pause button pressed")
        self.pause.emit()

    def stop_button_pressed(self):
        """
        Handler for when the stop button is pressed.
        """
        pyfx_log.debug("Stop button pressed")
        self.stop.emit()

    def loop_button_toggled(self, state: bool):  # noqa: FBT001
        """
        Handler for when the loop button's state is toggled.
        :param state: The new state of the loop button (True if the button is checked).
        """
        state_str = "on" if state else "off"
        pyfx_log.debug(f"Looping set to {state_str}")
        self.loop.emit(state)
