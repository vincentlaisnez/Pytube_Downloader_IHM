import os
from pathlib import Path
from pytube import YouTube


# config directory
def directory_change():
    PATH = Path.home()
    DL_DIR = PATH.joinpath(PATH / "Documents" / "Pytube_Downloader")
    DL_DIR.mkdir(exist_ok=True)
    os.chdir(DL_DIR)


# download sounds and save .mp3
def download(item):
    """
    :param item: url Youtube
    :return: bool for succes dl
    """
    if item.startswith("https://www.youtube.com/") or item.startswith("https://youtu.be/"):
        youtube_video = YouTube(item)
        # youtube_video.streams pour voir les différents itag video et audio
        # utiliser .itag(numéro itag) pour télécharger uniquement par le tag
        stream = youtube_video.streams.filter(only_audio=True).first()
        stream.download(filename=f'{youtube_video.title}.mp3')
        return True


if __name__ == '__main__':
    print("download sound YouTube")
