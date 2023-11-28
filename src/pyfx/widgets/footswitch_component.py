from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QMenu, QMessageBox, QWidget

from pyfx.config import FootswitchConfig
from pyfx.logging import pyfx_log
from pyfx.ui.footswitch_component_ui import Ui_FootswitchComponent
from pyfx.widgets.footswitch_config_dialog import FootswitchConfigDialog


class FootswitchComponent(QWidget, Ui_FootswitchComponent):
    remove_footswitch = Signal(object)

    def __init__(self, footswitch_config: FootswitchConfig):
        super().__init__()
        self.setupUi(self)
        self.footswitch_config = footswitch_config
        self.state = footswitch_config.state
        self.footswitch_name.setText(footswitch_config.name)
        self.footswitch_name.setStyleSheet("color: #ffffff;")
        self.footswitch.load_footswitch_config(footswitch_config)
        self.footswitch.footswitch_pressed.connect(self.footswitch_pressed)
        self.footswitch.footswitch_released.connect(self.footswitch_released)
        self.footswitch.footswitch_clicked.connect(self.footswitch_clicked)
        self.footswitch.footswitch_toggled.connect(self.footswitch_toggled)
        self.footswitch_name.label_changed.connect(footswitch_config.change_footswitch_name)
        self.update_footswitch_editbox_visibility()
        self.update_footswitch_editbox()

    def update_footswitch_editbox_visibility(self):
        visible = self.footswitch_config.display_enabled
        self.footswitch_editbox.setVisible(visible)
        self.footswitch_editbox_placeholder.setVisible(not visible)

    def update_footswitch_editbox(self):
        footswitch_type = self.footswitch_config.footswitch_type
        if footswitch_type in ["latching", "momentary"]:
            footswitch_editbox_str = "on" if self.footswitch_config.state else "off"
        elif footswitch_type == "mode":
            footswitch_editbox_str = self.footswitch_config.mode
        self.footswitch_editbox.setText(footswitch_editbox_str)

    def footswitch_pressed(self):
        self.update_footswitch_editbox()

    def footswitch_released(self):
        self.update_footswitch_editbox()

    def footswitch_clicked(self):
        self.update_footswitch_editbox()

    def footswitch_toggled(self, state: bool):
        self.update_footswitch_editbox()

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)

        # Add actions to the context menu
        action_config_footswitch = context_menu.addAction("Configure Footswitch")
        action_remove_footswitch = context_menu.addAction("Remove Footswitch")

        # Show the context menu at the cursor position
        action = context_menu.exec(event.globalPos())

        # Handle actions
        if action == action_remove_footswitch:
            pyfx_log.debug("Remove Footswitch Pressed")
            if self.show_remove_footswitch_prompt(self.footswitch_config.name) == QMessageBox.Yes:
                self.footswitch_config.remove_footswitch()
        elif action == action_config_footswitch:
            pyfx_log.debug("Configure Footswitch Pressed")

            dialog = FootswitchConfigDialog(self.footswitch_config)
            dialog_result = dialog.exec_()
            if dialog_result == QDialog.Accepted:
                pyfx_log.debug(f"Updating {self.footswitch_config.name} footswitch configuration")
                self.footswitch.load_footswitch_config(self.footswitch_config)
                self.update_footswitch_editbox_visibility()
                self.update_footswitch_editbox()
            else:
                pyfx_log.debug(f"Not updating {self.footswitch_config.name} footswitch configuration: {dialog_result}")

    def show_remove_footswitch_prompt(self, name: str):
        return QMessageBox.question(
            self,
            "Confirmation",
            f"Are you sure you want to remove the {name} footswitch?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
