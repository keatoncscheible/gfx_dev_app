from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QDialog, QListWidgetItem, QMenu, QMessageBox, QPushButton, QWidget

from pyfx.config import FootswitchConfig
from pyfx.logging import pyfx_log


class Footswitch(QPushButton):
    footswitch_pressed = Signal()
    footswitch_released = Signal()
    footswitch_clicked = Signal()
    footswitch_toggled = Signal(bool)

    def __init__(self, parent):
        super().__init__(parent)

    def load_footswitch_config(self, footswitch_config: FootswitchConfig):
        pyfx_log.debug(f"Loading Footswitch config: {footswitch_config.name}")
        self.footswitch_config = footswitch_config
        footswitch_type = footswitch_config.footswitch_type
        try:
            self.pressed.disconnect()
        except RuntimeError:
            pass
        try:
            self.released.disconnect()
        except RuntimeError:
            pass
        try:
            self.toggled.disconnect()
        except RuntimeError:
            pass
        try:
            self.clicked.disconnect()
        except RuntimeError:
            pass

        if footswitch_type == "latching":
            self.setCheckable(True)
            self.setChecked(footswitch_config.state)
            self.toggled.connect(self.footswitch_toggled_cb)
        elif footswitch_type == "momentary":
            self.setCheckable(True)
            self.setChecked(footswitch_config.default_state)
            self.pressed.connect(self.footswitch_pressed_cb)
            self.released.connect(self.footswitch_released_cb)
        elif footswitch_type == "mode":
            self.setCheckable(False)
            self.clicked.connect(self.footswitch_clicked_cb)

    def footswitch_pressed_cb(self):
        pyfx_log.debug(f"{self.footswitch_config.name} pressed")
        state = not self.footswitch_config.default_state
        self.footswitch_config.set_state(state)
        self.setChecked(state)
        self.footswitch_pressed.emit()

    def footswitch_released_cb(self):
        pyfx_log.debug(f"{self.footswitch_config.name} released")
        state = self.footswitch_config.default_state
        self.footswitch_config.set_state(state)
        self.setChecked(state)
        self.footswitch_released.emit()

    def footswitch_toggled_cb(self, state: bool):
        state_str = "on" if state else "off"
        pyfx_log.debug(f"{self.footswitch_config.name} turned {state_str}")
        self.footswitch_config.set_state(state)
        self.footswitch_toggled.emit(state)

    def footswitch_clicked_cb(self):
        self.footswitch_config.next_mode()
        pyfx_log.debug(f"{self.footswitch_config.name} mode changed to {self.footswitch_config.mode}")
        self.footswitch_clicked.emit()


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
        self.footswitch_name.setStyleSheet("color: #ffffff;")
        self.footswitch.load_footswitch_config(footswitch_config)
        self.footswitch.footswitch_pressed.connect(self.footswitch_pressed)
        self.footswitch.footswitch_released.connect(self.footswitch_released)
        self.footswitch.footswitch_clicked.connect(self.footswitch_clicked)
        self.footswitch.footswitch_toggled.connect(self.footswitch_toggled)
        self.footswitch_name.label_changed.connect(self.change_footswitch_name)
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
        if action == action_remove_footswitch:
            pyfx_log.debug("Remove Footswitch Pressed")
            if self.show_remove_footswitch_prompt(self.footswitch_config.name) == QMessageBox.Yes:
                self.remove_footswitch.emit(self)
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
                pyfx_log.debug(f"Not updating {self.footswitch_config.name} knob configuration: {dialog_result}")

    def show_remove_footswitch_prompt(self, name: str):
        return QMessageBox.question(
            self,
            "Confirmation",
            f"Are you sure you want to remove the {name} footswitch?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )


from pyfx.ui.footswitch_config_dialog_ui import Ui_FootswitchConfigDialog


class FootswitchConfigDialog(QDialog, Ui_FootswitchConfigDialog):
    def __init__(self, footswitch_config: FootswitchConfig):
        pyfx_log.debug("Footswitch Config Dialog opened")
        super().__init__()
        self.setupUi(self)
        self.footswitch_config = footswitch_config
        footswitch_type = footswitch_config.footswitch_type
        self.footswitch_type_combobox.setCurrentText(footswitch_type)
        self.enable_display_checkbox.setChecked(footswitch_config.display_enabled)
        if footswitch_type == "momentary":
            self.default_combobox.setCurrentText("on" if footswitch_config.default_state else "off")
        elif footswitch_type == "mode":
            for mode in self.footswitch_config.modes:
                self.add_mode(mode)

        self.footswitch_type_combobox.currentTextChanged.connect(self.change_footswitch_type_settings)
        self.change_footswitch_type_settings(footswitch_config.footswitch_type)
        self.add_mode_button.pressed.connect(self.add_mode)
        self.remove_mode_button.pressed.connect(self.remove_selected_mode)
        self.move_mode_up_button.pressed.connect(self.move_selected_mode_up)
        self.move_mode_down_button.pressed.connect(self.move_selected_mode_down)

        self.button_box.clicked.connect(self.apply_clicked)

    def apply_clicked(self):
        pyfx_log.debug("Footswitch Config applied")
        footswitch_type = self.footswitch_type_combobox.currentText()
        self.footswitch_config.set_footswitch_type(footswitch_type)
        self.footswitch_config.set_display_enabled(self.enable_display_checkbox.isChecked())
        if footswitch_type == "latching":
            self.footswitch_config.set_state(True)
            self.footswitch_config.set_default_state(True)
            self.footswitch_config.set_modes(None)
        elif footswitch_type == "momentary":
            default_state = True if self.default_combobox.currentText() == "on" else False
            self.footswitch_config.set_modes(None)
            self.footswitch_config.set_default_state(default_state)
            self.footswitch_config.set_state(default_state)
        elif footswitch_type == "mode":
            modes = [self.modes_list.item(i).text() for i in range(self.modes_list.count())]
            self.footswitch_config.set_modes(modes)
            self.footswitch_config.set_default_state(None)
            self.footswitch_config.set_state(None)

        super().accept()

    def change_footswitch_type_settings(self, footswitch_type: str):
        pyfx_log.debug(f"Footswitch type changed to {footswitch_type}")
        if footswitch_type == "latching":
            self.hide_mode_widgets()
            self.hide_default_state_widgets()
        elif footswitch_type == "momentary":
            self.hide_mode_widgets()
            self.show_default_state_widgets()
        elif footswitch_type == "mode":
            self.hide_default_state_widgets()
            self.show_mode_widgets()
        self.adjustSize()

    def hide_default_state_widgets(self):
        self.default_combobox.hide()
        self.default_label.hide()

    def show_default_state_widgets(self):
        self.default_combobox.show()
        self.default_label.show()

    def hide_mode_widgets(self):
        self.modes_label.hide()
        self.modes_list.hide()
        self.add_mode_button.hide()
        self.remove_mode_button.hide()
        self.move_mode_up_button.hide()
        self.move_mode_down_button.hide()

    def show_mode_widgets(self):
        self.modes_label.show()
        self.modes_list.show()
        self.add_mode_button.show()
        self.remove_mode_button.show()
        self.move_mode_up_button.show()
        self.move_mode_down_button.show()

    def add_mode(self, name: str = None):
        if name is None:
            mode_idx = self.modes_list.count() + 1
            name = f"Mode {mode_idx}"
        item = QListWidgetItem(name, self.modes_list)
        item.setFlags(item.flags() | Qt.ItemIsEditable)

    def remove_selected_mode(self):
        selected_item = self.modes_list.currentItem()
        if selected_item:
            row = self.modes_list.row(selected_item)
            self.modes_list.takeItem(row)

    def move_selected_mode_up(self):
        row = self.modes_list.currentRow()
        if row > 0:
            item = self.modes_list.takeItem(row)
            self.modes_list.insertItem(row - 1, item)
            self.modes_list.setCurrentRow(row - 1)

    def move_selected_mode_down(self):
        row = self.modes_list.currentRow()
        if row < self.modes_list.count() - 1:
            item = self.modes_list.takeItem(row)
            self.modes_list.insertItem(row + 1, item)
            self.modes_list.setCurrentRow(row + 1)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            event.ignore()
        else:
            super().keyPressEvent(event)
