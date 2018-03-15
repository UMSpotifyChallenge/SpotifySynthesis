from Model import Model
from random import shuffle

class Playlist(Model):
    # def __init__(self, pid):
    #     self.pid = pid # playlist id
    #     self.tracks = []

    def add_track(self, t):
        t.added_to_playlist(self)
        self.contains.append(t)

    def shuffle(self):
        shuffle(self.contains)

    # def count(self):
    #     return len(self.tracks)


