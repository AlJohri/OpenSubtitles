import sys, csv
import babelfish
from subliminal.providers.opensubtitles import OpenSubtitlesProvider

class OpenSubtitlesDownloader():

	def __init__(self):
		self.provider = OpenSubtitlesProvider()
		self.provider.initialize()

	def download(self, imdb_id):
		subtitles = self.provider.query(set([babelfish.Language('eng')]), imdb_id=imdb_id)
		# import pdb; pdb.set_trace()
		for subtitle in subtitles:
			try:
				return self.provider.download_subtitle(subtitle)
			except Exception as e:
				print e
				continue

imdb_movies = []

with open("opensubtitles_imdb.tsv", 'rU') as f:
	reader = csv.DictReader(f, delimiter='\t')
	imdb_movies = [row for row in reader]

x = OpenSubtitlesDownloader()

for imdb_movie in imdb_movies:
	print imdb_movie['MovieName'], imdb_movie['MovieYear'],
	y = x.download(imdb_movie['IDMovieImdb']) # 218817

	if y:
		print "success"
	else:
		print "failed"
		continue

	with open("data/%s.txt" % imdb_movie['IDMovieImdb'], 'w') as f:
		f.write(y.encode('utf-8', 'ignore'))
