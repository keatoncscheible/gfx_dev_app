from PySide6.QtWidgets import QDialog, QMessageBox

from pyfx.ui.new_pedal_variant_dialog_ui import Ui_NewPedalVariantDialog


class NewPedalVariantDialog(QDialog, Ui_NewPedalVariantDialog):
    """
    A dialog for creating a new pedal variant.
    Allows the user to input a name for the new pedal variant.
    """

    def __init__(self):
        """
        Initializes the NewPedalVariantDialog.
        """
        super().__init__()
        self.setupUi(self)
        self.new_pedal_variant = None

    def accept(self):
        """
        Overrides the accept method to include validation of the new pedal variant name.
        Proceeds with the dialog acceptance only if a valid name is provided.
        """
        new_pedal_variant = self.new_pedal_variant_editbox.text().strip()
        if new_pedal_variant:
            self.new_pedal_variant = new_pedal_variant
            super().accept()
        else:
            self.show_no_variant_prompt()

    def show_no_variant_prompt(self):
        """
        Shows a prompt indicating that a name must be set for the new variant.
        """
        QMessageBox.warning(self, "No Variant Provided", "You must set the name of the variant")
