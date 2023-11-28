from __future__ import annotations

import numpy as np

from pyfx.footswitch import PyFxFootswitch
from pyfx.knob import PyFxKnob
from pyfx.pedal import PyFxPedal, PyFxPedalVariant


class Pedal1Pedal(PyFxPedal):
    """Pedal 1 Base Class"""

    def __init__(self):
        name = "Pedal 1"
        knobs = {
            "Knob 1": PyFxKnob(
                name="Knob 1",
                minimum_value=0,
                maximum_value=1,
                default_value=0.5,
                precision=0.01,
                sensitivity=1,
                mode="linear",
                display_enabled=True,
                value=0.75,
            ),
            "Knob 2": PyFxKnob(
                name="Knob 1",
                minimum_value=0,
                maximum_value=1,
                default_value=0.5,
                precision=0.01,
                sensitivity=1,
                mode="linear",
                display_enabled=True,
                value=0.75,
            ),
        }
        footswitches = {
            "Footswitch 1": PyFxFootswitch(
                name="Footswitch 1",
                footswitch_type="mode",
                default_state=True,
                state=False,
                mode="Mode 2",
                modes=["Mode 1", "Mode 2", "Mode 3"],
                display_enabled=True,
            ),
        }
        variants = [
            DefaultPedal1Pedal(
                name="Default Pedal 1",
                knobs=knobs,
                footswitches=footswitches,
            )
        ]
        variant = variants[0]
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


class DefaultPedal1Pedal(PyFxPedalVariant):
    def process_audio(self, data: np.ndarray):
        """Default Pedal 1 Processing"""

        # TODO: Replace this line with your processing code
        processed_data = data

        return processed_data
