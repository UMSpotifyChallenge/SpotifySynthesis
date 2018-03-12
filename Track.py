class Track:
    tracks = []

    def __init__(self, tid, gid):
        self.tid = tid # track id
        self.gid = gid # genre id ??
        self.playlist = []

    @classmethod
    def createTrack(cls):
        count = len(cls.tracks)
        t = Track(count, -1)
        cls.tracks.append(t)
        return t

    def added_to_playlist(self, p):
        self.playlist.append(p)

    def number_of_appearance(self):
        return len(self.playlist)
