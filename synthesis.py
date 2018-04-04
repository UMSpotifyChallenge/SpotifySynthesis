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
    parser.add_argument("--min_tracks_per_playlist", type=int, default=30, help="min number of songs per playlist")
    parser.add_argument("--max_tracks_per_playlist", type=int, default=60, help="max number of songs per playlist")
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
        biasFeat1 = random.randrange(Feature1.counts())
        biasFeat2 = random.randrange(Feature2.counts())
        biasFeat3 = random.randrange(Feature3.counts())

        weights = [1] * genreCount
        weightsFeat1 = [1] * Feature1.counts()
        weightsFeat2 = [1] * Feature2.counts()
        weightsFeat3 = [1] * Feature3.counts()
        weights[biasGenre] = genreCount * random.choice(range(3, 9))  # probability of biased genre is 75% ~ 90%
        weightsFeat1[biasFeat1] = Feature1.counts() * random.choice(range(5, 9))   # probability of biased feat is 80% ~ 90%
        weightsFeat2[biasFeat2] = Feature2.counts() * random.choice(range(4, 9))   # probability of biased feat is 78% ~ 90%
        weightsFeat3[biasFeat3] = Feature3.counts() * random.choice(range(3, 9))   # probability of biased feat is 75% ~ 90%

        tracksPerPlaylist = random.choice(tracksPerPlaylistRange)  # random number of tracks
        for _ in range(tracksPerPlaylist):
            genre = random.choices(Genre.all_items, weights)[0]  # it chooses random genre with bias
            feat1 = random.choices(Feature1.all_items, weightsFeat1)[0]  # it chooses random feat with bias
            feat2 = random.choices(Feature2.all_items, weightsFeat2)[0]  # it chooses random feat with bias
            feat3 = random.choices(Feature3.all_items, weightsFeat3)[0]  # it chooses random feat with bias

            genreTracks = genre.tracks()
            random.shuffle(genreTracks)
            for track in genreTracks:

                correctFeats = []
                correctFeats.append(track.f1 == feat1)
                correctFeats.append(track.f2 == feat2)
                correctFeats.append(track.f3 == feat3)
                if sum(correctFeats) < 2:  # if less than 2 features are correct, do not add track
                    continue
                if playlist.add_track(track):  # check no duplicate
                    break

        if len(playlist.tracks()) < tracksPerPlaylist:
            print("Warning: Playlist {} failed to be filled with tracks (short by {})".format(str(Playlist.counts()-1),str(tracksPerPlaylist - len(playlist.tracks()))))
        playlist.shuffle()
        # To get analysis
        # total_length = len(playlist.tracks())

        # f1 = Feature1.all_items[biasGenre % Feature1.counts()]
        # f1_list = list(filter(lambda t: t.f1 == f1, playlist.tracks()))
        # f1_length = len(f1_list)

        # f2 = Feature2.all_items[biasGenre % Feature2.counts()]
        # f2_list = list(filter(lambda t: t.f2 == f2, playlist.tracks()))
        # f2_length = len(f2_list)

        # f3 = Feature3.all_items[biasGenre % Feature3.counts()]
        # f3_list = list(filter(lambda t: t.f3 == f3, playlist.tracks()))
        # f3_length = len(f3_list)

        # print("{0:.2f}, {0:.2f}, {0:.2f}".format(f1_length/total_length, f2_length/total_length, f3_length/total_length))


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
    totalCount = 0
    sortedByCount = sorted(Track.all_items, key=methodcaller('number_of_appearance'), reverse=True)
    binSize = 50
    steps = int(Track.counts() / binSize)
    for i in range(steps):
        count = 0
        bin = range(i*binSize, min((i+1)*binSize, Track.counts()))
        for j in bin:
            count += sortedByCount[j].number_of_appearance()
        print("\tTracks in {}:\t{}".format(bin, count), file=file)
        totalCount += count
    print("total # appearance: ", totalCount, file=file)

    print("Top 10 tracks", file=file)
    for i in range(10):
        t = sortedByCount[i]
        print("\tTrack{}:\t{}".format(t.iid, t.number_of_appearance()), file=file)

    for f in features:
        f.print_result(file)
        f.print_hypergraph()

    Album.print_hypergraph()
    Artist.print_hypergraph()
    Genre.print_hypergraph()
    Playlist.print_hypergraph()
    Track.print_playlist()
