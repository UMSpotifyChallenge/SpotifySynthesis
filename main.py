import argparse
import random
from operator import methodcaller
from Model import Genre, Artist, Album, Track, Playlist

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--genre", type=int, default=8, help="number of genres")
    parser.add_argument("--artist", type=int, default=50, help="number of artists")
    parser.add_argument("--playlist", type=int, default=100, help="number of playlists")
    parser.add_argument("--min_albums_per_artist", type=int, default=1, help="min number of albums per artists")
    parser.add_argument("--max_albums_per_artist", type=int, default=5, help="max number of albums per artists")
    parser.add_argument("--min_tracks_per_album", type=int, default=5, help="min number of songs per album")
    parser.add_argument("--max_tracks_per_album", type=int, default=15, help="max number of songs per album")
    parser.add_argument("--min_tracks_per_playlist", type=int, default=20, help="min number of songs per playlist")
    parser.add_argument("--max_tracks_per_playlist", type=int, default=50, help="max number of songs per playlist")
    parser.add_argument("--overlap", type=int, default=30, help="percentage of tracks overlapping")
    args = parser.parse_args()

    genreCount = args.genre
    artistCount = args.artist
    playlistCount = args.playlist
    albumsPerArtistRange = range(args.min_albums_per_artist, args.max_albums_per_artist+1)
    tracksPerAlbumRange = range(args.min_tracks_per_album, args.max_tracks_per_album+1)
    tracksPerPlaylistRange = range(args.min_tracks_per_playlist, args.max_tracks_per_playlist+1)
    overlapPercentage = args.overlap

    for _ in range(genreCount):
        Genre.create()

    for artistID in range(artistCount):
        artist = Artist.create()
        weights = [1] * genreCount
        biasGenre = artistID % genreCount  # an artist is likely to stick to one genre
        weights[biasGenre] = genreCount * random.choice(range(3, 9))  # probability of biased genre is 75% ~ 90%
        albumsPerArtist = random.choice(albumsPerArtistRange)
        for albumID in range(albumsPerArtist):
            album = Album.create()
            album.added_to_artist(artist)
            genre = random.choices(Genre.all_items, weights)[0]  # random genre (with bias) chosen
            album.added_to_genre(genre)
            tracksPerAlbum = random.choice(tracksPerAlbumRange)
            # print("Artist {}\tAlbum {}:\t{} tracks".format(artistID, albumID, tracksPerAlbum))
            for _ in range(tracksPerAlbum):
                track = Track.create()
                track.added_to_album(album)
        # print()

    # file = None
    file = open("result.txt", "w")
    print("Total tracks: ", Track.counts(), file=file)
    print("Total albums: ", Album.counts(), file=file)

    print("Total genres: ", Genre.counts(), file=file)
    for g in Genre.all_items:
        print("\tGenre {}:\t{} albums,\t{} tracks".format(g.iid, len(g.contains), len(g.tracks())), file=file)

    print("Total artists: ", Artist.counts(), file=file)
    for a in Artist.all_items:
        genres = [0] * genreCount
        for album in a.contains:
            genres[album.genre.iid] = 1
        differentGenreCount = genres.count(1)
        print("\tArtist {}:\t{} albums,\t{} tracks\tin {} genres".format(a.iid, len(a.contains), len(a.tracks()), differentGenreCount), file=file)


    for _ in range(playlistCount):
        p = Playlist.create()
        tracksPerPlaylist = random.choice(tracksPerPlaylistRange)
        if p.iid == 0:
            for tid in range(tracksPerPlaylist):
                t = Track.create()
                t.added_to_playlist(p)
        else:
            overlapCount = int(tracksPerPlaylist*overlapPercentage/100)
            # randomly choose previously created tracks as many as overlap count
            previous = random.sample(range(Track.counts()), overlapCount)
            for tid in previous:
                t = Track.all_items[tid] # previous tracks
                t.added_to_playlist(p)
            # create new tracks
            for tid in range(tracksPerPlaylist - overlapCount):
                t = Track.create() # new track
                t.added_to_playlist(p)
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

