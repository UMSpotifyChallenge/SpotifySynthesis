class Playlist:
    def __init__(self, pid):
        self.pid = pid # playlist id
        self.tracks = []

    def add_track(self, t):
        t.added_to_playlist(self)
        self.tracks.append(t)

    # def count(self):
    #     return len(self.tracks)

    def print_edge_pair(self):
        with open("edgepair.txt", 'w') as f_out:
            for t in self.tracks:
                f_out.write(str(self.pid))
                f_out.write("\t")
                f_out.write(str(t.tid))
                f_out.write("\n")
                # print(self.pid, t.tid, sep="\t")

    def print_hypergraph(self):
        with open("hypergraph.txt", 'w') as f_out:
            # print(self.pid, end=":\t")
            f_out.write(str(self.pid))
            f_out.write("\t")
            for t in self.tracks:
                f_out.write(str(t.tid))
                f_out.write(",")
            f_out.write("\n")

