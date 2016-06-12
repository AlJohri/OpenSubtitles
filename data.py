#!/usr/bin/python3

import xml.etree.ElementTree as ET
import datetime
import os
import json
from gzip import GzipFile
import re
import pprint

def filesInDir(dirname):
    result = []
    for dirpath, dirs, files in os.walk(dirname):
        for filename in files:
            fname = os.path.join(dirpath, filename)
            result.append(fname)
    return result

def genList(tree):
    root = tree.getroot()

    timeFormat = '%H:%M:%S'
    maxDelta = datetime.timedelta(seconds=1)

    startTime = datetime.datetime.min
    strbuf = ''
    sentList = []

    for child in root:
        for elem in child:
            if elem.tag == 'time':
                elemID = elem.attrib['id']
                elemVal = elem.attrib['value'][:-4]
                if elemID[-1] == 'S':
                    startTime = datetime.datetime.strptime(elemVal, timeFormat)
                else:
                    sentList.append((strbuf.strip(), startTime, datetime.datetime.strptime(elemVal, timeFormat)))
                    strbuf = ''
            else:
                try:
                    strbuf = strbuf + " " + elem.text
                except:
                    pass

    resultPairs = []
    for idx in range(0, len(sentList) - 1):
        cur = sentList[idx]
        nxt = sentList[idx + 1]
        if nxt[1] - cur[2] <= maxDelta and cur and nxt:
            tmp = {}
            tmp['question'] = cur[0].replace('\\\'','\'')
            tmp['answer'] = nxt[0].replace('\\\'', '\'')
            tmp['docId'] = "OpenSubtitles"
            tmp['qSentId'] = 20160110
            tmp['aSentId'] = 20160110
            resultPairs.append(tmp)
    return resultPairs

def getXML(filepath):
    fext = os.path.splitext(filepath)[1]
    if fext == '.gz':
        tmp = GzipFile(filename=filepath)
        return ET.parse(tmp)
    else:
        return ET.parse(filepath)

def genForDir(dirname):
    pat = re.compile('\\.xml.*', re.DOTALL)

    dirList = filesInDir(dirname)
    for filepath in dirList:
        outputName = 'json' + re.sub(pat, '.json', filepath[1:])
        try:
            doc = getXML(filepath)
            result = genList(doc)
            if not os.path.exists(os.path.dirname(outputName)):
                os.makedirs(os.path.dirname(outputName))
            with open(outputName, 'w') as outputFile:
                json.dump(result, outputFile)
            print(outputName + " written from " + filepath)
        except:
            pass



a = datetime.datetime.now()
dirtest = './en/'
genForDir(dirtest)
b = datetime.datetime.now()
print('\nTotal time:')
print(b - a)

