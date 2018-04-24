#!/usr/bin/env python

import os
import sys
sys.path.insert(0, '/usr/local/lib/python2.7/dist-packages')
import cv2
from itertools import islice
from xml.dom.minidom import Document
import numpy as np

'''
#=====Object example:=======
    <object>
        <name>face</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>{{}}</xmin>
            <ymin>{{}}</ymin>
            <xmax>{{}}</xmax>
            <ymax>{{}}</ymax>
        </bndbox>
    </object>
'''
def insertObject(doc, box, imgSize):
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
    
    left = box[0]
    top = box[1]
    w = box[2]
    h = box[3]

    left = max(left,0.0)
    top  = max(top,0.0)
    right = min(left+w,imgSize[1]-1)
    bottom = min(top+h,imgSize[0]-1)

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


def anno_wider2voc(annos):
    matrix = np.asarray(annos)
    boxes = matrix[:,:4]
    labels = matrix[:,4:]

    #print boxes.shape, labels.shape
    assert boxes.shape[0]==labels.shape[0]
    return list(boxes), list(labels)

def isValidBox(box, imgSize):
    left = box[0]
    top = box[1]
    w = box[2]
    h = box[3]
    right = left+w
    bottom = top+h

    if left>=imgSize[1] or top>=imgSize[0] or right<=0 or bottom<=0 or w<=0 or h<=0:
        return False
    return True

'''
#=====Header and body example:=======
<?xml version="1.0" ?>
<annotation>
    <folder>images/0--Parade</folder>
    <filename>0_Parade_marchingband_1_12.jpg</filename>
    <source>
        <database>My Database</database>
        <annotation>WiderFace</annotation>
        <image>flickr</image>
        <flickrid>NULL</flickrid>
    </source>
    <owner>
        <flickrid>NULL</flickrid>
        <name>cuhk</name>
    </owner>
    <size>
        <width>1024</width>
        <height>768</height>
        <depth>3</depth>
    </size>
    <segmented>0</segmented>
    <object>
    {{}}
    </object>
</annotation>
'''
def create(pictureName, annotationsInMatrix, xmlName, listName):
    # inputs: picture file name, annotations matrix, where to save xml file, where to save picture annotation pair txt list 
    print pictureName
    img = cv2.imread(pictureName)
    imgSize = img.shape

    boxes, labels = anno_wider2voc(annotationsInMatrix)
    for objIndex, box in enumerate(boxes):
        if 0 == objIndex:
            # create header and structure
            folderString = pictureName.split('/')[-2]
            filenameString = pictureName.split('/')[-1]

            doc = Document()
            annotation = doc.createElement('annotation')
            doc.appendChild(annotation)
            
            folder = doc.createElement('folder')
            folder.appendChild(doc.createTextNode(folderString))
            annotation.appendChild(folder)
            
            filename = doc.createElement('filename')
            filename.appendChild(doc.createTextNode(filenameString))
            annotation.appendChild(filename)
            
            source = doc.createElement('source')                
            database = doc.createElement('database')
            database.appendChild(doc.createTextNode('WiderFace'))
            source.appendChild(database)
            source_annotation = doc.createElement('annotation')
            source_annotation.appendChild(doc.createTextNode('WiderFace'))
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

            if isValidBox(box, imgSize):
                annotation.appendChild(insertObject(doc, box, imgSize))
        else:
            if isValidBox(box, imgSize):
                annotation.appendChild(insertObject(doc, box, imgSize))

    try:
        f = open(xmlName, "w")
        f.write(doc.toprettyxml(indent = '    '))
        f.close()
        
        result = open(listName, 'a')
        # WIDER_val/images/8--Election_Campain/8_Election_Campain_Election_Campaign_8_498.jpg
        pic_path = '/'.join( pictureName.split('/')[-4:] )
        # Annotations_new/8_Election_Campain_Election_Campaign_8_498.xml
        xml_path = '/'.join( xmlName.split('/')[-2:] )
        result.write(pic_path + ' ' + xml_path + '\n')
        result.close()
    except:
        pass

def getAnnos(fidin, num):
    mat = []
    for i in range(num):
        line = fidin.readline().strip('\n')
        #print line, len(line), line.split(' ')[:-1]
        line = map(int, line.split(' ')[:-1])
        mat.append(list(line))
    return mat, fidin

if __name__ == '__main__':
    ## configurations
    setName = "val"
    xmlFolder = "xmls"
    # in
    img_list = '/home/smiles/hz/databases/WIDER-face/annotation_2017/wider_face_{}_bbx_gt.txt'.format(setName)
    picture_root = '/home/smiles/hz/databases/WIDER-face/WIDER_{}/images/'.format(setName)
    # out
    pl_Pair = '/home/smiles/hz/caffe-ssd/data/WIDER-face/{}.txt'.format(setName)
    xmlpath_new='/home/smiles/hz/databases/WIDER-face/{}/'.format(xmlFolder)

    f = open(pl_Pair, 'w')
    f.close()
    with open(img_list, 'r') as fidin: 
        line = fidin.readline().strip('\n')
        while line:
            pictureName = picture_root+line
            xmlName = xmlpath_new+line.split('/')[-1].replace('.jpg','.xml')
            line = fidin.readline().strip('\n')
            num = int(line)
            mat, fidin = getAnnos(fidin, num)
            create(pictureName, mat, xmlName, pl_Pair)
            line = fidin.readline().strip('\n')
    fidin.close()

