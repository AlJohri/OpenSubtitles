from os import listdir
import json
import sys
import glob

# year = sys.argv[1] if len(sys.argv) > 1 else None
# if not year: raise "shit"


years= [1985, 1986, 1987, 1988, 2012, 2013]
# years= [2013]
movies = []

for year in years:

	year = './OpenSubtitles2013/xml/en/'+str(year)

	for movieDir in glob.glob(year + '/*' * 1):
		movieFiles = listdir(movieDir)
		jsonFile  = filter(lambda x: x.endswith('.json'), movieFiles)
		if not jsonFile: continue
		script  = filter(lambda x: x.endswith('.txt'), movieFiles)
		if not script: continue
		json_data=open(movieDir+'/'+jsonFile[0])
		data = json.load(json_data)
		innerDict = {}
		for key, value in data.iteritems():
			innerDict[key] = value
		if innerDict.get('Genre'):
			innerDict['Genre']= innerDict['Genre'].split(', ')
		innerDict['osID'] = movieDir.split("/")[-1]
		if not innerDict.get('Type')=='movie': continue
		f = open(movieDir+'/'+script[0])
		text= ""
		for line in f.readlines():
			text+=line
		innerDict['script']=text
		movies.append(innerDict)
