#!/usr/bin/env python

import os
import sys
sys.path.insert(0, '/usr/local/lib/python2.7/dist-packages')
import cv2
from itertools import islice
from xml.dom.minidom import Document

# in
imglist = '/home/smiles/hz/databases/WIDER-face/data/WIDER_new-trainval.txt'
label_new = "labels-new"
# out
plPair = '/home/smiles/hz/caffe-ssd/data/WIDER-face/trainval_new.txt'
xmlpath_new='Annotations_new_512/'
foldername='WiderFace'


def insertObject(doc, datas, imgSize):
    obj = doc.createElement('object')
    name = doc.createElement('name')
    #name.appendChild(doc.createTextNode(datas[0]))
    name.appendChild(doc.createTextNode('face'))
    obj.appendChild(name)
    pose = doc.createElement('pose')
    pose.appendChild(doc.createTextNode('Unspecified'))
    obj.appendChild(pose)
    truncated = doc.createElement('truncated')
    truncated.appendChild(doc.createTextNode(str(0)))
    obj.appendChild(truncated)
    difficult = doc.createElement('difficult')
    difficult.appendChild(doc.createTextNode(str(0)))
    obj.appendChild(difficult)
    bndbox = doc.createElement('bndbox')

    if  '\r' == str(datas[4])[-1] or '\n' == str(datas[4])[-1]:
        datas[4] = str(datas[4])[0:-1]
    else:
        datas[4] = str(datas[4])
    
    x = float(datas[1]) * imgSize[1]
    y = float(datas[2]) * imgSize[0]
    w = float(datas[3]) * imgSize[1]
    h = float(datas[4]) * imgSize[0]

    left = max(x-w*0.5,0.0)
    top  = max(y-h*0.5,0.0)
    right = min(x+w*0.5,imgSize[1]-1)
    bottom = min(y+h*0.5,imgSize[0]-1)

    xmin = doc.createElement('xmin')
    xmin.appendChild(doc.createTextNode(str(int(left))))
    bndbox.appendChild(xmin)    
    ymin = doc.createElement('ymin')                
    ymin.appendChild(doc.createTextNode(str(int(top))))
    bndbox.appendChild(ymin)                
    xmax = doc.createElement('xmax')                
    xmax.appendChild(doc.createTextNode(str(int(right))))
    bndbox.appendChild(xmax)                
    ymax = doc.createElement('ymax')    
    ymax.appendChild(doc.createTextNode(str(int(bottom))))
    bndbox.appendChild(ymax)

    obj.appendChild(bndbox)                
    return obj


def create():
    result = open(plPair, 'w')
    l = open(imglist,'r')
    line = l.readline().strip('\n')
    
    while line:
        label_path = line.replace('image','label').replace('jpg','txt')       
        fidin=open( label_path,'r' )

        lines = fidin.readlines()
        objIndex = 0        
        for data in lines:        
            objIndex += 1
            data=data.strip('\n')
            datas = data.split(' ')
            if 5 != len(datas):
                print 'bounding box information error'
                continue

            imageFile = line
            pictureName = line.split('/')[-1]
            folderName = '/'.join(line.split('/')[0:-1])

            img = cv2.imread(imageFile)
            imgSize = img.shape

            if 1 == objIndex:
                xmlName = pictureName.replace('.jpg', '.xml')
                print xmlpath_new + xmlName
                f = open(xmlpath_new + xmlName, "w")
                doc = Document()
                annotation = doc.createElement('annotation')
                doc.appendChild(annotation)
                
                folder = doc.createElement('folder')
                folder.appendChild(doc.createTextNode('/'.join(line.split('/')[-3:-1])))
                annotation.appendChild(folder)
                
                filename = doc.createElement('filename')
                filename.appendChild(doc.createTextNode(pictureName))
                annotation.appendChild(filename)
                
                source = doc.createElement('source')                
                database = doc.createElement('database')
                database.appendChild(doc.createTextNode('My Database'))
                source.appendChild(database)
                source_annotation = doc.createElement('annotation')
                source_annotation.appendChild(doc.createTextNode(foldername))
                source.appendChild(source_annotation)
                image = doc.createElement('image')
                image.appendChild(doc.createTextNode('flickr'))
                source.appendChild(image)
                flickrid = doc.createElement('flickrid')
                flickrid.appendChild(doc.createTextNode('NULL'))
                source.appendChild(flickrid)
                annotation.appendChild(source)
                
                owner = doc.createElement('owner')
                flickrid = doc.createElement('flickrid')
                flickrid.appendChild(doc.createTextNode('NULL'))
                owner.appendChild(flickrid)
                name = doc.createElement('name')
                name.appendChild(doc.createTextNode('cuhk'))
                owner.appendChild(name)
                annotation.appendChild(owner)
                
                size = doc.createElement('size')
                width = doc.createElement('width')
                width.appendChild(doc.createTextNode(str(imgSize[1])))
                size.appendChild(width)
                height = doc.createElement('height')
                height.appendChild(doc.createTextNode(str(imgSize[0])))
                size.appendChild(height)
                depth = doc.createElement('depth')
                depth.appendChild(doc.createTextNode(str(imgSize[2])))
                size.appendChild(depth)
                annotation.appendChild(size)
                
                segmented = doc.createElement('segmented')
                segmented.appendChild(doc.createTextNode(str(0)))
                annotation.appendChild(segmented)            
                annotation.appendChild(insertObject(doc, datas, imgSize))
            else:
                annotation.appendChild(insertObject(doc, datas, imgSize))
        try:
            f.write(doc.toprettyxml(indent = '    '))
            f.close()

            pic_path = '/'.join( line.split('/')[-4:] )
            xml_path = xmlpath_new + line.split('/')[-1].replace('jpg','xml')
            result.write(pic_path + ' ' + xml_path + '\n')

            fidin.close()
        except:
            pass
        line = l.readline().strip('\n')
    result.close()
          
if __name__ == '__main__':
    create()
