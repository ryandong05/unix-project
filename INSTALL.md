# How to install Movie Recommender

## Step 1.1
### Install Kodi on Raspberry Pi:
- Start up Raspberry Pi via instruction manual
- when booting, select LibreELEC (Kodi) as OS
- The Raspberry Pi will now boot as Kodi

## Step 1.2
### Install Netflix:
- Download Castagnait add-on repository (https://github.com/CastagnaIT/repository.castagnait) and put it somewhere on the Raspberry Pi
- Within Kodi:
    - Go to Settings > System > Add-Ons and toggle on Unknown sources
    - Go to Add-Ons > Install from zipfile > [Select Castagnait .zip]
    - Navigate to Add-ons > Install from repository > CastagnaIT Repository > Video add-ons > Netflix.
    - Log into Netflix with credentials (If you require an authorization key, just refer to the CastagnaIT repository from earlier.)

#### *Once set up, Netflix will create the MyVideos75.db SQLite database to store watch history.*

#### *NOTE: For all paths within the script and such, you must edit the paths based on your system. You can easily do so by just browsing the files through the Kodi GUI*

## Step 1.3
### Create Docker on Raspberry Pi in order to run python script:
- Install Docker add-on on Kodi (Go to Add-Ons > Search > 'Docker' and install)

- Connect to the raspberry pi via ssh (whichever way you want) (since im Windows I am using PuTTY for ssh)
    - root password will be 'libreelec' by default but you can easily change that through the Kodi GUI

- Pull and Create a python based Docker Container
    - ex: docker pull python (since it comes prepackaged with all the modern dependencies needed for ML)

- Create a Persistent Directory for Your Script Create a directory on the Raspberry Pi to store your script, data, and models:
    - ex: mkdir -p /storage/python-projects
    
- Copy your script and necessary files (e.g., metadata.csv, tfidf_matrix.pkl, and database .db file) to this directory:
    - ex: scp /path/to/your/script.py root@<raspberry-pi-ip>:/storage/python-projects/
          scp /path/to/your/csv_and_pickle_files root@<raspberry-pi-ip>:/storage/python-projects/
    NOTE: Update paths to MovieRecommenderScript.py depending on where the MyVideos75.db file is, where you put the CSV, script files, and etc. on your version of Kodi

    #### *But if you are on Windows device using PuTTY like me, download pscp.exe from PuTTY's website and use pscp instead but in cmd.exe*
    - ex: pscp C:\path\to\file\ root@10.0.0.149:/tvshows

- Run a Container and Mount the Directory Start a container using the python:3.9-slim image and mount the directory for persistent storage:
    - ex: docker run -it --name recommendation-engine \
            -v /storage/python-projects:/app \
            python /bin/bash

- Install Dependencies in the Container
    - ex: pip install pandas scikit-learn sqlite3 email_validator

## Step 1.4
### Make the Script Persistent
- Detach the Container: Run the container in detached mode:
    - docker run -d --name recommendation-engine \
        -v /storage/python-projects:/app \
        python python /app/<your-script-name>.py

- Restart on Reboot: Configure Docker to restart the container on system boot:
    - docker update --restart always recommendation-engine

#### *And I pray that it works for you :)*  

#### *However, this method might not work when trying to install dependencies (pandas and scikit-learn in particular), so you can also try a Ubuntu or Debian based image as so:*


# Step 2.1: Pull the Ubuntu Image
Pull the official Ubuntu 24.04 image:
- docker pull ubuntu:24.04

## Step 2.2: Run and Set Up the Container
Create and start a Docker container with a mounted directory for your project files:
- docker run -it --name recommendation-engine \
  -v /storage/python-projects:/app \
  ubuntu:24.04 /bin/bash

## Step 2.3: Set Up the Environment Inside the Container
Update the Package Manager: Update and upgrade system packages:
- apt update && apt upgrade -y

Install Python and Essential Tools: Install Python 3, pip, and other essential tools for building Python packages:
- apt install -y python3 python3-pip python3-venv build-essential libatlas-base-dev libopenblas-dev

Create a Virtual Environment: Create a Python virtual environment within the mounted /app directory:
- python3 -m venv /app/venv

Install pandas and scikit-learn (pray it works for you): 
- apt-install python3-pandas
- apt-install python3-scikit-learn

## Step 2.4: Detach the Container: Run the container in detached mode to allow it to execute in the background:
- docker run -d --name recommendation-engine \
  -v /storage/python-projects:/app \
  ubuntu:24.04 bash -c "source /app/venv/bin/activate && python /app/your_script.py"

**Ensure Restart on Reboot:** Configure Docker to restart the container automatically:
- docker update --restart always recommendation-engine

#### *BUT OF COURSE! Again, installing scikit-learn doesn't work for me as shown above, so if it's the same for you, try manually cloning the packages from git, and running the docker through :*

**IMPORTANT**-Build scikit-learn from Source:

## Step 3.1: Install Build Tools:
- apt install -y build-essential python3-dev python3-pip gfortran libatlas-base-dev

## Step 3.2: Clone the scikit-learn Repository:
- git clone https://github.com/scikit-learn/scikit-learn.git

Install Build Tools (if not already installed): Ensure that necessary tools for building Python packages are installed:
- apt update
- apt install -y build-essential python3-dev python3-pip

## Step 3.3 Clone the Cython Repository: Use Git to clone the Cython source code (needed for scikit-learn):
- git clone https://github.com/cython/cython.git
- cd cython

Build and Install Cython: Build Cython from source:
- python3 setup.py build
- python3 setup.py install

## Step 3.4 Go back to scikit-learn directory and install it through venv:
- source /app/venv/bin/activate
- pip3 install .

**IMPORTANT**: Ensure your project files (script, database, CSV, pickle files, etc.) are in the /storage/python-projects directory on your Raspberry Pi. These files will now be accessible in the container under /app.
- scp /path/to/your_script.py root@<raspberry-pi-ip>:/storage/python-projects/
- acp /path/to/netflix_data.csv root@<raspberry-pi-ip>:/storage/python-projects/
- scp /path/to/tfidf_matrix.pkl root@<raspberry-pi-ip>:/storage/python-projects/
- scp /path/to/MyVideos75.db root@<raspberry-pi-ip>:/storage/python-projects/

## Step 3.5 Automate Script Execution:
Detach the Container: Run the container in detached mode to allow it to execute in the background:
- docker run -d --name recommendation-engine \
    -v /storage/python-projects:/app \
    ubuntu:24.04 bash -c "source /app/venv/bin/activate && python /app/your_script.py"

Ensure Restart on Reboot: Configure Docker to restart the container automatically:
- docker update --restart always recommendation-engine

#### *AND IF EVEN THAT FAILS, it might be due to that since you are within a venv, you cannot execute pip commands, so as the terminal might've told you, you must use apt install and etc.*
#### *Therefore, running 'pip3 install .' will not be feasable. So you might say why not use 'python3 install setup.py build' like how we did for cython. Great suggestion! Except of course the latest version of scikit-learn does not contain a setup.py file. So now what you must do is:*

## Step 4.1: Find a version of scikit-learn that contains a setup.py file:
- Go through the versions of git, pick random versions, download the source code and try to find one that has it.
- Then repeat the steps done in Step 3.X to clone it locally onto the container.

## Step 4.2: Pray and install:
Like with cython, within the scikit-learn directory, you can now run:
- python3 setup.py build
- python3 setup.py install
But for me personally, it told me that I needed numpy installed to install scikit-learn. Thing is, I did :)
So this marks the point where I, Ryan Dong, officially gave up and admitted defeat.

**IMPORTANT:** And if all else fails like for me, trying using OSMC Kodi, as it is another Kodi distribution, except with additional functionalities that may allow installation of the necessary dependencies.

**BUT ENSURE:**
- It is a 64-bit instance of OSMC, as a full python environment that can run a ML model requires it to be 64-bit (if you try 32-bit python won't be able to find scikit-learn or potentially pandas)
- To build on the previous bullet point, OSMC Versions are tailored to specific Raspberry Pi models, so in my case (RPi4), there are no 64-bit OSMC versions available so I cannot try this method
And if you meet the necessary requirements Steps 1.X should work for you.

Enjoy :)