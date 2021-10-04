# Lesson 2. Introduction to Geopandas

In this lesson we'll learn about a package that is core to using geospatial data in Python. We'll go through the structure of the data (it's not too different from regular DataFrames!), geometries, shapefiles, and how to save your hard work.

- 2.1 What is GeoPandas?
- 2.2 Read in a shapefile
- 2.3 Explore the GeoDataFrame
- 2.4 Plot the GeoDataFrame
- 2.5 Subset the GeoDataFrame
- 2.6 Save your data
- 2.7 Recap
- **Exercise**: IO, Manipulation, and Mapping

<br>
<font color='grey'>
    <b>Instructor Notes</b>

- Datasets used
    - 'notebook_data/california_counties/CaliforniaCounties.shp'
    - 'notebook_data/census/Places/cb_2018_06_place_500k.zip'

- Expected time to complete
    - Lecture + Questions: 30 minutes
    - Exercises: 5 minutes
</font>

## 2.1 What is GeoPandas?

### GeoPandas and related Geospatial Packages

[GeoPandas](http://geopandas.org/) is a relatively new package that makes it easier to work with geospatial data in Python. In the last few years it has grown more powerful and stable. This is really great because previously it was quite complex to work with geospatial data in Python. GeoPandas is now the go-to package for working with `vector` geospatial data in Python. 

> **Protip**: If you work with `raster` data you will want to checkout the [rasterio](https://rasterio.readthedocs.io/en/latest/) package. We will not cover raster data in this tutorial.

### GeoPandas = pandas + geo
GeoPandas gives you access to all of the functionality of [pandas](https://pandas.pydata.org/), which is the primary data analysis tool for working with tabular data in Python. GeoPandas extends pandas with attributes and methods for working with geospatial data.




### Import Libraries

Let's start by importing the libraries that we will use.

import pandas as pd
import geopandas as gpd

import matplotlib # base python plotting library
import matplotlib.pyplot as plt # submodule of matplotlib

# To display plots, maps, charts etc in the notebook
%matplotlib inline  

## 2.2 Read in a shapefile

As we discussed in the initial geospatial overview, a *shapefile* is one type of geospatial data that holds vector data. 

> To learn more about ESRI Shapefiles, this is a good place to start: [ESRI Shapefile Wiki Page](https://en.wikipedia.org/wiki/Shapefile) 

The tricky thing to remember about shapefiles is that they're actually a collection of 3 to 9+ files together. Here's a list of all the files that can make up a shapefile:
 
>`shp`: The main file that stores the feature geometry
>
>`shx`: The index file that stores the index of the feature geometry  
>
>`dbf`: The dBASE table that stores the attribute information of features 
>
>`prj`: The file that stores the coordinate system information. (should be required!)
>
>`xml`: Metadata —Stores information about the shapefile.
>
>`cpg`: Specifies the code page for identifying the character set to be used.

But it remains the most commonly used file format for vector spatial data, and it's really easy to visualize in one go!

Let's try it out with California counties, and use `geopandas` for the first time. `gpd.read_file` is a flexible function that let's you read in many different types of geospatial data.

# Read in the counties shapefile
counties = gpd.read_file('notebook_data/california_counties/CaliforniaCounties.shp')

# Plot out California counties
counties.plot()

Bam! Amazing! We're off to a running start.

## 2.3 Explore the GeoDataFrame

Before we get in too deep, let's discuss what a *GeoDataFrame* is and how it's different from `pandas` *DataFrames*.

### The GeoPandas GeoDataFrame

A [GeoPandas GeoDataFrame](https://geopandas.org/data_structures.html#geodataframe), or `gdf` for short, is just like a pandas dataframe (`df`) but with an extra geometry column and methods & attributes that work on that column. I repeat because it's important:

> `A GeoPandas GeoDataFrame is a pandas DataFrame with a geometry column and methods & attributes that work on that column.`

> This means all the methods and attributes of a pandas DataFrame also work on a Geopandas GeoDataFrame!!

With that in mind, let's start exploring out dataframe just like we would do in `pandas`.

# Find the number of rows and columns in counties
counties.shape

# Look at the first couple of rows in our geodataframe
counties.head()

# Look at all the variables included in our data
counties.columns

It looks like we have a good amount of information about the total population for different years and the densities, as well as race, age, and occupancy info.

## 2.4 Plot the GeoDataFrame

We're able to plot our GeoDataFrame because of the extra `geometry` column.

### Geopandas Geometries
There are three main types of geometries that can be associated with your geodataframe: points, lines and polygons:

<img src ="assets/images/fig_create4.png" width="600"></img>

In the geodataframe these geometries are encoded in a format known as [Well-Known Text (WKT)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry). For example:

> - POINT (30 10)
> - LINESTRING (30 10, 10 30, 40 40)
> - POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))
>
> *where coordinates are separated by a space and coordinate pairs by a comma*

Your geodataframe may also include the variants **multipoints, multilines, and multipolgyons** if the row-level feature of interest is comprised of multiple parts. For example, a geodataframe of states, where one row represents one state, would have a POLYGON geometry for Utah but MULTIPOLYGON for Hawaii, which includes many islands.

> It's ok to mix and match geometries of the same family, e.g., POLYGON and MULTIPOLYGON, in the same geodatafame.




<img src="http://www.pngall.com/wp-content/uploads/2016/03/Light-Bulb-Free-PNG-Image.png" width="20" align=left >  **Question** What kind of geometry would a roads geodataframe have? What about one that includes landmarks in the San Francisco Bay Area?




Your response here:






You can check the types of geometries in a geodataframe or a subset of the geodataframe by combining the `type` and `unique` methods.

# Let's check what geometries we have in our counties geodataframe
counties['geometry'].head()

# Let's check to make sure that we only have polygons and multipolygons 
counties['geometry'].type.unique()

counties.plot()

Just like with other plots you can make in Python, we can start customizing our map with colors, size, etc.

# We can run the following line of code to get more info about the parameters we can specify:

?counties.plot

# Make the figure size bigger
counties.plot(figsize=(6,9))

counties.plot(figsize=(6,9), 
              edgecolor='grey',  # grey colored border lines
              facecolor='pink' , # fill in our counties as pink
              linewidth=2)       # make the linedwith a width of 2

## 2.5 Subset the GeoDataframe

Since we'll be focusing on Berkeley later in the workshop, let's subset our GeoDataFrame to just be for Alameda County.

# See all county names included in our dataset
counties['NAME'].values

It looks like Alameda county is specified as "Alameda" in this dataset.

counties

Now we can create a new geodataframe called `alameda_county` that is a subset of our counties geodataframe.

alameda_county = counties.loc[counties['NAME'] == 'Alameda'].copy().reset_index(drop=True)

# Plot our newly subsetted geodataframe
alameda_county.plot()

Nice! Looks like we have what we were looking for.

*FYI*: You can also make dynamic plots of one or more county without saving to a new gdf.

bay_area_counties = ['Alameda', 'Contra Costa', 'Marin', 'Napa', 'San Francisco', 
                        'San Mateo', 'Santa Clara', 'Santa Cruz', 'Solano', 'Sonoma']
counties.loc[counties['NAME'].isin(bay_area_counties)].plot()


## 2.6 Save your Data

Let's not forget to save out our Alameda County geodataframe `alameda_county`. This way we won't need to repeat the processing steps and attribute join we did above.

We can save it as a shapefile.

alameda_county.to_file("outdata/alameda_county.shp")

One of the problems of saving to a shapefile is that our column names get truncated to 10 characters (a shapefile limitation.) 

Instead of renaming all columns with obscure names that are less than 10 characters, we can save our GeoDataFrame to a spatial data file format that does not have this limation - [GeoJSON](https://en.wikipedia.org/wiki/GeoJSON) or [GPKG](https://en.wikipedia.org/wiki/GeoPackage) (geopackage) file.
- These formats have the added benefit of outputting only one file in contrast tothe multi-file shapefile format.

alameda_county.to_file("outdata/alameda_county.json", driver="GeoJSON")

alameda_county.to_file("outdata/alameda_county.gpkg", driver="GPKG")

You can read these in, just as you would a shapefile with `gpd.read_file`

alameda_county_test = gpd.read_file("outdata/alameda_county.gpkg")
alameda_county_test.plot()

alameda_county_test2 = gpd.read_file("outdata/alameda_county.json")
alameda_county_test2.plot()

There are also many other formats we could use for data output.

**NOTE**: If you're working with point data (i.e. a single latitude and longitude value per feature),
then CSV might be a good option!

## 2.7 Recap

In this lesson we learned about...
- The `geopandas` package 
- Reading in shapefiles 
    - `gpd.read_file`
- GeoDataFrame structures
    - `shape`, `head`, `columns`
- Plotting GeoDataFrames
    - `plot`
- Subsetting GeoDatFrames
    - `loc`
- Saving out GeoDataFrames
    - `to_file`

## Exercise: IO, Manipulation, and Mapping

Now you'll get a chance to practice the operations we learned above.

In the following cell, compose code to:

1. Read in the California places data (`notebook_data/census/Places/cb_2018_06_place_500k.zip`)
2. Subset the data to Berkeley
3. Plot, and customize as desired
4. Save out as a shapefile (`outdata/berkeley_places.shp`)


*Note: pulling in a zipped shapefile has the same syntax as just pulling in a shapefile. The only difference is that insead of just putting in the filepath you'll want to write `zip://notebook_data/census/Places/cb_2018_06_place_500k.zip`*

To see the solution, double-click the Markdown cell below.

# YOUR CODE HERE



## Double-click to see solution!

<!--
# SOLUTION

# 1. Read in the California places data 
california_places = gpd.read_file('zip://notebook_data/census/Places/cb_2018_06_place_500k.zip')
california_places.head()

# 2. Subset the data to Berkeley
berkeley_places = california_places.loc[california_places['NAME']=='Berkeley'].copy().reset_index(drop=True)

# 3. Plot and customize
berkeley_places.plot(edgecolor='grey', color='lightgreen')

# 4. Save to a shapefile
berkeley_places.to_file("outdata/berkeley_places.shp")

-->

---
<div style="display:inline-block;vertical-align:middle;">
<a href="https://dlab.berkeley.edu/" target="_blank"><img src ="assets/images/dlab_logo.png" width="75" align="left">
</a>
</div>

<div style="display:inline-block;vertical-align:middle;">
    <div style="font-size:larger">&nbsp;D-Lab @ University of California - Berkeley</div>
    <div>&nbsp;Team Geo<div>
</div>
        

