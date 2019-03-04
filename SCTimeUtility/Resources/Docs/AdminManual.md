# Administrator manual

## Requirements

Running this program requires Anaconda/Miniconda in order to install the virtual environment. The program was testing with **Miniconda 4.5.11**, but it may also work with older versions of the software.

## Installing the environment

The steps for installing the environment differ depending on the operating system.

### On Windows

If you are using Command Prompt (`cmd`), ensure that `conda`1 can be found in the `%PATH%`. If `conda` is in `%PATH`, or if you are using `conda`'s included "Anaconda Prompt," run the followwing in the root directory of the repository

	conda create -n "timer-utility" --file Install\envBuild_Windows.txt
	
This should craete a `conda` environment named `timer-utility`. The environment can then be activated by using `activate "timer-utility"`. See the **User manual** for more instructions on the running the program.

### On macOS and Linux

From a terminal, run the following in the root directory of the repository

	conda env create -f environment.yml
	
This should craete a `conda` environment named `timer-utility`. The environment can then be activated by using `source activate "timer-utility"`. See the **User manual** for more instructions on running the program.

	
