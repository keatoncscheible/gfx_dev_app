from PySide6.QtCore import Qt
from PySide6.QtWidgets import QAbstractButton, QDialog, QDialogButtonBox, QMessageBox

from pyfx.knob import PyFxKnob
from pyfx.logging import pyfx_log
from pyfx.ui.knob_config_dialog_ui import Ui_KnobConfigDialog


class KnobConfigDialog(QDialog, Ui_KnobConfigDialog):
    """
    Dialog for configuring the settings of a knob, including minimum, maximum, default values,
    precision, sensitivity, mode, and display options.
    """

    def __init__(self, knob: PyFxKnob):
        """
        Initializes the KnobConfigDialog with a specified knob.

        :param knob: The PyFxKnob object to configure.
        """
        super().__init__()
        self.setupUi(self)
        self.knob = knob

        # Set initial state of UI elements based on the current configuration of the knob
        self.minimum_spinbox.setValue(knob.minimum_value)
        self.maximum_spinbox.setValue(knob.maximum_value)
        self.default_spinbox.setValue(knob.default_value)
        self.precision_spinbox.setValue(knob.precision)
        self.sensitivity_spinbox.setValue(knob.sensitivity)
        self.mode_combobox.setCurrentText(knob.mode)
        self.enable_display_checkbox.setChecked(knob.display_enabled)

        # Connect UI signals to methods
        self.button_box.clicked.connect(self.button_box_clicked)
        self.mode_combobox.currentTextChanged.connect(self.update_mode_settings)
        self.update_mode_settings(knob.mode)

    def button_box_clicked(self, button: QAbstractButton):
        """
        Handles the button box click event. Updates the knob configuration based on the dialog's settings
        if the apply button was clicked.

        :param button: The button that was clicked.
        """
        standard_button = self.button_box.standardButton(button)
        if standard_button == QDialogButtonBox.Apply:
            pyfx_log.debug("Knob Config applied")
            self.apply_changes()
        else:
            pyfx_log.debug("Knob Config aborted")
            self.reject()

    def apply_changes(self):
        """
        Applies the changes made in the dialog to the knob.
        """
        pyfx_log.debug("Knob Config applied")
        self.knob.set_minimum_value(self.minimum_spinbox.value())
        self.knob.set_maximum_value(self.maximum_spinbox.value())
        self.knob.set_default_value(self.default_spinbox.value())
        self.knob.set_precision(self.precision_spinbox.value())
        self.knob.set_sensitivity(self.sensitivity_spinbox.value())
        self.knob.set_mode(self.mode_combobox.currentText())
        if self.enable_display_checkbox.isChecked():
            self.knob.set_display_enabled()
        else:
            self.knob.set_display_disabled()

        if self.knob.maximum_value < self.knob.minimum_value:
            self.show_invalid_min_max_prompt()
            return

        if not (self.knob.minimum_value <= self.knob.default_value <= self.knob.maximum_value):
            self.show_invalid_default_prompt()
            return

        super().accept()

    def update_mode_settings(self, mode: str):
        """
        Updates the dialog UI based on the selected knob mode.

        :param mode: The mode of the knob ('linear' or 'logarithmic').
        """
        suffix = " dB" if mode == "logarithmic" else ""
        self.minimum_spinbox.setSuffix(suffix)
        self.maximum_spinbox.setSuffix(suffix)
        self.default_spinbox.setSuffix(suffix)
        self.precision_spinbox.setSuffix(suffix)

    def show_invalid_min_max_prompt(self):
        """
        Shows a prompt indicating that the minimum value must be less than the maximum value.
        """
        QMessageBox.warning(self, "Invalid Min/Max Values", "The minimum value must be less than the maximum value")

    def show_invalid_default_prompt(self):
        """
        Shows a prompt indicating that the default value must be within the min and max value range.
        """
        QMessageBox.warning(
            self, "Invalid Default Value", "The default value must be within the minimum and maximum value range"
        )

    def keyPressEvent(self, event):  # noqa: N802
        """
        Overrides the key press event to ignore Enter and Return keys.

        :param event: The key press event.
        """
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            event.ignore()
        else:
            super().keyPressEvent(event)
