# Notebooks

We've organizated the workflow for prepping videos and running DLC with python code that is organized in notebooks. A notebook is an interactive interface for running code and a popular Python format for this is known as a 'Jupyter notebook' (file extenion '.ipynb'). We've stored jupyter notebooks for kineKit in the 'notebooks' directory within the root kineKit directory.

Here's a listing of the notebooks and their major functions:

1. [video_preprocess](/notebooks/video_preprocess.ipynb) - For prepping video for DLC using videoTools. 
The code can handle image sequences or stand-alone video files and also allow for the selection of a region-of-interest. 
It is a very good idea to compress and downsample movies before using them to train DLC.

1. [dlc_run](/notebooks/dlc_run.ipynb) - Steps through an initial DLC training and acquisition of coordinates.

1. [dlc_evaluate](/notebooks/dlc_evaluate.ipynb) - Evaluates the network, improves it, and uses it to analyze new videos. 