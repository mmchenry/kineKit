# Setup & Installation for DeepLabCut

Here we explain some of the tools that you will want to install and configure for DLC and kineKit.

## Anaconda

kineKit and DLC use Python, which is a popular scripting language that can be used to operate lower-level compiled software.
We aspire to make kineKit usable for people with no prior exposure to Python.
Python code is generally written in text files (with a 'py' extension) that are run by an interpreter, which translates the text into lower-level machine code to perform the requested tasks. 

Whether you are setting up on a desktop or labtop computer, we'll assume that you are running software that is based on [Anaconda](https://www.anaconda.com). An anaconda installation includes python interpreters, as well as packages for scientific computing. Packages are python code that expand the set of functions available. For example, Anaconda includes the packages 'Numpy', for mathematical operations, 'Pandas', for organizing data, and 'Matplotlib', for visualizing data. Anaconda is easy to install for MacOS, Windows, or Linux from their [website](https://www.anaconda.com) and we will henceforth assume that you have performed that installation. Once installed, the Anaconda-Navigator provides a GUI gateway for python tools.

## Environments

Open-source software frequently draws on code from other packages. For example, Pandas uses Numpy as a basis for calculations that are performed upon a tabulated organization of data. As a consequence, updates to one package can introduce errors when called by a package that was assuming an earlier version of the code. These dependencies between packages can become a nightmare to maintain if you are running different code that assumes a variety of versions of the same package. 

Environments provide a means to manage versions of packages that are compatible with one-another. When you run python code within a particular environment, it uses a specific  version of the python interpreter and versions of the packages that have been explicity installed. Anaconda comes with a 'base' environment and if you browse to that in the Anaconda Navigator, then you can see all of the packages and their version number included in the base installation. In preparation for kineKit and DLC, you will want to launch a terminal window from within that environment by clicking on 'Open Terminal', which is available from the green arrow next to 'base (root)':

![Open Terminal](assets/open_terminal.png)

There are different programs for installing and managing packages within an environment using commands within a terminal window. Anaconda uses the 'Conda' package manager by default. 'pip' is another one.

You may enter an environment at the command line:

    conda activate <env name>

Where \<env name\> corresponds to the title of the DLC environment (e.g., DEEPLABCUT, DEEPLABCUT_M1).

## Docker

An alternative to conda environments is Docker, which the DLC people recommend for Linux installations. I cound not get it to work, but my partial instructions for that can be found [here](/docs/docker.md).

## DeepLabCut (DLC)

### Machine that does NOT use Apple Silicon

As explained in the documentation for a Conda [DLC installation](https://deeplabcut.github.io/DeepLabCut/docs/installation.html), you can create an environment for DLC by first downloading the conda file from [here](http://www.mackenziemathislab.org/s/DEEPLABCUT.yaml). Then launch a terminal window (see above), and (using the 'cd' command) browse to the directory containing the download. On my machine, I did that as follows:

    cd ~/Downloads

On Linux, run the following (this is to fix trouble with wxWidgets):

    conda install -c conda-forge gtk3

The, enter the following command into at the terminal window:

    conda env create -f DEEPLABCUT.yaml

This should install an envronment called DEEPLABCUT that you will use henceforth to run DLC and kineKit code. You can launch a terminal from within that environment following the same steps described above for the base environment.

If this did not work, then check out [Special installations and resolving headaches ](/docs/installation_trouble.md).

## ffmpeg

ffmpeg is an open-source project that allows for the conversion of video files. It should be installed in the DLC environment (as explained above). To check, query for the version at the command line when within the environment:

    ffmpeg --version

If ffmpeg is not installed . . .

For MacOS, you first need to install the Homebrew package manager:

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

Then, install ffmpeg:

    brew install ffmpeg

For linux, simply run the following command at the terminal: 

    sudo apt install ffmpeg

Windows is more complicated, but its steps are detailed [here](https://www.wikihow.com/Install-FFmpeg-on-Windows).

## VS Code

Microsoft's Visual Studio Code (VS Code) is an Integrated Development Environment (IDE) that allows for the composition and running of code in a variety of languages. We will use VS Code to run kineKit and DLC. Because it has the ability to work with so many languages, VS Code requires the installation of some extensions to code in Python and to edit some of the file types that are going to be useful for DLC. 

Start by downloading an installing VS Code from [here](https://code.visualstudio.com).

Launch the program and click on the Extensions tab on the left. Then search for, and install, the following extensions:

1. Python (Microsoft).
1. Jupyter (Microsoft).
1. YAML (Red Hat).

These packages will allow you to read and edit the following useful files for kineKit and DLC: .py, .ipynb, .yaml. You might adjust your file browser to launch VS Code for these file types.

If you envision yourself editing the python code, then I also recommend doing the following:

1. Open Settings in VS Code
1. Search for 'jupyter runstart' and then click on the link to edit 'settings.json'
1. Edit the settings to include the following: 

    "jupyter.runStartupCommands": [
    "%load_ext autoreload", "%autoreload 2"
],

The json file should look something like this:

![json settings](assets/json_set.png)

The reason for this configuration is that VS Code will now reload a package whenever you make changes and save the code. You otherwise have to restart the kernel to load a package, which gets irritating.

When running code in VS Code, you'll want to specify that you will be running it in your DLC environment, which should be an option in the upper right corner of the window when you open a .py or .ipynb file, like this:

![VC Vode window](assets/vs_code_env.png) 

## Github

Github Source Control Provider (SCP), which is a cloud service for hosting code using the Git version control system. There's lots to learn about the workings of Git and the use of Github, but for the moment think of it as a means of distribution of kineKit and DLC. 

You can simply download the latest version of the kineKit code in a ZIP archive from its [gitHub page](https://github.com/mmchenry/kineKit.git). The more advanced approach is to create a github account and to configure VS Code to download the latest versions of kineKit (outlined [here](https://code.visualstudio.com/docs/editor/versioncontrol)). A download from the cloud is accomplished by a 'Pull' command from the GitHub servers. VS Code has a 'Source Control' tab on the left-hand pallet for managing Pulls and to monitor the status of files in your local copy of the 'archive'. The archive is the current version of the code, as well as its entire history of versions.