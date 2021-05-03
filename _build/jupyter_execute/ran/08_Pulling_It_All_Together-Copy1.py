# 08. Pulling it all Together

For this last lesson, we'll practice going through a full workflow!! We'll answer the question:
## What is the total grocery-store sales volume of each census tract?


### WORKFLOW:

<br>
Here's a set of steps that we will implement in the labeled cells below:

<u> 8.1 Read in and Prep Data</u>
- read in tracts acs joined data
- read our grocery-data CSV into a Pandas DataFrame (it lives at `'notebook_data/other/ca_grocery_stores_2019_wgs84.csv`)
- coerce it to a GeoDataFrame
- define its CRS (EPSG:4326)
- transform it to match the CRS of `tracts_acs_gdf_ac`
- take a peek

<u>8.2 Spatial Join and Dissolve</u>
- join the two datasets in such a way that you can then...
- group by tract and calculate the total grocery-store sales volume
- don't forget to check the dimensions, contents, and any other relevant aspects of your results

<u>8.3 Plot and Review</u>
- plot the tracts, coloring them by total grocery-store sales volume
- plot the grocery stores on top
- bonus points for devising a nice visualization scheme that helps you heuristically check your results!



### INSTRUCTIONS:
**We've written out some of the code for you, but you'll need to replace the ellipses with the correct
content.**

*You can check your answers by double-clicking on the Markdown cells where indicated.*


<br>
<font color='grey'>
    <b>Instructor Notes</b>

- Datasets used
    - 'outdata/tracts_acs_gdf_ac.json'
    - 'notebook_data/other/ca_grocery_stores_2019_wgs84.csv'

- Expected time to complete
    - Lecture + Questions: N/A
    - Exercises: 30 minutes
</font>



-----------------


---------------------------------------


### Install Packages

import pandas as pd
import geopandas as gpd

import matplotlib # base python plotting library
import matplotlib.pyplot as plt # submodule of matplotlib

# To display plots, maps, charts etc in the notebook
%matplotlib inline  

------------------

## 8.1 Read in the Prep Data

We first need to prepare our data by loading both our tracts/acs and grocery data, and conduct our usual steps to make there they have the same CRS.

- read in our tracts acs joined data 
- read our grocery-data CSV into a Pandas DataFrame (it lives at `'notebook_data/other/ca_grocery_stores_2019_wgs84.csv`)
- coerce it to a GeoDataFrame
- define its CRS (EPSG:4326)
- transform it to match the CRS of `tracts_acs_gdf_ac`
- take a peek



# read in tracts acs data

tracts_acs_gdf_ac = gpd.read_file(..)

# read our grocery-data CSV into a Pandas DataFrame

grocery_pts_df = pd.read_csv(...)

# coerce it to a GeoDataFrame

grocery_pts_gdf = gpd.GeoDataFrame(grocery_pts_df, 
                                   geometry=gpd.points_from_xy(...,...))

# define its CRS (NOTE: Use EPSG:4326)

grocery_pts_gdf.crs = ...

# transform it to match the CRS of tracts_acs_gdf_ac

grocery_pts_gdf.to_crs(..., inplace=...)

# take a peek

print(grocery_pts_gdf.head())

## Double-click here to see solution!

<!--

# SOLUTION:

########################
# read in and prep data:
#-----------------------
# read in tracts acs data
tracts_acs_gdf_ac = gpd.read_file('outdata/tracts_acs_gdf_ac.json')
# read in the grocery-store data
grocery_pts_df = pd.read_csv('notebook_data/other/ca_grocery_stores_2019_wgs84.csv')
# coerce to a GeoDataFrame
grocery_pts_gdf = gpd.GeoDataFrame(grocery_pts_df, 
                               geometry=gpd.points_from_xy(grocery_pts_df.X, grocery_pts_df.Y))
# define the CRS
grocery_pts_gdf.crs = "epsg:4326"
# transform to our census-tract CRS
grocery_pts_gdf.to_crs(tracts_acs_gdf_ac.crs, inplace=True)
print(grocery_pts_gdf.head())

-->

-----------------------

## 8.2 Spatial Join and Dissolve

Now that we have our data and they're in the same projection, we're going to conduct an *attribute join* to bring together the two datasets. From there we'll be able to actually *aggregate* our data to count the total sales volume.

