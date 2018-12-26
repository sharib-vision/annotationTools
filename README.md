# annotationTools

[VIA](https://www.robots.ox.ac.uk/~vgg/software/via/via-2.0.1.html) is an annotation tool which we have used to achieve ground truth for semantic segmentation for EAD challenge. This repo is made to help us convert the acquired json files to their corresponding mask images. Only parts of code are useful for EAD2019 challege. Part of semantic has also been using AIDA toolset for annotation. We provide with corresponding json to mask file converters for both in this repo.


[1] Convertion of ``bounding boxes for detection`` of AIDA (Json) to txt file (yolo format but unnormalized)

    use json2yolo.py
    
[2] Convertion of ``semantic segmentation`` of VIA (Json) to maskImage (# of masked images = # of class labels)

    use json2maskImage_VIA.py

[3] Convertion of ``semantic segmentation`` of AIDA (Json) to maskImage (# of masked images = # of class labels)

    use json2maskImage.py

[4] Convertion of bounding boxes to csv file

    use yolo2csv.py
    
[5] Evaluation (DICE and Jaccard)

    see evaluation/ 



  `` Note: we are still testing github-repo for semantic segmentation so the code can be messy``
