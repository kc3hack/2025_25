from pydub import AudioSegment
from functools import reduce

def main():
    src_dir = "./src/assets/audio/m4a/"
    dist_dir = "./src/assets/audio/mp3/"

    file_name = "NOUlyulQ30I.m4a"

    sound = AudioSegment.from_file(src_dir + file_name, file_name.split(".")[-1])

    new_file_name = reduce(lambda p,c: p+"."+c, file_name.split(".")[:-1] + ["mp3"])
    sound.export(dist_dir + new_file_name, format="mp3")

if __name__ == "__main__":
    main()