"""Grid combination for the demo pipelne

This script set up the output image directory as well!

Author: Kristof Rozgonyi
e-mail: rstofi@gmail.com
License: MIT
Date: 2019
"""
#==========================================================================
#            _____ __  __ _____   ____  _____ _______ _____ 
#           |_   _|  \/  |  __ \ / __ \|  __ \__   __/ ____|
#             | | | \  / | |__) | |  | | |__) | | | | (___  
#             | | | |\/| |  ___/| |  | |  _  /  | |  \___ \ 
#            _| |_| |  | | |    | |__| | | \ \  | |  ____) |
#           |_____|_|  |_|_|     \____/|_|  \_\ |_| |_____/ 
#==========================================================================
#=== Basic imports ===
import numpy as np;
import os;
import sys;
import copy;
import shutil;

#=== Imports from the DGP wrapper ===
from dgp.util.parameters import dgp_path,get_rms;
from dgp.image.read_and_create import get_sky_image_property_from_MS,\
    create_ARLimage_from_MS, create_ARLimage_from_CASAimage,\
    create_ARLimage_from_CASAimage_array_and_template;
from dgp.visualization.image import plot_sky_as_image;
from dgp.imaging.data_models import Parset, create_parset_from_template;
from dgp.simulation.util import get_combination_matrix;

#=== Import CASACORE tables ===
from casacore import images as casaimage;

#=== Logging ===
import logging;
#log = logging.getLogger(__name__);
log = logging.getLogger();

#=============================================================================
#             _____ _      ____  ____          _       _____ 
#            / ____| |    / __ \|  _ \   /\   | |     / ____|
#           | |  __| |   | |  | | |_) | /  \  | |    | (___  
#           | | |_ | |   | |  | |  _ < / /\ \ | |     \___ \ 
#           | |__| | |___| |__| | |_) / ____ \| |____ ____) |
#            \_____|______\____/|____/_/    \_\______|_____/ 
#
#============================================================================= 
#==== Main paramteers ===
#The number of datasets
N_dataset = 4;#I don't use this now

N_combination = 3;#I use this now

