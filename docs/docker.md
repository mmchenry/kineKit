# Docker in Linux

The DLC people strongly recommend the use of Docker to manage envrionments on Linux. I had some trouble getting the installation to work [as suggested](https://deeplabcut.github.io/DeepLabCut/docs/recipes/installTips.html#installation-on-ubuntu-20-04-lts), but the following steps worked for me.

Open a terminal and run the following commands.

First this:

    sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

Then this:

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

Then this:

    echo \
    "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
Here's where things diverged from the instructions . . .

Run this: 

    sudo apt install apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

And then these

    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu `lsb_release -cs` test"
    sudo apt update
    sudo apt install docker-ce

Do some house cleaning:

     sudo apt autoremove

Then, verify the installation by checking the version:

    docker -v

As an additional check, run the following:

    sudo docker run hello-world

Try to launch Docker:

    deeplabcut-docker gui

If you are like me, you will then have to run the following and try the above command again (which sets an environmental variable for docker to run as sudo):

    export DOCKER="sudo docker"

Once you provide your password, docker should start to download deeplabcut code.

It is alternatively possible (actually, desirable), to run DLC at the command line, which can be initiated like this:

    deeplabcut-docker bash

Once in docker at the command line (the prompt ends in '$'), I entered ipython to run DLC.

Another possibility is to run Jupyter notebooks, like this:

    deeplabcut-docker notebook

However, this is where things ended for me. Within Docker, I cannot access my project files, but instead navigating at the command line gives the impression that one is in an entirely different machine. I'm sure this is by design, but how do I get my needed files into  This leads me to think that maybe 

To gain access to the Docker folder, I had to expand the permissions to all of its contents. I browsed to /var/lib and then changed the permissions as follows (this may be bad security practice, but I'm desperate):

    sudo -Rv chmod o=rwx,g=rwx docker

This did not help. 
I did find that I could copy my DLC files into a container.
First, I found the ID for the container:

    sudo docker container ls

I then used that to copy, as follows:

    sudo docker cp geotaxis-mmchenry-2022-05-25/ 5a44305af233:/geotaxis-mmchenry-2022-05-25

But, when I jumped back to the docker command-prompt, I cannot see the files anywhere.  Where did they go?  I clearly would need to learn more about docker to make this work.
