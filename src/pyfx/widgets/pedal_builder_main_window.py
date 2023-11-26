from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox

from pyfx.audio_processor import AudioProcessor
from pyfx.config import PedalConfig
from pyfx.exceptions import PedalDoesNotExistException
from pyfx.logging import pyfx_log
from pyfx.pedal_builder.pedal_builder import PedalBuilder
from pyfx.ui.pedal_builder_main_window_ui import Ui_PedalBuilderMainWindow
from pyfx.widgets.about_widget import AboutWidget
from pyfx.widgets.new_pedal_config_dialog import NewPedalConfigDialog
from pyfx.widgets.open_pedal_dialog import OpenPedalDialog
from pyfx.widgets.pedal_widget import PedalWidget


class PedalBuilderMainWindow(QMainWindow, Ui_PedalBuilderMainWindow):
    audio_assets = Path("src/pyfx/assets/audio")

    def __init__(self, pedal_builder: PedalBuilder, audio_processor: AudioProcessor):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("src/pyfx/assets/pyfx_logo.png"))
        self.pedal_builder = pedal_builder
        self.audio_processor = audio_processor
        if pedal_builder.pedal_config is not None:
            self.pedal_widget = PedalWidget(pedal_config=self.pedal_builder.pedal_config)
            self.pedal_layout.insertWidget(1, self.pedal_widget)
            all_knobs_displays_enabled = all(
                knob_widget.knob_config.display_enabled for knob_widget in self.pedal_widget.knob_widgets
            )
            self.action_knob_displays.setChecked(all_knobs_displays_enabled)
            all_footswitch_displays_enabled = all(
                footswitch_widget.footswitch_config.display_enabled
                for footswitch_widget in self.pedal_widget.footswitch_widgets
            )
            self.action_footswitch_displays.setChecked(all_footswitch_displays_enabled)

        else:
            self.pedal_widget = None

        # Setup transport control
        self.transport_control.set_audio_folder(self.audio_assets)
        self.transport_control.play.connect(audio_processor.play)
        self.transport_control.pause.connect(audio_processor.pause)
        self.transport_control.stop.connect(audio_processor.stop)
        self.transport_control.loop.connect(audio_processor.loop)
        self.transport_control.set_audio_file.connect(audio_processor.set_audio_file)

        self.adjust_and_center()

    """File Menu Callbacks"""

    def file__new_pedal_cb(self):
        pyfx_log.debug("File->New Pedal pressed")
        if self.prompt_for_save_if_needed():
            self.new_pedal()

    def file__open_pedal_cb(self):
        pyfx_log.debug("File->Open Pedal pressed")
        if self.prompt_for_save_if_needed():
            open_pedal_dialog = OpenPedalDialog(pedal_folder=self.pedal_builder.root_pedal_folder)
            open_pedal_dialog.open_pedal.connect(self.open_pedal)
            open_pedal_dialog.exec_()

    def file__close_pedal_cb(self):
        pyfx_log.debug("File->Close Pedal pressed")
        if self.prompt_for_save_if_needed():
            self.pedal_builder.remove_previous_pedal_file()
            self.close_pedal()

    def file__save_pedal_cb(self):
        pyfx_log.debug("File->Save Pedal pressed")
        self.save_pedal()

    def file__quit_cb(self):
        pyfx_log.debug("File->Quit pressed")
        self.close()

    """Pedal Menu Callbacks"""

    def pedal__add_knob_cb(self):
        pyfx_log.debug("Pedal->Add Knob pressed")
        self.pedal_widget.add_knob()

    def pedal__add_footswitch_cb(self):
        pyfx_log.debug("Pedal->Add Footswitch pressed")
        self.pedal_widget.add_footswitch()

    """View Menu Callbacks"""

    def view__knob_displays_cb(self, state: bool):
        pyfx_log.debug(f"View->Knob Displays pressed: {state}")
        if state:
            self.pedal_widget.show_all_knob_displays()
        else:
            self.pedal_widget.hide_all_knob_displays()

    def view__footswitch_displays_cb(self, state: bool):
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

    def show_invalid_pedal_prompt(self):
        pedal_name_missing_prompt = QMessageBox()
        pedal_name_missing_prompt.setWindowTitle("Invalid Pedal")
        pedal_name_missing_prompt.setText("The folder that you selected does not contain a valid pedal configuration.")
        pedal_name_missing_prompt.setStandardButtons(QMessageBox.Ok)
        pedal_name_missing_prompt.exec_()

    def show_no_open_pedal_prompt(self):
        nonexistent_pedal_prompt = QMessageBox()
        nonexistent_pedal_prompt.setWindowTitle("No Open Pedal")
        nonexistent_pedal_prompt.setText("There is no open pedal")
        nonexistent_pedal_prompt.setStandardButtons(QMessageBox.Ok)
        nonexistent_pedal_prompt.exec_()

    def show_save_pedal_prompt(self):
        nonexistent_pedal_prompt = QMessageBox()
        nonexistent_pedal_prompt.setWindowTitle("Save Pedal?")
        nonexistent_pedal_prompt.setText("There are changes to the current pedal. Would you like to save them")
        nonexistent_pedal_prompt.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        return nonexistent_pedal_prompt.exec_()

    def prompt_for_save_if_needed(self):
        """Prompt the user to save if there are unsaved changes

        Returns:
            True if the user saved or there was nothing to save
            False if the user decided to cancel the operation
        """
        if self.pedal_widget and self.pedal_builder.pedal_config.is_modified:
            save_pedal_prompt_response = self.show_save_pedal_prompt()
            if save_pedal_prompt_response == QMessageBox.Yes:
                self.pedal_builder.save_pedal()
            elif save_pedal_prompt_response == QMessageBox.Cancel:
                return False
        return True

    def new_pedal(self):
        self.close_pedal()
        self.pedal_builder.create_new_pedal()
        self.pedal_widget = PedalWidget(pedal_config=self.pedal_builder.pedal_config)
        self.pedal_layout.insertWidget(1, self.pedal_widget)
        self.adjust_and_center()

    def open_pedal(self, name: str):
        pyfx_log.debug(f"Opening {name} pedal")
        self.close_pedal()
        self.pedal_builder.open_pedal(name)
        self.pedal_widget = PedalWidget(pedal_config=self.pedal_builder.pedal_config)
        self.pedal_layout.insertWidget(1, self.pedal_widget)
        self.adjust_and_center()

    def close_pedal(self):
        if self.pedal_widget:
            self.pedal_builder.close_pedal()
            self.pedal_layout.removeWidget(self.pedal_widget)
            self.pedal_widget.hide()
            self.pedal_widget.deleteLater()
            self.pedal_widget = None
            self.adjust_and_center()

    def save_pedal(self):
        try:
            self.pedal_builder.save_pedal()
        except PedalDoesNotExistException:
            pass

    """Helper Functions"""

    def adjust_and_center(self):
        self.update_margins()
        self.adjustSize()
        self.central_widget.adjustSize()

        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = 50
        self.move(x, y)

    def update_margins(self):
        for i in range(self.pedal_layout.count()):
            item = self.pedal_layout.itemAt(i)
            widget = item.widget()
            if widget and isinstance(widget, PedalWidget):
                self.pedal_layout.setContentsMargins(20, 20, 20, 20)
                return
        self.pedal_layout.setContentsMargins(0, 0, 0, 0)

    """Widget Method Overrides"""

    def closeEvent(self, event):
        if self.prompt_for_save_if_needed():
            self.close_pedal()
            self.audio_processor.stop()
            QApplication.instance().closeAllWindows()
            event.accept()
        else:
            event.ignore()
