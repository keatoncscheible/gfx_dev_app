from PySide6.QtWidgets import QWidget

from pyfx.audio_interface import AudioInterface
from pyfx.ui.preferences_widget_ui import Ui_PreferencesWidget


class PreferencesWidget(QWidget, Ui_PreferencesWidget):
    def __init__(self, audio_interface: AudioInterface):
        super().__init__()
        self.setupUi(self)
        self.audio_preferences.audio_interface = audio_interface
