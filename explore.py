#!/usr/bin/env python

print ("loading data... ")
from load import movies
print ("loaded data")

genres = set()

for movie in movies:
	for genre in movie.get('Genre', []):
		genres.add(genre)

print "List of Genres:"
print list(genres)