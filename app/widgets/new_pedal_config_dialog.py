import random

from gfx.pedal import GfxPedalConfig
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QDialog, QMessageBox
from ui.new_pedal_config_dialog_ui import Ui_NewPedalConfigDialog
from widgets.knob import KnobConfig


class NewPedalConfigDialog(QDialog, Ui_NewPedalConfigDialog):
    create_new_pedal = Signal(object)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        def generate_pedal_color():
            red = random.randint(0, 255)
            green = random.randint(0, 255)
            blue = random.randint(0, 255)
            pedal_color = (red, green, blue)
            return pedal_color

        def generate_text_color(pedal_color):
            # Calculate the complementary color for a given RGB color
            red, green, blue = pedal_color
            text_color = (255 - red, 255 - green, 255 - blue)
            return text_color

        pedal_color = generate_pedal_color()
        text_color = generate_text_color(pedal_color)

        self.pedal_color.set(QColor(*pedal_color))
        self.text_color.set(QColor(*text_color))

    def accept(self):
        name = self.pedal_name_editbox.text()
        knob_cnt = self.knob_cfg_spinbox.value()
        switch_cnt = self.switch_cfg_spinbox.value()
        pedal_color = self.pedal_color.value()
        text_color = self.text_color.value()

        if not name:
            self.show_pedal_name_missing_prompt()
            return

        knobs = {f"Knob {knob_idx}": KnobConfig() for knob_idx in range(knob_cnt)}
        switches = {f"Switch {switch_idx}": True for switch_idx in range(switch_cnt)}

        pedal_config = GfxPedalConfig(
            name=name,
            knobs=knobs,
            switches=switches,
            pedal_color=pedal_color,
            text_color=text_color,
        )

        self.create_new_pedal.emit(pedal_config)
        super().accept()

    def show_pedal_name_missing_prompt(self):
        pedal_name_missing_prompt = QMessageBox()
        pedal_name_missing_prompt.setWindowTitle("Missing pedal name")
        pedal_name_missing_prompt.setText("You must provide a pedal name")
        pedal_name_missing_prompt.setStandardButtons(QMessageBox.Ok)
        pedal_name_missing_prompt.exec_()
