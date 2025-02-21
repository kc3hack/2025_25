import os
import torch

from utils import getSubFilePaths, read_audio, save_audio
from modules.AudioPreProcessor import AudioPreProcessor
from modules.AudioSilenceRemover import AudioSilenceRemover
from modules.AudioAugmenter import AudioAugmenter
from modules.AudioFeatureExtractor import AudioFeatureExtractor

def main():
    processor = AudioPreProcessor()

    src_dir = "./src/assets/audio/JTubeSpeech/"
    dist = "./src/assets/tensor/"

    sources = {
        "hyogo": ["AAD", "ADR", "AKK"],
        "kyoto": ["AFX", "D0010"],
        "osaka": ["ADK", "AFV", "AHZ"]
    }

    wave = AudioSilenceRemover().removeSilence("_temp.mp3")
    augmenter = AudioAugmenter()
    extractor = AudioFeatureExtractor()

    for key in sources:
        for v in sources[key]:
            dist_dir = dist + key + "/"
            channel_id = v

            paths = getSubFilePaths(src_dir + channel_id)

            fps = 16000
            audios = [read_audio(path) for path in paths]

            waves = [(processor.to_monophonic(audio[0]), audio[1]) for audio in audios]
            waves = [processor.change_samplingRate(wave[0], wave[1], fps) for wave in waves]

            wave = processor.concat_waves(waves)
            wave = processor.standardize(wave)

            save_audio(wave, fps, "_temp.mp3")

            os.remove("_temp.mp3")

            waves = augmenter.augment_audio(wave, fps)
            features = extractor.extract_features(waves, fps)

            torch.save(features, dist_dir + channel_id + ".pth")

if __name__ == "__main__":
    main()