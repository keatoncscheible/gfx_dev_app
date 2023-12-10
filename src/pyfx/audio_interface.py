from __future__ import annotations

import time
from dataclasses import dataclass

import numpy as np
import pyaudio

from pyfx.logging import pyfx_log


@dataclass
class AudioDevice:
    name: str
    index: int
    struct_version: int
    host_api: int
    max_input_channels: int
    max_output_channels: int
    default_low_input_latency: float
    default_low_output_latency: float
    default_high_input_latency: float
    default_high_output_latency: float
    default_sample_rate: int

    def __repr__(self):
        return "\n".join(
            [
                self.name,
                f"    index: {self.index}",
                f"    struct_version: {self.struct_version}",
                f"    host_api: {self.host_api}",
                f"    max_input_channels: {self.max_input_channels}",
                f"    max_output_channels: {self.max_output_channels}",
                f"    default_low_input_latency: {self.default_low_input_latency}",
                f"    default_low_output_latency: {self.default_low_output_latency}",
                f"    default_high_input_latency: {self.default_high_input_latency}",
                f"    default_high_output_latency: {self.default_high_output_latency}",
                f"    default_sample_rate: {self.default_sample_rate}",
            ]
        )


class AudioInterface:
    def __init__(self):
        self._pa = pyaudio.PyAudio()
        self.devices = self._get_devices()
        self.input_devices = self._get_input_devices()
        self.output_devices = self._get_output_devices()
        self.driver_types = self._get_driver_types()
        self.sample_rate = 44100
        self.sample_rates = [8000, 16000, 32000, 44100, 48000, 96000]
        self.input_buffer_size = 0
        self.output_buffer_size = 128
        self.test_tone_volume_db = 0
        self.test_tone_frequency = 440
        self.simulated_cpu_usage = 0.5
        self.host_api_id = 0
        self.audio_input_id = 0
        self.audio_output_id = 0
        self._stream = None

    @property
    def input_latency(self):
        return self.input_buffer_size / self.sample_rate

    @property
    def output_latency(self):
        return self.output_buffer_size / self.sample_rate

    @property
    def overall_latency(self):
        return self.input_latency + self.output_latency

    def _get_devices(self) -> dict[int, AudioDevice]:
        """List all available audio devices."""
        info = self._pa.get_host_api_info_by_index(0)
        num_devices = info.get("deviceCount")
        devices = {}
        for device_id in range(0, num_devices):
            device_info = self._pa.get_device_info_by_host_api_device_index(0, device_id)
            devices[device_id] = AudioDevice(
                name=device_info["name"],
                index=device_info["index"],
                struct_version=device_info["structVersion"],
                host_api=device_info["hostApi"],
                max_input_channels=device_info["maxInputChannels"],
                max_output_channels=device_info["maxOutputChannels"],
                default_low_input_latency=device_info["defaultLowInputLatency"],
                default_low_output_latency=device_info["defaultLowOutputLatency"],
                default_high_input_latency=device_info["defaultHighInputLatency"],
                default_high_output_latency=device_info["defaultHighOutputLatency"],
                default_sample_rate=device_info["defaultSampleRate"],
            )
        return devices

    def _get_input_devices(self) -> dict[int, AudioDevice]:
        return {device_id: device for device_id, device in self.devices.items() if device.max_input_channels > 0}

    def _get_output_devices(self) -> dict[int, AudioDevice]:
        return {device_id: device for device_id, device in self.devices.items() if device.max_output_channels > 0}

    def _get_driver_types(self) -> dict[int, str]:
        host_api_count = self._pa.get_host_api_count()
        driver_types = {}
        for host_api_id in range(host_api_count):
            api_info = self._pa.get_host_api_info_by_index(host_api_id)
            driver_types[host_api_id] = api_info["name"]
        return driver_types

    def _check_sample_rate(self, device_info: AudioDevice, rate: int):
        try:
            stream = self._pa.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=rate,
                input=device_info.max_input_channels > 0,
                output=device_info.max_output_channels > 0,
                input_device_index=device_info.index,
            )
            stream.close()
            return True
        except Exception:
            return False

    def _get_supported_sample_rates(self, device_info):
        sample_rates = [8000, 16000, 32000, 44100, 48000, 96000]
        return [rate for rate in sample_rates if self._check_sample_rate(device_info=device_info, rate=rate)]

    def _check_buffer_size(self, device_info: AudioDevice, buffer_size: int):
        try:
            stream = self._pa.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=int(device_info.default_sample_rate),
                input=device_info.max_input_channels > 0,
                output=device_info.max_output_channels > 0,
                input_device_index=device_info.index,
                frames_per_buffer=buffer_size,
            )
            stream.close()
            return True
        except Exception:
            return False

    def _get_supported_buffer_sizes(self, device_info):
        buffer_sizes = [32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]
        return [
            buffer_size
            for buffer_size in buffer_sizes
            if self._check_buffer_size(device_info=device_info, buffer_size=buffer_size)
        ]

    def set_audio_input(self, audio_input_id: int):
        pyfx_log.debug(f"Setting audio input to {self.devices[audio_input_id].name}")
        self.audio_input_id = audio_input_id

    def set_audio_output(self, audio_output_id: int):
        pyfx_log.debug(f"Setting audio output to {self.devices[audio_output_id].name}")
        self.audio_output_id = audio_output_id

    def set_sample_rate(self, sample_rate: int):
        pyfx_log.debug(f"Setting sample rate to {sample_rate} Hz")
        self.sample_rate = sample_rate

    def set_input_buffer_size(self, input_buffer_size: int):
        pyfx_log.debug(f"Setting input buffer size to {input_buffer_size} samples")
        self.input_buffer_size = input_buffer_size

    def set_output_buffer_size(self, output_buffer_size: int):
        pyfx_log.debug(f"Setting output buffer size to {output_buffer_size} samples")
        self.output_buffer_size = output_buffer_size

    def set_driver_type(self, host_api_id: int):
        pyfx_log.debug(f"Setting driver type to {self.driver_types[host_api_id]}")
        self.host_api_id = host_api_id

    def set_test_tone_volume(self, volume_db: int):
        pyfx_log.debug(f"Setting test tone volume to {self.test_tone_volume_db} dB")
        self.test_tone_volume_db = volume_db

    def set_test_tone_frequency(self, frequency: int):
        pyfx_log.debug(f"Setting test tone frequency to {self.test_tone_frequency} dB")
        self.test_tone_frequency = frequency

    def set_simulated_cpu_usage(self, simulated_cpu_usage: int):
        pyfx_log.debug(f"Setting simulated CPU usage to {simulated_cpu_usage} %")
        self.simulated_cpu_usage = simulated_cpu_usage / 100

    def audio_callback(self, in_data, frame_count, time_info, status):
        # Process audio data here
        # Example: simply pass through the input to output
        return (in_data, pyaudio.paContinue)

    def start_stream(self):
        missing_parameters = []
        if self.audio_input_id is None:
            missing_parameters.append("audio input")
        if self.audio_output_id is None:
            missing_parameters.append("audio output")
        if self.sample_rate is None:
            missing_parameters.append("sample rate")
        if self.input_buffer_size is None:
            missing_parameters.append("input buffer size")
        if self.output_buffer_size is None:
            missing_parameters.append("output buffer size")
        if missing_parameters:
            msg = f"The following parameters must be defined to start a stream: {missing_parameters}"
            raise ValueError(msg)

        if self._stream is not None:
            self._stream.stop_stream()
            self._stream.close()

        self._stream = self._pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            output=True,
            input_device_index=self.audio_input_id,
            output_device_index=self.audio_output_id,
            frames_per_buffer=self.output_buffer_size,
            input_host_api_specific_stream_info=self.host_api_id,
            output_host_api_specific_stream_info=self.host_api_id,
            stream_callback=self.audio_callback,
        )

        self._stream.start_stream()

    def stop_stream(self):
        if self._stream is not None:
            self._stream.stop_stream()
            self._stream.close()
            self._stream = None

    def play_test_tone(self):
        """Start playing a test tone continuously using the callback approach."""
        pyfx_log.debug(f"Playing a {self.test_tone_volume_db} dB {self.test_tone_frequency} Hz test tone")
        self.playing_test_tone = True

        def test_tone_callback(in_data, frame_count, time_info, status):
            if not hasattr(test_tone_callback, "theta"):
                test_tone_callback.theta = 0

            sample_period = 1 / self.sample_rate
            duration = frame_count * sample_period
            t = np.arange(start=0, stop=duration, step=sample_period)
            tone = 10 ** (self.test_tone_volume_db / 20) * np.sin(
                self.test_tone_frequency * t * 2 * np.pi + test_tone_callback.theta
            )
            tone = np.int16(tone * 32767)
            test_tone_callback.theta += 2 * np.pi * self.test_tone_frequency * duration
            test_tone_callback.theta = test_tone_callback.theta % (2 * np.pi)

            # Simulate CPU load
            time.sleep(duration * self.simulated_cpu_usage)

            return (tone.tobytes(), pyaudio.paContinue)

        # Open stream
        self._stream = self._pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            output=True,
            output_device_index=self.audio_output_id,
            frames_per_buffer=self.output_buffer_size,
            input_host_api_specific_stream_info=self.host_api_id,
            output_host_api_specific_stream_info=self.host_api_id,
            stream_callback=test_tone_callback,
        )

        # Play stream
        self._stream.start_stream()

    def stop_test_tone(self):
        """Stop playing the test tone and wait for the stream to finish."""
        pyfx_log.debug("Stop playing the test tone")
        self.playing_test_tone = False
        if self._stream is not None:
            self._stream.stop_stream()
            self._stream.close()


if __name__ == "__main__":
    ai = AudioInterface()
    devices = ai.devices
    for device in ai.devices.values():
        pyfx_log.debug(device)

    pyfx_log.debug("Input devices")
    for device_id, device in ai.input_devices.items():
        pyfx_log.debug(f"    {device_id}: {device.name}")

    pyfx_log.debug("Output devices")
    for device_id, device in ai.output_devices.items():
        pyfx_log.debug(f"    {device_id}: {device.name}")

    pyfx_log.debug("Driver Types")
    for host_api_id, driver_type in ai.driver_types.items():
        pyfx_log.debug(f"    {host_api_id}: {driver_type}")

    ai.set_audio_input(1)
    ai.set_audio_output(4)
    ai.set_output_buffer_size(64)
    ai.set_sample_rate(48000)
    ai.set_driver_type(1)
    ai.play_test_tone()
    time.sleep(2)
    ai.stop_test_tone()
    # ai.start_stream()
    # time.sleep(5)
    # ai.stop_stream()
