from pygame import mixer
from path_config import SOUND_DIR
import os


class BGM:
    def __init__(self):
        self.music_path = os.path.join(SOUND_DIR, "bgm", "freelike-touhou125-music.ogg") # let say "for a while"
        self.volume = 1 # default
    
    def play(self):
        mixer.init()
        mixer.music.load(self.music_path)
        mixer.music.set_volume(self.volume)
        mixer.music.play(loops=-1)

    def stop():
        mixer.music.unload()
        mixer.music.stop()


