from PySide6.QtCore import Qt
from PySide6.QtWidgets import QAbstractButton, QDialog, QDialogButtonBox, QMessageBox

from pyfx.knob import PyFxKnob
from pyfx.logging import pyfx_log
from pyfx.ui.knob_config_dialog_ui import Ui_KnobConfigDialog


class KnobConfigDialog(QDialog, Ui_KnobConfigDialog):
    def __init__(self, knob: PyFxKnob):
        pyfx_log.debug("Knob Config Dialog opened")
        super().__init__()
        self.setupUi(self)
        self.knob = knob
        self.minimum_spinbox.setValue(knob.minimum_value)
        self.maximum_spinbox.setValue(knob.maximum_value)
        self.default_spinbox.setValue(knob.default_value)
        self.precision_spinbox.setValue(knob.precision)
        self.sensitivity_spinbox.setValue(knob.sensitivity)
        self.mode_combobox.setCurrentText(knob.mode)
        self.enable_display_checkbox.setChecked(knob.display_enabled)
        self.button_box.clicked.connect(self.button_box_clicked)
        self.mode_combobox.currentTextChanged.connect(self.change_mode_settings)

    def button_box_clicked(self, button: QAbstractButton):
        """
        Handles the button box click event. Updates the knob configuration based on the dialog's settings if the
        apply button was clicked.
        """
        standard_button = self.button_box.standardButton(button)
        if standard_button == QDialogButtonBox.Apply:
            pyfx_log.debug("Knob Config applied")
            self.knob.set_minimum_value(self.minimum_spinbox.value())
            self.knob.set_maximum_value(self.maximum_spinbox.value())
            self.knob.set_default_value(self.default_spinbox.value())
            self.knob.set_precision(self.precision_spinbox.value())
            self.knob.set_sensitivity(self.sensitivity_spinbox.value())
            self.knob.set_mode(self.mode_combobox.currentText())
            self.knob.set_display_enabled(self.enable_display_checkbox.isChecked())

            if self.knob.maximum_value < self.knob.minimum_value:
                self.show_invalid_min_max_prompt()
                return

            if not (self.knob.minimum_value <= self.knob.default_value <= self.knob.maximum_value):
                self.show_invalid_default_prompt()
                return

            super().accept()
        else:
            pyfx_log.debug("Knob Config aborted")
            super().reject()

    def change_mode_settings(self, mode: str):
        if mode == "logarithmic":
            self.minimum_spinbox.setSuffix(" dB")
            self.maximum_spinbox.setSuffix(" dB")
            self.default_spinbox.setSuffix(" dB")
            self.precision_spinbox.setSuffix(" dB")
        else:
            self.minimum_spinbox.setSuffix("")
            self.maximum_spinbox.setSuffix("")
            self.default_spinbox.setSuffix("")
            self.precision_spinbox.setSuffix("")

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            # Ignore Enter and Return keys
            event.ignore()
        else:
            # Handle other key events normally
            super().keyPressEvent(event)

    def show_invalid_min_max_prompt(self):
        pedal_name_missing_prompt = QMessageBox()
        pedal_name_missing_prompt.setWindowTitle("Invalid Min/Max Values")
        pedal_name_missing_prompt.setText("The minimum value must be less than the maximum value")
        pedal_name_missing_prompt.setStandardButtons(QMessageBox.Ok)
        pedal_name_missing_prompt.exec_()

    def show_invalid_default_prompt(self):
        pedal_name_missing_prompt = QMessageBox()
        pedal_name_missing_prompt.setWindowTitle("Invalid Default Value")
        pedal_name_missing_prompt.setText("The default value must be within the minimum and maximum value range")
        pedal_name_missing_prompt.setStandardButtons(QMessageBox.Ok)
        pedal_name_missing_prompt.exec_()
