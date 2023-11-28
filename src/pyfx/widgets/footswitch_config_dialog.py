from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QListWidgetItem

from pyfx.config import FootswitchConfig
from pyfx.logging import pyfx_log
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

    def add_mode(self, name: Optional[str] = None):
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
