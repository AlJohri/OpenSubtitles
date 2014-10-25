#!/usr/bin/env python

import fileinput
from os import listdir
import sys
import glob

# years = range(0, 1985)
years = range(1983, 1985)

# can't even deal right now
# 1951 deleted
# 1953 deleted

for xyear in years:

	year = './OpenSubtitles2013/xml/en/%d' % xyear

	for movieDir in glob.glob(year + '/*' * 1):
		movieFiles = listdir(movieDir)
		script = filter(lambda x: x.endswith('.xml'), movieFiles)[0]

		text = ""
		f=open(movieDir+'/'+script)
		for line in f.readlines():
		    text += line

		print movieDir+'/'+script

		from lxml import etree
		root = etree.fromstring(text)
		result = ""
		tmp = []
		for x in root.xpath('//document/s/w'):
			tmp.append(x.text)
		for i in range(len(tmp)-1):
			result += tmp[i]
			if tmp[i+1] == None: 
				continue
			char = tmp[i+1][0]
			if (char >= 'A' and char <='z') or (char >= '0' and char <='9'):
				result += ' '
		#print result
		with open(movieDir+'/subtitle.txt', 'w') as g:
			g.write(result.encode('utf-8', 'ignore'))
