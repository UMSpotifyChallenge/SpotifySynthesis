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

    def print_edge_pair(self):
        with open(self.__class__.__name__+"_edgepair.txt", 'a') as f_out:
            for t in self.contains:
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
            for t in self.contains:
                f_out.write(str(t.iid))
                f_out.write(",")
            f_out.write("\n")



class Artist(Model):
    # def add_album(self, album):
    #     album.added_to_artist(self)
    #     self.contains.append(album)
    pass


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


class Genre(Model):
    # def add_album(self, album):
    #     album.added_to_genre(self)
    #     self.contains.append(album)
    pass
