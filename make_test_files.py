#!/usr/bin/python

import os

if __name__ == "__main__":
	cwd = os.getcwd()
	playlistFile = cwd + '/Playlist_hypergraph.txt'
	outputFolder = cwd + '/testStartingIds'
	testPlaylists = {}
	with open(playlistFile, 'r') as f:
		for line in f:
			track_id, playlist = line.split()
			if int(playlist) > 699:
				if playlist not in testPlaylists:
					testPlaylists[playlist] = []
				testPlaylists[playlist].append(track_id)
	f.close()

	for key, value in testPlaylists.items():
		outputFile = outputFolder + '/' + str(key)
		with open(outputFile, 'w+') as f:
			for node in value:
				f.write("{0}\n".format(node))
		f.close()
