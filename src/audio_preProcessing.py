from pydub import AudioSegment
import numpy as np

from utils import getSubFilePaths
from AudioPreProcessor import AudioPreProcessor

def read_audio(path: str) -> tuple[np.ndarray, int, int]:
    song = AudioSegment.from_file(path, path.split(".")[-1])
    wav = np.array(song.get_array_of_samples())
    return wav, song.channels, song.frame_rate

def save_audio(wave: np.ndarray, channels: int, fps: int, file_name: str) -> None:
    wave = wave.astype("int16")

    sound = AudioSegment(
        data=wave.tobytes(),
        sample_width=2,
        frame_rate=fps,
        channels=channels
    )

    sound.export(file_name, format=file_name.split(".")[-1])

def main():
    processor = AudioPreProcessor()

    src_dir = "./src/assets/audio/JTubeSpeech/"
    dist_dir = "./src/assets/audio/regions/kanto/"
    channel_id = "ACF"

    paths = getSubFilePaths(src_dir + channel_id)

    fps = 16000
    audios = [read_audio(path) for path in paths]

    waves = [(processor.to_monophonic(audio[0], audio[1]), audio[2]) for audio in audios]
    waves = [processor.change_samplingRate(wave[0], wave[1], fps) for wave in waves]

    wave = processor.concat_waves(waves)
    wave = processor.cancel_noise(wave, fps)
    wave = processor.standardize(wave) * 1500

    save_audio(wave, 1, fps, dist_dir + channel_id + ".mp3")

if __name__ == "__main__":
    main()