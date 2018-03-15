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

    def print_edge_pair(self):
        with open("edgepair.txt", 'a') as f_out:
            for t in self.contains:
                f_out.write(str(self.iid))
                f_out.write("\t")
                f_out.write(str(t.iid))
                f_out.write("\n")
                # print(self.pid, t.tid, sep="\t")

    def print_hypergraph(self):
        with open("hypergraph.txt", 'a') as f_out:
            # print(self.pid, end=":\t")
            f_out.write(str(self.iid))
            f_out.write("\t")
            for t in self.contains:
                f_out.write(str(t.iid))
                f_out.write(",")
            f_out.write("\n")

