# README

This repository contains the Google Colaboratory notebooks and metadata required for the Nature Scientific Data manuscript. This references the Zenodo record "AI-derived annotations for the NLST and NSCLC-Radiomics computed tomography imaging collections" [here](https://zenodo.org/record/7822904#.ZGP7jXbMKUk). 
- We use two publicly available pre-trained AI models for CT volumes (nnUNet and BodyPartRegression) to run inference on a subset of the NLST collection and the NSCLC-Radiomics collection. 
- We use the IDC platform and leverage Google Cloud components such as BigQuery, Cloud Storage, Compute Engine, and Google Healthcare API to demonstrate the ability to create reproducible workflows and analysis. 
- We create standardized DICOM Segmentation objects to hold thoracic organ segmentations for the two collections, and additionally extract shape radiomics features from the segments and save as DICOM Structured Reports (SR). For the BodyPartRegression analysis we create a landmarks SR to hold the transverse location of organs and bones, and a regions SR to hold the body part regions assigned to each transverse slice (head, neck, chest, abdomen, pelvis, legs). 
- These objects were uploaded to Zenodo where they were then ingested into v14 release of IDC!

Directory structure: 
- The [nnunet](https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/tree/main/nnunet), [bpr](https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/tree/main/bpr) and [common](https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/tree/main/common/queries) directories hold the code and metadata for creating the DICOM Segmentation and SR objects. 
- The [usage_notebooks](https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/tree/main/usage_notebooks) directory contains materials to demonstrate how to interact with the data, downloading of data from IDC, conversion of DICOM to alternate medical imaging formats, and visualization using open source programs. 

To interact with the enhanced metadata, one option is to click on [this link](https://nbviewer.org/github/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/scientific_data_paper_usage_notes.ipynb) to open the usage notebook interactively with nbviewer. This will allow you to click on points in the bokeh plot and open the corresponding OHIF viewer urls. 

Or, click on the plots below to interact with them! Here's an example of how to interact: 

![](https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_demo.gif)

Figure 4 - Evaluation of the AI-generated annotations with respect to the expert annotations of the heart for NSCLC-Radiomics. 
[![](https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure4.JPG)](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_4_dice_heart.html)

We also provide the other Dice, Hausdorff distance and Hausdorff 95 metrics for the heart and the esophagus at these links: 
- [Dice score of the heart](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_4_dice_heart.html)
- [Hausdorff distance of the heart](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_4_hd_heart.html)
- [Hausdorff distance 95 of the heart](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_4_hd_95_heart.html)
- [Dice score of the esophagus](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_4_dice_esophagus.html)
- [Hausdorff distance of the esopahgus](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_4_hd_esophagus.html)
- [Hausdorff distance 95 of the esophagus](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_4_hd_95_esophagus.html)

Figure 5 - Evaluation of the heart sphericity radiomics features from the AI-generated annotations compared to the expert from NSCLC-Radiomics.

[![](https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure5.JPG)](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_5.html)

Figure 6 - Evaluation of the sphericity radiomics features from the AI-generated annotations from NLST. 

[![](https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure6.JPG)](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_6.html)

Figure 7 - Difference between the expert lung segmentation and the BPR derived lung_start and lung_end landmarks for NSCLC-Radiomics.  

[![](https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure7.JPG)](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_7.html)

Figure 8 - Evaluation of the distribution of distances between the start and end of the lungs in mm for the NLST collection. 

[![](https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure8.JPG)](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_8.html)

Figure 9 - Evaluation of the AI-generated annotations with respect to the expert annotations of the heart for NSCLC-Radiomics. 

[![](https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure9.JPG)](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_9.html)


<!---
- Alternatively, click on these links to interact with the bokeh plots that are included in the Scientific Data manuscript:
  - [Figure 4](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_4_dice_heart.html) - Evaluation of the AI-generated annotations with respect to the expert annotations of the heart for NSCLC-Radiomics. 
  - We also provide the other Dice, Hausdorff distance and Hausdorff 95 metrics for the heart and the esophagus: 
    - [Dice score of the heart](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_4_dice_heart.html)
    - [Hausdorff distance of the heart](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_4_hd_heart.html)
    - [Hausdorff distance 95 of the heart](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_4_hd_95_heart.html)
    - [Dice score of the esophagus](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_4_dice_esophagus.html)
    - [Hausdorff distance of the esopahgus](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_4_hd_esophagus.html)
    - [Hausdorff distance 95 of the esophagus](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_4_hd_95_esophagus.html)
  - [Figure 5](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_5.html) - Evaluation of the heart sphericity radiomics features from the AI-generated annotations compared to the expert from NSCLC-Radiomics.
  - [Figure 6](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_6.html) - Evaluation of the sphericity radiomics features from the AI-generated annotations from NLST. 
  - [Figure 7](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_7.html) - Difference between the expert lung segmentation and the BPR derived lung_start and lung_end landmarks for NSCLC-Radiomics. 
  - [Figure 8](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_8.html) - Evaluation of the distribution of distances between the start and end of the lungs in mm for the NLST collection. 
  - [Figure 9](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_9.html) - Evaluation of the percentage of slices assigned to each region (head, neck, chest, abdomen, pelvis and legs) for the NLST collection.
-->