#===================================================
#            __  __          _____ _   _ 
#           |  \/  |   /\   |_   _| \ | |
#           | \  / |  /  \    | | |  \| |
#           | |\/| | / /\ \   | | | . ` |
#           | |  | |/ ____ \ _| |_| |\  |
#           |_|  |_/_/    \_\_____|_| \_|
#
#===================================================
if __name__ == '__main__':
    """Create combined images
    """

    #Setup logging
    log.setLevel(logging.INFO);
    log.addHandler(logging.StreamHandler(sys.stdout));

    #=== Create the workind directory tree ===
    #We expect that the imaging directory exist
    cwd = os.getcwd();#Current working directory
    input_images_dir_path = cwd + '/test/demo_first_pass_images';
    simulation_setup_dir_path = cwd + '/test/demo_simulations';

    assert os.path.isdir(input_images_dir_path), 'The directory: {0:s} not existing!'.format(input_images_dir_path);
    assert os.path.isdir(simulation_setup_dir_path), 'The directory: {0:s} not existing!'.format(simulation_setup_dir_path);

    log.info('Setup enviroment');

    #Create the directory which we gonna create the images
    grid_combination_dir_path = cwd + '/test/demo_final_image';

    #Delete the folder if exist
    if os.path.isdir(grid_combination_dir_path):
        shutil.rmtree(grid_combination_dir_path);
        os.mkdir(grid_combination_dir_path);
    else:
        os.mkdir(grid_combination_dir_path);

    #Get the index list of the input images => this is surplus now
    grid_index_list = np.arange(0,N_dataset);

        #We only take the grids created by 
    #one major cycle!
    grid_name_list = ['0.0.prefft.imag','0.0.prefft.real',
                    '1.0.prefft.imag','1.0.prefft.real',
                    '2.0.prefft.imag','2.0.prefft.real',
                    '3.0.prefft.imag','3.0.prefft.real',
                    '4.0.prefft.imag','4.0.prefft.real',
                    '5.0.prefft.imag','5.0.prefft.real'];

    #=== Setup some imaging parameters ===    
    #Image names
    image_name_base = 'demo_first_pass';


    log.info('\n=== Combine {0:d} grids ===\n'.format(N_combination));

    #Select N_combined_dataset from the index list randomly
    #Creates a 2D matrix by default but we look at only one combination
    selected_grid_indices_list = get_combination_matrix(N=N_dataset,k=N_combination,
                                N_comb=1)[0];

    log.info('Selected grids: {}'.format(selected_grid_indices_list));

    #Save the selected image indice list => this is important if we perform more combinations
    np.savetxt('./selected_grid_indices.dat',selected_grid_indices_list);

    #=== Move a dataset to the combined folder and cretae empty grid template ===
    log.info('Copy grids');

    #Copy grids but always use the 0th image
    imaging_subdir_path = input_images_dir_path + '/demo_image_no_{0:d}_first_pass'.format(0);
    for grid_name in grid_name_list:
        shutil.copytree('{0:s}/{1:s}'.format(imaging_subdir_path,grid_name),grid_combination_dir_path + '/{0:s}'.format(grid_name));

    log.info('Create ARL image template for the grids');
    #Select the grids to combine
    #The grids before the restoring major cycle. The name depends on th umber of major cycles!
    combined_grid_name_real = grid_combination_dir_path + '/3.0.prefft.real';
    combined_grid_name_imag = grid_combination_dir_path + '/3.0.prefft.imag';

    #Make the arlimage teamplate => set the values to 0
    combined_grid_real_arlimage = create_ARLimage_from_CASAimage(combined_grid_name_real);
    combined_grid_imag_arlimage = create_ARLimage_from_CASAimage(combined_grid_name_imag);

    combined_grid_real_arlimage.data[...] = 0.;
    combined_grid_imag_arlimage.data[...] = 0.;

    log.info('Combine the grids:')
    #Now combine the datasets
    for i in range(0,N_combination):
        log.info('\tUsing grid no. {0:d}'.format(int(selected_grid_indices_list[i])));
        grid_index = selected_grid_indices_list[i];

        single_imaging_subdir_path = input_images_dir_path + '/demo_image_no_{0:d}_first_pass'.format(int(selected_grid_indices_list[i]));

        #Get the image paths
        grid_name_real = single_imaging_subdir_path + '/3.0.prefft.real';
        grid_name_imag = single_imaging_subdir_path + '/3.0.prefft.imag';

        #Cretae an ARL image from the grids
        sub_grid_real_arlimage = create_ARLimage_from_CASAimage(grid_name_real);
        sub_grid_imag_arlimage = create_ARLimage_from_CASAimage(grid_name_imag);

        #Add it to the combined arlimage
        combined_grid_real_arlimage.data += sub_grid_real_arlimage.data;
        combined_grid_imag_arlimage.data += sub_grid_imag_arlimage.data;

    log.info('Normalise combined grids');
    #Normnalise the combined image
    combined_grid_real_arlimage.data /= N_combination;
    combined_grid_imag_arlimage.data /= N_combination;

    log.info('Write combined grid back to the grids');
    #write this back to the dataset
    combined_grid_real_casaimage = casaimage.image(combined_grid_name_real);
    combined_grid_real_casaimage_data = combined_grid_real_casaimage.getdata();

    combined_grid_imag_casaimage = casaimage.image(combined_grid_name_imag);
    combined_grid_imag_casaimage_data = combined_grid_imag_casaimage.getdata();

    #Put the arl object to the CASAimage object
    combined_grid_real_casaimage_data[...] = combined_grid_real_arlimage.data;
    combined_grid_imag_casaimage_data[...] = combined_grid_imag_arlimage.data;

    #Write it back to the image
    combined_grid_real_casaimage.putdata(combined_grid_real_casaimage_data);
    combined_grid_imag_casaimage.putdata(combined_grid_imag_casaimage_data);
    
    #Deleting the variables closes the image, which release the lock
    #Another soulution would be is to do this inside a function....
    del combined_grid_real_casaimage;
    del combined_grid_imag_casaimage;
