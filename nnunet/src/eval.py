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
import utils.eval_utils as utils

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
  
  rt_segmasks_folder_name = config["rt_segmasks_folder_name"]
  pred_segmasks_folder_name = config["pred_segmasks_folder_name"]
  
  structures_to_eval = config["structures_to_eval"]
  
  res_base_path = config["res_base_path"]
  
  if not os.path.exists(res_base_path):
    os.makedirs(res_base_path)
    
  
  # list of all the patients for which a non-corrupt prediction was outputted from the inference phase
  pred_pat_nii = [f for f in sorted(os.listdir(output_path_nii)) if ".nii.gz" in f]
  
  dc_dict = dict()
  hd_dict = dict()

  
  for idx, pred_nii_file in enumerate(pred_pat_nii):
        
    pred_nii_path = os.path.join(output_path_nii, pred_nii_file)
    pat = os.path.basename(pred_nii_path).split(".nii.gz")[0]
    
    dc_dict[pat] = dict()
    hd_dict[pat] = dict()
    
    rt_segmasks_folder = os.path.join(preproc_path_nrrd, pat, rt_segmasks_folder_name)
    pred_segmasks_folder = os.path.join(preproc_path_nrrd, pat, pred_segmasks_folder_name)
    
    print("(%g/%g) processing patient %s"%(idx + 1, len(pred_pat_nii), pat))
 
    for jdx, structure in enumerate(structures_to_eval):
      
      print("Structure %g of %g (%s)"%(jdx + 1, len(structures_to_eval), structure))
      
      key = structure.lower()
      
      dc_dict[pat][key] = dict()
      hd_dict[pat][key] = dict()

      rt_nrrd_path_heart = os.path.join(rt_segmasks_folder, "%s.nrrd"%structure)
      pred_nrrd_path_heart = os.path.join(pred_segmasks_folder, "%s.nrrd"%structure)

      # Dice Coefficient
      try: 
          dc_summary_dict = pypla.dice(path_to_reference_img = rt_nrrd_path_heart,
                                       path_to_test_img = pred_nrrd_path_heart)

          dc_dict[pat][key] = dc_summary_dict

      except Exception as e:
          dc_dict[pat][key] = dict()
          print(e)

      # Hausdorff Distance
      try: 
          hd_summary_dict = pypla.hd(path_to_reference_img = rt_nrrd_path_heart,
                                     path_to_test_img = pred_nrrd_path_heart)

          hd_dict[pat][key] = hd_summary_dict

      except Exception as e:
          hd_dict[pat][key] = dict()
          print(e)
          

  res_dict_path_dc = os.path.join(res_base_path, "dc_dict.json")
  res_dict_path_hd = os.path.join(res_base_path, "hd_dict.json")
    
  with open(res_dict_path_dc, "w") as fp:
    json.dump(dc_dict, fp, indent = 2)
  
  with open(res_dict_path_hd, "w") as fp:
    json.dump(hd_dict, fp, indent = 2)
    
  
  # export CSVs as well - more human readable and easier to use for dataviz 
  for structure in structures_to_eval:
    
    key = structure.lower()
    
    dc_df = utils.dc_dict_to_df(dc_dict = dc_dict, structure_name = key)
    hd_df = utils.hd_dict_to_df(hd_dict = hd_dict, structure_name = key)

    dc_df_path = os.path.join(res_base_path, "dc_%s.csv"%key)
    hd_df_path = os.path.join(res_base_path, "hd_%s.csv"%key)

    dc_df.to_csv(dc_df_path)
    hd_df.to_csv(hd_df_path)
                    
## ----------------------------------------
## ----------------------------------------
      
if __name__ == '__main__':

  base_conf_file_path = '.'
  
  parser = argparse.ArgumentParser(description = 'nnU-Net @ IDC - quantitative evaluation exploiting Plastimatch.')

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
  rt_segmasks_folder_name = yaml_conf["data"]["rt_segmasks_folder_name"]
  pred_segmasks_folder_name = yaml_conf["data"]["pred_segmasks_folder_name"]
  
  # final directory where the dataset should be stored to allow for nnU-Net processing
  output_path_nii = yaml_conf["data"]["output_path_nii"]
  
  # name of the dataset, will set the name for all the created subfolders
  # expected to be found as a prefix to all the files needed for the pre-processing
  dataset_name = yaml_conf["dataset"]["name"]
  
  preproc_path_nrrd = os.path.join(preproc_base_path, dataset_name, 'nrrd')
  
  # names of the structures to eval for 
  # for the SegThor model on LUNG1, the structures with manual GT available are:
  # - Esophagus
  # - Heart
  structures_to_eval = yaml_conf["eval"]["structures_to_eval"]
  
  res_base_path = yaml_conf["eval"]["results_base_path"]
  
  ## ----------------------------------------
  
  # dictionary to be passed to the main function
  config = dict()

  config["preproc_path_nrrd"] = preproc_path_nrrd
  config["rt_segmasks_folder_name"] = rt_segmasks_folder_name
  config["pred_segmasks_folder_name"] = pred_segmasks_folder_name
  
  config["output_path_nii"] = output_path_nii
  config["structures_to_eval"] = structures_to_eval
  
  config["res_base_path"] = res_base_path
  
  # TODO: dump this as a log somewhere in the data folder

  # TODO: implement config parameters overwrite from command line
  
  # TODO: implement a class to parse the config file + custom command line params
  
  main(config)