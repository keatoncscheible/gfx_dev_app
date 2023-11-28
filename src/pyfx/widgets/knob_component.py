import numpy as np
from PySide6.QtWidgets import QDialog, QMenu, QMessageBox, QWidget

from pyfx.knob import PyFxKnob
from pyfx.logging import pyfx_log
from pyfx.ui.knob_component_ui import Ui_KnobComponent
from pyfx.widgets.knob_config_dialog import KnobConfigDialog


class KnobComponent(QWidget, Ui_KnobComponent):
    def __init__(self, knob_config: PyFxKnob):
        super().__init__()
        self.setupUi(self)
        self.knob_config = knob_config
        self.knob_name.setText(knob_config.name)
        self.knob_name.setStyleSheet("color: #ffffff;")
        self.knob.load_knob_config(knob_config)
        knob_config.add_set_knob_value_observer(self.change_knob)
        # self.knob.set_knob_value(knob_config.value)
        self.knob_name.label_changed.connect(knob_config.change_knob_name)
        self.update_knob_editbox_visibility()
        # self.update_knob_editbox()
        self.change_knob(knob_config.value)

    def update_knob_editbox_visibility(self):
        visible = self.knob_config.display_enabled
        self.knob_editbox.setVisible(visible)
        self.knob_editbox_placeholder.setVisible(not visible)

    # def update_knob_editbox(self):
    #     precision = self.knob_config.precision
    #     round_amount = int(np.log10(1 / precision))
    #     value = self.knob_config.value
    #     if self.knob_config.mode == "logarithmic":
    #         value_db = 20 * np.log10(value)
    #         self.knob_editbox.setText(f"{round(value_db, round_amount)} dB")
    #     else:
    #         self.knob_editbox.setText(f"{round(value, round_amount)}")

    def change_knob(self, value: float):
        pyfx_log.debug(f"{self.knob_config.name} changed to {value}")
        precision = self.knob_config.precision
        round_amount = int(np.log10(1 / precision))
        if self.knob_config.mode == "logarithmic":
            value_db = 20 * np.log10(value)
            self.knob_editbox.setText(f"{round(value_db, round_amount)} dB")
        else:
            self.knob_editbox.setText(f"{round(value, round_amount)}")

    def change_knob_name(self, new_name: str):
        self.knob_config.chan(new_name)

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)

        # Add actions to the context menu
        action_config_knob = context_menu.addAction("Configure Knob")
        action_remove_knob = context_menu.addAction("Remove Knob")

        # Show the context menu at the cursor position
        action = context_menu.exec(event.globalPos())

        # Handle actions
        if action == action_config_knob:
            pyfx_log.debug("Configure Knob Pressed")

            dialog = KnobConfigDialog(self.knob_config)
            dialog_result = dialog.exec_()
            if dialog_result == QDialog.Accepted:
                pyfx_log.debug(f"Updating {self.knob_config.name} knob configuration")
                self.knob.load_knob_config(self.knob_config)
                self.update_knob_editbox_visibility()
            else:
                pyfx_log.debug(f"Not updating {self.knob_config.name} knob configuration: {dialog_result}")

        elif action == action_remove_knob:
            pyfx_log.debug("Remove Knob Pressed")
            if self.show_remove_knob_prompt(self.knob_config.name) == QMessageBox.Yes:
                self.knob_config.remove_knob()

    def show_remove_knob_prompt(self, name: str):
        return QMessageBox.question(
            self,
            "Confirmation",
            f"Are you sure you want to remove the {name} knob?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
