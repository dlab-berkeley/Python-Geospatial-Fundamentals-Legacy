# Welcome to Geospatial Fundamentals in Python

This workshop will teach you how to work with Geospatial Data in Python. 

# 0.0 Pre-requisites
You'll probably get the most out of this workshop if you a basis in Python and Pandas. Here are a couple of suggestions for materials to check-out prior to the workshop.

D-Lab Workshops:
 - [Python Fundamentals](https://github.com/dlab-berkeley/python-fundamentals)
 - [Pandas](https://github.com/dlab-berkeley/introduction-to-pandas)

Other:
 - [Learn Python on Kaggle](https://www.kaggle.com/learn/python)
 - [Programming in Python - Software Carpentry](http://swcarpentry.github.io/python-novice-inflammation/)
 - [Learn Pandas on Kaggle](https://www.kaggle.com/learn/pandas)
 - [Plotting in Python - Software Carpentry](http://swcarpentry.github.io/python-novice-gapminder/)


# 1.0 Python and Jupyter Notebook installation 
* Anaconda installs IDEs and several important packages like NumPy, Pandas, and so on, and this is a really convenient package which can be downloaded and installed.

Anaconda is a free and open-source distribution of Python. Anaconda installs IDEs (integrated development environments, aka where you can write and run code) and several important packages like NumPy and Pandas, making it a really convenient package to use.

### 1.1 Download Anaconda:
Follow this link to download Anaconda: https://www.anaconda.com/distribution/#windowsDownload. The same link can be used for Mac, Windows, and Linux. 

We recommend downloading the latest version, which will be Python 3. There is a lot of code written in Python 2 but support for that version is ending this year and will be difficult to work with in the future.
<img src="../assets/images/anaconda_download_instructions.png" width="650">
    
Open the .exe file that was downloaded and follow the instructions in the installation wizard prompt.

### 1.2 Launch Anaconda and open a Jupyter Notebook

Once installation is complete open Anaconda Navigator and launch Jupyter Notebook. 

<img src="../assets/images/anaconda_navigator_launch.png" width="650">

Jupyter Notebook will open in your web browser (it does not require internet to work). In Jupyter, navigate to the folder where you saved the code file you plan to use and open the .ipynb file (the extension for Jupyter Notebook files written in Python) to view it in the Notebook.

# 2.0 Installing Geopandas

To install GeoPandas on your own computer, see the instructions on the [GeoPandas.org](https://geopandas.org) website.

However, you may have problems if you already have any of the underlying libraries installed and the versions do not match what is needed by the current version of Geopandas.  

If that is the case, then see this helper file: `installing_geopandas_tips.md`

If that is the case, we suggest you install Geopands in it's own [conda virtual Python environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).

To do this:

1. Close all Jupyter notebooks.
2. Make sure you download the file `geo_environment.yml`
3. In a text editor take a look at the contents of the `yml` file. This lists all the packages that will be installed in this virtual environment. You can add or remove if you like.
3. Open a terminal window in the folder that contains the `yml` file and run the following commands

<pre>
$ conda env create -f geo_environment.yml
$ conda activate geo_env 
</pre>

Once you activate the environment your notebooks will have access to all the packages installed therein.

However, once you close the terminal window you will exit this virtual environment and return to your base Python environment. That means you need to activate the environment each time you want to run the geo notebooks.
