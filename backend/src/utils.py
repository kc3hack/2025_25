import os
import numpy as np
import torchaudio
import torch

def getSubFilePaths(dir_path: str) -> list[str]:
    if dir_path[-1] != "/": dir_path += "/"
    return [dir_path + path for path in os.listdir(dir_path)]

def read_audio(path: str) -> tuple[np.ndarray, int]:
    wave, fps = torchaudio.load(path)
    return wave.detach().cpu().numpy(), fps

def save_audio(wave: np.ndarray, fps: int, file_name: str) -> None:
    torchaudio.save(
        file_name,
        torch.tensor(wave),
        fps,
        bits_per_sample=16
    )
