from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QMessageBox

from pyfx.config import KnobConfig
from pyfx.logging import pyfx_log
from pyfx.ui.knob_config_dialog_ui import Ui_KnobConfigDialog


class KnobConfigDialog(QDialog, Ui_KnobConfigDialog):
    def __init__(self, knob_config: KnobConfig):
        pyfx_log.debug("Knob Config Dialog opened")
        super().__init__()
        self.setupUi(self)
        self.knob_config = knob_config
        self.minimum_spinbox.setValue(knob_config.minimum_value)
        self.maximum_spinbox.setValue(knob_config.maximum_value)
        self.default_spinbox.setValue(knob_config.default_value)
        self.precision_spinbox.setValue(knob_config.precision)
        self.sensitivity_spinbox.setValue(knob_config.sensitivity)
        self.mode_combobox.setCurrentText(knob_config.mode)
        self.enable_display_checkbox.setChecked(knob_config.display_enabled)
        self.button_box.clicked.connect(self.apply_clicked)
        self.mode_combobox.currentTextChanged.connect(self.change_mode_settings)

    def apply_clicked(self):
        self.knob_config.set_minimum_value(self.minimum_spinbox.value())
        self.knob_config.set_maximum_value(self.maximum_spinbox.value())
        self.knob_config.set_default_value(self.default_spinbox.value())
        self.knob_config.set_precision(self.precision_spinbox.value())
        self.knob_config.set_sensitivity(self.sensitivity_spinbox.value())
        self.knob_config.set_mode(self.mode_combobox.currentText())
        self.knob_config.set_display_enabled(self.enable_display_checkbox.isChecked())

        if self.knob_config.maximum_value < self.knob_config.minimum_value:
            self.show_invalid_min_max_prompt()
            return

        if not (self.knob_config.minimum_value <= self.knob_config.default_value <= self.knob_config.maximum_value):
            self.show_invalid_default_prompt()
            return
        pyfx_log.debug("Knob Config applied")
        super().accept()

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
