# Advanced installation tips

All of the instructions below are executed at a Linux terminal, but should be adaptable to Windows.

## Anaconda installation 

DeepLabCut requires Anaconda, which is a Python package for scientific computing.  Each account requires its own anaconda installation.  Here are the steps for installation:

1. Within the terminal, update the command-line installer (note: ‘sudo’ executes commands as an administrator): 

        sudo apt-get update

1. Then, download packages that are needed to run GUI packages.  This is all probably already installed, but good to do, just in case: 

        apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6

1. Download the 64-bit (x86) [Anaconda installer for Python 3.7](https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh)

1. In the terminal, run the installer script that you just downloaded, which presently looks like this (note that the ~ symbol is a shortcut for one’s home folder): 

        bash ~/Downloads/Anaconda3-2020.02-Linux-x86_64.sh

1. Respond in the affirmative to the license agreement and be sure to install anaconda at ~/anaconda3. Also, respond with a “yes” to the question “Do you wish the installer to initialize Anaconda3 by running conda init?”

1. If that question did not pop up, then you can initialize conda by typing (note: change path, if you installed in a different directory): 

        source ~/anaconda3/bin/activate 

1. And then type: 

        conda init

1. Close your terminal window and open another to access anaconda’s functionality.

1. Test the installation by typing cd ~ and then conda list at the command line.  If it gives a listing of packages, then you are all set -- anaconda is accessible from the command line.  If it gives you an error message then tell Matt and we’ll try to troubleshoot the problem.

## CUDA 

DeepLabCut uses deep learning neural networks to track landmarks. In particular, it relies on Tensorflow, which is a deep learning toolbox developed by Facebook.

Deep learning works best when run on a GPU. I believe that NIVIDIA GPUs are the only ones supported by Tensorflow. NVIDIA has developed low-level software called CUDA to control the GPUs.  DeepLabCut, like all deep learning code, runs only on certain versions of tensorflow and CUDA.  The Lambda computers ship with CUDA, so an installation should not be necessary.  

Check that your system is using a compatible version of CUDA with the following terminal command: 

    nvcc --version 

If the nvcc command is not recognized, then the system probably needs a CUDA install.  Check with Matt if you are using one of the Lambda computers.  If this is another system, then follow the [CUDA installation instructions](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html)

At the time of this writing, DeepLabCut does not support versions of CUDA above 10.0, so check with Matt about changing versions, if needed.

## DeepLabCut

A lot of python coding relies on open-source packages and updates to these packages will often not be backward compatible. So, it’s best to be able to control the version of the package that you are working with and to have that code not change as the packages are updated. 

To control the packages this, people use ‘environments’, which control the versions of code used for a particular project. The developers of DLC offer their own environment that is assured of working with DLC.  So, the steps below entail downloading DLC and setting up its compatible environment:

1. I have been placing the DLC code in the anaconda environments directory, which is probably not required, but it works.  So, browse to that in the terminal: 

        cd ~/anaconda3/envs

1. Download the DLC code at this location: 

        git clone https://github.com/DeepLabCut/DeepLabCut.git

1. Browse to the DLC environments:

        cd DeepLabCut/conda-environments

1. Set up the environment:

        conda env create -f DEEPLABCUT.yaml

1. If creating env fails due to wxpython run the following:
        
        conda remove --name DEEPLABCUT --all 

1. open the DLC-GPU.yaml file (any text editor!) and change deeplabcut[gui] to deeplabcut. Then run: 

        conda env create -f DEEPLABCUT.yaml

1. Now, make a DLC projects folder in your documents folder and browse to it:

        mkdir ~/Documents/deeplabcut
        mkdir ~/Documents/deeplabcut/test
        cd ~/Documents/deeplabcut/test

1. Test that your environment is accessible:

        conda activate DEEPLABCUT

1. If everything worked, then your terminal prompt should begin with “DEEPLABCUT”.

1. Now, you should be able to run the gui for DLC as follows:

        python -m deeplabcut