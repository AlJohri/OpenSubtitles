# http://www.omdbapi.com/?i=tt0103644

import csv, glob, os.path

imdb_movies = []

with open("opensubtitles_imdb.tsv", 'rU') as f:
	reader = csv.DictReader(f, delimiter='\t')
	imdb_movies = {row['IDMovie']: row for row in reader}

# iterate through all subtitles

for f in glob.glob('./OpenSubtitles2013/xml/en' + '/*' * 2):
	os_id = f.split("/")[-1]
	imdb_id = imdb_movies.get(os_id, {}).get('IDMovieImdb', {})
	print f, "|", "OpenSubtitles ID: ", os_id, "|", "IMDB ID: ", imdb_id

# iterate through 2013 subtitles

for f in glob.glob('./OpenSubtitles2013/xml/en/2013' + '/*' * 1):
	os_id = f.split("/")[-1]
	imdb_id = imdb_movies.get(os_id, {}).get('IDMovieImdb', {})
	print f, "|", "OpenSubtitles ID: ", os_id, "|", "IMDB ID: ", imdb_id

