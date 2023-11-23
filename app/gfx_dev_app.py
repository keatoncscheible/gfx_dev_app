import sys
from datetime import datetime

from gfx.backend import GfxDevBackend
from gfx_dev_logging import gfx_dev_log
from PySide6.QtWidgets import QApplication
from widgets.gfx_dev_main_window import GfxDevMainWindow


def load_stylesheet(filepath):
    with open(filepath, "r") as file:
        return file.read()


def gfx_dev_app():
    gfx_dev_log.info(
        "GFX Dev Opened: {}".format(datetime.now().strftime("%b-%d-%Y %H:%M:%S"))
    )

    app = QApplication(sys.argv)

    stylesheet = load_stylesheet("app/gfx_dev_app_stylesheet.qss")
    app.setStyleSheet(stylesheet)

    gfx = GfxDevBackend()
    window = GfxDevMainWindow(gfx=gfx)
    # default_pedal = "saturate"
    # window.open_pedal(default_pedal)
    window.transport_control.audio_file_combobox.setCurrentText(
        "acoustic_melody_17.wav"
    )

    window.show()

    ret = app.exec()

    gfx_dev_log.info(
        "GFX Dev Closed: {}\n".format(datetime.now().strftime("%b-%d-%Y %H:%M:%S"))
    )

    sys.exit(ret)


if __name__ == "__main__":
    gfx_dev_app()
