# DLC at the command line

Running DLC through a Jupyter notebook has limitations because it may not launch an interactive GUI. This can instead be achieved by operating DLC at a terminal command line. As you become familiar with the DLC commands, then you may find it more time-efficient to run DLC at the terminal. 

There are multiple ways of entering DLC from the command line, but in each case, you want to start python from within the DEEPLABCUT environment.

## Launch from the Anaconda Navigator

As explained in our [setup doc](/docs/setup.md), you can launch a terminal window by clicking on 'Open Terminal', which is available from the green arrow next to 'base (root)':

![Open Terminal](/docs/assets/open_terminal.png)


## Open a terminal directly

On a Mac, you can press command-space and then start typing 'terminal', or the Terminal app may be found in 'Utilities' in the applications folder. If you're a linux user, I'm going to assume you know how to open a terminal.

In either case, you enter the deeplabcut environment with this command:

    conda activate <env name>

with 'DEEPLABCUT_M1' (for an M1 Mac) or 'DEEPLABCUT' entered for \<env name\>.

## Starting python

The anaconda installation offers a couple of interfaces for python. We're going to use the version called iPython, which is launched by typing 'ipython'. However, if you are on a mac and want to use any of the DLC GUIs, then you'll instead type 'pythonw'.

## Importing DLC

You can expand on the base-level functionality of python by importing packages, which include a variety of functions. DLC is a package and therefore needs to be first imported to access its functions, like this:

    import deeplabcut as dlc

Note that I've added the 'as dlc' so that we can avoid typing 'deeplabcut' all the time. Note that if you copy code from examples online, then you'll want to convert 'deeplabcut' to 'dlc'.

You can test the installation with one of its commands, like this one:

    dlc.__version__

Most of the DLC functions require the address for the config.yaml file.  So, you'll want to define that, with a command like this:

    configPath = '/Users/mmchenry/Documents/Projects/geotaxis/dlc/geotaxis-mmchenry-2022-05-20/config.yaml'

You can similarly define paths to individual video files or directories of video files. Then you can reference that path definition with commands like this:

    dlc.create_training_dataset(configPath, augmenter_type='imgaug')

