from __future__ import annotations

import numpy as np

from pyfx.footswitch import PyFxFootswitch
from pyfx.knob import PyFxKnob
from pyfx.pedal import PyFxPedal, PyFxPedalVariant


class Pedal1Pedal(PyFxPedal):
    """Pedal 1 Class"""

    def __init__(self):
        name = "Pedal 1"
        knobs = {
            "Linear": PyFxKnob(
                name="Linear",
                minimum_value=0,
                maximum_value=10.0,
                default_value=0.5,
                precision=0.01,
                sensitivity=1,
                mode="linear",
                display_enabled=True,
                value=5.0,
            ),
            "Logarithmic": PyFxKnob(
                name="Logarithmic",
                minimum_value=0,
                maximum_value=80.0,
                default_value=0.0,
                precision=1.0,
                sensitivity=1,
                mode="logarithmic",
                display_enabled=True,
                value=2511.88643150958,
            ),
        }

        footswitches = {
            "Latching": PyFxFootswitch(
                name="Latching",
                footswitch_type="latching",
                default_state=True,
                state=False,
                mode=None,
                modes=None,
                display_enabled=True,
            ),
            "Momentary": PyFxFootswitch(
                name="Momentary",
                footswitch_type="momentary",
                default_state=False,
                state=False,
                mode=None,
                modes=None,
                display_enabled=True,
            ),
            "Mode": PyFxFootswitch(
                name="Mode",
                footswitch_type="mode",
                default_state=None,
                state=None,
                mode="Mode 1",
                modes=[
                    "Mode 1",
                    "Mode 2",
                    "Mode 3",
                ],
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
