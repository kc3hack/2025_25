import numpy as np
import math

class AudioPreProcessor:
    def can_devide(self, target: int, by: int) -> bool:
        return float(target / by).is_integer()

    def to_monophonic(self, wave: np.ndarray, channels: int) -> np.ndarray:
        assert len(wave.shape) == 1
        assert self.can_devide(wave.shape[0], channels)

        return wave.reshape(-1, channels).mean(axis=-1).reshape(-1)
    
    def change_samplingRate(self, wave: np.ndarray, fps_before: int, fps_after: int) -> np.ndarray:
        if fps_before == fps_after: return wave
        else: raise

    def concat_waves(self, waves: list[np.ndarray]) -> np.ndarray:
        return np.concatenate(waves, axis=-1)
    
    def mask_spectrum(self, spec: np.ndarray, f_min: int, f_max: int) -> np.ndarray:
        mask = np.zeros_like(spec)
        mask[:, f_min:f_max] = np.ones_like(spec)[:, f_min:f_max]
        return spec * mask

    def cancel_noise(self, wave: np.ndarray, fps: int) -> np.ndarray:
        pad =  np.zeros((fps - wave.shape[0] % fps))
        wave = np.concatenate((wave,pad), axis=-1)
        wave = wave.reshape(-1, fps)

        wave = np.concatenate((wave, np.zeros((wave.shape[0], 2**math.ceil(math.log2(fps)) - fps))), axis=-1)
        spec = np.fft.fft(wave, axis=-1)

        spec = self.mask_spectrum(spec, 100, 1000)

        wave = np.fft.ifft(spec, axis=-1).real

        return wave[:, :fps].reshape(-1)
    
    def standardize(self, wave: np.ndarray) -> np.ndarray:
        mean = wave.mean()
        std = wave.std()

        wave = (wave - mean) / std
        wave = wave.clip(-2, 2)

        return wave