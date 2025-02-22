import torchaudio

from analyze_voice import analyze_voice

if __name__ == "__main__":
    path = "./src/assets/audio/01_1_3.m4a"
    audio_data, fps = torchaudio.load(path)
    result = analyze_voice(audio_data.detach().cpu().numpy(), fps)
    print(result)