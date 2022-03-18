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

from google.cloud import storage


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
  bash_command += ["cat", "%s"%gs_file_path]

  ps = subprocess.Popen(bash_command, stdout = subprocess.PIPE)

  bash_command = list()
  bash_command = ["gsutil", "-q", "-m", "cp", "-Ir", "%s"%download_path]

  bash_return = subprocess.check_output(bash_command, stdin = ps.stdout)
  ps.wait()

  elapsed = time.time() - start_time
  print("Done in %g seconds."%elapsed)

  start_time = time.time()
  print("\nSorting DICOM files..." )

  # 
  bash_command = list()
  bash_command += ["python", "src/dicomsort/dicomsort.py", "-k", "-u",
                   "%s"%download_path, "%s/%%PatientID/%%Modality/%%SOPInstanceUID.dcm"%sorted_base_path]

  bash_return = subprocess.run(bash_command, check = True, text = True)

  elapsed = time.time() - start_time
  print("Done in %g seconds."%elapsed)

  print("Sorted DICOM data saved at: %s"%(os.path.join(sorted_base_path, pat_id)))

  # get rid of the temporary folder, storing the unsorted DICOM data 
  if remove_raw:
    print("Removing un-sorted data at %s..."%(download_path))
    shutil.rmtree(download_path) 
    print("... Done.")

# ----------------------------------
# ----------------------------------

def file_exists_in_bucket(project_name, bucket_name, file_gs_uri):
  
  """
  Check whether a file exists in the specified Google Cloud Storage Bucket.

  Arguments:
    project_name : required - name of the GCP project.
    bucket_name  : required - name of the bucket (without gs://)
    file_gs_uri  : required - file GS URI
  
  Returns:
    file_exists : boolean variable, True if the file exists in the specified,
                  bucket, at the specified location; False if it doesn't.

  Outputs:
    This function [...]
  """

  storage_client = storage.Client(project = project_name)
  bucket = storage_client.get_bucket(bucket_name)
  
  bucket_gs_url = "gs://%s/"%(bucket_name)
  path_to_file_relative = file_gs_uri.split(bucket_gs_url)[-1]

  print("Searching `%s` for: \n%s\n"%(bucket_gs_url, path_to_file_relative))

  file_exists = bucket.blob(path_to_file_relative).exists(storage_client)

  return file_exists

# ----------------------------------
# ----------------------------------

def listdir_bucket(project_name, bucket_name, dir_gs_uri):
  
  """
  Export DICOM SEG object from segmentation masks stored in NRRD files.

  Arguments:
    project_name : required - name of the GCP project.
    bucket_name  : required - name of the bucket (without gs://)
    file_gs_uri  : required - directory GS URI
  
  Returns:
    file_list : list of files in the specified GCS bucket.

  Outputs:
    This function [...]
  """

  storage_client = storage.Client(project = project_name)
  bucket = storage_client.get_bucket(bucket_name)
  
  bucket_gs_url = "gs://%s/"%(bucket_name)
  path_to_dir_relative = dir_gs_uri.split(bucket_gs_url)[-1]


  print("Getting the list of files at `%s`..."%(dir_gs_uri))

  file_list = list()

  for blob in storage_client.list_blobs(bucket_name,  prefix = path_to_dir_relative):
    fn = os.path.basename(blob.name)
    file_list.append(fn)

  return file_list