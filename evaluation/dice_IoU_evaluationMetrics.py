#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 22:57:04 2018

@author: shariba
"""
import numpy as np

def file_lines_to_list(path):
  # open txt file lines to a list
  with open(path) as f:
    content = f.readlines()
  # remove whitespace characters like `\n` at the end of each line
  content = [x.strip() for x in content]
  return content

def calculate_confusion_matrix_from_arrays(prediction, ground_truth, nr_labels):
    replace_indices = np.vstack((ground_truth.flatten(),prediction.flatten())).T
    confusion_matrix, _ = np.histogramdd(replace_indices, bins=(nr_labels, nr_labels),range=[(0, nr_labels), (0, nr_labels)])
    confusion_matrix = confusion_matrix.astype(np.uint32)
    return confusion_matrix


def calculate_iou(confusion_matrix):
    ious = []
    for index in range(confusion_matrix.shape[0]):
        true_positives = confusion_matrix[index, index]
        false_positives = confusion_matrix[:, index].sum() - true_positives
        false_negatives = confusion_matrix[index, :].sum() - true_positives
        denom = true_positives + false_positives + false_negatives
        if denom == 0:
            iou = 0
        else:
            iou = float(true_positives) / denom
        ious.append(iou)
    return ious

def calculate_dice(confusion_matrix):
    dices = []
    for index in range(confusion_matrix.shape[0]):
        true_positives = confusion_matrix[index, index]
        false_positives = confusion_matrix[:, index].sum() - true_positives
        false_negatives = confusion_matrix[index, :].sum() - true_positives
        denom = 2 * true_positives + false_positives + false_negatives
        if denom == 0:
            dice = 0
        else:
            dice = 2 * float(true_positives) / denom
        dices.append(dice)
    return dices



def jaccard(y_true, y_pred):
    intersection = (y_true * y_pred).sum()
    union = y_true.sum() + y_pred.sum() - intersection
    return (intersection + 1e-15) / (union + 1e-15)


def dice(y_true, y_pred):
    return (2 * (y_true * y_pred).sum() + 1e-15) / (y_true.sum() + y_pred.sum() + 1e-15)


if __name__ == '__main__':
    
    import cv2
    
    result_dice = []
    result_jaccard = []
    
    classTypes = ['Specularity', 'Saturation', 'Artefact', 'Blur', 'Contrast', 'Bubbles', 'Instrument']
    #classTypes = ['specularity', 'saturation', 'artefact', 'blur', 'contrast', 'bubbles', 'instrument']
    
#    testing only
    file_name_GT='../masks/Frame_00002233_mask_Artefact.png'
    file_name_predicted='../masks/Frame_00002233_mask_artefact_predicted.png'
    
    
    y_true = (cv2.imread(str(file_name_GT), 0) > 0).astype(np.uint8)
 
#    pred_image = (cv2.imread(str(pred_file_name), 0) > 255 * 0.5).astype(np.uint8)
    pred_image = (cv2.imread(str(file_name_predicted), 0) >0).astype(np.uint8)
    y_pred=pred_image.flatten()
    result_dice = [dice(y_true.flatten(), y_pred)]
    print(result_dice)
    
    result_jaccard = [jaccard(y_true.flatten(), y_pred)]
    print(result_jaccard)
    
#   result_dice += [dice(y_true, y_pred)]
    
    testing=1
    if testing:
        frameName = 'Frame_00002233'
        import tifffile as tiff
#        GT masks
        file_name_GT_txt ='../masks/'+frameName+'_GT_mask.txt'
        file_name_GT_maskImage ='../masks/'+frameName+'_GT_mask.tiff'
        
        y_true_Array = tiff.imread(file_name_GT_maskImage)
        
#        =============>>>>>>>>>>>>>>>>>predicted maskes (change me!!!)
#        file_name_eval_txt ='../masks/'+frameName+'_eval_mask.txt'
#        file_name_eval_maskImage ='../masks/'+frameName+'_eval_mask.tiff'
        file_name_eval_txt=file_name_GT_txt
        file_name_eval_maskImage=file_name_GT_maskImage
        
#        read txt files as array
        textfile_GT = file_lines_to_list(file_name_GT_txt)
        textfile_eval = file_lines_to_list(file_name_eval_txt)
        
        y_pred_Array = tiff.imread(file_name_eval_maskImage)
        
        dice_val =[]
        jaccard_val=[]
        for i in range(len(textfile_GT)):
            for j in range (len(textfile_eval)):
                compare_class = [textfile_GT[i] == textfile_eval[j]]
                if str(compare_class[0])=='True':
#                    print([textfile_GT[i] == textfile_eval[j]])
                    y_true = (((y_true_Array[i, :, :])> 0).astype(np.uint8))
                    y_pred = (((y_true_Array[j, :, :])> 0).astype(np.uint8))
                    result_dice = [dice(y_true.flatten(), y_pred.flatten())]
                    result_jaccard = [jaccard(y_true.flatten(), y_pred.flatten())]
                    
                    dice_val.append(result_dice)
                    jaccard_val.append(result_jaccard)

                    
        print('diceval {}'.format(dice_val))
#    get mean values
        meanDiceVal = np.mean(dice_val)  
        meanJaccard = np.mean(jaccard_val)  
        print('mean dice {} and mean jaccard {}'.format(meanDiceVal, meanJaccard))
    