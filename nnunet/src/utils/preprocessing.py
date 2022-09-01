"""
    ----------------------------------------
    IDC-MedImA-misc - pre-processing utils
    ----------------------------------------
    
    ----------------------------------------
    Author: Dennis Bontempi
    Email:  dennis_bontempi@dfci.harvard.edu
    ----------------------------------------
    
"""

import os
import shutil
import pyplastimatch as pypla


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

# ----------------------------------
# ----------------------------------

def pypla_dicom_ct_to_nifti(sorted_base_path, processed_nifti_path,
                            pat_id, verbose = True):
  
  """
  Sorted DICOM patient data to NIfTI file (CT volume).

  Arguments:
    sorted_base_path     : required - path to the folder where the sorted data should be stored.
    processed_nifti_path : required - path to the folder where the preprocessed NIfTI data are stored
    remove_raw           : required - patient ID (used for naming purposes).
    verbose              : optional - whether to run pyplastimatch in verbose mode. Defaults to true.
  
  Outputs:
    This function [...]
  """

  # given that everything is standardised already, compute the paths
  path_to_dicom_ct_folder = os.path.join(sorted_base_path, pat_id, "CT")
  
  # sanity check
  assert(os.path.exists(path_to_dicom_ct_folder))
  
  pat_dir_nifti_path = os.path.join(processed_nifti_path, pat_id)
  if not os.path.exists(pat_dir_nifti_path):
    os.mkdir(pat_dir_nifti_path)

  # output NRRD CT
  ct_nifti_path = os.path.join(pat_dir_nifti_path, pat_id + "_CT.nii.gz")

  # logfile for the plastimatch conversion
  log_file_path = os.path.join(pat_dir_nifti_path, pat_id + '_pypla.log')

  # DICOM CT to NRRD conversion (if the file doesn't exist yet)
  if not os.path.exists(ct_nifti_path):
    convert_args_ct = {"input" : path_to_dicom_ct_folder,
                       "output-img" : ct_nifti_path}

    # clean old log file if it exist
    if os.path.exists(log_file_path): os.remove(log_file_path)
    
    pypla.convert(verbose = verbose,
                  path_to_log_file = log_file_path,
                  **convert_args_ct)

# ----------------------------------
# ----------------------------------

def pypla_dicom_rtstruct_to_nrrd(sorted_base_path, processed_nrrd_path,
                                 pat_id, verbose = True):
  
  """
  Sorted DICOM patient data to NRRD file (RTSTRUCT).

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
  path_to_dicom_rt_folder = os.path.join(sorted_base_path, pat_id, "RTSTRUCT")

  pat_dir_nrrd_path = os.path.join(processed_nrrd_path, pat_id)

  # sanity check
  assert(os.path.exists(path_to_dicom_rt_folder))
  assert(os.path.exists(pat_dir_nrrd_path))

  # output NRRD CT
  rt_folder_path = os.path.join(pat_dir_nrrd_path, "rt_segmasks")
  rt_list_path = os.path.join(rt_folder_path, pat_id + "_rt_list.txt")

  # path to the file storing the names of the exported segmentation masks
  # (from the DICOM RTSTRUCT)
  log_file_path = os.path.join(pat_dir_nrrd_path, pat_id + '_pypla.log')

  # DICOM CT to NRRD conversion (if the file doesn't exist yet)
  if not os.path.exists(rt_folder_path):
    convert_args_rt = {"input" : path_to_dicom_rt_folder, 
                       "referenced-ct" : path_to_dicom_ct_folder,
                       "output-prefix" : rt_folder_path,
                       "prefix-format" : 'nrrd',
                       "output-ss-list" : rt_list_path}

    pypla.convert(verbose = verbose,
                  path_to_log_file = log_file_path,
                  **convert_args_rt)

# ----------------------------------
# ----------------------------------

def prep_input_data(processed_nifti_path, model_input_folder, pat_id):
  
  """
  Sorted DICOM patient data to NRRD file (RTSTRUCT).

  Arguments:
    src_folder : required - path to the folder where the sorted data should be stored.
    dst_folder : required - path to the folder where the preprocessed NRRD data are stored
    pat_id     : required - patient ID (used for naming purposes).
  
  Outputs:
    This function [...]
  """

  pat_dir_nifti_path = os.path.join(processed_nifti_path, pat_id)
  ct_nifti_path = os.path.join(pat_dir_nifti_path, pat_id + "_CT.nii.gz")
  
  copy_to_path = os.path.join(model_input_folder, pat_id + "_0000.nii.gz")
    
  # copy NIfTI to the right dir for nnU-Net processing
  if not os.path.exists(copy_to_path):
    print("Copying %s\nto %s..."%(ct_nifti_path, copy_to_path))
    shutil.copy(ct_nifti_path, copy_to_path)
    print("... Done.")

# ----------------------------------
# ----------------------------------
