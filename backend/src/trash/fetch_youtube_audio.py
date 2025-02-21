from yt_dlp import YoutubeDL

# 注）音声ファイルをダウンロードしたいディレクトリに移動してから実行すること

def main():
    link = "https://www.youtube.com/watch?v=NOUlyulQ30I"
    file_name = "%(id)s.%(ext)s"

    options = {
        "format": "bestaudio[ext=m4a]",
        "outtmpl": file_name
    }

    with YoutubeDL(options) as ydl:
        ydl.download([link])

if __name__ == "__main__":
    main()