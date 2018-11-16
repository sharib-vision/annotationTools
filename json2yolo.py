#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 22:02:14 2018

@author: shariba
"""

'''
if useparseing = 1

usage: python json2yolo.py -jsonFileName /Users/shariba/development/miscFunctions/jsonFiles/AIDA_annotation-adam_2233.json \
    -txtFileFolder /Users/shariba/development/miscFunctions/jsonFiles/

output: saves txtfile with class and bbox in yolo format and a json file

'''
def read_json_file(jsonFile):
    import json
    import objectpath
    category = []
    bbox = []
    with open(jsonFile) as json_data:
        data = json.load(json_data)
        print(data)
        for p in data["layers"]:
            if len(p['items'])!=0:
                category.append(p['name'])
                jsonnn_tree = objectpath.Tree(p['items'])
                result_tuple_from = tuple(jsonnn_tree.execute('$..from'))
                result_tuple_to = tuple(jsonnn_tree.execute('$..to'))
                #  convert to string from dict/ check how many corners are present
                xbottom=json.dumps(result_tuple_from)
                bottom = re.findall("\d+\.\d+", xbottom)
                if len(bottom)>2:
                    for k in range ((int)(len(bottom)/2)-1):
                        category.append(p['name'])
                bbox.append(result_tuple_from)
                bbox.append(result_tuple_to)

    return category, bbox

def read_json_file_admin(jsonFile):
    import json
    import objectpath
    category = []
    bbox = []
    with open(jsonFile) as json_data:
        data = json.load(json_data)
#        print(data)
        X=data["annotation"]
        imageName=data["images"]
        frameName=imageName[0].get('name')
#        all annotations are inside this layer
        for p in X["layers"]:
            if len(p['items'])!=0:
                category.append(p['name'])
                jsonnn_tree = objectpath.Tree(p['items'])
                result_tuple_from = tuple(jsonnn_tree.execute('$..from'))
                result_tuple_to = tuple(jsonnn_tree.execute('$..to'))
                #  convert to string from dict/ check how many corners are present
                xbottom=json.dumps(result_tuple_from)
                bottom = re.findall("\d+\.\d+", xbottom)
                if len(bottom)>2:
                    for k in range ((int)(len(bottom)/2)-1):
                        category.append(p['name'])
                bbox.append(result_tuple_from)
                bbox.append(result_tuple_to) 
    return category, bbox, frameName, data

useParsing=0
annotator=['adam', 'barbara']

if __name__=="__main__":

    import json
    import re
    import os
    import argparse
    from collections import Counter
#    import pandas as pd
    
    debug = 0

    artefactsList=[]
 
    file = ''
    
    if useParsing:
    
        parser = argparse.ArgumentParser()
        parser.add_argument('-jsonFileName', action='store', help='please include the full path of the folder with bounding boxes (.json)', type=str)
        parser.add_argument('-txtFileFolder', action='store', help='folder only (fullpath)', type=str)
        args = parser.parse_args()
    
        jsonFile=args.jsonFileName
        txtFolder = args.txtFileFolder
        
#        uncomment and use this if you are using the annotation from json file directly from the annotator source
#        category,  bbox = read_json_file(jsonFile)
        
#        use below if you are using the file downloaded from the admin (only save most recent json files--> convert to proper json format)
        category,  bbox, frameName, data = read_json_file_admin(jsonFile)
        
        file = txtFolder+frameName+annotator[0]+'.txt'
        jsonFileRenamed=txtFolder+frameName+'_'+annotator[0]+'.json'
        
        fileObj= open(jsonFileRenamed, "w")
        json.dump(data, fileObj)
        fileObj.close()
#        also save the json file with annotator name and corresponding file name
        
        
    else:
#        jsonFile='AIDA_annotation-2.json'//data can be deprecated
        jsonFile='annotation_test_admin.json'
        category,  bbox, frameName, data = read_json_file_admin(jsonFile)
        file = frameName+'_adam.txt'
        jsonFileRenamed=frameName+'_'+annotator[0]+'.json'
        fileObj= open(jsonFileRenamed, "w")
        json.dump(data, fileObj)
        fileObj.close()
    
    uvalue=Counter(category).values()
    uval=list(uvalue)
    
    
    
    if debug:
        print('length of unique lists',len(uval))
        print ('classes in category', (int)(len(category)/2))
        
    count = 0
    cnt=0
    for k in range (len(uval)):
        # top
        for l in range (uval[k]):
            artefactsList.append(category[count])
            x_top = bbox[cnt][l]
            xtop=json.dumps(x_top)
            top = re.findall("\d+\.\d+", xtop)
            artefactsList.append(top)
            # bottom
            x_bottom = bbox[cnt+1][l]
            xbottom=json.dumps(x_bottom)
            bottom = re.findall("\d+\.\d+", xbottom)
            artefactsList.append(bottom)
            count=count+1
       
     
        cnt = cnt+2   
    
    if debug:    
        print(artefactsList)
    
    """
    write bounding-box in text files TODO print bboxes on sample test image
    
    [1] Read image shape
    [2] Normalize to 1
    [3] Write to image_no.txt with [0...7][bbox]
    
    """
   
    try:
        os.remove(file)
    except OSError:
        pass
    
    textfile = open(file, 'a')
    cnt = 0
    
    for i in range (len(category)):
        if debug:
            print(artefactsList[cnt])
            print(artefactsList[cnt+1])
            print(artefactsList[cnt+2])
        
        textfile.write(artefactsList[cnt]+ ' '+ str(float(artefactsList[cnt+1][0]))+ ' '+str(float(artefactsList[cnt+1][1]))+' '+ str(float(artefactsList[cnt+2][0]))+ ' '+ str(float(artefactsList[cnt+2][1])))
        textfile.write('\n')
        cnt = cnt+3
    
    textfile.close()