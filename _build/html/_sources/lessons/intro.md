# Welcome to Geospatial Fundamentals in Python: From A to Z to Fancy

## Overview

Geospatial data are an important component of data visualization and analysis in the social sciences, humanities, and elsewhere. The Python programming language is a great platform for exploring these data and integrating them into your research. This JupyterBook explores everything from *A to Z* to get started to work with Geospatial data in Python. We then take you all the way to *fancy* to work with online data sources, basemaps, interactive maps, geocoding, tessellation, and raster data.

### 1. Getting Started with Spatial Dataframes

Part one will introduce basic methods for working with geospatial data in Python using the [GeoPandas library](https://geopandas.org). You will learn how to import and export spatial data and store them as GeoPandas GeoDataFrames (or spatial dataframes). We will explore and compare several methods for mapping the data including the GeoPandas plot function and the matplotlib library. We will review coordinate reference systems and methods for reading, defining and transforming these. 


### 2. Geoprocessing and Analysis

Part two dives deeper into data driven mapping in Python, using color palettes and data classification to communicate information with maps. We will also introduce basic methods for processing spatial data, which are the building blocks of common spatial analysis workflows. 


### 3. Exercises

Part 3 provides two full workflows for you to try to work through on your own. These exercises uses techniques and concepts from both the first and second parts.

### 4. Get Fancy

Part 4 dives builds off of the foundational work from the earlier sections. The topics included involve:
- Reading in online sources data
- Adding basemaps
- Creating interactive maps
- Geocoding addresses
- Using Altair for plotting
- Creating voronoi tessellations
- Starting out with raster data


###  Pre-requisites

#### Knowledge Requirements
You'll probably get the most out of this workshop if you have a basic foundation in Python and Pandas, similar to what you would have from taking the D-Lab Python Fundamentals workshop series. Here are a couple of suggestions for materials to check-out prior to the workshop.

`D-Lab Workshops`:
 - [Python Fundamentals](https://github.com/dlab-berkeley/python-fundamentals)
 - [Pandas](https://github.com/dlab-berkeley/introduction-to-pandas)

`Other`:
 - [Learn Python on Kaggle](https://www.kaggle.com/learn/python)
 - [Programming in Python - Software Carpentry](http://swcarpentry.github.io/python-novice-inflammation/)
 - [Learn Pandas on Kaggle](https://www.kaggle.com/learn/pandas)
 - [Plotting in Python - Software Carpentry](http://swcarpentry.github.io/python-novice-gapminder/)
: Basic knowledge of geospatial data is expected. R experience equivalent to the D-Lab R Fundamentals workshop series is required to follow along with the tutorial. Knowledge of ggplot helpful.

#### Technology Requirements: 

Bring a laptop with Python and the following packages installed: pandas, geopandas, matplotlib, descartes and dependencies. More details are provided on the workshop github page https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python).


## 1.0 Python and Jupyter Notebook installation 

There are many ways to install python and python libraries, distributed as packages, on your computer. Here is one way that we recommend.


* Anaconda installs IDEs and several important packages like NumPy, Pandas, and so on, and this is a really convenient package which can be downloaded and installed.

Anaconda is a free and open-source distribution of Python. Anaconda installs IDEs (integrated development environments, aka where you can write and run code) and several important packages like NumPy and Pandas, making it a really convenient package to use.

### 1.1 Download Anaconda:

Follow this link to download Anaconda: https://www.anaconda.com/distribution. The same link can be used for Mac, Windows, and Linux. 


We recommend downloading the latest version, which will be Python 3.
![downloadinstruc](assets/images/anaconda_download_instructions.png)
    
Open the .exe file that was downloaded and follow the instructions in the installation wizard prompt.

### 1.2 Launch Anaconda and open a Jupyter Notebook

Once installation is complete open Anaconda Navigator and launch Jupyter Notebook. 
![launchnav](assets/images/anaconda_navigator_launch.png)

Jupyter Notebook will open in your web browser (it does not require internet to work). In Jupyter, navigate to the folder where you saved the code file you plan to use and open the .ipynb file (the extension for Jupyter Notebook files written in Python) to view it in the Notebook.

## 2.0 Installing Geopandas

- From within Anaconda Navigator click on the `Environments` selection in the left sidebar menu
> ![anacondanav](assets/images/anaconda1_navigator_home.png)

- Click on the arrow to the right of your `base (root)` environment and select **Open Terminal** 

> ![anacondanav](assets/images/anaconda2_base_open_teriminal.png)

- This will give you access to the command line interface (CLI) on your computer in a window that looks like this:

> ![openterminal](assets/images/anaconda2_base_open_teriminal.png)

- Install some needed software by entering the following commands, one at a time:

```
conda install python=3 geopandas
conda install juypter
conda install matplotlib
conda install descartes
conda install mapclassify
conda install contextily
```
Once you have those libraries all installed you will be able to go to Anaconda Navigator, launch a `Jupyter Notebook`, navigate to the workshop files and run all of the notebooks.


*Optionally you can create a virtual environment In the terminal window, type the **conda** commands shown on the [GeoPandas website](https://geopandas.org/install.html#creating-a-new-environment) for installing Geopandas in a virtual environment. These are:*

````
conda create -n geo_env
conda activate geo_env
conda config --env --add channels conda-forge
conda config --env --set channel_priority strict
conda install python=3 geopandas
````

*After creating your virtual environment, you can process and install the rest of your packages listed above. You will be able to select your `geo_env` in Anaconda Navigator.*



---
<div style="display:inline-block;vertical-align:middle;">
<a href="https://dlab.berkeley.edu/" target="_blank"><img src ="assets/images/dlab_logo.png" width=75 align=left>
</a>
</div>

<div style="display:inline-block;vertical-align:middle;">
    <div style="font-size:larger">&nbsp;D-Lab @ University of California - Berkeley</div>
    <div>&nbsp;Team Geo<div>
</div>
      

