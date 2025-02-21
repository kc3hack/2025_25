import numpy as np
import torch
import torchaudio

class AudioPreProcessor:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def to_monophonic(self, wave: np.ndarray) -> np.ndarray:
        assert len(wave.shape) == 2
        return wave.mean(axis=0, keepdims=True)
    
    def change_samplingRate(self, wave: np.ndarray, fps_before: int, fps_after: int) -> np.ndarray:
        transform = torchaudio.transforms.Resample(fps_before, fps_after).to(device=self.device)
        waveTensor = torch.tensor(wave, dtype=torch.float32, device=self.device)
        return transform(waveTensor).detach().cpu().numpy()

    def concat_waves(self, waves: list[np.ndarray]) -> np.ndarray:
        return np.concatenate(waves, axis=-1)
        
    def standardize(self, wave: np.ndarray) -> np.ndarray:
        mean = wave.mean(axis=-1)
        std = wave.std(axis=-1)

        wave = (wave - mean) / std
        wave = wave.clip(-2, 2)

        return wave