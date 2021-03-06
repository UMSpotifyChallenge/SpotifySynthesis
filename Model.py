import random


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

    @classmethod
    def print_hypergraph(cls):
        file = open(cls.__name__+"_hypergraph.txt", 'w')
        # for i in cls.all_items:
        #     print(i.iid, end="\t", file=file)
        #     for t in i.tracks():
        #         print(t.iid, end=",", file=file)
        #     print(file=file)
        for i in cls.all_items:
            for t in i.tracks():
                print(t.iid, i.iid, sep="\t", file=file)

    # def print_edge_pair(self):
    #     with open(self.__class__.__name__+"_edgepair.txt", 'a') as f_out:
    #         for t in self.tracks():
    #             f_out.write(str(self.iid))
    #             f_out.write("\t")
    #             f_out.write(str(t.iid))
    #             f_out.write("\n")
    #             # print(self.pid, t.tid, sep="\t")
    #
    # def print_hypergraph(self):
    #     with open(self.__class__.__name__+"_hypergraph.txt", 'a') as f_out:
    #         # print(self.pid, end=":\t")
    #         f_out.write(str(self.iid))
    #         f_out.write("\t")
    #         for t in self.tracks():
    #             f_out.write(str(t.iid))
    #             f_out.write(",")
    #         f_out.write("\n")


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
        self.f1 = None
        self.f2 = None
        self.f3 = None

    def added_to_album(self, album):
        self.album = album
        album.contains.append(self)

        self.f1 = Feature1.chooseRandom()  # feature value is arbitrarily random
        self.f1.contains.append(self)
        self.f2 = Feature2.chooseRandom()  # feature value is arbitrarily random
        self.f2.contains.append(self)
        self.f3 = Feature3.chooseRandom()  # feature value is arbitrarily random
        self.f3.contains.append(self)

    def added_to_playlist(self, p):
        self.playlists.append(p)
        p.contains.append(self)

    def number_of_appearance(self):
        return len(self.playlists)

    @classmethod
    def print_playlist(cls):
        file = open("Track_playlistList.txt", 'w')
        for t in cls.all_items:
            print(t.iid, end="\t", file=file)
            for p in t.playlists:
                print(p.iid, end=",", file=file)
            print(file=file)


class Playlist(Model):
    def shuffle(self):
        random.shuffle(self.contains)

    def add_track(self, track):
        if track in self.contains:
            return False
        else:
            track.added_to_playlist(self)
            return True


class Feature(Model):
    @classmethod
    def createFeatures(cls):
        for _ in range(random.choice(range(3, 10))):
            cls.create()

    @classmethod
    def chooseRandom(cls):
        return random.choice(cls.all_items)

    @classmethod
    def print_result(cls, file):
        print(cls.__name__, file=file)
        for f in cls.all_items:
            print("\tvalue {}:\t{} tracks".format(f.iid, len(f.tracks())), file=file)


class Feature1(Feature):
    pass

class Feature2(Feature):
    pass

class Feature3(Feature):
    pass
