import numpy as np
import whisper
import torch

from utils import read_audio

class AudioSilenceRemover:
    def __init__(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self.whisper_model = whisper.load_model("small")
        self.whisper_model.to(device=device)

    def removeSilence(self, path: str) -> np.ndarray:
        wave, fps = read_audio(path)
        result = self.whisper_model.transcribe(path)

        segment_waves = []
        for segment in result["segments"]:
            start = int(segment["start"] * fps)
            end = int(segment["end"] * fps)

            segment_waves.append(wave[:, start:end])

        wave = np.concat(segment_waves, axis=-1)
        
        return wave