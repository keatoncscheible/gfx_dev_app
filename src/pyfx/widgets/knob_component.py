import numpy as np
from PySide6.QtWidgets import QDialog, QMenu, QMessageBox, QWidget

from pyfx.knob import PyFxKnob
from pyfx.logging import pyfx_log
from pyfx.ui.knob_component_ui import Ui_KnobComponent
from pyfx.widgets.knob_config_dialog import KnobConfigDialog


class KnobComponent(QWidget, Ui_KnobComponent):
    """
    Custom widget to represent a knob component. This includes interactive elements like
    a knob widget, an editable label for the knob's name, and an edit box to display the knob's value.
    """

    def __init__(self, knob: PyFxKnob):
        """
        Initialize the knob component with a given PyFxKnob object.
        :param knob: Instance of PyFxKnob to be used in this component.
        """
        super().__init__()
        self.setupUi(self)
        self.knob = knob
        self.knob_name.setText(knob.name)
        self.knob_name.setStyleSheet("color: #ffffff;")
        self.knob_widget.configure_knob(knob)

        # Register an observer for knob value changes
        knob.add_set_knob_value_observer(self.change_knob)

        self.knob_name.label_changed.connect(knob.change_knob_name)
        self.update_knob_editbox_visibility()
        self.change_knob(knob.value)

    def update_knob_editbox_visibility(self):
        """
        Updates the visibility of the knob edit box based on the knob's display settings.
        """
        visible = self.knob.display_enabled
        self.knob_editbox.setVisible(visible)
        self.knob_editbox_placeholder.setVisible(not visible)

    def change_knob(self, value: float):
        """
        Update the knob's display in response to a change in value.
        :param value: The new value of the knob.
        """
        pyfx_log.debug(f"{self.knob.name} changed to {value}")
        precision = self.knob.precision
        round_amount = int(np.log10(1 / precision))
        if self.knob.mode == "logarithmic":
            value_db = 20 * np.log10(value)
            self.knob_editbox.setText(f"{round(value_db, round_amount)} dB")
        else:
            self.knob_editbox.setText(f"{round(value, round_amount)}")

    def contextMenuEvent(self, event):  # noqa: N802
        """
        Overridden method to provide a context menu for the knob component.
        :param event: The event triggering the context menu.
        """
        context_menu = QMenu(self)

        # Add actions to the context menu
        action_config_knob = context_menu.addAction("Configure Knob")
        action_remove_knob = context_menu.addAction("Remove Knob")

        # Show the context menu and handle actions
        action = context_menu.exec(event.globalPos())
        if action == action_config_knob:
            self._handle_configure_knob()
        elif action == action_remove_knob:
            self._handle_remove_knob()

    def _handle_configure_knob(self):
        """Handles the configuration of the knob."""
        pyfx_log.debug("Configure Knob Pressed")
        dialog = KnobConfigDialog(self.knob)
        dialog_result = dialog.exec_()
        if dialog_result == QDialog.Accepted:
            pyfx_log.debug(f"Updating {self.knob.name} knob configuration")
            self.knob_widget.configure_knob(self.knob)
            self.update_knob_editbox_visibility()

    def _handle_remove_knob(self):
        """Handles the removal of the knob."""
        pyfx_log.debug("Remove Knob Pressed")
        if self.show_remove_knob_prompt(self.knob.name) == QMessageBox.Yes:
            self.knob.remove_knob()

    def show_remove_knob_prompt(self, name: str):
        """
        Shows a confirmation prompt before removing a knob.
        :param name: The name of the knob being removed.
        :return: User response from the prompt.
        """
        return QMessageBox.question(
            self,
            "Confirmation",
            f"Are you sure you want to remove the {name} knob?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
