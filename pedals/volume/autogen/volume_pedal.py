"""
DO NOT MODIFY THIS FILE
This file was generated using the Pedal Builder App.
Use the Pedal Builder App to make changes to this file.
"""

from default_volume_pedal import DefaultVolumePedal

from pyfx.footswitch import PyFxFootswitch
from pyfx.knob import PyFxKnob
from pyfx.pedal import PyFxPedal


class VolumePedal(PyFxPedal):
    """Volume Class"""

    def __init__(self):
        name = "Volume"
        knobs = {
            "Output": PyFxKnob(
                name="Output",
                minimum_value=-50.0,
                maximum_value=20.0,
                default_value=0.0,
                precision=1.0,
                sensitivity=1,
                mode="logarithmic",
                display_enabled=True,
                value=3.1622776601683795,
            ),
        }
        footswitches = {
            "On/Off": PyFxFootswitch(
                name="On/Off",
                footswitch_type="latching",
                default_state=True,
                state=True,
                mode=None,
                modes=None,
                display_enabled=True,
            ),
        }
        variants = {
            "Default": DefaultVolumePedal(
                name="Default",
                knobs=knobs,
                footswitches=footswitches,
            ),
        }
        variant = variants["Default"]
        pedal_color = "#0000FF"
        text_color = "#FFFFFF"
        super().__init__(
            name=name,
            knobs=knobs,
            footswitches=footswitches,
            variant=variant,
            variants=variants,
            pedal_color=pedal_color,
            text_color=text_color,
        )
