#!/usr/bin/python

import os

if __name__ == "__main__":

	# Input File Format: track_id \t item_id
	inputFiles = []
	for filename in os.listdir(os.getcwd()):
		root, ext = os.path.splitext(filename)
		if root.endswith('hypergraph') and ext == '.txt':
			inputFiles.append(filename)

	inputFiles.remove("Playlist_hypergraph.txt")

	# Need to keep track of all the hyper-edge membership
	all_edges = []
	hyper_edge_count = 0
	for filename in inputFiles:
		current_edge_mapping = {}
		filename = os.getcwd() + '/' + filename
		with open(filename, 'r') as f:
			for line in f:
				track_id, item_id = line.split()
				# Need to transform from local mapping to global mapping
				if item_id not in current_edge_mapping:
					current_edge_mapping[item_id] = hyper_edge_count
					hyper_edge_count += 1
				edge_pair = (current_edge_mapping[item_id], track_id)
				all_edges.append(edge_pair)
		f.close()

	playlist_file = os.getcwd() + '/Playlist_hypergraph.txt'
	current_edge_mapping = {}
	with open(playlist_file, 'r') as f:
		for line in f:
			track, playlist = line.split()
			if int(playlist) < 700:
				if playlist not in current_edge_mapping:
					current_edge_mapping[playlist] = hyper_edge_count
					hyper_edge_count += 1
				edge_pair = (current_edge_mapping[playlist], track_id)
				all_edges.append(edge_pair)

	outputFile = os.getcwd() + '/track_hypergraph_all_features.csv'
	with open(outputFile, 'w+') as f:
		for ep in all_edges:
			line = "{0},{1}\n".format(ep[0], ep[1])
			f.write(line)
	f.close()
	print("Finished making track hypergraph")
