import numpy as np

from modules.AudioPreProcessor import AudioPreProcessor

def analyze_voice(audio_data: np.ndarray, sampling_rate: int) -> dict[str, float]:
    processor = AudioPreProcessor()

    audio_data = processor.change_samplingRate(audio_data, sampling_rate)

    return {"大阪": 0.15, "京都": 0.28, "兵庫": 0.57}