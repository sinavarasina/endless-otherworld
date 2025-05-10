from pygame import mixer
from path_config import SOUND_DIR
import os


class BGM:
    def __init__(self):
        self.music_path = os.path.join(SOUND_DIR, "bgm", "freelike-touhou125-music.ogg")
        self.volume = 0
        self.playing = False

    def play(self):
        if not self.playing:
            mixer.init()
            mixer.music.load(self.music_path)
            mixer.music.set_volume(self.volume)
            mixer.music.play(loops=-1)
            self.playing = True
        else:
            mixer.music.set_volume(self.volume) 

    def stop(self):
        mixer.music.stop()
        mixer.music.unload()
        self.playing = False

