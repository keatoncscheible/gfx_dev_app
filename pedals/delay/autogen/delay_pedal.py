"""
DO NOT MODIFY THIS FILE
This file was generated using the Pedal Builder App.
Use the Pedal Builder App to make changes to this file.
"""

from default_delay_pedal import DefaultDelayPedal

from pyfx.footswitch import PyFxFootswitch
from pyfx.knob import PyFxKnob
from pyfx.pedal import PyFxPedal


class DelayPedal(PyFxPedal):
    """Delay Class"""

    def __init__(self):
        name = "Delay"
        knobs = {
            "Feedback": PyFxKnob(
                name="Feedback",
                minimum_value=0,
                maximum_value=1,
                default_value=0.5,
                precision=0.01,
                sensitivity=1,
                mode="linear",
                display_enabled=False,
                value=0.37,
            ),
            "Time": PyFxKnob(
                name="Time",
                minimum_value=0,
                maximum_value=1,
                default_value=0.5,
                precision=0.01,
                sensitivity=1,
                mode="linear",
                display_enabled=False,
                value=0.26,
            ),
            "Dry/Wet": PyFxKnob(
                name="Dry/Wet",
                minimum_value=0,
                maximum_value=1,
                default_value=0.5,
                precision=0.01,
                sensitivity=1,
                mode="linear",
                display_enabled=False,
                value=0.47000000000000003,
            ),
            "Output": PyFxKnob(
                name="Output",
                minimum_value=-50.0,
                maximum_value=40.0,
                default_value=0.0,
                precision=1.0,
                sensitivity=1,
                mode="logarithmic",
                display_enabled=False,
                value=7.943282347242816,
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
                display_enabled=False,
            ),
        }
        variants = {
            "Default": DefaultDelayPedal(
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
