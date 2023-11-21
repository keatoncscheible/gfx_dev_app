from gfx_dev_logging import gfx_dev_log
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget
from ui.gfx_switch_widget_ui import Ui_GfxSwitchWidget


class GfxSwitchWidget(QWidget, Ui_GfxSwitchWidget):
    switch_toggled = Signal(str, bool)
    switch_name_changed = Signal(str, str)

    def __init__(self, name: str, state: bool, label_color: QColor):
        super().__init__()
        self.setupUi(self)
        self.name = name
        self.gfx_switch_name.setText(name)
        self.gfx_switch.setChecked(state)
        self.gfx_switch_name.setStyleSheet(f"color: {label_color.name()};")
        self.gfx_switch_name.label_changed.connect(self.gfx_switch_name_changed)

    def gfx_switch_toggled(self, state: bool):
        state_str = "on" if state else "off"
        gfx_dev_log.debug(f"{self.name} turned {state_str}")
        self.switch_toggled.emit(self.name, state)

    def gfx_switch_name_changed(self, new_name: str):
        old_name = self.name
        if old_name == new_name:
            return
        gfx_dev_log.debug(f"Switch name changed from {old_name} to {new_name}")
        self.name = new_name
        self.switch_name_changed.emit(old_name, new_name)
