from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QMessageBox
from ui.new_pedal_variant_dialog_ui import Ui_NewPedalVariantDialog


class NewPedalVariantDialog(QDialog, Ui_NewPedalVariantDialog):
    # create_new_pedal_variant = Signal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.new_pedal_variant = None

    def accept(self):
        new_pedal_variant = self.new_pedal_variant_editbox.text()
        if new_pedal_variant:
            self.new_pedal_variant = new_pedal_variant
            # self.create_new_pedal_variant.emit(new_pedal_variant)
            super().accept()
        else:
            self.show_no_variant_prompt()

    def show_no_variant_prompt(self):
        pedal_name_missing_prompt = QMessageBox()
        pedal_name_missing_prompt.setWindowTitle("No Variant Provided")
        pedal_name_missing_prompt.setText("You must set the name of the variant")
        pedal_name_missing_prompt.setStandardButtons(QMessageBox.Ok)
        pedal_name_missing_prompt.exec_()
