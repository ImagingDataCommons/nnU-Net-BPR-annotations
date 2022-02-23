"""
    ----------------------------------------
    nnUNet @ IDC
    
    useful functions (data handling/proc)
    ----------------------------------------
    
    ----------------------------------------
    Author: Dennis Bontempi
    Email:  dennis_bontempi@dfci.harvard.edu
    ----------------------------------------
    
"""

import os
import json
import pydicom
import numpy as np
import SimpleITK as sitk


def split_segmask_segthor(pred_nrrd):
    
  """
  blablabla - TASK DEPENDENT
    
  Args:
    pred_nrrd
  """
    
  pred_nrrd_esophagus = np.copy(pred_nrrd)
  pred_nrrd_heart = np.copy(pred_nrrd)
  pred_nrrd_trachea = np.copy(pred_nrrd)
  pred_nrrd_aorta = np.copy(pred_nrrd)
    
  # zero every segmask other than the esophagus and make the mask binary (0/1)
  pred_nrrd_esophagus[pred_nrrd != 1] = 0
  pred_nrrd_esophagus[pred_nrrd_esophagus != 0] = 1
    
  # zero every segmask other than the heart and make the mask binary (0/1)
  pred_nrrd_heart[pred_nrrd != 2] = 0
  pred_nrrd_heart[pred_nrrd_heart != 0] = 1
    
  # zero every segmask other than the trachea and make the mask binary (0/1)
  pred_nrrd_trachea[pred_nrrd != 3] = 0
  pred_nrrd_trachea[pred_nrrd_trachea != 0] = 1
    
  # zero every segmask other than the aorta and make the mask binary (0/1)
  pred_nrrd_aorta[pred_nrrd != 4] = 0
  pred_nrrd_aorta[pred_nrrd_aorta != 0] = 1
    
  return pred_nrrd_esophagus, pred_nrrd_heart, pred_nrrd_trachea, pred_nrrd_aorta
  
## ----------------------------------------

def split_segmask_gtv(pred_nrrd):
    
  """
  blablabla - TASK DEPENDENT
    
  Args:
    pred_nrrd
  """
    
  # no action needed - the inferred GTV mask is already binary
  # keep the function in for now for consistency wrt the other use cases
    
  return pred_nrrd
  
## ----------------------------------------

def save_binary_segmask(path_to_header_file, path_to_output, pred_binary_segmask):
    
    """
    blabla (task-independent)
    
    Args:
        path_to_header_file: path to the NRRD file to be read with SITK in order to copy the 
                             header information from it (segmask resulting from the inference phase)
        path_to_output: location where to save the binary segmask
        pred_binary_segmask: binary segmask to save
    """
    
    sitk_copy_header = sitk.ReadImage(path_to_header_file)
    
    sitk_pred_binary = sitk.GetImageFromArray(pred_binary_segmask)
    sitk_pred_binary.CopyInformation(sitk_copy_header)
    sitk.WriteImage(sitk_pred_binary, path_to_output)
    
## ----------------------------------------