- join the two datasets in such a way that you can then...
- group by tract and calculate the total grocery-store sales volume
- don't forget to check the dimensions, contents, and any other relevant aspects of your results

# join the two datasets in such a way that you can then...

tracts_joingrocery = gpd.sjoin(..., ..., how= ...)

# group by tract and calculate the total grocery-store sales volume

tracts_totsalesvol = tracts_joingrocery[['GEOID','geometry','SALESVOL']].dissolve(by= ...,
                                                                                  aggfunc=..., as_index=False)

# don't forget to check the dimensions, contents, and any other relevant aspects of your results

# check the dimensions
print('Dimensions of result:', ...)
print('Dimesions of census tracts:', ...)

# check the result
print(tracts_totsalesvol.head())

## Double-click here to see solution!

<!--

# SOLUTION:

############################
# spatial join and dissolve:
#---------------------------
# join the grocery stores onto the tracts
tracts_joingrocery = gpd.sjoin(tracts_acs_gdf_ac, grocery_pts_gdf, how='left')
# dissolve the joined object, summing the SALESVOL column by GEOID
tracts_totsalesvol = tracts_joingrocery[['GEOID','geometry','SALESVOL']].dissolve(by='GEOID',
                                                                                  aggfunc="sum",as_index=False)
# check the dimensions
# print('Dimensions of result:', tracts_totsalesvol.shape)
# print('Dimesions of census tracts:', tracts_acs_gdf_ac.shape)

# check the result
print(tracts_totsalesvol.head())

-->

----------------------

## 8.3 Plot and Review

With any time of geospatial analysis you do, it's always nice to plot and visualize your results to check your work and start to understand the full story of your analysis.

- Plot the tracts, coloring them by total grocery-store sales volume
- Plot the grocery stores on top
- Bonus points for devising a nice visualization scheme that helps you heuristically check your results!

# create the figure and axes

fig, ax = plt.subplots(figsize = (20,20)) 

# plot the tracts, coloring by total SALESVOL

tracts_totsalesvol.plot(ax=ax, column= ..., scheme="quantiles", cmap="autumn", edgecolor="grey",
                        legend=True, legend_kwds={'title':...})

# subset the stores for only those within our tracts, to keep map within region of interest

grocery_pts_gdf_ac = grocery_pts_gdf.loc[..., ]

# add the grocery stores, coloring by SALESVOL, for a visual check

grocery_pts_gdf_ac.plot(ax=ax, column= ... , cmap= ..., linewidth= ..., markersize= ...,
                        legend=True, legend_kwds={'label': ... , 'orientation': "horizontal"})

## Double-click here to see solution!

<!--

# SOLUTION:

##################
# plot and review:
#-----------------

# create the figure and axes
fig, ax = plt.subplots(figsize = (20,20)) 
# plot the tracts, coloring by total SALESVOL
tracts_totsalesvol.plot(ax=ax,column='SALESVOL', scheme="quantiles", cmap="autumn", edgecolor="grey",
                        legend=True, legend_kwds={'title':'Total grocery-store sales volume ($; tracts)'})
# subset the stores for only those within our tracts, to keep map within region of interest
grocery_pts_gdf_ac = grocery_pts_gdf.loc[grocery_pts_gdf.within(tracts_acs_gdf_ac.unary_union), ]
# add the grocery stores, coloring by SALESVOL, for a visual check
grocery_pts_gdf_ac.plot(ax=ax, column='SALESVOL', cmap='Greys_r', linewidth=0.3, markersize=25,
                     legend=True, legend_kwds={'label': "sales volume ($; stores)", 'orientation': "horizontal"})

-->

-------------------

<br>
<br>
<br>
<br>
<br>
<br>

***

# Congrats!! Thanks for Joining Us for Geospatial Fundamentals!!

<img src="https://statmodeling.stat.columbia.edu/wp-content/uploads/2016/07/cat-globe.png">

---
<div style="display:inline-block;vertical-align:middle;">
<a href="https://dlab.berkeley.edu/" target="_blank"><img src ="assets/images/dlab_logo.png" width="75" align="left">
</a>
</div>

<div style="display:inline-block;vertical-align:middle;">
    <div style="font-size:larger">&nbsp;D-Lab @ University of California - Berkeley</div>
    <div>&nbsp;Team Geo<div>
</div>
        



