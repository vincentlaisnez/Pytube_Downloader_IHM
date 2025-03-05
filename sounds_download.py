import os
from pathlib import Path
from pytubefix import YouTube


# config directory
def directory_change():
    PATH = Path.home()
    DL_DIR = PATH.joinpath(PATH / "Documents" / "Pytube_Downloader")
    DL_DIR.mkdir(exist_ok=True)
    os.chdir(DL_DIR)


# download sounds and save .mp3 or mp4 if error
def download(item):
    """
    :param item: url Youtube
    :return: bool for succes dl
    """
    youtube_video = YouTube(item)
    stream = youtube_video.streams.filter(only_audio=True).first()
    try:
        stream.download(filename=f'{youtube_video.title}.mp3')
    except OSError:
        print(f"Impossible de telecharger {youtube_video.title}.mp3")
        print("téléchargement en mp4")
        stream.download()
    return True


if __name__ == '__main__':
    print("download sound YouTube")
