from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QMenu, QMessageBox, QPushButton, QWidget

from pyfx.config import FootswitchConfig
from pyfx.logging import pyfx_log


class Footswitch(QPushButton):
    def __init__(self, parent):
        super().__init__()


from pyfx.ui.footswitch_component_ui import Ui_FootswitchComponent


class FootswitchComponent(QWidget, Ui_FootswitchComponent):
    footswitch_name_changed = Signal(str, str)
    remove_footswitch = Signal(object)

    def __init__(self, footswitch_config: FootswitchConfig):
        super().__init__()
        self.setupUi(self)

        self.footswitch_config = footswitch_config
        self.state = footswitch_config.state
        self.footswitch_name.setText(footswitch_config.name)
        self.footswitch.setChecked(self.state)
        self.footswitch_name.setStyleSheet("color: #ffffff;")
        self.footswitch_name.label_changed.connect(self.change_footswitch_name)

    def footswitch_toggled(self, state: bool):
        state_str = "on" if state else "off"
        pyfx_log.debug(f"{self.footswitch_config.name} turned {state_str}")
        self.footswitch_config.set_state(state)

    def change_footswitch_name(self, new_name: str):
        old_name = self.footswitch_config.name
        if old_name == new_name:
            return
        pyfx_log.debug(f"Footswitch name changed from {old_name} to {new_name}")
        self.footswitch_name_changed.emit(old_name, new_name)

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)

        # Add actions to the context menu
        action_config_footswitch = context_menu.addAction("Configure Footswitch")
        action_remove_footswitch = context_menu.addAction("Remove Footswitch")

        # Show the context menu at the cursor position
        action = context_menu.exec(event.globalPos())

        # Handle actions
        if action == action_config_footswitch:
            pyfx_log.debug("Configure Footswitch Pressed")
        elif action == action_remove_footswitch:
            pyfx_log.debug("Remove Footswitch Pressed")
            if self.show_remove_footswitch_prompt(self.name) == QMessageBox.Yes:
                self.remove_footswitch.emit(self)

    def show_remove_footswitch_prompt(self, name: str):
        return QMessageBox.question(
            self,
            "Confirmation",
            f"Are you sure you want to remove the {name} footswitch?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
