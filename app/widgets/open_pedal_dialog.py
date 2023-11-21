from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QMessageBox
from ui.open_pedal_dialog_ui import Ui_OpenPedalDialog


class OpenPedalDialog(QDialog, Ui_OpenPedalDialog):
    open_pedal = Signal(str)

    def __init__(self, pedal_folder: Path):
        super().__init__()
        self.setupUi(self)
        self.pedal_folder = pedal_folder

        pedal_names = [
            pedal_asset_folder.name
            for pedal_asset_folder in pedal_folder.iterdir()
            if pedal_asset_folder.is_dir()
        ]
        for pedal_name in pedal_names:
            self.pedal_list.addItem(pedal_name)

    def accept(self):
        selected_pedal = self.pedal_list.currentItem()
        if selected_pedal:
            pedal_to_open = selected_pedal.text()
            self.open_pedal.emit(pedal_to_open)
            super().accept()
        else:
            self.show_no_pedal_selected_prompt()

    def show_no_pedal_selected_prompt(self):
        pedal_name_missing_prompt = QMessageBox()
        pedal_name_missing_prompt.setWindowTitle("No Pedal Selected")
        pedal_name_missing_prompt.setText("You must select a pedal to open")
        pedal_name_missing_prompt.setStandardButtons(QMessageBox.Ok)
        pedal_name_missing_prompt.exec_()
