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
    """
    PedalWidget represents a UI component for a guitar pedal, with controls for knobs and footswitches.
    It also supports changing pedal color and handling various pedal variants.
    """

    max_knob_columns = 3
    max_footswitch_columns = 3

    def __init__(self, pedal: PyFxPedal):
        """
        Initialize the PedalWidget.
        :param pedal: PyFxPedal object representing the pedal configuration.
        """
        super().__init__()
        self.setupUi(self)
        self.pedal = pedal

        # Connecting pedal changes to UI updates
        self.pedal.add_change_pedal_name_observer(self.set_pedal_name)
        self.pedal.add_add_knob_observer(self.add_knob)
        self.pedal.add_remove_knob_observer(self.remove_knob)
        self.pedal.add_add_footswitch_observer(self.add_footswitch)
        self.pedal.add_remove_footswitch_observer(self.remove_footswitch)
        self.pedal.add_set_pedal_color_observer(self.set_pedal_color)
        self.pedal.add_set_text_color_observer(self.set_text_color)
        self.pedal_name_label.label_changed.connect(self.pedal.change_pedal_name)

        # Dictionaries to manage knob and footswitch components
        self.knob_widgets: dict[PyFxKnob, KnobComponent] = {}
        self.footswitch_widgets: dict[PyFxFootswitch, FootswitchComponent] = {}

        # Initialize the UI components for existing knobs and footswitches
        for knob in pedal.knobs.values():
            self.add_knob(knob)
        for footswitch in pedal.footswitches.values():
            self.add_footswitch(footswitch)

        # Set initial states for pedal name, color, and text color
        self.set_pedal_name(self.pedal.name)
        self.set_pedal_color(self.pedal.pedal_color)
        self.set_text_color(self.pedal.text_color)

    def contextMenuEvent(self, event):  # noqa: N802
        """
        Overrides the context menu event to add custom actions like adding knobs, footswitches, and handling pedal
        variants.
        :param event: The event instance containing data about the context menu event.
        """
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

        def variant_selected(variant_name: str):
            pyfx_log.debug(f"Variant {variant_name} selected")
            self.pedal.set_variant(variant_name)

        def show_remove_variant_conformation_prompt(variant_name: str):
            message = f"Are you sure you want to remove the {variant_name} variant? These changes cannot be undone."
            confirmation_prompt = QMessageBox()
            confirmation_prompt.setIcon(QMessageBox.Warning)
            confirmation_prompt.setWindowTitle("Confirm Variant Removal")
            confirmation_prompt.setText(message)
            confirmation_prompt.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            confirmation_prompt.setDefaultButton(QMessageBox.No)

            return confirmation_prompt.exec() == QMessageBox.Yes

        def variant_removed(variant_name: str):
            if show_remove_variant_conformation_prompt(variant_name):
                pyfx_log.debug(f"Variant {variant_name} removed")
                self.pedal.remove_variant(variant_name)

        def variant_name_changed(variant_name: str):
            new_variant_name, ok = QInputDialog.getText(None, "Input New Variant", "New Variant Name:")
            if not ok or not new_variant_name:
                return None
            pyfx_log.debug(f"Variant name changed from {variant_name} to {new_variant_name}")
            self.pedal.change_variant_name(variant_name, new_variant_name)

        for variant in self.pedal.variants:
            select_variant_action = select_variant_menu.addAction(variant.name)
            select_variant_action.setCheckable(True)
            select_variant_action.setChecked(variant == self.pedal.variant)
            select_variant_action.triggered.connect(partial(variant_selected, variant.name))
            remove_variant_action = remove_variant_menu.addAction(variant.name)
            remove_variant_action.triggered.connect(partial(variant_removed, variant.name))
            change_variant_name_action = change_variant_name_menu.addAction(variant.name)
            change_variant_name_action.triggered.connect(partial(variant_name_changed, variant.name))

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
                variant_name = dialog.new_pedal_variant
                pyfx_log.debug(f"Created {variant_name} variant")
                self.pedal.add_variant(variant_name)
        elif action == change_pedal_color_action:
            pyfx_log.debug("Change Pedal Color Pressed")
            color = QColorDialog.getColor()
            self.pedal.set_pedal_color(color.name())
        elif action == change_text_color_action:
            pyfx_log.debug("Change Pedal Color Pressed")
            color = QColorDialog.getColor()
            self.pedal.set_text_color(color.name())

    def set_pedal_name(self, name: str):
        """
        Sets the name of the pedal.
        :param name: The new name of the pedal.
        """
        pyfx_log.debug(f"Pedal name changed from {self.pedal.name} to {name}")
        self.pedal_name_label.setText(name)

    def set_pedal_color(self, color: str):
        """
        Sets the color of the pedal.
        :param color: The new color for the pedal.
        """
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
        """
        Sets the text color for the pedal.
        :param color: The new text color.
        """
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
        """
        Generates a unique name for a new knob.
        :return: A string representing the new knob name.
        """
        knob_idx = 1
        while True:
            knob_name = f"Knob {knob_idx}"
            if knob_name not in self.pedal.knobs:
                return knob_name
            knob_idx += 1

    def generate_footswitch_name(self):
        """
        Generates a unique name for a new footswitch.
        :return: A string representing the new footswitch name.
        """
        footswitch_idx = 1
        while True:
            footswitch_name = f"Footswitch {footswitch_idx}"
            if footswitch_name not in self.pedal.footswitches:
                return footswitch_name
            footswitch_idx += 1

    def add_knob(self, knob: PyFxKnob):
        """
        Adds a knob to the pedal widget.
        :param knob: The PyFxKnob object to be added.
        """
        knob_widget = KnobComponent(knob=knob)
        self.knob_widgets[knob] = knob_widget
        knob_cnt = len(self.knob_widgets)
        row = int((knob_cnt - 1) / self.max_knob_columns)
        column = (knob_cnt - 1) % self.max_knob_columns
        self.knob_layout.addWidget(knob_widget, row, column)

    def remove_knob(self, knob: PyFxKnob):
        """
        Removes a knob from the pedal widget.
        :param knob: The PyFxKnob object to be removed.
        """
        self.knob_layout.removeWidget(self.knob_widgets[knob])
        self.knob_widgets[knob].deleteLater()
        del self.knob_widgets[knob]

    def add_footswitch(self, footswitch: PyFxFootswitch = None):
        """
        Adds a footswitch to the pedal widget.
        :param footswitch: The PyFxFootswitch object to be added.
        """
        footswitch_widget = FootswitchComponent(footswitch=footswitch)
        self.footswitch_widgets[footswitch] = footswitch_widget
        footswitch_cnt = len(self.footswitch_widgets)
        row = int((footswitch_cnt - 1) / self.max_footswitch_columns)
        column = (footswitch_cnt - 1) % self.max_footswitch_columns
        self.footswitch_layout.addWidget(footswitch_widget, row, column)

    def remove_footswitch(self, footswitch: FootswitchComponent):
        """
        Removes a footswitch from the pedal widget.
        :param footswitch: The FootswitchComponent object to be removed.
        """
        self.footswitch_layout.removeWidget(self.footswitch_widgets[footswitch])
        self.footswitch_widgets[footswitch].deleteLater()
        del self.footswitch_widgets[footswitch]

    def hide_all_knob_displays(self):
        """
        Hides the display for all knobs in the pedal widget.
        """
        for knob_widget in self.knob_widgets.values():
            knob_widget.knob_editbox.hide()
            knob_widget.knob.set_display_disabled()
            knob_widget.update_knob_editbox_visibility()

    def show_all_knob_displays(self):
        """
        Shows the display for all knobs in the pedal widget.
        """
        for knob_widget in self.knob_widgets.values():
            knob_widget.knob_editbox.show()
            knob_widget.knob.set_display_enabled()
            knob_widget.update_knob_editbox_visibility()

    def hide_all_footswitch_displays(self):
        """
        Hides the display for all footswitches in the pedal widget.
        """
        for footswitch_widget in self.footswitch_widgets.values():
            footswitch_widget.footswitch_editbox.hide()
            footswitch_widget.footswitch.set_display_disabled()
            footswitch_widget.update_footswitch_editbox_visibility()

    def show_all_footswitch_displays(self):
        """
        Shows the display for all footswitches in the pedal widget.
        """
        for footswitch_widget in self.footswitch_widgets.values():
            footswitch_widget.footswitch_editbox.show()
            footswitch_widget.footswitch.set_display_enabled()
            footswitch_widget.update_footswitch_editbox_visibility()
