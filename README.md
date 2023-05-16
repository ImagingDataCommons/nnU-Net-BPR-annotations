# README

This repository contains the Google Colaboratory notebooks and metadata required for the (in progress) Nature Scientific Data manuscript, which references the Zenodo record "AI-derived annotations for the NLST and NSCLC-Radiomics computed tomography imaging collections" [here](https://zenodo.org/record/7822904#.ZGP7jXbMKUk). We use two publicly available pre-trained AI models for CT volumes (nnUNet and BodyPartRegression) to run inference on a subset of the NLST collection and the NSCLC-Radiomics collection. We use the IDC platform and leverage Google Cloud components such as BigQuery, Cloud Storage, Compute Engine, and Google Healthcare API to demonstrate the ability to create reproducible workflows and analysis. We create standardized DICOM Segmentation objects to hold thoracic organ segmentations for the two collections, and additionally extract shape radiomics features from the segments and save as DICOM Structured Reports (SR). For the BodyPartRegression analysis we create a landmarks SR to hold the transverse location of organs and bones, and a regions SR to hold the body part regions assigned to each transverse slice (head, neck, chest, abdomen, pelvis, legs). 

The [nnunet](https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/tree/main/nnunet), [bpr](https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/tree/main/bpr) and [common](https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/tree/main/common/queries) directories hold the code and metadata for creating the DICOM Segmentation and SR objects. 

The [usage_notebooks](https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/tree/main/usage_notebooks) directory contains materials to demonstrate how to interact with the data, downloading of data from IDC, conversion of DICOM to alternate medical imaging formats, and visualization using open source programs. 

Click on [this link](https://nbviewer.org/github/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/scientific_data_paper_usage_notes.ipynb) to open the usage notebook interactively with nbviewer. This will allow you to click on points in the bokeh plot and open the corresponding OHIF viewer urls. 

Alternatively, click on these links to interact with the bokeh plots that are included in the Scientific Data manuscript:

[Figure 5](https://htmlpreview.github.io/?https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_5.html) - Evaluation of the heart sphericity radiomics features from the AI-generated annotations compared to the expert from NSCLC-Radiomics.


