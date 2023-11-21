from gfx.pedal import GfxPedal
from gfx_dev_logging import gfx_dev_log
from PySide6.QtWidgets import QFrame
from ui.pedal_widget_ui import Ui_PedalWidget
from utils.color_utils import calculate_color_gradient
from widgets.gfx_knob_widget import GfxKnobWidget
from widgets.gfx_switch_widget import GfxSwitchWidget


class PedalWidget(QFrame, Ui_PedalWidget):
    max_knob_columns = 3
    max_switch_columns = 3

    def __init__(self, pedal: GfxPedal):
        super().__init__()
        self.setupUi(self)
        self.pedal = pedal

        self.pedal_name_label.label_changed.connect(self.change_pedal_name)

        light_pedal_color, dark_pedal_color = calculate_color_gradient(
            pedal.pedal_color, 0.5, 0.5
        )

        self.setObjectName("pedal")
        style_sheet = f"""
            #pedal {{
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                                        stop:0 {light_pedal_color.name()}, stop:1 {dark_pedal_color.name()});
                border: 3px solid {pedal.pedal_color.name()};
            }}
        """
        self.setStyleSheet(style_sheet)

        self.pedal_name_label.setText(pedal.name)
        self.pedal_name_label.setStyleSheet(f"color: {pedal.text_color.name()};")

        self.knobs = {}
        for knob_name, knob_value in pedal.knobs.items():
            knob_widget = GfxKnobWidget(
                name=knob_name, value=knob_value, label_color=pedal.text_color
            )
            knob_widget.knob_changed.connect(pedal.change_knob_value)
            knob_widget.knob_name_changed.connect(self.pedal.change_knob_name)
            self.knobs[knob_name] = knob_widget

        self.switches = {}
        for switch_name, switch_state in pedal.switches.items():
            switch_widget = GfxSwitchWidget(
                name=switch_name, state=switch_state, label_color=pedal.text_color
            )
            switch_widget.switch_toggled.connect(pedal.change_switch_state)
            switch_widget.switch_name_changed.connect(self.pedal.change_switch_name)
            self.switches[switch_name] = switch_widget

        for knob_idx, knob in enumerate(self.knobs.values()):
            row = int(knob_idx / self.max_knob_columns)
            column = knob_idx % self.max_knob_columns
            self.knob_layout.addWidget(knob, row, column)

        for switch_idx, switch in enumerate(self.switches.values()):
            row = int(switch_idx / self.max_switch_columns)
            column = switch_idx % self.max_switch_columns
            self.switch_layout.addWidget(switch, row, column)

    def change_pedal_name(self, value: str):
        gfx_dev_log.debug(f"Pedal name changed from {self.pedal.name} to {value}")
        self.pedal.set_name(value)
