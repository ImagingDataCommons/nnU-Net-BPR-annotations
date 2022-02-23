"""
    ----------------------------------------
    nnUNet @ IDC
    
    STEP1 - preprocessing (task-independent)
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

"""

def run_core(pat_dict):

  pat = pat_dict["pat"]
  pat_dir_path_nrrd = pat_dict["pat_dir_path_nrrd"]
  pat_dir_path_nii = pat_dict["pat_dir_path_nii"]
    
  # patient subfolder where all the preprocessed NRRDs will be stored
  if not os.path.exists(pat_dir_path_nrrd): os.mkdir(pat_dir_path_nrrd)
    
  # patient subfolder where all the preprocessed NIfTIs will be stored
  if not os.path.exists(pat_dir_path_nii): os.mkdir(pat_dir_path_nii)
    
  path_to_ct_dir = pat_dict["path_to_ct_dir"]
  ct_nrrd_path = pat_dict["ct_nrrd_path"]
  ct_nii_path = pat_dict["ct_nii_path"]
    
  path_to_rt_dir = pat_dict["path_to_rt_dir"]
  rt_folder = pat_dict["rt_folder"]
  rt_list_path = pat_dict["rt_list_path"]
  
  verbose = pat_dict["verbose"]
  
  # logfile for the plastimatch conversion
  log_file_path_nrrd = os.path.join(pat_dir_path_nrrd, pat + '_pypla.log')
  log_file_path_nii = os.path.join(pat_dir_path_nii, pat + '_pypla.log')
    
  # DICOM CT to NRRD conversion (if the file doesn't exist yet)
  if not os.path.exists(ct_nrrd_path):
    convert_args_ct = {"input" : path_to_ct_dir,
                       "output-img" : ct_nrrd_path}
    
    # clean old log file if it exist
    if os.path.exists(log_file_path_nrrd): os.remove(log_file_path_nrrd)
    
    pypla.convert(verbose = verbose, path_to_log_file = log_file_path_nrrd, **convert_args_ct)

  # DICOM RTSTRUCT to NRRD conversion (if the file doesn't exist yet)
  if not os.path.exists(rt_folder):
    convert_args_rt = {"input" : path_to_rt_dir, 
                       "referenced-ct" : path_to_ct_dir,
                       "output-prefix" : rt_folder,
                       "prefix-format" : 'nrrd',
                       "output-ss-list" : rt_list_path}
    
    # clean old log file if it exist
    if os.path.exists(log_file_path_nrrd): os.remove(log_file_path_nrrd)
    
    pypla.convert(verbose = verbose, path_to_log_file = log_file_path_nrrd, **convert_args_rt)

  # DICOM CT to NIfTI conversion (if the file doesn't exist yet)
  if not os.path.exists(ct_nii_path):
    convert_args_nii = {"input" : path_to_ct_dir, 
                        "output-img" : ct_nii_path}
    
    # clean old log file if it exist
    if os.path.exists(log_file_path_nii): os.remove(log_file_path_nii)
    
    pypla.convert(verbose = verbose, path_to_log_file = log_file_path_nii, **convert_args_nii)
  
## ----------------------------------------

