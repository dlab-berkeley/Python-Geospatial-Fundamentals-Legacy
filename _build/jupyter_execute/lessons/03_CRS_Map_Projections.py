# Lesson 3. Coordinate Reference Systems (CRS) & Map Projections

Building off of what we learned in the previous notebook, we'll get to understand an integral aspect of geospatial data: Coordinate Reference Systems.

- 3.1 California County Shapefile
- 3.2 USA State Shapefile
- 3.3 Plot the Two Together
- 3.4 Coordinate Reference System (CRS)
- 3.5 Getting the CRS
- 3.6 Setting the CRS
- 3.7 Transforming or Reprojecting the CRS
- 3.8 Plotting States and Counties Togther
- 3.9 Recap
- **Exercise**: CRS Management

<br>
<font color='grey'>
    <b>Instructor Notes</b>

- Datasets used
    - ‘notebook_data/california_counties/CaliforniaCounties.shp’
    - ‘notebook_data/us_states/us_states.shp’
    - ‘notebook_data/census/Places/cb_2018_06_place_500k.zip’

- Expected time to complete
    - Lecture + Questions: 45 minutes
    - Exercises: 10 minutes
</font>

### Import Libraries

import pandas as pd
import geopandas as gpd

import matplotlib # base python plotting library
import matplotlib.pyplot as plt # submodule of matplotlib

# To display plots, maps, charts etc in the notebook
%matplotlib inline  

## 3.1 California County shapefile
Let's go ahead and bring back in our California County shapefile. As before, we can read the file in using `gpd.read_file` and plot it straight away.

counties = gpd.read_file('notebook_data/california_counties/CaliforniaCounties.shp')
counties.plot(color='darkgreen')

Even if we have an awesome map like this, sometimes we want to have more geographical context, or we just want additional information. We're going to try **overlaying** our counties GeoDataFrame on our USA states shapefile.

## 3.2 USA State shapefile

We're going to bring in our states geodataframe, and let's do the usual operations to start exploring our data.

# Read in states shapefile
states = gpd.read_file('notebook_data/us_states/us_states.shp')

# Look at the first few rows
states.head()

# Count how many rows and columns we have
states.shape

# Plot our states data
states.plot()

You might have noticed that our plot extends beyond the 50 states (which we also saw when we executed the `shape` method). Let's double check what states we have included in our data.

states['STATE'].values

Beyond the 50 states we seem to have American Samoa, Puerto Rico, Guam, Commonwealth of the Northern Mariana Islands, and United States Virgin Islands included in this geodataframe. To make our map cleaner, let's limit the states to the contiguous states (so we'll also exclude Alaska and Hawaii).

# Define list of non-contiguous states
non_contiguous_us = [ 'American Samoa','Puerto Rico','Guam',
                      'Commonwealth of the Northern Mariana Islands',
                      'United States Virgin Islands', 'Alaska','Hawaii']
# Limit data according to above list
states_limited = states.loc[~states['STATE'].isin(non_contiguous_us)]

# Plot it
states_limited.plot()

To prepare for our mapping overlay, let's make our states a nice, light grey color.

states_limited.plot(color='lightgrey', figsize=(10,10))

## 3.3 Plot the two together

Now that we have both geodataframes in our environment, we can plot both in the same figure.

**NOTE**: To do this, note that we're getting a Matplotlib Axes object (`ax`), then explicitly adding each our layers to it
by providing the `ax=ax` argument to the `plot` method.

fig, ax = plt.subplots(figsize=(10,10))
counties.plot(color='darkgreen',ax=ax)
states_limited.plot(color='lightgrey', ax=ax)

Oh no, what happened here?

<img src="http://www.pngall.com/wp-content/uploads/2016/03/Light-Bulb-Free-PNG-Image.png" width="20" align=left >  **Question** Without looking ahead, what do you think happened?



Your response here:







<br>
<br>
If you look at the numbers we have on the x and y axes in our two plots, you'll see that the county data has much larger numbers than our states data. It's represented in some different type of unit other than decimal degrees! 

In fact, that means if we zoom in really close into our plot we'll probably see the states data plotted. 

%matplotlib inline
fig, ax = plt.subplots(figsize=(10,10))
counties.plot(color='darkgreen',ax=ax)
states_limited.plot(color='lightgrey', ax=ax)
ax.set_xlim(-140,-50)
ax.set_ylim(20,50)

This is a key issue that you'll have to resolve time and time again when working with geospatial data!

It all revolves around **coordinate reference systems** and **projections**.

----------------------------

## 3.4 Coordinate Reference Systems (CRS)

