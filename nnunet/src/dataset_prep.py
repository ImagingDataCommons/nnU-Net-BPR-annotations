"""
    ----------------------------------------
    nnUNet @ IDC
    
    STEP2 - dataset prep (task-dependent)
    ----------------------------------------
    
    ----------------------------------------
    Author: Dennis Bontempi
    Email:  dennis_bontempi@dfci.harvard.edu
    ----------------------------------------
    
"""

import os
import sys
sys.path.append('../..')

import tqdm
import time
import shutil
import argparse
import multiprocessing

import json
import yaml

import numpy as np
import pandas as pd
import SimpleITK as sitk

import pyplastimatch.pyplastimatch.pyplastimatch as pypla

## ----------------------------------------

"""
BLABLABLA

SCRIPT DESCRIPTION HERE ^

N.B. Follows the nnU-Net conventions!

"""


def main(config):
  
  # parse from the config dict
  preproc_path_nii = config["preproc_path_nii"]
  preproc_path_nrrd = config["preproc_path_nrrd"]
  model_input_path = config["model_input_path"]

  if not os.path.exists(model_input_path):
    os.makedirs(model_input_path)
  
  exported_pat_nii = sorted([d for d in os.listdir(preproc_path_nii) if os.path.isdir(os.path.join(preproc_path_nii, d))])
  exported_pat_nrrd = sorted([d for d in os.listdir(preproc_path_nrrd) if os.path.isdir(os.path.join(preproc_path_nrrd, d))])
    
  # for every patient exported for which the CT NIfTI file exists
  for idx, pat in enumerate(exported_pat_nrrd):
    
    print("Processing patient %d/%d (%s)..."%(idx + 1, len(exported_pat_nrrd), pat), end = "\r")
    
    pat_base_dir_path = os.path.join(preproc_path_nii, pat)
    pat_nii_path = os.path.join(pat_base_dir_path, pat + "_ct.nii.gz")
  
    copy_path = os.path.join(model_input_path, pat + "_0000.nii.gz")
    
    # copy NIfTI to the right dir for nnU-Net processing
    if not os.path.exists(copy_path):
      shutil.copy(src = pat_nii_path, dst = copy_path)
      
  print("Processing patient %d/%d (%s)... Done."%(idx + 1, len(exported_pat_nrrd), pat))
                
## ----------------------------------------
## ----------------------------------------
      
if __name__ == '__main__':

  base_conf_file_path = '.'
  
  parser = argparse.ArgumentParser(description = 'nnU-Net @ IDC - prepare dataset for inference.')

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
  model_input_path = yaml_conf["data"]["model_input_path"]
  
  # name of the dataset, will set the name for all the created subfolders
  # expected to be found as a prefix to all the files needed for the pre-processing
  dataset_name = yaml_conf["dataset"]["name"]
  
  preproc_path_nii = os.path.join(preproc_base_path, dataset_name, 'nii')
  preproc_path_nrrd = os.path.join(preproc_base_path, dataset_name, 'nrrd')
  
  ## ----------------------------------------
  
  # dictionary to be passed to the main function
  config = dict()
  
  config["preproc_path_nii"] = preproc_path_nii
  config["preproc_path_nrrd"] = preproc_path_nrrd
  config["model_input_path"] = model_input_path
  
  # TODO: dump this as a log somewhere in the data folder

  # TODO: implement config parameters overwrite from command line
  
  # TODO: implement a class to parse the config file + custom command line params
  
  main(config)