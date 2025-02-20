from utils import getSubFilePaths, read_audio, save_audio
from modules.AudioPreProcessor import AudioPreProcessor

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
    wave = processor.standardize(wave) * 1500

    save_audio(wave, 1, fps, dist_dir + channel_id + ".mp3")

if __name__ == "__main__":
    main()