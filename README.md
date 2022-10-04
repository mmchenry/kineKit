# kineKit

## Overview

Set of tools for acquiring kinematics. 
Current version includes videoTools, which is code for preprocessing video and Jupyter notebooks for a workflow that uses [DeepLabCut (DLC)](http://www.mackenziemathislab.org/deeplabcut), which allows for automated tracking of the coordinates of landmarks.


## videoTools

### [videotools docs](/docs/videotools.md)
Catalog of the videoTools functions.

### [video_preprocess](/notebooks/video_preprocess.ipynb)
Jupyter notebook that illustrates use of the videoTools functions for preprocessing video, including batch processing.


## DeepLabCut
There are numerous ways of using DLC and other tools that we feature, but we're going to recommend a particular workflow with software selected for the task. 
At this stage, we are interested only in single-animal experiments, but intend to implement the ability to extract 3D coordinates from experiments using 2 or more cameras. 
DLC runs most effectively on a desktop computer with a high-powered NVIDIA GPU, but some components of our workflow can be managed on a laptop and the project can be transferred over to the desktop for the serious number crunching. 

The following docs provide details for each aspect of the kineKit workflow for DeepLabCut:

### [Setup & Installation](/docs/dlc_setup.md)

### [Advanced installation tips](/docs/advanced_install.md)

### [Jupyter notebooks](/docs/notebooks.md)

### [Running DLC at the terminal](/docs/command_line.md)

