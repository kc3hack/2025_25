import whisper
import os

def transcribe_files(model: whisper.Whisper, file_paths: list[str]) -> list[str]:
    transcribes = []
    for file_path in file_paths:
        result = model.transcribe(file_path)["text"]
        assert type(result) is str

        transcribes.append(result)

    return transcribes

def save_contents(contents: list[str], file_paths: list[str]) -> None:
    for i, file_path in enumerate(file_paths):
        with open(file_path, mode="w") as f:
            f.write(contents[i])

def transcribe_channel_contents(model: whisper.Whisper, src_dir: str, dist_dir: str, channel_id: str) -> None:
    file_paths = [src_dir + channel_id + "/" + path for path in os.listdir(src_dir + channel_id)]
    dist_paths = [dist_dir + channel_id + "/" + path[:-len(path.split(".")[-1])] + "txt" for path in os.listdir(src_dir + channel_id)]

    transcribes = transcribe_files(model, file_paths)

    if not os.path.isdir(dist_dir + channel_id):
        os.mkdir(dist_dir + channel_id)

    save_contents(transcribes, dist_paths)

def main():
    src_dir = "./src/assets/audio/JTubeSpeech/"
    dist_dir = "./src/assets/text/JTubeSpeech/"

    channel_ids = os.listdir(src_dir)

    model = whisper.load_model("large")
    for channel_id in channel_ids:
        transcribe_channel_contents(model, src_dir, dist_dir, channel_id)

if __name__ == "__main__":
    main()