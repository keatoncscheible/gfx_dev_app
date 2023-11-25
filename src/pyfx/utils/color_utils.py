from PySide6.QtGui import QColor


def lighten_color(color: QColor, factor: float):
    # Convert the color to HSL
    h, s, l, _ = color.getHsl()

    # Increase the lightness
    lightened_l = int(l + (255 - l) * factor)
    lightened_l = min(255, max(0, lightened_l))  # Ensure within range

    # Create the new lightened color
    lightened_color = QColor()
    lightened_color.setHsl(h, s, lightened_l)
    return lightened_color.toRgb()


def darken_color(color: QColor, factor: float):
    # Convert the color to HSV
    h, s, v, _ = color.getHsv()

    # Decrease the value
    darkened_v = int(v * (1 - factor))
    darkened_v = min(255, max(0, darkened_v))  # Ensure within range

    # Create the new darkened color
    darkened_color = QColor()
    darkened_color.setHsv(h, s, darkened_v)
    return darkened_color.toRgb()


def calculate_color_gradient(color: QColor, light_factor: float, dark_factor: float):
    light_color = lighten_color(color=color, factor=light_factor)
    dark_color = darken_color(color=color, factor=dark_factor)
    return light_color, dark_color
