from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QListWidgetItem, QMessageBox

from pyfx.ui.open_pedal_dialog_ui import Ui_OpenPedalDialog


class OpenPedalDialog(QDialog, Ui_OpenPedalDialog):
    """
    A dialog for opening an existing pedal configuration.
    Lists pedals from a specified folder and emits a signal when a pedal is selected to be opened.
    """

    open_pedal = Signal(str)

    def __init__(self, pedal_folder: Path):
        """
        Initializes the OpenPedalDialog with a specified pedal folder.

        :param pedal_folder: A Path object representing the folder where pedal configurations are stored.
        """
        super().__init__()
        self.setupUi(self)
        self.pedal_folder = pedal_folder

        # Populate the list with pedal names found in the pedal folder
        self.populate_pedal_list()

    def populate_pedal_list(self):
        """Populate the list widget with the names of pedal folders."""
        pedal_names = [
            pedal_asset_folder.name for pedal_asset_folder in self.pedal_folder.iterdir() if pedal_asset_folder.is_dir()
        ]
        for pedal_name in pedal_names:
            item = QListWidgetItem(pedal_name)
            self.pedal_list.addItem(item)

    def accept(self):
        """
        Overrides the accept method to include validation of the pedal selection.
        Emits a signal to open the selected pedal if valid, otherwise shows a prompt.
        """
        selected_pedal = self.pedal_list.currentItem()
        if selected_pedal:
            self.open_pedal.emit(selected_pedal.text())
            super().accept()
        else:
            self.show_no_pedal_selected_prompt()

    def show_no_pedal_selected_prompt(self):
        """
        Shows a prompt indicating that a pedal must be selected to open.
        """
        QMessageBox.warning(self, "No Pedal Selected", "You must select a pedal to open")
