# geopandas_intro
Intro to Geospatial data in Python with Geopandas for Digital Humanities 101

### Try it on mybinder.org
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/dlab-geo/geopandas_intro/master?filepath=Geopandas_intro.ipynb)


### Try it on Google Collab

Login to **Google Collaboratory** at <https://colab.research.google.com/notebooks/welcome.ipynb>

From the **File** menu select **New Python3 Notebook**

In a blank notebook, copy and paste the following code into a cell

<pre>
x = !ls
print(x)
if str(x).find('geopandas_intro') < 0:
  # Run this once to copy the files from the GITHUB repo to your Google Collab folder
  !git clone https://github.com/dlab-geo/geopandas_intro
else:
  print('You already have the files')
print("Got to the File menu and select Open Notebook > Geopandas_intro_for_gcollab.ipynb to open the notebook in Google Collab")

</pre>

Run the code cell and proceed as directed.
