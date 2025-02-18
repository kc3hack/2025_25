from pydub import AudioSegment
import numpy as np
from functools import reduce
import os

def change_frame_rate(wave: np.ndarray, fps_before: int, fps_after: int) -> np.ndarray:
    duration = wave.shape[0]/fps_before

    assert float(duration).is_integer()

    duration = int(duration)
    
    spec = np.fft.fft(wave)

    mask = np.zeros_like(spec)
    n = int(fps_after/2)
    mask[:n] = np.ones(n)
    spec = spec*mask
    
    wave = np.fft.ifft(spec)

    indexs = np.floor(np.arange(fps_after*duration) * fps_before/fps_after).astype(np.int32)
    wave = wave[indexs]

    return wave

def main():
    dir_name = "./src/assets/audio/mp3/"
    file_name = "NOUlyulQ30I.mp3"

    # 音声ファイルを読み込み
    sound = AudioSegment.from_file(dir_name + file_name, "mp3")

    # numpyに変換
    wav = np.array(sound.get_array_of_samples())
    channels = sound.channels
    fps = sound.frame_rate

    wav = wav.reshape(-1, channels).mean(axis=-1)

    period_seconds = 5
    period = (fps * period_seconds)

    sub_dir_name = dir_name + reduce(lambda p,c: p+"."+c, file_name.split(".")[:-1]) + "/"
    if not os.path.isdir(sub_dir_name):
        os.mkdir(sub_dir_name)

    for i in range(int(wav.shape[0] / period)): # 最後の半端な区間は切り捨てる(長さ統一のため)
        w = wav[i*period:(i+1)*period]
        w = w.reshape(-1)

        # サンプリング周波数を変える
        fps_after = 16000
        w = change_frame_rate(w, fps, fps_after)

        s = AudioSegment(
            data=w.astype("int16").tobytes(),
            sample_width=2,
            frame_rate=fps_after,
            channels=1
        )
        
        section_id = str(i)
        padded_section_id = "0" * (4 - len(section_id)) + section_id
        section_file_name = padded_section_id + ".mp3"
        s.export(sub_dir_name + section_file_name, format="mp3")

if __name__ == "__main__":
    main()