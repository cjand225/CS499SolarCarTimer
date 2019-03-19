# Administrator manual

## Requirements

It is recommended that a virtual environment be used for creating the dev environment and an IDE be used for project management.

You may use ones like Anaconda Package Manager, Pipenv, venv, etc.

Anaconda was originally used to create and manage the environment for this project, as well as Pycharm for an IDE.

### Packages:
        -numpy >= 1.15.4
        -matplotlib >= 2.2.3
        -PyQt5 >= 5.6.0
        -opencv-contrib-python >= 3.4.3
        -pywin32 >= 1.0; platform_system == "Windows"

# Creating Environment

#### Creating a Clean Environment

First, create the environment using:

    conda create -n <name>
    
Activate it using:

    conda activate <name>
    
Then install the packages (from the package list) using either `pip` or `conda`:

    conda install <package-name>
    pip install <package-name>
    
    
After installing all the required packages, run (in the project folder):

    python -m SCTimeUtility
    
_Note: If using conda to install packages, you may want to use [conda-forge](https://conda-forge.org) as the package provider._


#### Creating from pre-existing environement list

      conda create -n <name> --file <envFileName>

# Building Package

### Building from Source

To build the program package (depending on what platform you want):

Python Wheel (Cross-Platform):
    
    python setup.py -bdist_wheel

EXE (Windows):

    python setup.py -bdist_wininst

MSI (Windows):

    python setup.py -bdist_msi

RPM (Linux):

    python setup.py -bdist_rpm
    