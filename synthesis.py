import argparse
import random
import numpy as np
from operator import methodcaller
from Model import Genre, Artist, Album, Track, Playlist
from Model import Feature1, Feature2, Feature3

if __name__ == '__main__':
    file = open("README", "w") # README is our result, so that github will show it nicely :)

    parser = argparse.ArgumentParser()
    parser.add_argument("--genre", type=int, default=8, help="number of genres")
    parser.add_argument("--artist", type=int, default=100, help="number of artists")
    parser.add_argument("--playlist", type=int, default=1000, help="number of playlists")
    parser.add_argument("--min_albums_per_artist", type=int, default=1, help="min number of albums per artists")
    parser.add_argument("--max_albums_per_artist", type=int, default=5, help="max number of albums per artists")
    parser.add_argument("--min_tracks_per_album", type=int, default=5, help="min number of songs per album")
    parser.add_argument("--max_tracks_per_album", type=int, default=15, help="max number of songs per album")
    parser.add_argument("--min_tracks_per_playlist", type=int, default=20, help="min number of songs per playlist")
    parser.add_argument("--max_tracks_per_playlist", type=int, default=50, help="max number of songs per playlist")
    args = parser.parse_args()

    parser.print_help(file=file)
    print(file=file)

    genreCount = args.genre
    artistCount = args.artist
    playlistCount = args.playlist
    albumsPerArtistRange = range(args.min_albums_per_artist, args.max_albums_per_artist+1)
    tracksPerAlbumRange = range(args.min_tracks_per_album, args.max_tracks_per_album+1)
    tracksPerPlaylistRange = range(args.min_tracks_per_playlist, args.max_tracks_per_playlist+1)

    features = [Feature1, Feature2, Feature3]
    for f in features:
        f.createFeatures()

    for _ in range(genreCount):
        Genre.create()

    for artistID in range(artistCount):
        artist = Artist.create()
        biasGenre = artistID % genreCount  # an artist is likely to stick to certain genre
        weights = [1] * genreCount
        weights[biasGenre] = genreCount * random.choice(range(3, 9))  # probability of biased genre is 75% ~ 90%
        albumsPerArtist = random.choice(albumsPerArtistRange)  # random number of albums
        for albumID in range(albumsPerArtist):
            album = Album.create()
            album.added_to_artist(artist)
            genre = random.choices(Genre.all_items, weights)[0]  # random genre (with bias) chosen
            album.added_to_genre(genre)
            tracksPerAlbum = random.choice(tracksPerAlbumRange)  # random number of tracks
            for _ in range(tracksPerAlbum):
                track = Track.create()
                track.added_to_album(album)

    for pid in range(playlistCount):
        playlist = Playlist.create()
        biasGenre = pid % genreCount  # a playlist is likely to be based on certain genre
        weights = [1] * genreCount
        weights[biasGenre] = genreCount * random.choice(range(3, 9))  # probability of biased genre is 75% ~ 90%
        tracksPerPlaylist = random.choice(tracksPerPlaylistRange)  # random number of tracks
        for _ in range(tracksPerPlaylist):
            genre = random.choices(Genre.all_items, weights)[0]  # it chooses random genre with bias
            while True:
                t = int(np.random.triangular(0, 0, len(genre.tracks())))  # lower-numbered tracks are more likely
                track = genre.tracks()[t]
                if playlist.add_track(track):  # check no duplicate
                    break
        playlist.shuffle()

    print("# tracks: ", Track.counts(), file=file)
    print("# albums: ", Album.counts(), file=file)

    print("# genres: ", Genre.counts(), file=file)
    for g in Genre.all_items:
        print("\tGenre {}:\t{} albums,\t{} tracks".format(g.iid, len(g.contains), len(g.tracks())), file=file)

    print("# artists: ", Artist.counts(), file=file)
    for a in Artist.all_items:
        genres = [0] * genreCount
        for album in a.contains:
            genres[album.genre.iid] = 1
        differentGenreCount = genres.count(1)
        print("\tArtist {}:\t{} albums,\t{} tracks\tin {} genres".format(a.iid, len(a.contains), len(a.tracks()), differentGenreCount), file=file)

    print("# appearance of track in playlists", file=file)
    sortedByCount = sorted(Track.all_items, key=methodcaller('number_of_appearance'), reverse=True)
    binSize = 50
    steps = int(Track.counts() / binSize)
    for i in range(steps):
        count = 0
        bin = range(i*binSize, min((i+1)*binSize, Track.counts()))
        for j in bin:
            count += Track.all_items[j].number_of_appearance()
        print("\tTracks in {}:\t{}".format(bin, count), file=file)

    for f in features:
        f.print_result(file)
        f.print_hypergraph()

    Album.print_hypergraph()
    Artist.print_hypergraph()
    Genre.print_hypergraph()
    Playlist.print_hypergraph()
