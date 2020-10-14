
# How to Install GeoPandas vi Ananaconda Navigator

## Install [Anaconda](https://www.anaconda.com/) - Individual edition

Go to the Anaconda web page and read the instructions for downloading and installing the software on your computer.

## Launch Anaconda Navigator

Once installed, Launch Anaconda Navigator. Your interface should look something like the image below.

[ADD IMAGE]

## Go to home > environments > open terminal

Click on the Environments button and open a new terminal window. This will give you access to the command line interface.


[ADD IMAGE]


## Follow the [Geopandas Conda Install Instructions](https://geopandas.org/install.html#creating-a-new-environment)

In the terminal window enter the following lines, one at a time, responding **Y** to any questions.

<pre>
conda create -n geo_env
conda activate geo_env
conda config --env --add channels conda-forge
conda config --env --set channel_priority strict
conda install python=3 geopandas
</pre>


## Install additional Geo packages

In the terminal window - where your geo_env is active -  enter the following lines, one at a time, responding **Y** to any questions.

<pre>
conda install matplotlib
conda install descartes
conda install mapclassify
conda install contextily
conda install geopy
</pre>

## Install Jupyter and Jupter Lab

In the terminal window - where your geo_env is active -  enter the following lines, one at a time, responding **Y** to any questions.

<pre>
conda install jupyterlab
conda install jupyter
</pre>


## And start

Launch Jupyter Notebook or Jupyter Lab from the terminal window of your geo environment (geo_env) or from Anaconda Navigator.
