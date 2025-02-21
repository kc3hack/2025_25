import numpy as np
import torch
import torchaudio

class AudioAugmenter:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def augment_audio(self, wave: np.ndarray, fps: int) -> list[np.ndarray]:
        waves = []
        waveTensor = torch.tensor(wave, dtype=torch.float32, device=self.device)

        pitchShifts = [torchaudio.transforms.PitchShift(fps, n, 12).to(device=self.device) for n in [-6, -4, -2, 1, 2, 4, 6]]
        speeds = [torchaudio.transforms.Speed(fps, f).to(device=self.device) for f in [0.7, 0.85, 1, 1.15, 1.5, 2]]
        stds = [0, 0.1, 0.2, 0.3]
        for pitchShift in pitchShifts:
            w1 = pitchShift(waveTensor)
            for speed in speeds:
                w2 = speed(w1)[0]
                for std in stds:
                    w3 = w2 + torch.normal(0, std, w2.shape, dtype=w2.dtype, device=w2.device)
                    waves.append(w3.detach().cpu().numpy())

        return waves