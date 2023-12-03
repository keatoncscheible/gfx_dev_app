import threading
import time
import wave

import numpy as np
import pyaudio

from pyfx.logging import pyfx_log


def process_audio_default(data):
    return data


class AudioProcessor:
    def __init__(self):
        self._audio_file = None
        self._process_audio = process_audio_default
        self._pa = None
        self._stream = None
        self._frame_index = 0
        self._total_frames = None
        self._frame_rate = None
        self._paused = False
        self._looping = False
        self._playback_thread = None
        self._stop_playback = threading.Event()

    def set_audio_file(self, audio_file: str):
        pyfx_log.debug(f"Audio file set to {audio_file} in audio processor")
        self._audio_file = audio_file
        with wave.open(audio_file, "rb") as wf:
            self._total_frames = wf.getnframes()
            self._frame_rate = wf.getframerate()

    def set_audio_data_processor(self, process_audio_fcn: callable):
        self._process_audio = process_audio_fcn

    def play(self):
        self._stop_playback.clear()
        if self._paused:
            self._paused = False
            if self._stream is not None:
                self._stream.start_stream()
                return

        if self._audio_file and (self._stream is None or not self._stream.is_active()):
            self._playback_thread = threading.Thread(target=self._play_audio)
            self._playback_thread.start()

    def pause(self):
        if self._stream is not None and self._stream.is_active():
            self._paused = True
            self._stream.stop_stream()

    def stop(self):
        self._stop_playback.set()
        if self._playback_thread is not None:
            self._playback_thread.join()
        self._frame_index = 0
        self._paused = False

    def loop(self, state: bool):  # noqa: FBT001
        self._looping = state

    def _play_audio(self):
        while not self._stop_playback.is_set():
            with wave.open(self._audio_file, "rb") as wf:
                wf.setpos(self._frame_index)

                def callback(in_data, frame_count, time_info, status):
                    if self._stop_playback.is_set():
                        return (None, pyaudio.paComplete)
                    raw_data = wf.readframes(frame_count)
                    self._frame_index = wf.tell()
                    data = np.frombuffer(raw_data, np.int16).astype(np.float32)
                    data = self._process_audio(data)
                    data = np.clip(data, np.iinfo(np.int16).min, np.iinfo(np.int16).max).astype(np.int16)
                    return (data.tobytes(), pyaudio.paContinue)

                self._pa = pyaudio.PyAudio()
                self._stream = self._pa.open(
                    format=self._pa.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback,
                )
                self._stream.start_stream()

                while not self._stop_playback.is_set() and self._stream.is_active():
                    time.sleep(0.1)

                self._stream.stop_stream()
                self._stream.close()
                self._pa.terminate()
                self._stream = None
                self._pa = None

                if self._paused:
                    break
                else:
                    self._frame_index = 0
                    if not self._looping:
                        break
