import argparse
from random import sample
from operator import methodcaller
from Track import Track
from Playlist import Playlist

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", type=int, default=30, help="number of playlists")
    parser.add_argument("--t", type=int, default=50, help="number of tracks in each playlist")
    parser.add_argument("--o", type=int, default=20, help="number of tracks overlapping")
    args = parser.parse_args()

    playlistCount = args.p
    trackCountInPlaylist = args.t
    overlapCount = args.o

    playlists = []

    for pid in range(playlistCount):
        p = Playlist(pid)
        if pid == 0:
            for tid in range(trackCountInPlaylist):
                t = Track.createTrack()
                p.add_track(t)
        else:
            # randomly choose previously created tracks as many as overlap count
            previous = sample(range(len(Track.tracks)), overlapCount)
            for tid in previous:
                t = Track.tracks[tid] # previous tracks
                p.add_track(t)
            # create new tracks
            for tid in range(trackCountInPlaylist-overlapCount):
                t = Track.createTrack() # new track
                p.add_track(t)

        playlists.append(p)


    print("Result: number_of_appearance")
    sortedByCount = sorted(Track.tracks, key=methodcaller('number_of_appearance'), reverse=True)
    for i in range(min(20, len(Track.tracks))):
        print("track",i,"\t",sortedByCount[i].number_of_appearance())

    print("\nWrite graphs to file")
    playlists[0].print_edge_pair()
    playlists[0].print_hypergraph()

