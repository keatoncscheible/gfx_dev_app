from functools import partial

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QColorDialog, QDialog, QFrame, QInputDialog, QMenu, QMessageBox

from pyfx.footswitch import PyFxFootswitch
from pyfx.knob import PyFxKnob
from pyfx.logging import pyfx_log
from pyfx.pedal import PyFxPedal
from pyfx.ui.pedal_widget_ui import Ui_PedalWidget
from pyfx.utils.color_utils import calculate_color_gradient
from pyfx.widgets.footswitch_component import FootswitchComponent
from pyfx.widgets.knob_component import KnobComponent
from pyfx.widgets.new_pedal_variant_dialog import NewPedalVariantDialog


class PedalWidget(QFrame, Ui_PedalWidget):
    max_knob_columns = 3
    max_footswitch_columns = 3

    def __init__(self, pedal: PyFxPedal):
        super().__init__()
        self.setupUi(self)
        self.pedal = pedal
        self.pedal.add_change_pedal_name_observer(self.set_pedal_name)
        self.pedal.add_add_knob_observer(self.add_knob)
        self.pedal.add_remove_knob_observer(self.remove_knob)
        self.pedal.add_add_footswitch_observer(self.add_footswitch)
        self.pedal.add_remove_footswitch_observer(self.remove_footswitch)
        self.pedal.add_set_pedal_color_observer(self.set_pedal_color)
        self.pedal.add_set_text_color_observer(self.set_text_color)
        self.pedal_name_label.label_changed.connect(self.pedal.change_pedal_name)

        self.knob_widgets: dict[PyFxKnob, KnobComponent] = {}
        self.footswitch_widgets: dict[PyFxFootswitch, FootswitchComponent] = {}

        for knob_config in pedal.knobs.values():
            self.add_knob(knob_config)

        for footswitch_config in pedal.footswitches.values():
            self.add_footswitch(footswitch_config)

        self.set_pedal_name(self.pedal.name)
        self.set_pedal_color(self.pedal.pedal_color)
        self.set_text_color(self.pedal.text_color)

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)

        variants = self.pedal.variants

        # Add actions to the context menu
        add_knob_action = context_menu.addAction("Add Knob")
        add_footswitch_action = context_menu.addAction("Add Footswitch")
        context_menu.addSeparator()
        create_new_variant_action = context_menu.addAction("Create New Variant")
        if variants:
            select_variant_menu = context_menu.addMenu("Select Variant")
            remove_variant_menu = context_menu.addMenu("Remove Variant")
            change_variant_name_menu = context_menu.addMenu("Change Variant Name")
        context_menu.addSeparator()
        change_pedal_color_action = context_menu.addAction("Change Pedal Color")
        change_text_color_action = context_menu.addAction("Change Text Color")

        def variant_selected(variant):
            pyfx_log.debug(f"Variant {variant} selected")
            self.pedal.set_variant(variant)

        def show_remove_variant_conformation_prompt(variant: str):
            message = f"Are you sure you want to remove the {variant} variant? These changes cannot be undone."
            confirmation_prompt = QMessageBox()
            confirmation_prompt.setIcon(QMessageBox.Warning)
            confirmation_prompt.setWindowTitle("Confirm Variant Removal")
            confirmation_prompt.setText(message)
            confirmation_prompt.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            confirmation_prompt.setDefaultButton(QMessageBox.No)

            return confirmation_prompt.exec() == QMessageBox.Yes

        def variant_removed(variant):
            if show_remove_variant_conformation_prompt(variant):
                pyfx_log.debug(f"Variant {variant} removed")
                self.pedal.remove_variant(variant)

        def variant_name_changed(variant):
            new_variant, ok = QInputDialog.getText(None, "Input New Variant", "New Variant Name:")
            if not ok or not new_variant:
                return None
            pyfx_log.debug(f"Variant name changed from {variant} to {new_variant}")
            self.pedal.change_variant_name(variant, new_variant)

        for variant in self.pedal.variants:
            select_variant_action = select_variant_menu.addAction(variant)
            select_variant_action.setCheckable(True)
            select_variant_action.setChecked(variant == self.pedal.variant)
            select_variant_action.triggered.connect(partial(variant_selected, variant))
            remove_variant_action = remove_variant_menu.addAction(variant)
            remove_variant_action.triggered.connect(partial(variant_removed, variant))
            change_variant_name_action = change_variant_name_menu.addAction(variant)
            change_variant_name_action.triggered.connect(partial(variant_name_changed, variant))

        # Show the context menu at the cursor position
        action = context_menu.exec(event.globalPos())

        # Handle actions
        if action == add_knob_action:
            self.pedal.add_knob()
        elif action == add_footswitch_action:
            self.pedal.add_footswitch()
        elif action == create_new_variant_action:
            pyfx_log.debug("Create New Variant Pressed")
            dialog = NewPedalVariantDialog()
            if dialog.exec_() == QDialog.Accepted:
                variant = dialog.new_pedal_variant
                pyfx_log.debug(f"Created {variant} variant")

                self.pedal.add_variant(variant)
        elif action == change_pedal_color_action:
            pyfx_log.debug("Change Pedal Color Pressed")
            color = QColorDialog.getColor()
            self.pedal.set_pedal_color(color.name())
        elif action == change_text_color_action:
            pyfx_log.debug("Change Pedal Color Pressed")
            color = QColorDialog.getColor()
            self.pedal.set_text_color(color.name())

    def set_pedal_name(self, name: str):
        pyfx_log.debug(f"Pedal name changed from {self.pedal.name} to {name}")
        self.pedal_name_label.setText(name)

    def set_pedal_color(self, color: str):
        color = QColor(color)
        light_pedal_color, dark_pedal_color = calculate_color_gradient(color, 0.5, 0.5)

        self.setObjectName("pedal")
        style_sheet = f"""
            #pedal {{
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                                        stop:0 {light_pedal_color.name()}, stop:1 {dark_pedal_color.name()});
                border: 3px solid {color.name()};
            }}
        """
        self.setStyleSheet(style_sheet)

    def set_text_color(self, color: str):
        color = QColor(color)
        style_sheet = f"""
            color: {color.name()};
        """
        self.pedal_name_label.setStyleSheet(style_sheet)
        for knob_widget in self.knob_widgets.values():
            knob_widget.knob_name.setStyleSheet(style_sheet)
        for footswitch_widget in self.footswitch_widgets.values():
            footswitch_widget.footswitch_name.setStyleSheet(style_sheet)

    def generate_knob_name(self):
        knob_idx = 1
        while True:
            knob_name = f"Knob {knob_idx}"
            if knob_name not in self.pedal.knobs:
                return knob_name
            knob_idx += 1

    def generate_footswitch_name(self):
        footswitch_idx = 1
        while True:
            footswitch_name = f"Footswitch {footswitch_idx}"
            if footswitch_name not in self.pedal.footswitches:
                return footswitch_name
            footswitch_idx += 1

    def add_knob(self, knob_config: PyFxKnob):
        knob_widget = KnobComponent(knob_config=knob_config)
        self.knob_widgets[knob_config] = knob_widget
        knob_cnt = len(self.knob_widgets)
        row = int((knob_cnt - 1) / self.max_knob_columns)
        column = (knob_cnt - 1) % self.max_knob_columns
        self.knob_layout.addWidget(knob_widget, row, column)

    def remove_knob(self, knob_config: PyFxKnob):
        self.knob_layout.removeWidget(self.knob_widgets[knob_config])
        self.knob_widgets[knob_config].deleteLater()
        del self.knob_widgets[knob_config]

    def add_footswitch(self, footswitch_config: PyFxFootswitch = None):
        footswitch_widget = FootswitchComponent(footswitch_config=footswitch_config)
        self.footswitch_widgets[footswitch_config] = footswitch_widget
        footswitch_cnt = len(self.footswitch_widgets)
        row = int((footswitch_cnt - 1) / self.max_footswitch_columns)
        column = (footswitch_cnt - 1) % self.max_footswitch_columns
        self.footswitch_layout.addWidget(footswitch_widget, row, column)

    def remove_footswitch(self, footswitch_config: FootswitchComponent):
        self.footswitch_layout.removeWidget(self.footswitch_widgets[footswitch_config])
        self.footswitch_widgets[footswitch_config].deleteLater()
        del self.footswitch_widgets[footswitch_config]

    def hide_all_knob_displays(self):
        for knob_widget in self.knob_widgets.values():
            knob_widget.knob_editbox.hide()
            knob_widget.knob_config.set_display_enabled(False)
            knob_widget.update_knob_editbox_visibility()

    def show_all_knob_displays(self):
        for knob_widget in self.knob_widgets.values():
            knob_widget.knob_editbox.show()
            knob_widget.knob_config.set_display_enabled(True)
            knob_widget.update_knob_editbox_visibility()

    def hide_all_footswitch_displays(self):
        for footswitch_widget in self.footswitch_widgets.values():
            footswitch_widget.footswitch_editbox.hide()
            footswitch_widget.footswitch_config.set_display_enabled(False)
            footswitch_widget.update_footswitch_editbox_visibility()

    def show_all_footswitch_displays(self):
        for footswitch_widget in self.footswitch_widgets.values():
            footswitch_widget.footswitch_editbox.show()
            footswitch_widget.footswitch_config.set_display_enabled(True)
            footswitch_widget.update_footswitch_editbox_visibility()
