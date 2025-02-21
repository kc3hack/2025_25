import numpy as np
import torch
import math

from transformers import AutoFeatureExtractor, AutoModel
from transformers import Wav2Vec2FeatureExtractor, HubertModel
from transformers.modeling_outputs import BaseModelOutput

class AudioFeatureExtractor:
    def __init__(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model_name = "rinna/japanese-hubert-base"

        feature_extractor = AutoFeatureExtractor.from_pretrained(model_name)
        assert isinstance(feature_extractor, Wav2Vec2FeatureExtractor)
        model = AutoModel.from_pretrained(model_name)
        assert isinstance(model, HubertModel)

        model.to(device=device) #type: ignore
        model.eval()

        self.feature_extractor = feature_extractor
        self.model = model

    def extract_feature(self, waves: np.ndarray) -> torch.Tensor:
        assert len(waves.shape) == 2
        B, L = waves.shape

        assert L == 16000 * 5

        inputs = self.feature_extractor(
            waves,
            return_tensors="pt",
            sampling_rate=16000
        ).to(device=self.model.device)

        outputs = self.model(**inputs)
        assert isinstance(outputs, BaseModelOutput)

        return outputs.last_hidden_state

    def extract_features(self, waves: list[np.ndarray], fps: int) -> torch.Tensor:
        waves = [wave[:, :wave.shape[-1] - wave.shape[-1] % (fps * 5)].reshape(-1, fps * 5) for wave in waves]
        waveArr = np.concatenate(waves, axis=0)

        features = []

        idxs = torch.randint(0, waveArr.shape[0], (4000,))
        waveArr = waveArr[idxs]

        cap = 40
        for i in range(math.ceil(waveArr.shape[0] / cap)):
            features.append(self.extract_feature(waveArr[i*cap:(i+1)*cap]).detach().cpu())

        return torch.cat(features, dim=0)