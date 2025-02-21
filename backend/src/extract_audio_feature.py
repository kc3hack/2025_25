from pydub import AudioSegment

from transformers import AutoFeatureExtractor, AutoModel
from transformers import Wav2Vec2FeatureExtractor, HubertModel
from transformers.modeling_outputs import BaseModelOutput

import torch
import numpy as np

import os
from functools import reduce

def load_models(device: str | torch.device) -> tuple[Wav2Vec2FeatureExtractor, HubertModel]:
    model_name = "rinna/japanese-hubert-base"

    feature_extractor = AutoFeatureExtractor.from_pretrained(model_name)
    assert isinstance(feature_extractor, Wav2Vec2FeatureExtractor)
    model = AutoModel.from_pretrained(model_name)
    assert isinstance(model, HubertModel)

    model.to(device=device) #type: ignore
    model.eval()

    return feature_extractor, model

def read_audio(file_path: str) -> tuple[np.ndarray, int]:
    sound = AudioSegment.from_file(file_path, file_path.split(".")[-1])

    assert sound.channels == 1

    wav = np.array(sound.get_array_of_samples(), dtype=np.float32)
    fps = sound.frame_rate

    return wav, fps

def forward_feature(feature_extractor: Wav2Vec2FeatureExtractor, model: HubertModel, wav: np.ndarray) -> torch.Tensor:
    inputs = feature_extractor(
        wav,
        return_tensors="pt",
        sampling_rate=16000,
    ).to(device=model.device)

    outputs = model(**inputs)
    assert isinstance(outputs, BaseModelOutput)

    return outputs.last_hidden_state

def extract_file_feature(feature_extractor: Wav2Vec2FeatureExtractor, model: HubertModel, src_dir: str, dist_dir: str, audio_id: str, file_name: str) -> None:
    wav, fps = read_audio(src_dir + audio_id + "/" + file_name)
    assert fps == 16000

    features = forward_feature(feature_extractor, model, wav)

    sub_dir_name = dist_dir + audio_id + "/"
    if not os.path.isdir(sub_dir_name):
        os.mkdir(sub_dir_name)

    torch.save(features, sub_dir_name + reduce(lambda p,c: p+"."+c, file_name.split(".")[:-1]) + ".pth")

def extract_file_features(feature_extractor: Wav2Vec2FeatureExtractor, model: HubertModel, src_dir: str, dist_dir: str, audio_id: str) -> None:
    file_names = os.listdir(src_dir + audio_id)

    for file_name in file_names:
        extract_file_feature(feature_extractor, model, src_dir, dist_dir, audio_id, file_name)

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    feature_extractor, model = load_models(device)

    src_dir = "./src/assets/audio/mp3/"
    dist_dir = "./src/assets/tensor/"
    audio_id = "NOUlyulQ30I"

    extract_file_features(feature_extractor, model, src_dir, dist_dir, audio_id)

if __name__ == "__main__":
    main()