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


class Artist(Model):
    def add_album(self, album):
        album.added_to_artist(self)
        self.contains.append(album)


class Album(Model):
    def __init__(self, album_id):
        super().__init__(album_id)
        self.artist = None
        self.genre = None

    def added_to_artist(self, artist):
        self.artist = artist

    def added_to_genre(self, genre):
        self.genre = genre


class Genre(Model):
    def add_album(self, album):
        album.added_to_genre(self)
        self.contains.append(album)
