"""
    Functions to help operate DeepLabCut
"""
# Import packages
import os
import glob

def list_paths(vidPath,fileExt='mp4'):
# Returns listing of videos in vidPath to be used in the training

    # Check path
    if not os.path.isdir(vidPath):
        raise ValueError('path directory does not exist')  

    # Listing of movie files
    vidList = glob.glob(vidPath + os.path.sep + '*.' + fileExt)

    # Check for video files
    if len(vidList)==0:
        raise ValueError('No movie files found in ' + vidPath) 

    # Initialize output list
    pathList = [];

    # Loop thru and append paths
    for currVid in vidList:
        pathList.extend([currVid])

    return pathList

    