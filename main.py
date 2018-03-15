import argparse
import random
from operator import methodcaller
from Track import Track
from Playlist import Playlist
from Model import Artist, Album, Genre

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--genre", type=int, default=8, help="number of genres")
    parser.add_argument("--artist", type=int, default=50, help="number of artists")
    parser.add_argument("--playlist", type=int, default=100, help="number of playlists")
    parser.add_argument("--min_albums_per_artist", type=int, default=1, help="min number of albums per artists")
    parser.add_argument("--max_albums_per_artist", type=int, default=5, help="max number of albums per artists")
    parser.add_argument("--min_tracks_per_album", type=int, default=4, help="min number of songs per album")
    parser.add_argument("--max_tracks_per_album", type=int, default=10, help="max number of songs per album")
    parser.add_argument("--min_tracks_per_playlist", type=int, default=20, help="min number of songs per playlist")
    parser.add_argument("--max_tracks_per_playlist", type=int, default=50, help="max number of songs per playlist")
    parser.add_argument("--overlap", type=int, default=30, help="percentage of tracks overlapping")
    args = parser.parse_args()

    genreCount = args.genre
    artistCount = args.artist
    playlistCount = args.playlist
    albumsPerArtistRange = range(args.min_albums_per_artist, args.max_albums_per_artist)
    tracksPerAlbumRange = range(args.min_tracks_per_album, args.max_tracks_per_album)
    tracksPerPlaylistRange = range(args.min_tracks_per_playlist, args.max_tracks_per_playlist)
    overlapPercentage = args.overlap

    for _ in range(genreCount):
        Genre.create()

    for _ in range(artistCount):
        artist = Artist.create()
        albumsPerArtist = random.choice(albumsPerArtistRange)
        for _ in range(albumsPerArtist):
            album = Album.create()
            album.added_to_artist(artist)
            tracksPerAlbum = random.choice(tracksPerAlbumRange)
            for _ in range(tracksPerAlbum):
                track = Track.create()
                track.added_to_album(album)


    for _ in range(playlistCount):
        p = Playlist.create()
        tracksPerPlaylist = random.choice(tracksPerPlaylistRange)
        if p.iid == 0:
            for tid in range(tracksPerPlaylist):
                t = Track.create()
                p.add_track(t)
        else:
            overlapCount = int(tracksPerPlaylist*overlapPercentage/100)
            # randomly choose previously created tracks as many as overlap count
            previous = random.sample(range(Track.counts()), overlapCount)
            for tid in previous:
                t = Track.all_items[tid] # previous tracks
                p.add_track(t)
            # create new tracks
            for tid in range(tracksPerPlaylist - overlapCount):
                t = Track.create() # new track
                p.add_track(t)
        p.shuffle()


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

