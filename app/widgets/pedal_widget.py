from gfx.pedal import GfxPedal
from gfx_dev_logging import gfx_dev_log
from PySide6.QtCore import Signal
from PySide6.QtGui import QAction, QColor
from PySide6.QtWidgets import QColorDialog, QFrame, QMenu
from ui.pedal_widget_ui import Ui_PedalWidget
from utils.color_utils import calculate_color_gradient
from widgets.gfx_knob_widget import GfxKnobWidget
from widgets.gfx_switch_widget import GfxSwitchWidget
from widgets.new_pedal_variant_dialog import NewPedalVariantDialog


class PedalContextMenu(QMenu):
    pedal_color_changed = Signal(QColor)
    text_color_changed = Signal(QColor)
    create_new_pedal_variant = Signal(str)
    change_pedal_variant = Signal(str)

    def __init__(self, parent, variant_list, active_variant):
        super().__init__(parent)
        if variant_list is None:
            variant_list = []

        # Actions
        self.action_create_new_variant = QAction("Create New Variant", self)
        self.action_select_variant = QMenu("Select Variant", self)
        self.action_change_pedal_color = QAction("Change Pedal Color", self)
        self.action_change_text_color = QAction("Change Text Color", self)

        # Add actions to the context menu
        self.addAction(self.action_create_new_variant)
        self.addMenu(self.action_select_variant)
        self.addSeparator()  # Divider
        self.addAction(self.action_change_pedal_color)
        self.addAction(self.action_change_text_color)

        # Populate the 'Select Variant' submenu
        for variant in variant_list:
            variant_action = QAction(variant, self)
            variant_action.setCheckable(True)
            variant_action.setChecked(variant == active_variant)
            self.action_select_variant.addAction(variant_action)
            variant_action.changed.connect(lambda v=variant: self.variant_selected(v))

        # Connect actions
        self.action_create_new_variant.triggered.connect(
            self.create_new_variant_triggered
        )
        self.action_change_pedal_color.triggered.connect(
            self.change_pedal_color_triggered
        )
        self.action_change_text_color.triggered.connect(
            self.change_text_color_triggered
        )

    def create_new_variant_triggered(self):
        new_pedal_variant_dialog = NewPedalVariantDialog()
        new_pedal_variant_dialog.exec_()
        self.create_new_pedal_variant.emit(new_pedal_variant_dialog.new_pedal_variant)

    def variant_selected(self, variant):
        self.change_pedal_variant.emit(variant)

    def change_pedal_color_triggered(self):
        color = QColorDialog.getColor()
        self.pedal_color_changed.emit(color)

    def change_text_color_triggered(self):
        color = QColorDialog.getColor()
        self.text_color_changed.emit(color)


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

    def contextMenuEvent(self, event):
        context_menu = PedalContextMenu(self, self.pedal.variants, self.pedal.variant)
        context_menu.pedal_color_changed.connect(self.pedal.set_pedal_color)
        context_menu.text_color_changed.connect(self.pedal.set_text_color)
        context_menu.create_new_pedal_variant.connect(self.pedal.generate_pedal_variant)
        context_menu.create_new_pedal_variant.connect(self.pedal.load_variant)
        context_menu.change_pedal_variant.connect(self.pedal.load_variant)

        context_menu.exec_(event.globalPos())

    def change_pedal_name(self, value: str):
        gfx_dev_log.debug(f"Pedal name changed from {self.pedal.name} to {value}")
        self.pedal.set_name(value)
