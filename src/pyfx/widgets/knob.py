from __future__ import annotations

import numpy as np
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QContextMenuEvent
from PySide6.QtWidgets import QDial, QDialog, QMenu, QMessageBox, QSizePolicy, QSpacerItem, QWidget

from pyfx.config import KnobConfig
from pyfx.logging import pyfx_log


class Knob(QDial):
    def __init__(self, parent):
        super().__init__(parent)
        self.minimum_value = None
        self.maximum_value = None
        self.precision = None
        self.sensitivity = None
        self.default_value = None
        self.mode = None
        self.knob_value = None
        self.last_y = 0
        self.delta_acc = 0
        self.setFixedSize(75, 75)
        self.valueChanged.connect(self.calc_knob_value)

    def load_knob_config(self, knob_config: KnobConfig):
        pyfx_log.debug(f"Loading knob config: {knob_config.name}")
        self.knob_config = knob_config
        self.minimum_value = knob_config.minimum_value
        self.maximum_value = knob_config.maximum_value
        self.precision = knob_config.precision
        self.sensitivity = knob_config.sensitivity
        self.default_value = knob_config.default_value
        self.mode = knob_config.mode
        self.knob_value = np.clip(knob_config.value, self.minimum_value, self.maximum_value)
        self.update_knob_settings()

    def set_knob_value(self, value: float):
        value_int = int(value / self.precision)
        self.setValue(value_int)

    def update_knob_settings(self):
        self.minimum_value_int = int(self.minimum_value / self.precision)
        self.maximum_value_int = int(self.maximum_value / self.precision)
        single_step = self.sensitivity
        page_step = 10 * self.sensitivity
        self.setMinimum(self.minimum_value_int)
        self.setMaximum(self.maximum_value_int)
        self.setSingleStep(single_step)
        self.setPageStep(page_step)
        self.set_knob_value(self.knob_value)

    def calc_knob_value(self, value: int):
        if self.mode == "linear":
            float_value = value * self.precision
        else:  # logarithmic
            float_value = 10 ** (value * self.precision / 20)
        self.knob_config.set_value(float_value)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            context_event = QContextMenuEvent(QContextMenuEvent.Mouse, event.pos())
            super().contextMenuEvent(context_event)
        else:
            self.last_y = event.position().y()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            step_cnt = self.maximum_value_int - self.minimum_value_int
            knob_sensitifity_factor = step_cnt * self.sensitivity / 100
            self.delta_acc += knob_sensitifity_factor * (event.position().y() - self.last_y)
            self.last_y = event.position().y()
            delta = int(self.delta_acc)
            self.delta_acc -= delta
            current_value = self.value()
            new_value = np.clip(
                current_value - int(delta),
                self.minimum_value_int,
                self.maximum_value_int,
            )
            if current_value == new_value:
                return
            self.setValue(new_value)

    def mouseDoubleClickEvent(self, event):
        self.set_knob_value(self.default_value)

    def mouseReleaseEvent(self, event):
        """Ignore the mouseReleaseEvent"""


from pyfx.ui.knob_component_ui import Ui_KnobComponent


class KnobComponent(QWidget, Ui_KnobComponent):
    def __init__(self, knob_config: KnobConfig):
        super().__init__()
        self.setupUi(self)
        self.knob_config = knob_config
        self.knob_name.setText(knob_config.name)
        self.knob_name.setStyleSheet("color: #ffffff;")
        self.knob.load_knob_config(knob_config)
        self.knob_name.label_changed.connect(knob_config.change_knob_name)
        self.update_knob_editbox_visibility()
        self.update_knob_editbox()

    def update_knob_editbox_visibility(self):
        visible = self.knob_config.display_enabled
        self.knob_editbox.setVisible(visible)
        self.knob_editbox_placeholder.setVisible(not visible)

    def update_knob_editbox(self):
        precision = self.knob_config.precision
        round_amount = int(np.log10(1 / precision))
        value = self.knob_config.value
        if self.knob_config.mode == "logarithmic":
            value_db = 20 * np.log10(value)
            self.knob_editbox.setText(f"{round(value_db, round_amount)} dB")
        else:
            self.knob_editbox.setText(f"{round(value, round_amount)}")

    def change_knob(self, value: float):
        pyfx_log.debug(f"{self.knob_config.name} changed to {value}")
        self.knob_config.set_value(value)
        self.update_knob_editbox()

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