def main(config):
  
  # parse from the config dict
  preproc_data_path_nrrd = config["preproc_data_path_nrrd"]
  preproc_data_path_nii = config["preproc_data_path_nii"]
  dicom_path = config["dicom_path"]
  cpu_cores = config["cpu_cores"]
  
  # list of patient dictionaries storing the information needed for processing
  # (required for multiprocessing)
  pat_dict_list_mp = list()
  
  use_multiprocessing = True if cpu_cores > 1 else False
    
  # dataset subfolder where all the preprocessed NRRDs will be stored
  if not os.path.exists(preproc_data_path_nrrd): os.makedirs(preproc_data_path_nrrd)
  
  # dataset subfolder where all the preprocessed NIfTIs will be stored
  if not os.path.exists(preproc_data_path_nii): os.makedirs(preproc_data_path_nii)
  
  # list of patients to be pre-processed
  pat_list = list()
  
  print("Looking for patients folder at %s...\n\nPatients found:"%(dicom_path))
  
  for f in os.listdir(dicom_path):
    if os.path.isdir(os.path.join(dicom_path, f)):
      pat_list.append(f)
      print(f)
      
  # FIXME: debug
  pat_list = pat_list
  
  print("\nStarting the preprocessing...")
  
  for pat_num, pat in enumerate(pat_list):
    
    pat_dir_path_nrrd = os.path.join(preproc_data_path_nrrd, pat)
    pat_dir_path_nii = os.path.join(preproc_data_path_nii, pat)

    # location where the NRRD files (CT/RTSTRUCT) should be saved
    ct_nrrd_path = os.path.join(pat_dir_path_nrrd, pat + '_ct.nrrd')
    rt_nrrd_path = os.path.join(pat_dir_path_nrrd, pat + '_rt.nrrd')

    # location where the NIfTI file (CT) should be saved
    ct_nii_path = os.path.join(pat_dir_path_nii, pat + '_ct.nii.gz')
    
    # location of the file storing the names of the exported segmentation masks (from the DICOM RTSTRUCT)
    rt_list_path = os.path.join(pat_dir_path_nrrd, pat + '_rt_list.txt')
    
    # location of the folder storing the NRRD segmentation masks (from the DICOM RTSTRUCT)
    # (one NRRD volume is exported for each of the segmentation mask found)
    rt_folder = os.path.join(pat_dir_path_nrrd, "rt_segmasks")
      
    ## ----------------------------------------

    path_to_ct_dir = os.path.join(dicom_path, pat, "CT")
    path_to_rt_dir = os.path.join(dicom_path, pat, "RTSTRUCT")    

    # sanity check
    assert os.path.exists(path_to_ct_dir)
    assert os.path.exists(path_to_rt_dir)
    
    pat_dict = dict()
    pat_dict["pat"] = pat
    pat_dict["pat_dir_path_nrrd"] = pat_dir_path_nrrd
    pat_dict["pat_dir_path_nii"] = pat_dir_path_nii
    
    pat_dict["path_to_ct_dir"] = path_to_ct_dir
    pat_dict["ct_nrrd_path"] = ct_nrrd_path
    pat_dict["ct_nii_path"] = ct_nii_path
    
    pat_dict["path_to_rt_dir"] = path_to_rt_dir
    pat_dict["rt_folder"] = rt_folder
    pat_dict["rt_list_path"] = rt_list_path
    pat_dict["verbose"] = False if use_multiprocessing else True
    
    pat_dict_list_mp.append(pat_dict)
  
  # monitor performance
  tic = time.time()
  
  if use_multiprocessing:
    print("\nRunning on %g cores."%(cpu_cores))
    pool = multiprocessing.Pool(processes = cpu_cores)
    
    for _ in tqdm.tqdm(pool.imap_unordered(run_core, pat_dict_list_mp), total = len(pat_dict_list_mp)):
      pass
      
  else:
    print("\nRunning process on a single core.")
    for pat_dict in tqdm.tqdm(pat_dict_list_mp):
      run_core(pat_dict)
      
  toc = time.time()
  elapsed = toc - tic
  
  print('\nTask completed in %.2f seconds.'%(elapsed))

## ----------------------------------------
## ----------------------------------------
      
if __name__ == '__main__':

  base_conf_file_path = '.'
  
  parser = argparse.ArgumentParser(description = 'nnU-Net @ IDC - data preprocessing step')

  parser.add_argument('--conf',
                      required = False,
                      help = 'Specify the path to the YAML configuration file containing the run details.',
                      default = "config.yaml"
                     )

  args = parser.parse_args()

  conf_file_path = os.path.join(base_conf_file_path, args.conf)

  with open(conf_file_path) as f:
    yaml_conf = yaml.load(f, Loader = yaml.FullLoader)

  # base data directory
  data_base_path = yaml_conf["data"]["base_path"]
  
  # name of the dataset, will set the name for all the created subfolders
  # expected to be found as a prefix to all the files needed for the pre-processing
  dataset_name = yaml_conf["dataset"]["name"]
  
  ## ----------------------------------------

  # by default, the raw (DICOM) dataset (as pulled from IDC) should be stored
  # in a folder "raw" under the main data directory
  dataset_path = os.path.join(data_base_path, 'raw', dataset_name)
 
  # location of all the DICOM files within the dataset directory
  # the directory should be organised as all the IDC cohorts are
  # so that paths can be computed from the _table.csv file associated with the cohort
  # or from the dataset structure defined through DICOMsort
  dicom_path = os.path.join(dataset_path, 'dicom')

  # by default, the preprocessed dataset (converted to NRRD, NIfTI) will be stored
  # in a folder "preproc" under the main data directory
  preproc_base_path = os.path.join(data_base_path, "processed", dataset_name)

  # output folder for the NRRD files (CT, segmasks in the RTSTRUCTS, predicted masks)
  preproc_data_path_nrrd = os.path.join(preproc_base_path, 'nrrd')
  
  # output folder for the NIfTI files (CT only, needed for the nnU-Net processing)
  preproc_data_path_nii = os.path.join(preproc_base_path, 'nii')
  
  ## ----------------------------------------
  
  # dictionary to be passed to the main function
  config = dict()
  
  config["dicom_path"] = dicom_path
  config["preproc_data_path_nrrd"] = preproc_data_path_nrrd
  config["preproc_data_path_nii"] = preproc_data_path_nii
  
  # cores to use for multiprocessing
  config["cpu_cores"] = yaml_conf["proc"]["cpu_cores"]
  
  # TODO: dump this as a log somewhere in the data folder

  # TODO: implement config parameters overwrite from command line
  
  # TODO: implement a class to parse the config file + custom command line params
  
  main(config)