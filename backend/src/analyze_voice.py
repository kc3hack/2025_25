import numpy as np
import torch

from .modules.AudioPreProcessor import AudioPreProcessor
from .modules.AudioFeatureExtractor import AudioFeatureExtractor

def analyze_voice(audio_data: np.ndarray, sampling_rate: int) -> dict[str, float]:
    processor = AudioPreProcessor()
    extractor = AudioFeatureExtractor()

    audio_data = processor.to_monophonic(audio_data)
    audio_data = processor.change_samplingRate(audio_data, sampling_rate, 16000)
    audio_data = processor.standardize(audio_data)

    with torch.no_grad():
        features = extractor.extract_feature(audio_data, 16000)[0]

        device = "cuda" if torch.cuda.is_available() else "cpu"
        linear = torch.load("./src/ckpts/svm_linear_50000.pth", weights_only=False)
        linear.to(device=device)

        result = linear.forward(features).mean(dim=0)

    result = torch.nn.functional.softmax(result, dim=-1)
    result = result.detach().cpu().tolist()

    return {"大阪": result[0], "京都": result[1], "兵庫": result[2]}