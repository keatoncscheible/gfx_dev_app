import os
import sys
from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox

from pyfx.audio_interface import AudioInterface
from pyfx.audio_processor import AudioProcessor
from pyfx.exceptions import PedalDoesNotExistError
from pyfx.logging import pyfx_log
from pyfx.pedal import PyFxPedal, PyFxPedalVariant
from pyfx.pedal_builder.pedal_builder import PedalBuilder
from pyfx.ui.pedal_builder_main_window_ui import Ui_PedalBuilderMainWindow
from pyfx.widgets.about_widget import AboutWidget
from pyfx.widgets.open_pedal_dialog import OpenPedalDialog
from pyfx.widgets.pedal_widget import PedalWidget
from pyfx.widgets.preferences_widget import PreferencesWidget


class VariantReloadWatcher:
    def __init__(self, reload_cb: callable):
        update_rate = 1000
        self.variant_file = None
        self.last_modified = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_for_variant_file_update)
        self.timer.start(update_rate)
        self.reload_cb = reload_cb

    def set_variant_file(self, variant_file):
        variant_module_name = variant_file.__class__.__module__
        if variant_module_name in sys.modules:
            variant_module = sys.modules[variant_module_name]
            self.variant_file = variant_module.__file__
            pyfx_log.info(f"Watching {self.variant_file} for changes")

    def check_for_variant_file_update(self):
        if self.variant_file is not None:
            current_modified = os.path.getmtime(self.variant_file)
            if self.last_modified is None:
                self.last_modified = current_modified
            elif current_modified != self.last_modified:
                self.last_modified = current_modified
                pyfx_log.debug(
                    f"Variant file update: current_modified: {current_modified}  last_modified: {self.last_modified}"
                )
                self.on_variant_file_changed()
        else:
            self.last_modified = None

    def on_variant_file_changed(self):
        pyfx_log.debug(f"{self.variant_file} has been updated")
        self.reload_cb()


