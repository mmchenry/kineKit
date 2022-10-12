# %% 
""" Path function 
-----------------------------------------------------------------------------------------------------
"""

import platform

def give_paths():

    # These are the paths on Matt's laptop
    if platform.system() == 'Darwin' and os.path.isdir('/Users/mmchenry/'):

        root_code = '/Users/mmchenry/Documents/code'
        root_proj = '/Users/mmchenry/Documents/Projects/waketracking'

    # Matt on Linux
    elif platform.system() == 'Linux' and os.path.isdir('/home/mmchenry/'):

        root_code = '/home/mmchenry/code'
        root_proj = '/home/mmchenry/Documents/wake_tracking'

    # Catch alternatives
    else:
        raise ValueError('Do not recognize this account -- add lines of code to define paths here')

    # Directory structure wrt root folders
    paths = {
        # Path to kineKit code
        'kinekit':  root_code + os.sep + 'kineKit', 

        # Path to experiment catalog file
        'cat': root_proj + os.sep + 'experiment_log.csv', 

        # Path to experiment catalog file
        'data': root_proj + os.sep + 'data',

        # Path to raw videos
        'vidin': root_proj + os.sep + 'video' + os.sep + 'raw',

        # Path to exported videos
        'vidout': root_proj + os.sep + 'video' + os.sep + 'compressed',

        # Mask file
        'mask': root_proj + os.sep + 'masks',

        # Temporary video
        'tmp': root_proj + os.sep + 'video' + os.sep + 'tmp'
        }

    return paths


#%%
""" Parameters and packages 
-----------------------------------------------------------------------------------------------------
"""
import sys
import os
# import def_definepaths as dd

# Run these lines at the iPython interpreter when developing the module code
# %load_ext autoreload
# %autoreload 2
# Use this to check version update
# af.report_version()

# Get paths (specific to system running code)
path = give_paths()

# Add path to kineKit 'sources' directory using sys package
sys.path.insert(0, path['kinekit'] + os.path.sep + 'sources')

# Import from kineKit
import acqfunctions as af

# Extract experiment catalog info
cat = af.get_cat_info(path['cat'])

# Raw video extension
vid_ext_raw = 'MOV'

# Number of cores to use for parallel processing
num_cores = 8

# %%

# def batch_command(cmds):
#     # import time
#     import ipyparallel as ipp
#     import sys

#     # Report python and IPyparallel versions to make sure they exist
#     # print("Python Version : ", sys.version)
#     # print("IPyparallel Version : ", ipp.__version__)

#     # Set up clients 
#     client = ipp.Client()
#     type(client), client.ids

#     # Direct view allows shared data (balanced_view is the alternative)
#     direct_view = client[:]

#     # Function to execute the code
#     def run_command(idx):
#         import os
#         os.system(cmds_run.command[idx])
#         return idx

#     direct_view["cmds_run"] = cmds

#     res = []
#     for n in range(len(direct_view)):
#         res.append(client[n].apply(run_command, n))

# %%

def batch_command(cmds):
    # import time
    import ipyparallel as ipp
    import sys

    # Report python and IPyparallel versions to make sure they exist
    # print("Python Version : ", sys.version)
    # print("IPyparallel Version : ", ipp.__version__)

    # Set up clients 
    client = ipp.Client()
    type(client), client.ids

    # Direct view allows shared data (balanced_view is the alternative)
    direct_view = client[:]

    # Function to execute the code
    def run_command(idx):
        import os
        os.system(cmds_run.command[idx])
        return idx

    direct_view["cmds_run"] = cmds

    res = []
    for n in range(len(direct_view)):
        res.append(client[n].apply(run_command, n))

#%%
""" Uses kineKit to crop and compress video from catalog parameters 
-----------------------------------------------------------------------------------------------------
"""
# Extract experiment catalog info
cat = af.get_cat_info(path['cat'])

# Make the masked videos (stored in 'tmp' directory)
print(' ')
print('=====================================================')
print('First, creating masked videos . . .')
cmds = af.convert_masked_videos(cat, in_path=path['vidin'], out_path=path['tmp'], maskpath=path['mask'], vmode=False, 
                         imquality=1, num_cores=num_cores)

# Run FFMPEG commands in parallel
batch_command(cmds)

# [r.result() for r in res]


# %%
# Make the downsampled/cropped videos  (stored in 'pilot_compressed' directory)
print(' ')
print('=====================================================')
print('Second, creating downsampled and cropped videos . . .')
af.convert_videos(cat, in_path=path['tmp'], out_path=path['vidout'], vmode=False, imquality=0.75, vertpix=720, suffix_in='mp4')

# Survey resulting directories 
# Loop thru each video listed in cat
print(' ')
print('=====================================================')
print('Surveying results . . .')
for c_row in cat.index:
    # Input video path
    vid_in_path = path['vidin'] + os.sep + cat.video_filename[c_row] + '.' + os.sep + vid_ext_raw

    # Temp video path
    vid_tmp_path = path['tmp'] + os.sep + cat.video_filename[c_row] + '.mp4'

    # Output video path
    vid_out_path = path['vidout'] + os.sep + cat.video_filename[c_row] + '.mp4'

    # Check that output file was made
    if not os.path.isfile(vid_out_path):

        print('   Output movie NOT created successfully: ' + vid_out_path)

        if os.path.isfile(vid_tmp_path):
            print('   Also, temp. movie NOT created successfully: ' + vid_tmp_path)
        else:
            print('   But, temp. movie created successfully: ' + vid_tmp_path)
    else:

        print('   Output movie created successfully: ' + vid_out_path)

        # Delete temp file
        if os.path.isfile(vid_tmp_path):
            os.remove(vid_tmp_path)


#%%
""" Acquire the pixel intensity from movies in cat 
-----------------------------------------------------------------------------------------------------
"""

# # import videotools as vt
# import cv2 as cv  # openCV for interacting with video
# import numpy as np
# import pandas as pd

import def_acquisition as da

# Batch run to analyze pixel intensity of all videos in cat
da.measure_pixintensity(cat, path['data'], path['vidout'])


#%%
""" Plot pixel intensity for each video analyzed 
-----------------------------------------------------------------------------------------------------
"""

import pandas as pd
import glob
import plotly.express as px


# path = os.getcwd()
csv_files = glob.glob(os.path.join(path['data'], "*.pixelintensity"))

# Loop thru each video listed in cat
for c_row in cat.index:

    # Unique identifier for the current sequence
    exp_name = cat.date[c_row] + '_' + format(cat.exp_num[c_row],'03')

    # Path for output data for current sequence
    din_path = path['data'] + os.path.sep + exp_name + '_pixelintensity'

    # Read dataframe and plot pixel intensity
    df = pd.read_pickle(din_path)
    fig = px.line(df,x="time_s", y="meanpixval", title=exp_name)
    fig.show()



# %% 
""" Extract a single video frame """

import videotools as vt

full_path = path['vidin'] + os.path.sep + cat.video_filename[0] + '.' + os.sep + vid_ext_raw

im = vt.get_frame(full_path)