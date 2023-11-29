import numpy as np
from PySide6.QtWidgets import QDialog, QMenu, QMessageBox, QWidget

from pyfx.knob import PyFxKnob
from pyfx.logging import pyfx_log
from pyfx.ui.knob_component_ui import Ui_KnobComponent
from pyfx.widgets.knob_config_dialog import KnobConfigDialog


class KnobComponent(QWidget, Ui_KnobComponent):
    def __init__(self, knob: PyFxKnob):
        super().__init__()
        self.setupUi(self)
        self.knob = knob
        self.knob_name.setText(knob.name)
        self.knob_name.setStyleSheet("color: #ffffff;")
        self.knob_widget.configure_knob(knob)
        knob.add_set_knob_value_observer(self.change_knob)
        # self.knob_widget.set_knob_value(knob.value)
        self.knob_name.label_changed.connect(knob.change_knob_name)
        self.update_knob_editbox_visibility()
        # self.update_knob_editbox()
        self.change_knob(knob.value)

    def update_knob_editbox_visibility(self):
        visible = self.knob.display_enabled
        self.knob_editbox.setVisible(visible)
        self.knob_editbox_placeholder.setVisible(not visible)

    # def update_knob_editbox(self):
    #     precision = self.knob.precision
    #     round_amount = int(np.log10(1 / precision))
    #     value = self.knob.value
    #     if self.knob.mode == "logarithmic":
    #         value_db = 20 * np.log10(value)
    #         self.knob_editbox.setText(f"{round(value_db, round_amount)} dB")
    #     else:
    #         self.knob_editbox.setText(f"{round(value, round_amount)}")

    def change_knob(self, value: float):
        pyfx_log.debug(f"{self.knob.name} changed to {value}")
        precision = self.knob.precision
        round_amount = int(np.log10(1 / precision))
        if self.knob.mode == "logarithmic":
            value_db = 20 * np.log10(value)
            self.knob_editbox.setText(f"{round(value_db, round_amount)} dB")
        else:
            self.knob_editbox.setText(f"{round(value, round_amount)}")

    def change_knob_name(self, new_name: str):
        self.knob.chan(new_name)

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

            dialog = KnobConfigDialog(self.knob)
            dialog_result = dialog.exec_()
            if dialog_result == QDialog.Accepted:
                pyfx_log.debug(f"Updating {self.knob.name} knob configuration")
                self.knob_widget.configure_knob(self.knob)
                self.update_knob_editbox_visibility()
            else:
                pyfx_log.debug(f"Not updating {self.knob.name} knob configuration: {dialog_result}")

        elif action == action_remove_knob:
            pyfx_log.debug("Remove Knob Pressed")
            if self.show_remove_knob_prompt(self.knob.name) == QMessageBox.Yes:
                self.knob.remove_knob()

    def show_remove_knob_prompt(self, name: str):
        return QMessageBox.question(
            self,
            "Confirmation",
            f"Are you sure you want to remove the {name} knob?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