<img src="http://www.pngall.com/wp-content/uploads/2016/03/Light-Bulb-Free-PNG-Image.png" width="20" align=left >  **Question** Do you have experience with Coordinate Reference Systems?

Your response here:







<br><br>As a refresher, a CRS describes how the coordinates in a geospatial dataset relate to locations on the surface of the earth. 

A `geographic CRS` consists of: 
- a 3D model of the shape of the earth (a **datum**), approximated as a sphere or spheroid (aka ellipsoid)
- the **units** of the coordinate system (e.g, decimal degrees, meters, feet) and 
- the **origin** (i.e. the 0,0 location), specified as the meeting of the **equator** and the **prime meridian**( 

A `projected CRS` consists of
- a geographic CRS
- a **map projection** and related parameters used to transform the geographic coordinates to `2D` space.
  - a map projection is a mathematical model used to transform coordinate data

### A Geographic vs Projected CRS
<img src ="assets/images/fig_create2.jpg" width="600">

#### There are many, many CRSs

Theoretically the number of CRSs is unlimited!

Why? Primariy, because there are many different definitions of the shape of the earth, multiplied by many different ways to cast its surface into 2 dimensions. Our understanding of the earth's shape and our ability to measure it has changed greatly over time.

#### Why are CRSs Important?

- You need to know the data about your data (or `metadata`) to use it appropriately.


- All projected CRSs introduce distortion in shape, area, and/or distance. So understanding what CRS best maintains the characteristics you need for your area of interest and your analysis is important.


- Some analysis methods expect geospatial data to be in a projected CRS
  - For example, `geopandas` expects a geodataframe to be in a projected CRS for area or distance based analyses.


- Some Python libraries, but not all, implement dynamic reprojection from the input CRS to the required CRS and assume a specific CRS (WGS84) when a CRS is not explicitly defined.


- Most Python spatial libraries, including Geopandas, require geospatial data to be in the same CRS if they are being analysed together.

#### What you need to know when working with CRSs

- What CRSs used in your study area and their main characteristics
- How to identify, or `get`, the CRS of a geodataframe
- How to `set` the CRS of geodataframe (i.e. define the projection)
- Hot to `transform` the CRS of a geodataframe (i.e. reproject the data)

### Codes for CRSs commonly used with CA data

CRSs are typically referenced by an [EPSG code](http://wiki.gis.com/wiki/index.php/European_Petroleum_Survey_Group).  

It's important to know the commonly used CRSs and their EPSG codes for your geographic area of interest.  

For example, below is a list of commonly used CRSs for California geospatial data along with their EPSG codes.

##### Geographic CRSs
-`4326: WGS84` (units decimal degrees) - the most commonly used geographic CRS

-`4269: NAD83` (units decimal degrees) - the geographic CRS customized to best fit the USA. This is used by all Census geographic data.

>  `NAD83 (epsg:4269)` are approximately the same as `WGS84(epsg:4326)` although locations can differ by up to 1 meter in the continental USA and elsewhere up to 3m. That is not a big issue with census tract data as these data are only accurate within +/-7meters.
##### Projected CRSs

-`5070: CONUS NAD83` (units meters) projected CRS for mapping the entire contiguous USA (CONUS)

-`3857: Web Mercator` (units meters) conformal (shape preserving) CRS used as the default in web mapping

-`3310: CA Albers Equal Area, NAD83` (units meters)  projected CRS for CA statewide mapping and spatial analysis

-`26910: UTM Zone 10N, NAD83` (units meters) projected CRS for northern CA mapping & analysis

-`26911: UTM Zone 11N, NAD83` (units meters) projected CRS for Southern CA mapping & analysis

-`102641 to 102646: CA State Plane zones 1-6, NAD83` (units feet) projected CRS used for local analysis.

You can find the full CRS details on the website https://www.spatialreference.org

## 3.5 Getting the CRS

### Getting the CRS of a gdf

GeoPandas GeoDataFrames have a `crs` attribute that returns the CRS of the data.

counties.crs

states_limited.crs

As we can clearly see from those two printouts (even if we don't understand all the content!),
the CRSs of our two datasets are different! **This explains why we couldn't overlay them correctly!**

-----------------------------------------
The above CRS definition specifies 
- the name of the CRS (`WGS84`), 
- the axis units (`degree`)
- the shape (`datum`),
- and the origin (`Prime Meridian`, and the equator)
- and the area for which it is best suited (`World`)

> Notes:
>    - `geocentric` latitude and longitude assume a spherical (round) model of the shape of the earth
>    - `geodetic` latitude and longitude assume a spheriodal (ellipsoidal) model, which is closer to the true shape.
>    - `geodesy` is the study of the shape of the earth.

**NOTE**: If you print a `crs` call, Python will just display the EPSG code used to initiate the CRS object. Depending on your versions of Geopandas and its dependencies, this may or may not look different from what we just saw above.

print(states_limited.crs)

## 3.6 Setting the CRS

You can also set the CRS of a gdf using the `crs` attribute.  You would set the CRS if is not defined or if you think it is incorrectly defined.

> In desktop GIS terminology setting the CRS is called **defining the CRS**

As an example, let's set the CRS of our data to `None`

# first set the CRS to None
states_limited.crs = None

# Check it again
states_limited.crs

...hummm...

If a variable has a null value (None) then displaying it without printing it won't display anything!

# Check it again
print(states_limited.crs)

Now we'll set it back to its correct CRS.

# Set it to 4326
states_limited.crs = "epsg:4326"

# Show it
states_limited.crs

**NOTE**: You can set the CRS to anything you like, but **that doesn't make it correct**! This is because setting the CRS does not change the coordinate data; it just tells the software how to interpret it.

## 3.7 Transforming or Reprojecting the CRS
You can transform the CRS of a geodataframe with the `to_crs` method.


> In desktop GIS terminology transforming the CRS is called **projecting the data** (or **reprojecting the data**)

When you do this you want to save the output to a new GeoDataFrame.

states_limited_utm10 = states_limited.to_crs( "epsg:26910")

Now take a look at the CRS.

states_limited_utm10.crs

You can see the result immediately by plotting the data.

# plot geographic gdf
states_limited.plot();
plt.axis('square');

# plot utm gdf
states_limited_utm10.plot();
plt.axis('square')

# Your thoughts here

<div style="display:inline-block;vertical-align:top;">
    <img src="http://www.pngall.com/wp-content/uploads/2016/03/Light-Bulb-Free-PNG-Image.png" width="30" align=left > 
</div>  
<div style="display:inline-block;">

#### Questions
</div>

1. What two key differences do you see between the two plots above?
1. Do either of these plotted USA maps look good?
1. Try looking at the common CRS EPSG codes above and see if any of them look better for the whole country than what we have now. Then try transforming the states data to the CRS that you think would be best and plotting it. (Use the code cell two cells below.)

Your responses here:







# YOUR CODE HERE





**Double-click to see solution!**

<!--
#SOLUTION 
states_limited_conus = states_limited.to_crs("epsg:5070")
states_limited_conus.plot();
plt.axis('square')
-->

## 3.8 Plotting states and counties together

Now that we know what a CRS is and how we can set them, let's convert our counties GeoDataFrame to match up with out states' crs.

# Convert counties data to NAD83 
counties_utm10 = counties.to_crs("epsg:26910")

counties_utm10.plot()

# Plot it together!
fig, ax = plt.subplots(figsize=(10,10))
states_limited_utm10.plot(color='lightgrey', ax=ax)
counties_utm10.plot(color='darkgreen',ax=ax)

Since we know that the best CRS to plot the contiguous US from the above question is 5070, let's also transform and plot everything in that CRS.

counties_conus = counties.to_crs("epsg:5070")

fig, ax = plt.subplots(figsize=(10,10))
states_limited_conus.plot(color='lightgrey', ax=ax)
counties_conus.plot(color='darkgreen',ax=ax)

## 3.9 Recap

In this lesson we learned about...
- Coordinate Reference Systems 
- Getting the CRS of a geodataframe
    - `crs`
- Transforming/repojecting CRS
    - `to_crs`
- Overlaying maps

## Exercise: CRS Management

Now it's time to take a crack and managing the CRS of a new dataset. In the code cell below, write code to:

1. Bring in the CA places data (`notebook_data/census/Places/cb_2018_06_place_500k.zip`)
2. Check if the CRS is EPSG code 26910. If not, transform the CRS
3. Plot the California counties and places together.

To see the solution, double-click the Markdown cell below.

# YOUR CODE HERE



## Double-click to see solution!

<!--

# SOLUTION

# 1. Bring in the CA places data
california_places = gpd.read_file('zip://notebook_data/census/Places/cb_2018_06_place_500k.zip')
california_places.head()

# 2. Check and transorm the CRS if needed
california_places.crs
california_places_utm10 = california_places.to_crs( "epsg:26910")

# 3. Plot the California counties and places together
fig, ax = plt.subplots(figsize=(10,10))
counties_utm10.plot(color='lightgrey', ax=ax)
california_places_utm10 .plot(color='purple',ax=ax)

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
        