class PedalBuilderMainWindow(QMainWindow, Ui_PedalBuilderMainWindow):
    """
    Main window for the Pedal Builder application.
    Handles the creation, opening, saving, and display of pedal configurations.
    """

    audio_assets = Path("src/pyfx/assets/audio")

    def __init__(self, pedal_builder: PedalBuilder, audio_processor: AudioProcessor, audio_interface: AudioInterface):
        """
        Initialize the main window.

        :param pedal_builder: PedalBuilder instance used for managing pedal objects.
        :param audio_processor: AudioProcessor instance used for audio playback control.
        """
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("src/pyfx/assets/pyfx_logo.png"))
        self.preferences = PreferencesWidget(audio_interface=audio_interface)
        self.pedal_builder = pedal_builder
        self.audio_processor = audio_processor
        self.audio_interface = audio_interface
        self.variant_reload_watcher = VariantReloadWatcher(self.reload_pedal)
        self.initialize_pedal_widget()
        self.setup_transport_control()
        self.adjust_and_center()

    def initialize_pedal_widget(self):
        """
        Initialize the pedal widget if a pedal is already present in the pedal builder.
        """
        if self.pedal_builder.pedal:
            self.pedal: PyFxPedal = self.pedal_builder.pedal
            self.update_audio_processor(self.pedal.variant)
            self.variant_reload_watcher.set_variant_file(self.pedal.variant)
            self.pedal.add_set_variant_observer(self.update_audio_processor)
            self.pedal.add_set_variant_observer(self.variant_reload_watcher.set_variant_file)
            self.pedal_widget = PedalWidget(pedal=self.pedal)
            self.pedal_layout.insertWidget(1, self.pedal_widget)
            self.update_display_actions()
        else:
            self.pedal: PyFxPedal = None
            self.pedal_widget: PedalWidget = None

    def update_display_actions(self):
        """
        Update the check states of display-related actions in the view menu.
        """
        if self.pedal_widget:
            all_knobs_displays_enabled = len(self.pedal_widget.knob_widgets) > 0 and all(
                knob.display_enabled for knob in self.pedal_widget.knob_widgets.keys()
            )
            self.action_knob_displays.setChecked(all_knobs_displays_enabled)
            all_footswitch_displays_enabled = len(self.pedal_widget.footswitch_widgets) > 0 and all(
                footswitch.display_enabled for footswitch in self.pedal_widget.footswitch_widgets.keys()
            )
            self.action_footswitch_displays.setChecked(all_footswitch_displays_enabled)

    def setup_transport_control(self):
        """
        Setup the transport control widget with audio folder and connections to audio_processor.
        """
        self.transport_control.set_audio_folder(self.audio_assets)
        self.transport_control.play.connect(self.audio_processor.play)
        self.transport_control.pause.connect(self.audio_processor.pause)
        self.transport_control.stop.connect(self.audio_processor.stop)
        self.transport_control.loop.connect(self.audio_processor.loop)
        self.transport_control.set_audio_file.connect(self.audio_processor.set_audio_file)

    """File Menu Callbacks"""

    def file__new_pedal_cb(self):
        pyfx_log.debug("File->New Pedal pressed")
        if self.prompt_for_save_if_needed():
            self.new_pedal()
            self.adjust_and_center()

    def file__open_pedal_cb(self):
        pyfx_log.debug("File->Open Pedal pressed")
        if self.prompt_for_save_if_needed():
            open_pedal_dialog = OpenPedalDialog(pedal_folder=self.pedal_builder.root_pedal_folder)
            open_pedal_dialog.open_pedal.connect(self.open_pedal)
            open_pedal_dialog.exec_()
            self.adjust_and_center()

    def file__close_pedal_cb(self):
        pyfx_log.debug("File->Close Pedal pressed")
        if self.prompt_for_save_if_needed():
            self.pedal_builder.remove_previous_pedal_file()
            self.close_pedal()
            self.adjust_and_center()

    def file__save_pedal_cb(self):
        pyfx_log.debug("File->Save Pedal pressed")
        self.save_pedal()

    def file__quit_cb(self):
        pyfx_log.debug("File->Quit pressed")
        self.close()

    def file__preferences_cb(self):
        pyfx_log.debug("File->Preferences pressed")
        self.open_preferences()

    def new_pedal(self):
        """
        Creates a new pedal and initializes the pedal widget.

        This function first closes any currently open pedal, then uses the pedal builder to create a new pedal instance.
        After creating the new pedal, it initializes and displays the pedal widget in the main window layout.
        """
        self.close_pedal()
        self.pedal_builder.create_new_pedal()
        self.pedal = self.pedal_builder.pedal
        self.update_audio_processor(self.pedal.variant)
        self.pedal.add_set_variant_observer(self.update_audio_processor)
        self.pedal.add_set_variant_observer(self.variant_reload_watcher.set_variant_file)
        self.pedal_widget = PedalWidget(pedal=self.pedal)
        self.pedal_layout.insertWidget(1, self.pedal_widget)

    def open_pedal(self, name: str):
        """
        Opens an existing pedal by name.

        :param name: The name of the pedal to be opened.

        This function closes the current pedal (if any), then uses the pedal builder to open the specified pedal.
        It then initializes the pedal widget with the opened pedal and updates the main window layout.
        """
        pyfx_log.debug(f"Opening {name} pedal")
        self.close_pedal()
        self.pedal_builder.open_pedal(name)
        self.pedal: PyFxPedal = self.pedal_builder.pedal
        self.update_audio_processor(self.pedal.variant)
        self.pedal.add_set_variant_observer(self.update_audio_processor)
        self.pedal.add_set_variant_observer(self.variant_reload_watcher.set_variant_file)
        self.pedal_widget = PedalWidget(pedal=self.pedal)
        self.pedal_layout.insertWidget(1, self.pedal_widget)

    def close_pedal(self):
        """
        Closes the currently open pedal.

        If a pedal is currently open, this function will delegate to the pedal builder to handle the closing process.
        It then removes the pedal widget from the main window layout and ensures that the window is properly adjusted.
        """
        if self.pedal_widget:
            self.pedal_builder.close_pedal()
            self.pedal_layout.removeWidget(self.pedal_widget)
            self.pedal_widget.hide()
            self.pedal_widget.deleteLater()
            self.pedal_widget = None

    def save_pedal(self):
        """
        Saves the current state of the pedal.

        This function attempts to save the current pedal using the pedal builder.
        If the pedal does not exist, it catches the `PedalDoesNotExistError` exception.
        """
        try:
            self.pedal_builder.save_pedal()
        except PedalDoesNotExistError:
            pass

    def open_preferences(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.preferences.width()) // 2
        y = 50
        self.preferences.move(x, y)
        self.preferences.show()

    def update_audio_processor(self, variant: PyFxPedalVariant):
        """Update the audio processor to use the pedal variants process audio function"""
        pyfx_log.debug(f"Set audio processor to use the {variant.name} {self.pedal.name} pedal variant")
        self.audio_processor.set_audio_data_processor(variant.process_audio)

    def reload_pedal(self):
        if self.prompt_for_save_if_needed():
            self.open_pedal(self.pedal.name)
            self.update_audio_processor(self.pedal.variant)

    """Pedal Menu Callbacks"""

    def pedal__add_knob_cb(self):
        pyfx_log.debug("Pedal->Add Knob pressed")
        self.pedal.add_knob()

    def pedal__add_footswitch_cb(self):
        pyfx_log.debug("Pedal->Add Footswitch pressed")
        self.pedal.add_footswitch()

    def pedal__reload_cb(self):
        pyfx_log.debug("Pedal->Reload pressed")
        self.reload_pedal()

    """View Menu Callbacks"""

    def view__knob_displays_cb(self, state: bool):  # noqa: FBT001
        pyfx_log.debug(f"View->Knob Displays pressed: {state}")
        if state:
            self.pedal_widget.show_all_knob_displays()
        else:
            self.pedal_widget.hide_all_knob_displays()

    def view__footswitch_displays_cb(self, state: bool):  # noqa: FBT001
        pyfx_log.debug(f"View->Footswitch Displays pressed: {state}")
        if state:
            self.pedal_widget.show_all_footswitch_displays()
        else:
            self.pedal_widget.hide_all_footswitch_displays()

    """Help Menu Callbacks"""

    def help__about_cb(self):
        pyfx_log.debug("About pressed")
        self.about_widget = AboutWidget()
        self.about_widget.show()

    """Various Prompts"""

    def show_invalid_pedal_prompt(self):
        QMessageBox.warning(
            self, "Invalid Pedal", "The folder that you selected does not contain a valid pedal configuration."
        )

    def show_no_open_pedal_prompt(self):
        QMessageBox.warning(self, "No Open Pedal", "There is no open pedal.")

    def show_save_pedal_prompt(self):
        return QMessageBox.question(
            self,
            "Save Pedal?",
            "There are changes to the current pedal. Would you like to save them?",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
        )

    def prompt_for_save_if_needed(self):
        """Prompt the user to save if there are unsaved changes

        Returns:
            True if the user saved or there was nothing to save
            False if the user decided to cancel the operation
        """
        if self.pedal_widget and self.pedal.is_modified:
            response = self.show_save_pedal_prompt()
            if response == QMessageBox.Yes:
                self.pedal_builder.save_pedal()
            elif response == QMessageBox.Cancel:
                return False
        return True

    """Helper Functions"""

    def adjust_and_center(self):
        """
        Adjust the size and position of the main window.
        """
        self.update_margins()
        self.adjustSize()
        self.central_widget.adjustSize()

        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = 50
        self.move(x, y)

    def update_margins(self):
        """
        Update the margins of the pedal layout based on the presence of a pedal widget.
        """
        margins = (20, 20, 20, 20) if self.pedal_widget else (0, 0, 0, 0)
        self.pedal_layout.setContentsMargins(*margins)

    """Widget Method Overrides"""

    def closeEvent(self, event):  # noqa: N802
        """
        Override the close event to prompt for save if needed and stop audio processor.
        """
        if self.prompt_for_save_if_needed():
            self.close_pedal()
            self.audio_processor.stop()
            QApplication.instance().closeAllWindows()
            event.accept()
        else:
            event.ignore()
