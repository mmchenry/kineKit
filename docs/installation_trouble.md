# Special installations and resolving headaches 

## Removing a failed installation

If the basic installation did not work, first, remove the failed environment installation:

    conda remove --name DEEPLABCUT --all 

## Failures due to wxPython or wxwidgets
    
If the failure was due to some error to wxPython, then open the DLC-GPU.yaml file (which you downloaded in the install process) in a text editor and change 'deeplabcut[gui]' to 'deeplabcut'. 

Then run install again:

    conda env create -f DEEPLABCUT.yaml

Then, install pytorch:

    pip install torch 

At this state ('light mode'), deeplabcut will run at the command line. 
Running any of the guis will require further work. I failed to get the guis to work, but the following steps [were supposed to fix this issue](https://deeplabcut.github.io/DeepLabCut/docs/recipes/installTips.html#troubleshooting-note-if-you-get-a-failed-build-due-to-wxpython-note-this-does-not-happen-on-ubuntu-18-16-etc-i-e).

Install wxpython in the environment:

    conda activate DEEPLABCUT
    conda install -c conda-forge wxpython


<!-- At the time of writing, this installed v. 4.1.1 (found with conda list). This didn't fix the issue, so I tried an earlier version of wxpython:

    conda install -c conda-forge wxpython==4.1.0

I then ran into further difficulties when trying to launch deeplabcut (python -m deeplabcut). -->

<!-- First, I had to downgrade the version of numpy:

     pip install --force-reinstall numpy==1.22

Then, I had to install pytorch:

    pip install torch -->




### Install on a machine that uses Apple Silicon (e.g., M1 MacBook Air)

Follow the same steps, but use the DEEPLABCUT_M1.yaml (download from git [here](https://github.com/DeepLabCut/DeepLabCut/tree/master/conda-environments)) to install an environment for Apple Silicon. 

### Installing DLC 2.1

I have run into some issues installing DLC 2.2 (2.2.1, in particular -- something to do with wxpython). As a workaround, here's how I installed the last version of 2.1 on an Ubuntu machine. 

First, browse to the Downloads folder (cd ~/Downloads) and then download the git repository:

    git clone https://github.com/DeepLabCut/DeepLabCut.git

Then, checkout the last version of 2.1:

    git checkout e2c80479212daea55ff0e39a900ef3678783a11b

Browse to environment files:

    cd DeepLabCut/conda-environments

And create an environment for GPU analyses:

    conda env create -f DLC-GPU.yaml

This last step took some time.

### Further troubleshooting

DLC installation can get kind of hairy, given the variety of possible machines and operating systems. Consult the following websites if you have trouble: [How To Install DeepLabCut](https://deeplabcut.github.io/DeepLabCut/docs/installation.html), and [Installation Tips](https://deeplabcut.github.io/DeepLabCut/docs/recipes/installTips.html).
