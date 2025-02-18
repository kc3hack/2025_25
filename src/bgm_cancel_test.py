from pydub import AudioSegment
import numpy as np

def load_songWave(path: str) -> tuple[np.ndarray, int]:
    song = AudioSegment.from_file(path, path.split(".")[-1])

    wav = np.array(song.get_array_of_samples())
    wav = wav.reshape((-1, song.channels)).mean(axis=-1).reshape(-1)
    
    return wav, song.frame_rate

def cleanseWave(wav: np.ndarray, fps: int, resolution: float = 1) -> np.ndarray:
    section_size = fps / resolution
    assert section_size.is_integer() and wav.shape[0] >= section_size
    section_size = int(section_size)

    wav = wav[:int(wav.shape[0] / section_size) * section_size]

    wav = wav.reshape(-1, int(fps / resolution))
    spec = np.fft.fft(wav)

    mask = np.zeros_like(spec)

    range_min = int(25 / resolution)
    range_max = int(2000 / resolution)
    mask[:, range_min:range_max] = 0.2 * np.ones((mask.shape[0], (range_max - range_min)), dtype=np.int16)

    range_min = int(50 / resolution)
    range_max = int(1500 / resolution)
    mask[:, range_min:range_max] = 0.3 * np.ones((mask.shape[0], (range_max - range_min)), dtype=np.int16)

    range_min = int(100 / resolution)
    range_max = int(1000 / resolution)
    mask[:, range_min:range_max] = 0.4 * np.ones((mask.shape[0], (range_max - range_min)), dtype=np.int16)

    range_min = int(200 / resolution)
    range_max = int(800 / resolution)
    mask[:, range_min:range_max] = 1 * np.ones((mask.shape[0], (range_max - range_min)), dtype=np.int16)

    spec_after = spec * mask

    reconstruct = np.fft.ifft(spec_after)
    reconstruct = reconstruct.reshape(-1)

    return reconstruct

wav, fps = load_songWave("./src/assets/utako.mp3")

b_median = np.median(np.abs(wav))

wav = cleanseWave(wav, fps, resolution=0.0625)
wav = cleanseWave(wav, fps, resolution=0.125)
wav = cleanseWave(wav, fps, resolution=0.25)
wav = cleanseWave(wav, fps, resolution=0.5)
wav = cleanseWave(wav, fps, resolution=1)

wav *= b_median / np.median(np.abs(wav))
wav = wav.astype("int16")

sound = AudioSegment(
    data=wav.tobytes(),
    sample_width=2,
    frame_rate=fps,
    channels=1
)

sound.export("./src/assets/utako_filtered.mp3", format="mp3")