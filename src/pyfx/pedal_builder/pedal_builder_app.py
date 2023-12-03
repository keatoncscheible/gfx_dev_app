import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

from PySide6.QtWidgets import QApplication

from pyfx.audio_processor import AudioProcessor
from pyfx.logging import pyfx_log
from pyfx.pedal_builder.pedal_builder import PedalBuilder
from pyfx.widgets.pedal_builder_main_window import PedalBuilderMainWindow


def load_stylesheet(filepath):
    with open(filepath) as file:
        return file.read()


def pedal_builder_app(pedal_folder: Path):
    pedal_folder.mkdir(exist_ok=True)

    pyfx_log.info("Pedal Builder Opened: {}".format(datetime.now().strftime("%b-%d-%Y %H:%M:%S")))  # noqa: DTZ005

    app = QApplication(sys.argv)

    stylesheet = load_stylesheet("src/pyfx/pedal_builder/pedal_builder_app_stylesheet.qss")
    app.setStyleSheet(stylesheet)

    audio_processor = AudioProcessor()
    pedal_builder = PedalBuilder(root_pedal_folder=pedal_folder)
    window = PedalBuilderMainWindow(
        pedal_builder=pedal_builder,
        audio_processor=audio_processor,
    )

    window.transport_control.audio_file_combobox.setCurrentText("acoustic_melody_17.wav")

    window.show()

    ret = app.exec()

    pyfx_log.info("Pedal Builder Closed: {}\n".format(datetime.now().strftime("%b-%d-%Y %H:%M:%S")))  # noqa: DTZ005

    sys.exit(ret)


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Run Pedal Builder App.")
    parser.add_argument("-p", "--pedal_folder", default="./pedals", help="Specify the pedal folder path.")
    args = parser.parse_args()

    pedal_folder = Path(args.pedal_folder)
    # if pedal_folder.exists():
    #     shutil.rmtree(pedal_folder)
    pedal_builder_app(pedal_folder)
