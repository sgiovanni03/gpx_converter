'''
Author: Giovanni Serrato
Description: Used to create maps .gpx
'''

import datetime
from tkinter import filedialog as fd
from xml.dom import minidom
import json

''' Get Input File'''
filename_cords = fd.askopenfilename()

name = (filename_cords.split('/')[-1])
#filename = fd.askopenfilename()

#with open(filename) as f:
#    lines = f.readlines()

''' Set Variables'''

outputFile_name = name + '.gpx' #lines[0].replace('\n','')
author = "Giovanni Serrato" #lines[1].replace('\n','')
map_name = name #lines[2].replace('\n','')
keywords = "pythonCreated" #lines[3].replace('\n','')
desc = name #lines[4].replace('\n','')
ele_n = 0

''' Set up XML headers '''
gpx_body = minidom.Document()

gpx_file = gpx_body.createElement('gpx') 
gpx_file.setAttribute('xmlns', 'http://www.topografix.com/GPX/1/1')
gpx_file.setAttribute('version', '1.1')
gpx_file.setAttribute('creator', author)
gpx_file.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
gpx_file.setAttribute('xsi:schemaLocation', 'http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd')
gpx_body.appendChild(gpx_file)

''' Create metadata '''
metadata = gpx_body.createElement('metadata')

metadata_name = gpx_body.createElement('name')
metadata_name.appendChild(gpx_body.createTextNode(map_name))

metadata_keyword = gpx_body.createElement('keywords')
metadata_keyword.appendChild(gpx_body.createTextNode(keywords))

metadata_desc = gpx_body.createElement('desc')
metadata_desc.appendChild(gpx_body.createTextNode(desc))

metadata.appendChild(metadata_name)
metadata.appendChild(metadata_keyword)
metadata.appendChild(metadata_desc)
gpx_file.appendChild(metadata)

''' Create Track Name '''
trk = gpx_body.createElement('trk')
trk_name = gpx_body.createElement('name')
trk_name.appendChild(gpx_body.createTextNode(map_name))

trk.appendChild(trk_name)

''' Get File Of Coordinates '''
#filename_cords = fd.askopenfilename()
f = open(filename_cords,)
data = json.load(f)
entries = data.get('log').get('entries')

coordinates = []

for response in entries:
    content = response.get('response').get('content')
    text = content.get('text')
    mimeType = content.get('mimeType')
    if mimeType == "text/plain": 
        tmp = json.loads(text).get('geometries')[0]
        if len(tmp) == 2:
            coordinates.append([tmp['y'],tmp['x']])

''' Create Track Points '''
trkseg = gpx_body.createElement('trkseg')

for y,x in coordinates:
    trkpt = gpx_body.createElement('trkpt')
    trkpt.setAttribute('lat', str(y))
    trkpt.setAttribute('lon', str(x))
    trkpt_ele = gpx_body.createElement('ele')
    trkpt_time = gpx_body.createElement('time')

    trkpt_ele.appendChild(gpx_body.createTextNode(str(ele_n)))
    trkpt_time.appendChild(gpx_body.createTextNode(str(datetime.datetime.now().isoformat())+'Z'))

    trkpt.appendChild(trkpt_ele)
    trkpt.appendChild(trkpt_time)
    trkseg.appendChild(trkpt)

    ele_n+=1

trk.appendChild(trkseg)
gpx_file.appendChild(trk)

''' Create File '''
xml_str = gpx_body.toprettyxml(encoding="UTF-8", indent ="\t") 
  
save_path_file = "D:\\sgiov\\Documents\\GPX\\Created\\" + outputFile_name
  
with open(save_path_file, "wb") as f:
    f.write(xml_str) 