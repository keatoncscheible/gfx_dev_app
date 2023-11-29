from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QMenu, QMessageBox, QWidget

from pyfx.footswitch import PyFxFootswitch
from pyfx.logging import pyfx_log
from pyfx.ui.footswitch_component_ui import Ui_FootswitchComponent
from pyfx.widgets.footswitch_config_dialog import FootswitchConfigDialog


class FootswitchComponent(QWidget, Ui_FootswitchComponent):
    """
    Custom widget to represent a footswitch component. It includes interactive elements
    like a name label, state edit box, and the footswitch button itself.
    """

    remove_footswitch = Signal(object)

    def __init__(self, footswitch: PyFxFootswitch):
        """
        Initialize the footswitch component with a given PyFxFootswitch object.
        :param footswitch: Instance of PyFxFootswitch to be used in this component.
        """
        super().__init__()
        self.setupUi(self)
        self.footswitch = footswitch
        self.state = footswitch.state
        self.footswitch_name.setText(footswitch.name)
        self.footswitch_name.setStyleSheet("color: #ffffff;")
        self.footswitch_widget.configure_footswitch(footswitch)

        # Connect signals to slots
        self._connect_signals()

        # Update UI components based on footswitch settings
        self.update_footswitch_editbox_visibility()
        self.update_footswitch_editbox()

    def _connect_signals(self):
        """
        Connects signals from the footswitch widget to corresponding slots in this class.
        """
        self.footswitch_widget.footswitch_pressed.connect(self.footswitch_pressed)
        self.footswitch_widget.footswitch_released.connect(self.footswitch_released)
        self.footswitch_widget.footswitch_clicked.connect(self.footswitch_clicked)
        self.footswitch_widget.footswitch_toggled.connect(self.footswitch_toggled)
        self.footswitch_name.label_changed.connect(self.footswitch.change_footswitch_name)

    def update_footswitch_editbox_visibility(self):
        """
        Updates the visibility of the footswitch edit box based on the footswitch's display settings.
        """
        visible = self.footswitch.display_enabled
        self.footswitch_editbox.setVisible(visible)
        self.footswitch_editbox_placeholder.setVisible(not visible)

    def update_footswitch_editbox(self):
        """
        Updates the text displayed in the footswitch edit box based on the current state or mode.
        """
        footswitch_type = self.footswitch.footswitch_type
        if footswitch_type in ["latching", "momentary"]:
            footswitch_editbox_str = "on" if self.footswitch.state else "off"
        elif footswitch_type == "mode":
            footswitch_editbox_str = self.footswitch.mode
        self.footswitch_editbox.setText(footswitch_editbox_str)

    def footswitch_pressed(self):
        """Updates the edit box when the footswitch is pressed."""
        self.update_footswitch_editbox()

    def footswitch_released(self):
        """Updates the edit box when the footswitch is released."""
        self.update_footswitch_editbox()

    def footswitch_clicked(self):
        """Updates the edit box when the footswitch is clicked."""
        self.update_footswitch_editbox()

    def footswitch_toggled(self, state: bool):
        """
        Updates the edit box when the footswitch state is toggled.
        :param state: The new state of the footswitch.
        """
        self.update_footswitch_editbox()

    def contextMenuEvent(self, event):
        """
        Overridden method to provide a context menu for the footswitch component.
        :param event: The event triggering the context menu.
        """
        context_menu = QMenu(self)

        # Add actions to the context menu
        action_config_footswitch = context_menu.addAction("Configure Footswitch")
        action_remove_footswitch = context_menu.addAction("Remove Footswitch")

        # Show the context menu and handle actions
        action = context_menu.exec(event.globalPos())
        if action == action_remove_footswitch:
            self._handle_remove_footswitch()
        elif action == action_config_footswitch:
            self._handle_configure_footswitch()

    def _handle_remove_footswitch(self):
        """Handles the removal of the footswitch."""
        pyfx_log.debug("Remove Footswitch Pressed")
        if self.show_remove_footswitch_prompt(self.footswitch.name) == QMessageBox.Yes:
            self.footswitch.remove_footswitch()

    def _handle_configure_footswitch(self):
        """Handles the configuration of the footswitch."""
        pyfx_log.debug("Configure Footswitch Pressed")
        dialog = FootswitchConfigDialog(self.footswitch)
        dialog_result = dialog.exec_()
        if dialog_result == QDialog.Accepted:
            pyfx_log.debug(f"Updating {self.footswitch.name} footswitch configuration")
            self.footswitch_widget.configure_footswitch(self.footswitch)
            self.update_footswitch_editbox_visibility()
            self.update_footswitch_editbox()
        else:
            pyfx_log.debug(f"Not updating {self.footswitch.name} footswitch configuration: {dialog_result}")

    def show_remove_footswitch_prompt(self, name: str):
        """
        Shows a confirmation prompt before removing a footswitch.
        :param name: The name of the footswitch being removed.
        :return: User response from the prompt.
        """
        return QMessageBox.question(
            self,
            "Confirmation",
            f"Are you sure you want to remove the {name} footswitch?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
