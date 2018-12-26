#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 17:25:52 2018

@author: ead2019
"""
''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

converts via annotator () to corresponding label images

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
#def rectangle(r0, c0, width, height):
def rectangle(height, width, c0, r0 ):
    rr, cc = [r0, r0 + width, r0 + width, r0], [c0, c0, c0 + height, c0 + height]
#    rr, cc = [r0, abs(r0 + width), abs(r0 + width), r0], [c0, c0, abs(c0 + height), abs(c0 + height)]
    return skimage.draw.polygon(rr, cc)

# explicit mention of file for testing
via_annotationFile = 'sampleJson/via_EAD_Challenge2019_Semantic_v3_MALI_v10.json'
via_annotationFile = 'sampleJson/via_EAD_Challenge2019_Semantic_v3_MALI_v15.json'

    
# todo: change to the class def
import json

annotations = json.load(open(via_annotationFile))
annotations_noDictKey = list(annotations.values())
#print(annotations_noDictKey)

# skip unannotated images
#annotations_annotated = [i for i in annotations_noDictKey if i['regions']]

'''
val_layer1 = annotations_noDictKey[1]
val_layer1['0000555.jpg86948']
val_layer1['0000555.jpg86948']['regions']

'''
import numpy as np
category = []
bbox = []
segment=[]
fileList=[]
result_tuple_from_segment=[]
    
with open(via_annotationFile) as json_data:
    data = json.load(json_data)
    for p in data["_via_img_metadata"].values():
        print(p)
        if len(p['regions'])!=0:
            fileList.append(p['filename'])
            segment.append(p['regions'])
            
            
            
# from segment find the dicts of polygon or other options
shapeFormat=[]
classCategory = []
segx = []
segy = []
rect = []
circ=[]
#len(segment)

for i in range (0, len(segment)):
    seg = segment[i]
    
    shapeFormat_1=[]
    classCategory_1 = []
    segx_1 = []
    segy_1 = []
    rect_1 = []
    circ_1=[]
    
    for k in range (0, len(seg)):
        seg_1 = seg[k]
        seg2 = seg_1['region_attributes']
        seg1 = seg_1['shape_attributes']  
        # for class identification
        seg1_category = seg2['EAD-Challenge2019']
        boolean = []
        if len(seg1_category) == 5:
            categoryList = ['Instrument', 'Specularity', 'Artefact' , 'Bubbles', 'Saturation']
        else:
            categoryList = ['Instrument', 'Artefact' , 'Bubbles', 'Saturation']
            
        listBoolCat = list(seg1_category.values())
        #classCategory_1.append(categoryList[int(np.where(listBoolCat)[0])])
        x = {k:v for k,v in enumerate(listBoolCat) if v == True}
        classCategory_1.append(list(x))
       
        # for shape identification
        shapesArray=['polygon', 'polyline', 'circle', 'rect']
        seg2_shape = seg1['name']  
        
        # loop here for all shapes included in each image [0], [1] e.g. 00216.jpg.  00219.jpg
        
        if seg2_shape == shapesArray[1]:
            print('polyline exists') 
            shapeFormat_1.append(seg2_shape)
            segx_1.append(seg1['all_points_x'])
            segy_1.append(seg1['all_points_y'])
            
        elif seg2_shape == shapesArray[0]:
            print('polygon exists')
            shapeFormat_1.append(seg2_shape)
            segx_1.append(seg1['all_points_x'])
            segy_1.append(seg1['all_points_y'])
            
        elif seg2_shape == shapesArray[2]:
            circleRegion=[]
            print('circle exists')
            shapeFormat_1.append(seg2_shape)
            circleRegion.append(int(seg1['cx']))
            circleRegion.append(int(seg1['cy']))
            circleRegion.append(int(seg1['r']))
            circ_1.append(circleRegion)
            
        elif seg2_shape == shapesArray[3]:
            print('rectangle exists')
            rectangleCoordinates=[]
            shapeFormat_1.append(seg2_shape)
            rectangleCoordinates.append(int(seg1['height']))
            rectangleCoordinates.append(int(seg1['width']))
            rectangleCoordinates.append(int(seg1['x']))
            rectangleCoordinates.append(int(seg1['y']))
            
            rect_1.append(rectangleCoordinates)
            
        else:
            print('unidentified')
            
        
   
    shapeFormat.append(shapeFormat_1)
    classCategory.append(classCategory_1)
    segx.append(segx_1)
    segy.append(segy_1)
    rect.append(rect_1)
    circ.append(circ_1)
 
    
classCategory = list(filter(None, classCategory))
shapeFormat = list(filter(None, shapeFormat))

#create your masks
import skimage.io
import skimage.draw
import os
from tifffile import imsave
from miscClasses import clearArray


dataset_dir= '../../via/semanticSegmentation_EAD2019/'
categoryList = ['Instrument', 'Specularity', 'Artefact' , 'Bubbles', 'Saturation']
unique_entries = set(categoryList)

for ll in range (0, len(fileList)):
    print(ll)
    
    image_path = os.path.join(dataset_dir, fileList[ll])
    image = skimage.io.imread(image_path)
    height, width = image.shape[:2]
    
    # get unique classes
    indices = { value : [ i for i, v in enumerate(classCategory) if v == value ] for value in unique_entries }
    
    mask = np.zeros([height, width, len(categoryList)], dtype=np.uint8)
    
    cnt = 0
    cnt_p=0
    cnt_r = 0
    
    for i in range (0, len(shapeFormat[ll])):
        
        if shapeFormat[ll][i]== 'polyline':
            print('we are dealing with polyline')
#            segy[ll][i].append(segy[ll][i][0])
#            segx[ll][i].append(segx[ll][i][0])
#
            rr, cc = skimage.draw.polygon(segy[ll][cnt_p], segx[ll][cnt_p])

            rr = np.clip(rr, 0, height-1)
            cc = np.clip(cc, 0, width-1) 
#                                
#            rr, cc= clearArray (rr, cc,width , 'width')
#            rr, cc= clearArray (rr, cc, height, 'height')
            cnt_p = cnt_p + 1
    
        elif shapeFormat[ll][i]== 'polygon':
            print('we are dealing polygon')
            
            rr, cc = skimage.draw.polygon(segy[ll][cnt_p], segx[ll][cnt_p])
            rr = np.clip(rr, 0, height-1)
            cc = np.clip(cc, 0, width-1)              
#            rr, cc= clearArray (rr, cc,width , 'width')
#            rr, cc= clearArray (rr, cc, height, 'height')
            
            cnt_p = cnt_p + 1
            
            
    
        elif shapeFormat[ll][i]== 'circle':
            print('we are dealing with circle')
            rr, cc = skimage.draw.circle(circ[ll][cnt][1], circ[ll][cnt][0], circ[ll][cnt][2])
            
            rr = np.clip(rr, 0, height-1)
            cc = np.clip(cc, 0, width-1) 
            
            rr = np.clip(rr, 0, height-1)
            cc = np.clip(cc, 0, width-1) 
            cnt = cnt +1
            
        elif shapeFormat[ll][i]== 'rect':
            import time
            rr, cc = rectangle(rect[ll][cnt_r][1], rect[ll][cnt_r][0], rect[ll][cnt_r][2],rect[ll][cnt_r][3] )
            rr = np.clip(rr, 0, height-1)
            cc = np.clip(cc, 0, width-1)     
            rr = np.clip(rr, 0, height-1)
            cc = np.clip(cc, 0, width-1) 
            print('we are dealing with rectangle')
            time.sleep(0.55)
            cnt_r = cnt_r+1
            
            
#        mask[rr,cc, categoryList.index(classCategory[ll][i])] = 255
        if (classCategory[ll][i]) == []:
            print('empty')
        else:
            mask[rr,cc, int(classCategory[ll][i][0])] = 255
    
    im_mask = mask.transpose([2,0,1])    

    saveImageFile=fileList[ll].split('.')[0]
    imsave(saveImageFile+'_mask.tif', im_mask)



# Convert polygons to a bitmap mask of shape
# [height, width, instance_count]
#mask = np.zeros([height, width, len(shapeFormat[0])], dtype=np.uint8)
#
#cnt = 0
#for i in range (0, len(shapeFormat[0])):
#    if shapeFormat[0][i]== 'polyline' or shapeFormat[0][i]== 'polygon':
#        print('we are dealing with polyline or polygon')
#        rr, cc = skimage.draw.polygon(segy[0][i], segx[0][i])
#    elif shapeFormat[0][i]== 'circle':
#        print('we are dealing with circle')
#        rr, cc = skimage.draw.circle(circ[0][cnt][1], circ[0][cnt][0], circ[0][cnt][2])
#        cnt = cnt + 1
#        
#    mask[rr,cc, i] = 255
#
#im_mask = mask.transpose([2,0,1])    
#from tifffile import imsave
#imsave('mask_xx.tif', im_mask)


#for i, p in enumerate(info["polygons"]):
#    # Get indexes of pixels inside the polygon and set them to 1
#    rr, cc = skimage.draw.polygon(p['all_points_y'], p['all_points_x'])
#    mask[rr, cc, i] = 1

    
