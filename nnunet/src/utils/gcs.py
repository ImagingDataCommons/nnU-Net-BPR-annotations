"""
    ----------------------------------------
    IDC-MedImA-misc - GCS utils
    ----------------------------------------
    
    ----------------------------------------
    Author: Dennis Bontempi
    Email:  dennis_bontempi@dfci.harvard.edu
    ----------------------------------------
    
"""

import os
import time
import shutil
import subprocess

def download_patient_data(raw_base_path, sorted_base_path,
                          patient_df, remove_raw = True):

  """
  Download raw DICOM data and run dicomsort to standardise the input format.

  Arguments:
    raw_base_path    : required - path to the folder where the raw data will be stored.
    sorted_base_path : required - path to the folder where the sorted data will be stored.
    patient_df       : required - Pandas dataframe (returned from BQ) storing all the
                                  patient information required to pull data from the IDC buckets.
    remove_raw       : optional - whether to remove or not the raw non-sorted data
                                  (after sorting with dicomsort). Defaults to True.
  
  Outputs:
    This function [...]
  """

  # FIXME: this gets overwritten every single time; use `tempfile` library?
  gs_file_path = "gcs_paths.txt"
  patient_df["gcs_url"].to_csv(gs_file_path, header = False, index = False)

  pat_id = patient_df["PatientID"].values[0]
  download_path = os.path.join(raw_base_path, pat_id)

  if not os.path.exists(download_path):
    os.mkdir(download_path)

  start_time = time.time()
  print("Copying files from IDC buckets to %s..."%(download_path))

  bash_command = list()
  bash_command += ["cat", "%s"%gs_file_path, "|", "gsutil", "-q", "-m", "cp", "-Ir", "%s"%download_path]

  subprocess.run(bash_command, check = True, text = True)

  elapsed = time.time() - start_time
  print("Done in %g seconds."%elapsed)

  start_time = time.time()
  print("\nSorting DICOM files..." )

  bash_command = list()
  bash_command += ["python", "../dicomsort/dicomsort.py", "-u",
                   "%s"%download_path, "%s/%PatientID/%Modality/%SOPInstanceUID.dcm"%sorted_base_path]

  elapsed = time.time() - start_time
  print("Done in %g seconds."%elapsed)

  print("Sorted DICOM data saved at: %s"%(os.path.join(sorted_base_path, pat_id)))

  # get rid of the temporary folder, storing the unsorted DICOM data 
  if remove_raw:
    print("Removing un-sorted data at %s..."%(download_path))
    shutil.rmtree(download_path) 
    print("... Done.")