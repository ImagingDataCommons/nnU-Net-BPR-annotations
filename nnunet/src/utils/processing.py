"""
    ----------------------------------------
    IDC-MedImA-misc - processing utils
    ----------------------------------------
    
    ----------------------------------------
    Author: Dennis Bontempi
    Email:  dennis_bontempi@dfci.harvard.edu
    ----------------------------------------
    
"""

import os
import time
import subprocess

def process_patient_nnunet(model_input_folder, model_output_folder, nnunet_model,
                           use_tta = False, export_prob_maps = False):

  """
  Infer the thoracic organs at risk segmentation maps using one of the nnU-Net models.

  Arguments:
    model_input_folder  : required - path to the folder where the data to be inferred should be stored.
    model_output_folder : required - path to the folder where the inferred segmentation masks will be stored.
    nnunet_model        : required - pre-trained nnU-Net model to use during the inference phase.
    use_tta             : optional - whether to use or not test time augmentation (TTA). Defaults to False.
    export_prob_maps    : optional - whether to export or not softmax probabilities. Defaults to False.

  Outputs:
    This function [...]
  """
  
  assert(nnunet_model in ["2d", "3d_lowres", "3d_fullres", "3d_cascade_fullres"])

  start_time = time.time()

  print("Running `nnUNet_predict` with `%s` model..."%(nnunet_model))

  pat_fn_list = sorted([f for f in os.listdir(model_input_folder) if ".nii.gz" in f])
  pat_fn_path = os.path.join(model_input_folder, pat_fn_list[-1])

  print("Processing file at %s..."%(pat_fn_path))

  # run the inference phase
  # note: this could also be done in a pythonic fashion by running
  #       `nnUNet/nnunet/inference/predict.py` - but it would require
  #       to set manually all the arguments that the user is not intended
  #       to fiddle with; so stick with the bash executable

  bash_command = list()
  bash_command += ["nnUNet_predict"]
  bash_command += ["--input_folder", "%s"%model_input_folder]
  bash_command += ["--output_folder", "%s"%model_output_folder]
  bash_command += ["--task_name", "Task055_SegTHOR"]
  bash_command += ["--model", "%s"%nnunet_model]
  
  if use_tta == False:
    bash_command += ["--disable_tta"]
  
  if export_prob_maps == True:
    bash_command += ["--save_npz"]

  bash_return = subprocess.run(bash_command, check = True, text = True)

  elapsed = time.time() - start_time

  print("Done in %g seconds."%elapsed)