from pathlib import Path

from gfx.backend import GfxDevBackend
from gfx.exceptions import GfxPedalDoesNotExistException
from gfx.pedal import GfxPedalConfig
from gfx_dev_logging import gfx_dev_log
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.gfx_dev_main_window_ui import Ui_GfxDevMainWindow
from widgets.about_widget import AboutWidget
from widgets.new_pedal_config_dialog import NewPedalConfigDialog
from widgets.open_pedal_dialog import OpenPedalDialog
from widgets.pedal_widget import PedalWidget


class GfxDevMainWindow(QMainWindow, Ui_GfxDevMainWindow):
    audio_assets = Path("app/assets/audio")

    def __init__(self, gfx: GfxDevBackend):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("app/assets/gfx_dev_logo.png"))
        self.pedal_widget = None
        self.gfx = gfx

        # Setup transport control
        self.transport_control.set_audio_folder(self.audio_assets)
        self.transport_control.play.connect(self.gfx.audio_processor.play)
        self.transport_control.pause.connect(self.gfx.audio_processor.pause)
        self.transport_control.stop.connect(self.gfx.audio_processor.stop)
        self.transport_control.loop.connect(self.gfx.audio_processor.loop)
        self.transport_control.set_audio_file.connect(
            self.gfx.audio_processor.set_audio_file
        )

        self.adjust_and_center()

    """File Menu Callbacks"""

    def file__new_pedal_cb(self):
        gfx_dev_log.debug("File->New Pedal pressed")
        if self.prompt_for_save_if_needed():
            new_pedal_config_dialog = NewPedalConfigDialog()
            new_pedal_config_dialog.create_new_pedal.connect(self.new_pedal)
            new_pedal_config_dialog.exec_()
            # TODO: Do we need this? If so, add it to all of the dialogs
            # new_pedal_config_dialog.deleteLater()

    def file__open_pedal_cb(self):
        gfx_dev_log.debug("File->Open Pedal pressed")
        if self.prompt_for_save_if_needed():
            open_pedal_dialog = OpenPedalDialog(pedal_folder=self.gfx.root_pedal_folder)
            open_pedal_dialog.open_pedal.connect(self.open_pedal)
            open_pedal_dialog.exec_()

    def file__close_pedal_cb(self):
        gfx_dev_log.debug("File->Close Pedal pressed")
        if self.prompt_for_save_if_needed():
            self.close_pedal()

    def file__save_pedal_cb(self):
        gfx_dev_log.debug("File->Save Pedal pressed")
        self.save_pedal()

    def file__quit_cb(self):
        gfx_dev_log.debug("File->Quit pressed")
        self.close()

    """Help Menu Callbacks"""

    def help__about_cb(self):
        gfx_dev_log.debug("About pressed")
        self.about_widget = AboutWidget()
        self.about_widget.show()

    def show_invalid_pedal_prompt(self):
        pedal_name_missing_prompt = QMessageBox()
        pedal_name_missing_prompt.setWindowTitle("Invalid Pedal")
        pedal_name_missing_prompt.setText(
            "The folder that you selected does not contain a valid pedal configuration."
        )
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
        nonexistent_pedal_prompt.setText(
            "There are changes to the current pedal. Would you like to save them"
        )
        nonexistent_pedal_prompt.setStandardButtons(
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        return nonexistent_pedal_prompt.exec_()

    def prompt_for_save_if_needed(self):
        """Prompt the user to save if there are unsaved changes

        Returns:
            True if the user saved or there was nothing to save
            False if the user decided to cancel the operation
        """
        if self.pedal_widget and self.gfx.pedal.pedal_config.is_modified:
            save_pedal_prompt_response = self.show_save_pedal_prompt()
            if save_pedal_prompt_response == QMessageBox.Yes:
                self.gfx.save_pedal()
            elif save_pedal_prompt_response == QMessageBox.Cancel:
                return False
        return True

    def new_pedal(self, pedal_config: GfxPedalConfig):
        self.close_pedal()
        self.gfx.create_new_pedal(pedal_config=pedal_config)
        self.gfx.pedal.add_pedal_updated_observer(self.reload_pedal)
        self.pedal_widget = PedalWidget(pedal=self.gfx.pedal)
        self.pedal_layout.insertWidget(1, self.pedal_widget)
        self.adjust_and_center()

    def open_pedal(self, name: str):
        gfx_dev_log.debug(f"Opening {name} pedal")
        self.close_pedal()
        self.gfx.open_pedal(name)
        self.gfx.pedal.add_pedal_updated_observer(self.reload_pedal)
        self.pedal_widget = PedalWidget(pedal=self.gfx.pedal)
        self.pedal_layout.insertWidget(1, self.pedal_widget)
        self.adjust_and_center()

    def close_pedal(self):
        if self.pedal_widget:
            self.gfx.pedal.remove_pedal_updated_observer(self.reload_pedal)
            self.pedal_layout.removeWidget(self.pedal_widget)
            self.pedal_widget.hide()
            self.pedal_widget.deleteLater()
            self.pedal_widget = None
            self.adjust_and_center()

    def save_pedal(self):
        try:
            self.gfx.save_pedal()
        except GfxPedalDoesNotExistException:
            pass

    def reload_pedal(self):
        pedal_name = self.pedal_widget.pedal.name
        gfx_dev_log.debug(f"Reloading {pedal_name} pedal widget")
        self.open_pedal(pedal_name)

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
            self.gfx.audio_processor.stop()
            QApplication.instance().closeAllWindows()
            event.accept()
        else:
            event.ignore()
