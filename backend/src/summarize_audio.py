import os
from functools import reduce

from utils import getSubFilePaths
from modules.AudioSummarizer import AudioSummarizer

def main():
    src_dir = "./src/assets/audio/JTubeSpeech/"
    dist_dir = "./src/assets/text/JTubeSpeech/"

    summarizer = AudioSummarizer()

    def summarize_channel_audio(channel_id: str) -> None:
        file_paths = getSubFilePaths(src_dir + channel_id)

        transcribe, answers = summarizer.summarize(file_paths)

        result_content = transcribe + "\n"*4 + reduce(lambda p, c: p + "\n"*3 + c, answers)

        with open(dist_dir + channel_id + ".txt", mode="w") as f:
            f.write(result_content)

    for channel_id in os.listdir(src_dir):
        summarize_channel_audio(channel_id)

if __name__ == "__main__":
    main()