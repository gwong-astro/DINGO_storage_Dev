#!/usr/bin/env python
# coding: utf-8
######################################################################
# Purpose: Create the parset file for the ASKAPsoft data reduction.
#
# Date: 17/02/20
# Author: G. Wong (g.wong@csiro.au)
#
# Notes:
# I need to run this on hyrmine.icrar.org
# Also set up the environment as described by Kristof's github page
# (https://github.com/rstofi/DINGO_gridded_pipeline/tree/master/notebook_setup_example)
#
# In particular 'source /home/krozgonyi/.bashrc' and 'dgp_develop_env_setup'
#
#
######################################################################
#
# Packages to import
import numpy as np
import os, sys, copy, shutil
from dgp.imaging.data_models import Parset, create_parset_from_template;
#
#
#
def ASKAPsoft_parset(default_template='NGC7232_no_tapering', ms_name_path='./NameOfFile.ms',\
                    image_name='./NameOfOutput.ms', parsetLocation = './'):
    """
    Create the parset file required for the ASKAPsoft pipeline.

    Based on Kristof's prototype of first_pass_imaging.py and
    second_pass_imaging.py.  Using a template, modify some of
    the values e.g. input, output and location to save the parset
    file.


    Key Parameters:
    default_template: Base template to modify the parset file (default is 'NGC7232_no_tapering').
    ms_name_path: Name of the UV data to pass into the ASKAPsoft imaging task.
    image_name: Name of the output UV grid data (stored as a casaimage format)
    parsetLocation: Location to save the parset file.
    """
    #
    parset_prec_test = create_parset_from_template(default_template);
    parset_prec_test.dataset = ms_name_path;                # Input ms file uvdata?
    parset_prec_test.Images_names = image_name;             # Output of UVgrid
    parset_prec_test.AltWProject_dumpgrid = 'true';         # Dump the grids
    parset_prec_test.preconditioner_Wiener_robustness = 2;  # Natural weighting

    parset_prec_test.summary();

    # Create parset file
    parset_prec_test.create_parset_file(imaging_subdir_path + 'parset.in');

    return
#
#
# 
def DINGO_parset(default_template='NGC7232_no_tapering', ms_name_path='./NameOfFile.ms',\
                image_name='./NameOfOutput.ms', parsetLocation = './'):
    """
    Create the parset file required for the DINGO pipeline.

    Based on Kristof's prototype of first_pass_imaging.py and
    second_pass_imaging.py.  Using a template, modify some of
    the values e.g. input, output and location to save the parset
    file.


    Key Parameters:
    default_template: Base template to modify the parset file (default is 'NGC7232_no_tapering').
    ms_name_path: Name of the UV data to pass into the ASKAPsoft imaging task.
    image_name: Name of the output UV grid data (stored as a casaimage format)
    parsetLocation: Location to save the parset file.
    """
    #
    parset_prec_test = create_parset_from_template(default_template);
    parset_prec_test.dataset = ms_name_path;                # Input ms file uvdata?
    parset_prec_test.Images_names = image_name;             # Output of UVgrid
    parset_prec_test.AltWProject_dumpgrid='false';          # Dump the grids
    parset_prec_test.AltWProject_importgrid='true';         # Import the preexisting grids
    parset_prec_test.preconditioner_Wiener_robustness=2;    # Natural weighting
    #
    parset_prec_test.summary();
    #
    #Create parset file
    parset_prec_test.create_parset_file(final_image_dir_path + '/parset.in');
    return


# In[10]:


def filePath_check(cwd = os.getcwd()):
    """
    Setup the file directory where to direct the input and output locations.

    Keyword parameters:
    cwd: Directory (default directory where the script was executed from)

    """
    setup_dir_path = cwd + '/test/demo_simulations';

    #Test if the -/test direcrory exist, abd build the tree under it!
    assert os.path.isdir(setup_dir_path), 'The directory: {0:s} not existing!'.format(setup_dir_path);

    #Create the directory which we gonna create the images
    imaging_dir_path = cwd + '/test/demo_first_pass_images'

    #Create dir if not existing
    if os.path.isdir(imaging_dir_path):
        pass;
    else:
        os.mkdir(imaging_dir_path)
    #
    #
    return setup_dir_path, imaging_dir_path

setup_dir_path, imaging_dir_path = filePath_check()
# print(setup_dir_path, imaging_dir_path)
# ASKAPsoft_parset()
# DINGO_parset()




#Change cwd and run the imager
# os.chdir(imaging_subdir_path);
# os.system('imager -c parset.in > logfile.log');
