# annotationTools

[AIDA](https://github.com/alanaberdeen/AIDA) is an annotation tool which we have used to achieve ground truth for semantic segmentation. This repo is made to help us convert the acquired json files to their corresponding mask images. 


[1] Convertion of ``bounding boxes for detection`` of AIDA (Json) to txt file (yolo format but unnormalized)

    use json2yolo.py

[2] Convertion of ``semantic segmentation`` of AIDA (Json) to maskImage (# of masked images = # of class labels)

    use json2maskImage.py

[3] Convertion of bounding boxes to csv file

    use yolo2csv.py
    
[4] Evaluation (DICE and Jaccard)

    see evaluation/ 



  `` Note: we are still testing github-repo for semantic segmentation so the code can be messy``
