import numpy as np
import whisper

from utils import read_audio

class AudioSilenceRemover:
    def __init__(self):
        self.whisper_model = whisper.load_model("small")

    def removeSilence(self, path: str) -> np.ndarray:
        wave, channels, fps = read_audio(path)
        result = self.whisper_model.transcribe(path)

        segment_waves = []
        for segment in result["segments"]:
            start = int(segment["start"] * fps)
            end = int(segment["end"] * fps)

            segment_waves.append(wave[start:end])

        wave = np.concat(segment_waves, axis=-1)
        
        return wave