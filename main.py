import argparse
from random import sample
from operator import methodcaller
from Track import Track
from Playlist import Playlist

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", type=int, default=100, help="number of playlists")
    parser.add_argument("--t", type=int, default=50, help="number of tracks in each playlist")
    parser.add_argument("--o", type=int, default=20, help="number of tracks overlapping")
    args = parser.parse_args()

    playlistCount = args.p
    trackCountInPlaylist = args.t
    overlapCount = args.o

    for _ in range(playlistCount):
        p = Playlist.create()
        if p.iid == 0:
            for tid in range(trackCountInPlaylist):
                t = Track.create()
                p.add_track(t)
        else:
            # randomly choose previously created tracks as many as overlap count
            previous = sample(range(Track.counts()), overlapCount)
            for tid in previous:
                t = Track.all_items[tid] # previous tracks
                p.add_track(t)
            # create new tracks
            for tid in range(trackCountInPlaylist-overlapCount):
                t = Track.create() # new track
                p.add_track(t)

        Playlist.all_items.append(p)


    print("Result: number_of_appearance")
    sortedByCount = sorted(Track.all_items, key=methodcaller('number_of_appearance'), reverse=True)
    for i in range(min(20, Track.counts())):
        print("track",i,"\t",sortedByCount[i].number_of_appearance())

    print("\nWrite graphs to file")
    # erase contents of the files
    open('edgepair.txt', 'w').close()
    open('hypergraph.txt', 'w').close()
    # append to them
    for p in Playlist.all_items:
        p.print_edge_pair()
        p.print_hypergraph()

