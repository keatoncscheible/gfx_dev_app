import pickle
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from gfx_dev_logging import gfx_dev_log
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QColor, QContextMenuEvent
from PySide6.QtWidgets import QDial, QDialog, QMenu, QMessageBox, QWidget


@dataclass
class KnobConfig:
    minimum_value: float = 0
    maximum_value: float = 1
    default_value: float = 0.5
    precision: float = 0.01
    sensitivity: float = 1
    mode: str = "linear"  # 'linear' or 'logarithmic'
    display_value: bool = False
    value: float = 0.5
    modified: bool = False

    def set_config_file(self, value: Path):
        if self.config_file != value:
            self.config_file = value
            self.modified = True

    def set_minimum_value(self, value: float):
        if self.minimum_value != value:
            self.minimum_value = value
            self.modified = True

    def set_maximum_value(self, value: float):
        if self.maximum_value != value:
            self.maximum_value = value
            self.modified = True

    def set_default_value(self, value: float):
        if self.default_value != value:
            self.default_value = value
            self.modified = True

    def set_precision(self, value: float):
        if self.precision != value:
            self.precision = value
            self.modified = True

    def set_sensitivity(self, value: float):
        if self.sensitivity != value:
            self.sensitivity = value
            self.modified = True

    def set_mode(self, value: str):
        if self.mode != value:
            self.mode = value
            self.modified = True

    def set_display_value(self, value: bool):
        if self.display_value != value:
            self.display_value = value
            self.modified = True

    def set_value(self, value):
        if self.value != value:
            self.value = value
            self.modified = True


class Knob(QDial):
    knob_changed = Signal(float)

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
        gfx_dev_log.debug(f"Loading knob config: {knob_config}")
        self.minimum_value = knob_config.minimum_value
        self.maximum_value = knob_config.maximum_value
        self.precision = knob_config.precision
        self.sensitivity = knob_config.sensitivity
        self.default_value = knob_config.default_value
        self.mode = knob_config.mode
        self.knob_value = np.clip(
            knob_config.value, self.minimum_value, self.maximum_value
        )
        self.update_knob_settings()

    def set_knob_value(self, value: float):
        if self.mode == "logarithmic":
            value = 20 * np.log10(value)

        if not (self.minimum_value <= value <= self.maximum_value):
            raise ValueError(
                f"Value must be within the range [{self.minimum_value}, {self.maximum_value}]"
            )
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
        self.knob_changed.emit(float_value)

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
            self.delta_acc += knob_sensitifity_factor * (
                event.position().y() - self.last_y
            )
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


class KnobComponentContextMenu(QMenu):
    def __init__(self, parent, knob_config: KnobConfig):
        super().__init__(parent)
        self.knob_config = knob_config

        # Actions
        self.action_config_knob = QAction("Configure Knob", self)

        # Add actions to the context menu
        self.addAction(self.action_config_knob)

        # Connect actions
        self.action_config_knob.triggered.connect(self.config_knob_triggered)

    def config_knob_triggered(self):
        self.knob_config_dialog = KnobConfigDialog(self.knob_config)
        if self.knob_config_dialog.exec_():
            gfx_dev_log.debug("HERE 1")
        else:
            gfx_dev_log.debug("HERE 2")


from ui.knob_component_ui import Ui_KnobComponent

# TODO: I think I may be able to change the knob values in the config without having to emit signals. Look into this


class KnobComponent(QWidget, Ui_KnobComponent):
    knob_changed = Signal(str, float)
    knob_name_changed = Signal(str, str)
    knob_config_changed = Signal(str, object)

    def __init__(self, name: str, knob_config: KnobConfig, label_color: QColor):
        super().__init__()
        self.setupUi(self)
        self.name = name
        self.knob_config = knob_config
        self.knob_name.setText(name)
        self.knob_name.setStyleSheet(f"color: {label_color.name()};")
        self.knob.load_knob_config(knob_config)
        self.knob.knob_changed.connect(self.change_knob)
        self.knob_name.label_changed.connect(self.change_knob_name)

    def change_knob(self, value: float):
        gfx_dev_log.debug(f"{self.name} changed to {value}")
        self.knob_changed.emit(self.name, value)

    def change_knob_name(self, new_name: str):
        old_name = self.name
        if old_name == new_name:
            return
        gfx_dev_log.debug(f"Knob name changed from {old_name} to {new_name}")
        self.name = new_name
        self.knob_name_changed.emit(old_name, new_name)

    def contextMenuEvent(self, event):
        self.context_menu = KnobComponentContextMenu(self, self.knob_config)
        self.context_menu.exec_(event.globalPos())
        knob_config = self.context_menu.knob_config
        if knob_config is not None and knob_config != self.knob_config:
            self.knob.load_knob_config(knob_config)
            self.knob_config_changed.emit(self.name, knob_config)
        else:
            x = 1


from ui.knob_config_dialog_ui import Ui_KnobConfigDialog


class KnobConfigDialog(QDialog, Ui_KnobConfigDialog):
    def __init__(self, knob_config: KnobConfig):
        gfx_dev_log.debug("Knob Config Dialog opened")
        super().__init__()
        self.setupUi(self)
        self.knob_config = knob_config
        self.minimum_spinbox.setValue(knob_config.minimum_value)
        self.maximum_spinbox.setValue(knob_config.maximum_value)
        self.default_spinbox.setValue(knob_config.default_value)
        self.precision_spinbox.setValue(knob_config.precision)
        self.sensitivity_spinbox.setValue(knob_config.sensitivity)
        self.mode_combobox.setCurrentText(knob_config.mode)
        self.display_value_checkbox.setChecked(knob_config.display_value)
        self.button_box.clicked.connect(self.apply_clicked)

    def apply_clicked(self):
        self.knob_config.set_minimum_value(self.minimum_spinbox.value())
        self.knob_config.set_maximum_value(self.maximum_spinbox.value())
        self.knob_config.set_default_value(self.default_spinbox.value())
        self.knob_config.set_precision(self.precision_spinbox.value())
        self.knob_config.set_sensitivity(self.sensitivity_spinbox.value())
        self.knob_config.set_mode(self.mode_combobox.currentText())
        self.knob_config.set_display_value(self.display_value_checkbox.isChecked())

        if self.knob_config.maximum_value < self.knob_config.minimum_value:
            self.show_invalid_min_max_prompt()
            return

        if not (
            self.knob_config.minimum_value
            <= self.knob_config.default_value
            <= self.knob_config.maximum_value
        ):
            self.show_invalid_default_prompt()
            return
        gfx_dev_log.debug("Knob Config applied")
        super().accept()

    def show_invalid_min_max_prompt(self):
        pedal_name_missing_prompt = QMessageBox()
        pedal_name_missing_prompt.setWindowTitle("Invalid Min/Max Values")
        pedal_name_missing_prompt.setText(
            "The minimum value must be less than the maximum value"
        )
        pedal_name_missing_prompt.setStandardButtons(QMessageBox.Ok)
        pedal_name_missing_prompt.exec_()

    def show_invalid_default_prompt(self):
        pedal_name_missing_prompt = QMessageBox()
        pedal_name_missing_prompt.setWindowTitle("Invalid Default Value")
        pedal_name_missing_prompt.setText(
            "The default value must be within the minimum and maximum value range"
        )
        pedal_name_missing_prompt.setStandardButtons(QMessageBox.Ok)
        pedal_name_missing_prompt.exec_()
