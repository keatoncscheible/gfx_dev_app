from gfx_dev_logging import gfx_dev_log
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget
from ui.gfx_knob_widget_ui import Ui_GfxKnobWidget


class GfxKnobWidget(QWidget, Ui_GfxKnobWidget):
    knob_changed = Signal(str, float)
    knob_name_changed = Signal(str, str)

    def __init__(self, name: str, value: float, label_color: QColor):
        super().__init__()
        self.setupUi(self)
        self.name = name
        self.gfx_knob_name.setText(name)
        self.gfx_knob_name.setStyleSheet(f"color: {label_color.name()};")
        self.gfx_knob.set_precision(2)
        self.gfx_knob.set_value(value)
        self.gfx_knob.knob_changed.connect(self.gfx_knob_changed)
        self.gfx_knob_name.label_changed.connect(self.gfx_knob_name_changed)

    def gfx_knob_changed(self, value: float):
        gfx_dev_log.debug(f"{self.name} changed to {value}")
        self.knob_changed.emit(self.name, value)

    def gfx_knob_name_changed(self, new_name: str):
        old_name = self.name
        gfx_dev_log.debug(f"Knob name changed from {old_name} to {new_name}")
        self.name = new_name
        self.knob_name_changed.emit(old_name, new_name)
