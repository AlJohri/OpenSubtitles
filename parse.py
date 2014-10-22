#!/usr/bin/env python

# http://www.omdbapi.com/?i=tt0103644

import csv, glob, os.path
import requests
import json
imdb_movies = []
def padNum(x):
	s = str(x)
	return "0"*(7-len(s))+s

with open("opensubtitles_imdb.tsv", 'rU') as f:
	reader = csv.DictReader(f, delimiter='\t')
	imdb_movies = {row['IDMovie']: row for row in reader}

# iterate through 2013 subtitles

for movieDir in glob.glob('./OpenSubtitles2013/xml/en' + '/*' * 2):
# for movieDir in glob.glob('./OpenSubtitles2013/xml/en/2013' + '/*' * 1):
	os_id = movieDir.split("/")[-1]
	imdb_id = imdb_movies.get(os_id, {}).get('IDMovieImdb', {})
	print movieDir, "|", "OpenSubtitles ID: ", os_id, "|", "IMDB ID: ", imdb_id
	response = requests.get("http://www.omdbapi.com/?i=tt"+padNum(imdb_id))
	text = response.json()	
	with open(movieDir+'/'+padNum(imdb_id)+'.json', 'w') as g:
		json.dump(text, g)
	print text.get('Genre')