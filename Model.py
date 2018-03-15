from random import shuffle


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        new_class = super(ModelMeta, cls).__new__(cls, name, bases, attrs)
        new_class.all_items = []
        return new_class


class Model(metaclass=ModelMeta):
    def __init__(self, iid):
        self.iid = iid
        self.contains = []

    @classmethod
    def create(cls):
        count = len(cls.all_items)
        i = cls(count)
        cls.all_items.append(i)
        return i

    @classmethod
    def counts(cls):
        return len(cls.all_items)

    def tracks(self):
        return self.contains

    def print_edge_pair(self):
        with open(self.__class__.__name__+"_edgepair.txt", 'a') as f_out:
            for t in self.tracks():
                f_out.write(str(self.iid))
                f_out.write("\t")
                f_out.write(str(t.iid))
                f_out.write("\n")
                # print(self.pid, t.tid, sep="\t")

    def print_hypergraph(self):
        with open(self.__class__.__name__+"_hypergraph.txt", 'a') as f_out:
            # print(self.pid, end=":\t")
            f_out.write(str(self.iid))
            f_out.write("\t")
            for t in self.tracks():
                f_out.write(str(t.iid))
                f_out.write(",")
            f_out.write("\n")


class Genre(Model):
    def tracks(self):
        result = []
        for album in self.contains:
            result += album.contains
        return result


class Artist(Model):
    def tracks(self):
        result = []
        for album in self.contains:
            result += album.contains
        return result


class Album(Model):
    def __init__(self, album_id):
        super().__init__(album_id)
        self.artist = None
        self.genre = None

    def added_to_artist(self, artist):
        self.artist = artist
        artist.contains.append(self)

    def added_to_genre(self, genre):
        self.genre = genre
        genre.contains.append(self)


class Track(Model):
    def __init__(self, iid):
        super().__init__(iid)
        self.album = None
        self.playlists = []

    def added_to_album(self, album):
        self.album = album
        album.contains.append(self)

    def added_to_playlist(self, p):
        self.playlists.append(p)
        p.contains.append(self)

    def number_of_appearance(self):
        return len(self.playlists)


class Playlist(Model):
    def shuffle(self):
        shuffle(self.contains)
