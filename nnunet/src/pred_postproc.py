"""
    ----------------------------------------
    nnUNet @ IDC
    
    STEP4 - segmasks post-proc (task-dependent)
    ----------------------------------------
    
    ----------------------------------------
    Author: Dennis Bontempi
    Email:  dennis_bontempi@dfci.harvard.edu
    ----------------------------------------
    
"""

import os
import sys
sys.path.append('..')
sys.path.append('../..')

import tqdm
import time
import shutil
import argparse

import json
import yaml

import numpy as np
import pandas as pd
import nibabel as nib
import SimpleITK as sitk

import pyplastimatch.pyplastimatch.pyplastimatch as pypla
import utils.data_utils as utils

## ----------------------------------------

"""
BLABLABLA

SCRIPT DESCRIPTION HERE ^

N.B. Follows the nnU-Net conventions!

"""


def main(config):
  
  # parse from the config dict
  output_path_nii = config["output_path_nii"]
  preproc_path_nrrd = config["preproc_path_nrrd"]
  structures_to_export = config["structures_to_export"]

  
  # list of all the patients for which a non-corrupt prediction was outputted from the inference phase
  pred_pat_nii = [f for f in sorted(os.listdir(output_path_nii)) if ".nii.gz" in f]
  
  for idx, pred_nii_file in enumerate(pred_pat_nii):
    
    pred_nii_path = os.path.join(output_path_nii, pred_nii_file)
    pat = pred_nii_file.split(".nii.gz")[0]

    print("\nProcessing patient %d/%d (%s)"%(idx + 1, len(pred_pat_nii), pat))
    
    ct_nrrd_path = os.path.join(preproc_path_nrrd, pat, pat + "_ct.nrrd")
    sitk_ct = sitk.ReadImage(ct_nrrd_path)
    
    nrrd_spacing = sitk_ct.GetSpacing()
    nrrd_dim = sitk_ct.GetSize()
    
    nii_spacing = tuple(nib.load(pred_nii_path).header['pixdim'][1:4])
    nii_dim = tuple(nib.load(pred_nii_path).get_fdata().shape)
    
    ## ----------------------------------------
    # NIfTI TO NRRD CONVERSION
    
    # path to the output NRRD file (inferred segmasks)
    pred_nrrd_path = os.path.join(preproc_path_nrrd, pat, pat + "_pred_segthor.nrrd")
    log_file_path = os.path.join(preproc_path_nrrd, pat, pat + "_pypla.log")
    
    # Inferred NIfTI segmask to NRRD
    convert_args_pred = {"input" : pred_nii_path, 
                         "output-img" : pred_nrrd_path}

    pypla.convert(path_to_log_file = log_file_path, **convert_args_pred)

    
    # FIXME: not sure I want the check to be this way 
    if not ((nrrd_spacing == nii_spacing) & (nrrd_dim == nii_dim)):
    
      print("SPACING OR DIM IS DIFFERENT (NRRD vs pred NIfTI)")
        
        
      ## ----------------------------------------
      # RESAMPLING (back to the original spacing if needed - in this case it should be never)

      # plastimatch arguments should be passed as string
      nrrd_spacing_str = "%s %s %s"%(nrrd_spacing[0], nrrd_spacing[1], nrrd_spacing[2])    
      nrrd_dim_str = "%s %s %s"%(nrrd_dim[0], nrrd_dim[1], nrrd_dim[2])

      resample_args_pred = {"input" : pred_nrrd_path_tmp, 
                            "output" : pred_nrrd_path,
                            "spacing" : nrrd_spacing_str,
                            "dim" : nrrd_dim_str,
                            "interpolation" : "nn"}

      pypla.resample(path_to_log_file = log_file_path, **resample_args_pred)
        
    
    # separate the inferred and resampled NRRD into several files
    # one for each segmented structure, as for the Plastimatch output
    # (and to make post-processing and evaluation with Plastimatch - on binary masks - easier)
    
    # load the NRRD segmask created by the steps above
    sitk_pred = sitk.ReadImage(pred_nrrd_path)
    pred_nrrd = sitk.GetArrayFromImage(sitk_pred)
    pred_nrrd_esophagus, pred_nrrd_heart, pred_nrrd_trachea, pred_nrrd_aorta = utils.split_segmask_segthor(pred_nrrd)
    
    pred_segmasks_folder = os.path.join(preproc_path_nrrd, pat, "pred_segmasks")
    if not os.path.exists(pred_segmasks_folder): os.makedirs(pred_segmasks_folder)
        
    ## keep this explicit for now to make changes and inter-use-cases adaptation easier
    for structure in structures_to_export:
        
      out_path = os.path.join(pred_segmasks_folder, structure + ".nrrd")
      var_name = "pred_nrrd_%s"%(structure.lower())

      #if os.path.exists(out_path): continue
            
      print("Exporting binary mask for %s..."%(structure.lower()), end = "")
      utils.save_binary_segmask(path_to_header_file = pred_nrrd_path,
                                path_to_output = out_path,
                                pred_binary_segmask = eval(var_name))
      print("Done.")
  
  
                
## ----------------------------------------
## ----------------------------------------
      
if __name__ == '__main__':

  base_conf_file_path = '.'
  
  parser = argparse.ArgumentParser(description = 'nnU-Net @ IDC - inferred masks.')

  parser.add_argument('--conf',
                      required = False,
                      help = 'Specify the path to the YAML configuration file containing the run details.',
                      default = "config.yaml"
                     )

  args = parser.parse_args()

  conf_file_path = os.path.join(base_conf_file_path, args.conf)

  with open(conf_file_path) as f:
    yaml_conf = yaml.load(f, Loader = yaml.FullLoader)

  # preproc data directory
  preproc_base_path = yaml_conf["data"]["preproc_base_path"]
  
  # final directory where the dataset should be stored to allow for nnU-Net processing
  output_path_nii = yaml_conf["data"]["output_path_nii"]
  
  # name of the dataset, will set the name for all the created subfolders
  # expected to be found as a prefix to all the files needed for the pre-processing
  dataset_name = yaml_conf["dataset"]["name"]
  
  # names of the structures to export for each patient under the pred_segmasks folder
  # for the SegThor model, the structures available are (ordered based on label):
  # - Esophagus (SegThor label: 1)
  # - Heart (SegThor label: 2)
  # - Trachea (SegThor label: 3)
  # - Aorta (SegThor label: 4)
  structures_to_export = yaml_conf["post"]["structures_to_export"]

  preproc_path_nrrd = os.path.join(preproc_base_path, dataset_name, 'nrrd')
  
  ## ----------------------------------------
  
  # dictionary to be passed to the main function
  config = dict()
  

  config["preproc_path_nrrd"] = preproc_path_nrrd
  config["output_path_nii"] = output_path_nii
  config["structures_to_export"] = structures_to_export
  
  # TODO: dump this as a log somewhere in the data folder

  # TODO: implement config parameters overwrite from command line
  
  # TODO: implement a class to parse the config file + custom command line params
  
  main(config)