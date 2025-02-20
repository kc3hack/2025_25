import os
import numpy as np
from pydub import AudioSegment

def getSubFilePaths(dir_path: str) -> list[str]:
    if dir_path[-1] != "/": dir_path += "/"
    return [dir_path + path for path in os.listdir(dir_path)]

def read_audio(path: str) -> tuple[np.ndarray, int, int]:
    song = AudioSegment.from_file(path, path.split(".")[-1])
    wav = np.array(song.get_array_of_samples())
    return wav, song.channels, song.frame_rate

def save_audio(wave: np.ndarray, channels: int, fps: int, file_name: str) -> None:
    wave = wave.astype("int16")

    sound = AudioSegment(
        data=wave.tobytes(),
        sample_width=2,
        frame_rate=fps,
        channels=channels
    )

    sound.export(file_name, format=file_name.split(".")[-1])
