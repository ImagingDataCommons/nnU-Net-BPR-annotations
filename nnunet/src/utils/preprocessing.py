"""
    ----------------------------------------
    IDC-MedImA-misc - preprocessing utils
    ----------------------------------------
    
    ----------------------------------------
    Author: Dennis Bontempi
    Email:  dennis_bontempi@dfci.harvard.edu
    ----------------------------------------
    
"""

import os
import sys
sys.path.append(["../"])

def pypla_dicom_ct_to_nrrd(sorted_base_path, processed_nrrd_path,
                           pat_id, verbose = True):
  
  """
  Sorted DICOM patient data to NRRD file (CT volume).

  Arguments:
    sorted_base_path    : required - path to the folder where the sorted data should be stored.
    processed_nrrd_path : required - path to the folder where the preprocessed NRRD data are stored
    remove_raw          : required - patient ID (used for naming purposes).
    verbose             : optional - whether to run pyplastimatch in verbose mode. Defaults to true.
  
  Outputs:
    This function [...]
  """

  # given that everything is standardised already, compute the paths
  path_to_dicom_ct_folder = os.path.join(sorted_base_path, pat_id, "CT")
  
  # sanity check
  assert(os.path.exists(path_to_dicom_ct_folder))
  
  pat_dir_nrrd_path = os.path.join(processed_nrrd_path, pat_id)
  if not os.path.exists(pat_dir_nrrd_path):
    os.mkdir(pat_dir_nrrd_path)

  # output NRRD CT
  ct_nrrd_path = os.path.join(pat_dir_nrrd_path, pat_id + "_CT.nrrd")

  # logfile for the plastimatch conversion
  log_file_path = os.path.join(pat_dir_nrrd_path, pat_id + '_pypla.log')

  # DICOM CT to NRRD conversion (if the file doesn't exist yet)
  if not os.path.exists(ct_nrrd_path):
    convert_args_ct = {"input" : path_to_dicom_ct_folder,
                       "output-img" : ct_nrrd_path}

    # clean old log file if it exist
    if os.path.exists(log_file_path): os.remove(log_file_path)
    
    pypla.convert(verbose = verbose,
                  path_to_log_file = log_file_path,
                  **convert_args_ct)