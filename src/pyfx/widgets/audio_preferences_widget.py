from pathlib import Path

from PySide6.QtWidgets import QFileDialog, QWidget

from pyfx.audio_interface import AudioInterface
from pyfx.logging import pyfx_log
from pyfx.ui.audio_preferences_widget_ui import Ui_AudioPreferencesWidget


class AudioPreferencesWidget(QWidget, Ui_AudioPreferencesWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._audio_interface: AudioInterface = None

    @property
    def audio_interface(self):
        return self._audio_interface

    @audio_interface.setter
    def audio_interface(self, audio_interface):
        self._audio_interface = audio_interface
        self.setup_audio_preferences()

    def setup_audio_preferences(self):
        for host_api_id, driver_type in self.audio_interface.driver_types.items():
            self.driver_type_combobox.addItem(driver_type, host_api_id)

        self.audio_input_device_combobox.addItem("Audio File", -1)
        for audio_input_id, audio_device in self.audio_interface.input_devices.items():
            self.audio_input_device_combobox.addItem(audio_device.name, audio_input_id)

        for audio_output_id, audio_device in self.audio_interface.output_devices.items():
            self.audio_output_device_combobox.addItem(audio_device.name, audio_output_id)

        self.audio_folder_editbox.setText(self.audio_interface.audio_folder)

        default_sample_rate = self.audio_interface.sample_rate
        for sample_rate in self.audio_interface.sample_rates:
            self.sample_rate_combobox.addItem(f"{sample_rate} Hz", sample_rate)
        self.sample_rate_combobox.setCurrentText(f"{default_sample_rate} Hz")

        self.input_buffer_size_changed(self.audio_interface.input_buffer_size)
        self.input_buffer_size_spinbox.setValue(self.audio_interface.input_buffer_size)
        self.output_buffer_size_changed(self.audio_interface.output_buffer_size)
        self.output_buffer_size_spinbox.setValue(self.audio_interface.output_buffer_size)
        self.tone_volume_spinbox.setValue(self.audio_interface.test_tone_volume_db)
        self.tone_frequency_spinbox.setValue(self.audio_interface.test_tone_frequency)
        self.simulated_cpu_usage_slider.setValue(int(self.audio_interface.simulated_cpu_usage * 100))

    def driver_type_changed(self, driver_type: str):
        pyfx_log.debug(f"Driver type changed to {driver_type}")
        driver_type_data = self.driver_type_combobox.currentData()
        self.audio_interface.set_driver_type(driver_type_data)

    def audio_input_device_changed(self, audio_input_device: str):
        pyfx_log.debug(f"Audio input device changed to {audio_input_device}")
        audio_input_device_data = self.audio_input_device_combobox.currentData()
        self.audio_interface.set_audio_input(audio_input_device_data)

    def audio_output_device_changed(self, audio_output_device: str):
        pyfx_log.debug(f"Audio output device changed to {audio_output_device}")
        audio_output_device_data = self.audio_output_device_combobox.currentData()
        self.audio_interface.set_audio_output(audio_output_device_data)

    def audio_folder_browse_button_pressed(self):
        initial_folder = self.audio_folder_editbox.text()
        folder_path = QFileDialog.getExistingDirectory(self, "Select Audio Folder", initial_folder)
        if folder_path:
            self.audio_folder_editbox.setText(folder_path)

    def audio_folder_editing_finished(self):
        audio_folder = Path(self.audio_folder_editbox.text())
        if audio_folder.exists() and audio_folder.is_dir():
            pyfx_log.debug(f"Updating audio folder to {audio_folder.as_posix()}")
            self.audio_folder_editbox.setStyleSheet("QLineEdit { background-color: #FFFFFF; }")
        else:
            pyfx_log.debug(f"{audio_folder.as_posix()} is not a valid folder")
            self.audio_folder_editbox.setStyleSheet("QLineEdit { background-color: #FF8888; }")

    def sample_rate_changed(self, sample_rate: int):
        pyfx_log.debug(f"Sample rate changed to {sample_rate}")
        sample_rate_data = self.sample_rate_combobox.currentData()
        self.audio_interface.set_sample_rate(sample_rate_data)

    def input_buffer_size_changed(self, input_buffer_size: int):
        pyfx_log.debug(f"Input buffer size changed to {input_buffer_size}")
        self.audio_interface.set_input_buffer_size(input_buffer_size)
        input_latency_ms = self.audio_interface.input_latency * 1000
        overall_latency_ms = self.audio_interface.overall_latency * 1000
        self.input_latency_editbox.setText(f"{input_latency_ms:.2f} ms")
        self.overall_latency_editbox.setText(f"{overall_latency_ms:.2f} ms")

    def output_buffer_size_changed(self, output_buffer_size: int):
        pyfx_log.debug(f"Output buffer size changed to {output_buffer_size}")
        self.audio_interface.set_output_buffer_size(output_buffer_size)
        output_latency_ms = self.audio_interface.output_latency * 1000
        overall_latency_ms = self.audio_interface.overall_latency * 1000
        self.output_latency_editbox.setText(f"{output_latency_ms:.2f} ms")
        self.overall_latency_editbox.setText(f"{overall_latency_ms:.2f} ms")

    def test_tone_button_toggled(self, state):
        pyfx_log.debug(f"Test tone turned {'on' if state else 'off'}")
        if state:
            self.test_tone_button.setText("On")
            self.audio_interface.play_test_tone()
        else:
            self.test_tone_button.setText("Off")
            self.audio_interface.stop_test_tone()

    def test_tone_volume_changed(self, volume_db: int):
        pyfx_log.debug(f"Test tone volume changed to {volume_db} dB")
        self.audio_interface.set_test_tone_volume(volume_db)

    def test_tone_frequency_changed(self, frequency: int):
        pyfx_log.debug(f"Test tone frequency changed to {frequency} dB")
        self.audio_interface.set_test_tone_frequency(frequency)

    def simulated_cpu_usage_changed(self, simulated_cpu_usage: int):
        pyfx_log.debug(f"Simulated CPU usage changed to {simulated_cpu_usage}")
        self.audio_interface.set_simulated_cpu_usage(simulated_cpu_usage)
        self.simulated_cpu_usage_editbox.setText(f"{simulated_cpu_usage} %")
        self.simulated_cpu_usage_editbox.setText(f"{simulated_cpu_usage} %")
