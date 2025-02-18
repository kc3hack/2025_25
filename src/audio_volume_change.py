from pydub import AudioSegment
import numpy as np

def load_songWave(path: str) -> tuple[np.ndarray, int]:
    song = AudioSegment.from_file(path, path.split(".")[-1])

    wav = np.array(song.get_array_of_samples())
    
    return wav, song.frame_rate

wav, fps = load_songWave("./src/assets/utako.mp3")

wav = wav * 15

sound = AudioSegment(
    data=wav.astype("int16").tobytes(),
    sample_width=2,
    frame_rate=fps,
    channels=2
)

sound.export("./src/assets/utako2.mp3", format="mp3")