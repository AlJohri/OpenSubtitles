from os import listdir
import json
import sys
import glob

# year = sys.argv[1] if len(sys.argv) > 1 else None
# if not year: raise "shit"

year = './OpenSubtitles2013/xml/en/1985'

# movies = {}
movies = []

for movieDir in glob.glob(year + '/*' * 1):
	movieFiles = listdir(movieDir)
	jsonFile  = filter(lambda x: x.endswith('.json'), movieFiles)[0]
	script  = filter(lambda x: x.endswith('.txt'), movieFiles)[0]
	json_data=open(movieDir+'/'+jsonFile)
	data = json.load(json_data)
	innerDict = {}
	for key, value in data.iteritems():
		innerDict[key] = value
	if innerDict.get('Genre'):
		innerDict['Genre']= innerDict['Genre'].split(', ')
	f = open(movieDir+'/'+script)
	text= ""
	for line in f.readlines():
		text+=line
	innerDict['script']=text
	movies.append(innerDict)
	# movies[jsonFile.split('.')[0]]=innerDict