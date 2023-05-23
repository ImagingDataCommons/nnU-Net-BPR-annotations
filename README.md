# Background

This repository contains the Google Colaboratory notebooks and other related materials accompanying the following dataset, which was generated as part of the effort to enrich the public data available within [NCI Imaging Data Commons (IDC)](https://imaging.datacommons.cancer.gov/):

> Krishnaswamy, D., Bontempi, D., Clunie, D., Aerts, H. & Fedorov, A. AI-derived annotations for the NLST and NSCLC-Radiomics computed tomography imaging collections. (2022). doi:[10.5281/zenodo.7473971](https://zenodo.org/record/7822904)

To generate this dataset, we use publicly available pre-trained AI tools to enhance CT lung cancer collections that are unlabeled or partially labeled. The first tool is the [nnU-Net v1 deep learning framework](https://github.com/MIC-DKFZ/nnUNet/tree/nnunetv1) for volumetric segmentation of organs, where we use a pretrained model (Task D18 using the SegTHOR dataset) for labeling volumetric regions in the image corresponding to the heart, trachea, aorta and esophagus. These are the major organs-at-risk for radiation therapy for lung cancer. We further enhance these annotations by computing 3D shape radiomics features using [pyradiomics](https://github.com/AIM-Harvard/pyradiomics). The second tool is [BodyPartRegression](https://github.com/MIC-DKFZ/BodyPartRegression) - a pretrained model for per-slice automatic labeling of anatomic landmarks and imaged body part regions in axial CT volumes. 

We focus on enhancing two publicly available collections, the Non-small Cell Lung Cancer Radiomics (NSCLC-Radiomics collection) (avaialble in [TCIA](https://wiki.cancerimagingarchive.net/display/Public/NSCLC-Radiomics) and [IDC](https://portal.imaging.datacommons.cancer.gov/explore/filters/?collection_id=Community&collection_id=nsclc_radiomics)), and the National Lung Screening Trial (NLST collection) (available in [TCIA](https://wiki.cancerimagingarchive.net/display/NLST/National+Lung+Screening+Trial) and [IDC](https://portal.imaging.datacommons.cancer.gov/explore/filters/?collection_id=Community&collection_id=nlst)). Importantly, the NSLSC-Radiomics collection includes expert-generated manual annotations of several chest organs, allowing us to quantify performance of the AI tools in that subset of data.

# Purpose of this repository

While the files corresponding to this dataset can be downloaded from the Zenodo record listed above, it is a lot more convenient to explore the dataset using NCI Imaging Data Commons, where it was included since data release v13, see [https://portal.imaging.datacommons.cancer.gov/explore/filters/?analysis_results_id=nnU-Net-BPR-annotations](https://portal.imaging.datacommons.cancer.gov/explore/filters/?analysis_results_id=nnU-Net-BPR-annotations). 

Code organization: 

- The [nnunet](https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/tree/main/nnunet), [bpr](https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/tree/main/bpr) and [common](https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/tree/main/common/queries) directories hold the code and metadata for creating the DICOM Segmentation and SR objects. 
- The [usage_notebooks](https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/tree/main/usage_notebooks) directory contains materials to demonstrate how to interact with the data, downloading of data from IDC, conversion of DICOM to alternate medical imaging formats, and visualization using open source tools. 

To get started with the dataset, check out [this usage notebook](https://nbviewer.org/github/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/scientific_data_paper_usage_notes.ipynb). This will allow you to explore the dataset by clicking on points in the bokeh plot and open the corresponding images using viewer links embedded in the plot. 

You can also use the pre-generated interactive bokeh plots referenced below. Each of the figures you see below is linked with its interactive version, as demonstrated in the video below.

![](https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/blob/main/usage_notebooks/bokeh_figures/figure_demo.gif)

**Click the figures below to interact with them!**

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

# Support

For any questions related to this dataset, please [open an issue in this repository\(https://github.com/ImagingDataCommons/nnU-Net-BPR-annotations/issues/new), or post your question in the [IDC forum](https://discourse.canceridc.dev/).
