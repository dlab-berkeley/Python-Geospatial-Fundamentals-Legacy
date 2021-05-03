# Lesson 6. Spatial Queries

In spatial analysis, our goal is not just to make nice maps,
but to actually run analyses that leverage the explicitly spatial
nature of our data. The process of doing this is known as 
**spatial analysis**.

To construct spatial analyses, we string together series of spatial
operations in such a way that the end result answers our question of interest.
There are many such spatial operations. These are known as **spatial queries**.


- 6.0 Load and prep some data
- 6.1 Measurement Queries
- 6.2 Relationship Queries
- **Exercise**: Spatial Relationship Query
- 6.3 Proximity Analysis
- **Exercise**: Proximity Analysis
- 6.4 Recap





<br>
<font color='grey'>
    <b>Instructor Notes</b>

- Datasets used
    - 'notebook_data/census/Tracts/cb_2013_06_tract_500k.zip'
    - 'notebook_data/protected_areas/CPAD_2020a_Units.shp'
    - 'notebook_data/berkeley/BerkeleyCityLimits.shp'
    - 'notebook_data/alco_schools.csv'
    - 'notebook_data/transportation/BerkeleyBikeBlvds.geojson'
    - 'notebook_data/transportation/bart.csv'

- Expected time to complete
    - Lecture + Questions: 45 minutes
    - Exercises: 20 minutes
</font>

-------------------

We will start by reviewing the most
fundamental set, which we'll refer to as **spatial queries**.
These can be divided into:

- <u>Measurement queries</u>
    - What is feature A's **length**?
    - What is feature A's **area**?
    - What is feature A's **perimeter**?
    - What is feature A's **distance** from feature B?
    - etc.
- <u>Relationship queries</u>
    - Is feature A **within** feature B?
    - Does feature A **intersect** with feature B?
    - Does feature A **cross** feature B?
    - etc.
    
We'll work through examples of each of those types of queries.

Then we'll see an example of a very common spatial analysis that 
is a conceptual amalgam of those two types: **proximity analysis**.

import pandas as pd
import geopandas as gpd

import matplotlib # base python plotting library
import matplotlib.pyplot as plt # submodule of matplotlib

# To display plots, maps, charts etc in the notebook
%matplotlib inline  

# 6.0 Load and prep some data

Let's read in our census tracts data again.

census_tracts = gpd.read_file("zip://notebook_data/census/Tracts/cb_2013_06_tract_500k.zip")
census_tracts.plot()

census_tracts.head()

Then we'll grab just the Alameda Country tracts.

census_tracts_ac = census_tracts.loc[census_tracts['COUNTYFP']=='001'].reset_index(drop=True)
census_tracts_ac.plot()

# 6.1 Measurement Queries

We'll start off with some simple measurement queries.

For example, here's how we can get the areas of each of our census tracts.

census_tracts_ac.area

Okay! 

We got... 

numbers!

...?

<div style="display:inline-block;vertical-align:top;">
    <img src="http://www.pngall.com/wp-content/uploads/2016/03/Light-Bulb-Free-PNG-Image.png" width="30" align=left > 
</div>  
<div style="display:inline-block;">

#### Questions
</div>

1. What do those numbers mean?
1. What are our units?
1. And if we're not sure, how might be find out?

Your responses here:







Let's take a look at our CRS.

census_tracts_ac.crs

Ah-hah! We're working in an unprojected CRS, with units of decimal degrees.

**When doing spatial analysis, we will almost always want to work in a projected CRS
that has natural distance units, such as meters!**

Time to project!

(As previously, we'll use UTM Zone 10N with a NAD83 data.
This is a good choice for our region of interest.)

census_tracts_ac_utm10 = census_tracts_ac.to_crs( "epsg:26910")

census_tracts_ac_utm10.crs

Now let's try our area calculation again.

census_tracts_ac_utm10.area

That looks much more reasonable!

<div style="display:inline-block;vertical-align:top;">
    <img src="http://www.pngall.com/wp-content/uploads/2016/03/Light-Bulb-Free-PNG-Image.png" width="30" align=left > 
</div>  
<div style="display:inline-block;">

#### Question
</div>

What are our units now?


Your response here:
    
    
    
    
    

You may have noticed that our census tracts already have an area column in them.

Let's do a sanity check on our results.

# calculate the area for the 0th feature
census_tracts_ac_utm10.area[0]

# get the area for the 0th feature according to its 'ALAND' attribute
census_tracts['ALAND'][0]

# check equivalence of the calculated areas and the 'ALAND' column
census_tracts_ac_utm10['ALAND'].values == census_tracts_ac_utm10.area

<div style="display:inline-block;vertical-align:top;">
    <img src="http://www.pngall.com/wp-content/uploads/2016/03/Light-Bulb-Free-PNG-Image.png" width="30" align=left > 
</div>  
<div style="display:inline-block;">

#### Question
</div>

What explains this disagreement? Are the calculated areas incorrect?


Your response here:
    
    
    
    
    
    

We can also sum the area for Alameda county by adding `.sum()` to the end of our area calculation.

census_tracts_ac_utm10.area.sum()

We can actually look up how large Alameda County is to check our work.The county is 739 miles<sup>2</sup>, which is around 1,914,001,213 meters<sup>2</sup>. I'd say we're pretty close!

As it turns out, we can similarly use another attribute
to get the features' lengths.

**NOTE**: In this case, given we're
dealing with polygons, this is equivalent to getting the features' perimeters.

census_tracts_ac_utm10.length

# 6.2 Relationship Queries


[Spatial relationship queries](https://en.wikipedia.org/wiki/Spatial_relation) consider how two geometries or sets of geometries relate to one another in space. 

<img src="https://upload.wikimedia.org/wikipedia/commons/5/55/TopologicSpatialRelarions2.png" height="300px"></img>


Here is a list of the most commonly used GeoPandas methods to test spatial relationships.

- [within](http://geopandas.org/reference.html?highlight=distance#geopandas.GeoSeries.within)
- [contains](http://geopandas.org/reference.html?highlight=distance#geopandas.GeoSeries.contains) (the inverse of `within`)
- [intersects](http://geopandas.org/reference.html?highlight=distance#geopandas.GeoSeries.intersects)

<br>
There several other GeoPandas spatial relationship predicates but they are more complex to properly employ. For example the following two operations only work with geometries that are completely aligned.

- [touches](http://geopandas.org/reference.html?highlight=distance#geopandas.GeoSeries.touches)
- [equals](http://geopandas.org/reference.html?highlight=distance#geopandas.GeoSeries.equals)


All of these methods takes the form:

    Geoseries.<predicate>(geometry)
    
For example:

    Geoseries.contains(geometry)

--------------------------------

Let's load a new dataset to demonstrate these queries.

This is a dataset containing all the protected areas (parks and the like) in California.

pas = gpd.read_file('./notebook_data/protected_areas/CPAD_2020a_Units.shp')

Does this need to be reprojected too?

pas.crs

Yes it does!

Let's reproject it.

pas_utm10 = pas.to_crs("epsg:26910")

One common use for spatial queries is for spatial subsetting of data.

In our case, lets use **intersects** to
find all of the parks that have land in Alameda County.

census_tracts_ac_utm10.geometry.squeeze()

pas_in_ac = pas_utm10.intersects(census_tracts_ac_utm10.geometry.unary_union)

If we scroll the resulting GeoDataFrame to the right we'll see that 
the `COUNTY` column of our resulting subset gives us a good sanity check on our results.

pas_utm10[pas_in_ac].head()

So does this overlay plot!

ax = census_tracts_ac_utm10.plot(color='gray', figsize=[12,16])
pas_utm10[pas_in_ac].plot(ax=ax, column='ACRES', cmap='summer', legend=True,
                          edgecolor='black', linewidth=0.4, alpha=0.8,
                          legend_kwds={'label': "acres",
                                       'orientation': "horizontal"})
ax.set_title('Protected areas in Alameda County, colored by area', size=18);

# color by county?

# Exercise: Spatial Relationship Query

Let's use a spatial relationship query to create a new dataset containing Berkeley schools!

Run the next two cells to load datasets containing Berkeley's city boundary and Alameda County's
schools and to reproject them to EPSG: 26910.

Then in the following cell, write your own code to:
1. subset the schools for only those `within` Berkeley
2. plot the Berkeley boundary and then the schools as an overlay map

To see the solution, double-click the Markdown cell below.

# load the Berkeley boundary
berkeley = gpd.read_file("notebook_data/berkeley/BerkeleyCityLimits.shp")

# transform to EPSG:26910
berkeley_utm10 = berkeley.to_crs("epsg:26910")

# display
berkeley_utm10.head()

# load the Alameda County schools CSV
schools_df = pd.read_csv('notebook_data/alco_schools.csv')

# coerce it to a GeoDataFrame
schools_gdf = gpd.GeoDataFrame(schools_df, 
                               geometry=gpd.points_from_xy(schools_df.X, schools_df.Y))
# define its unprojected (EPSG:4326) CRS
schools_gdf.crs = "epsg:4326"

# transform to EPSG:26910
schools_gdf_utm10 = schools_gdf.to_crs( "epsg:26910")

# display
schools_df.head()

# YOUR CODE HERE:






## Double-click to see solution!

<!--

# SOLUTION:

# get the boolean Series indicating which schools are in Berkeley
schools_in_berkeley = schools_gdf_utm10.within(berkeley_utm10.geometry.squeeze())

# use that series to subset the schools for only those that are in Berkeley
berkeley_schools = schools_gdf_utm10[schools_in_berkeley]

# create a fig with one Axes object
fig, ax = plt.subplots(figsize=(10,10))
# plot the Berkeley border on those Axes
berkeley_utm10.plot(color='lightgrey', ax=ax)
# add the Berkeley schools to those Axes
berkeley_schools.plot(color='purple',ax=ax)

-->

-------------------------------

# 6.3 Proximity Analysis

Now that we've seen the basic idea of spatial measurement and relationship queries,
let's take a look at a common analysis that combines those concepts: **promximity analysis**.

Proximity analysis seeks to identify all features in a focal feature set
that are within some maximum distance of features in a reference feature set.

A common workflow for this analysis is:

1. Buffer (i.e. add a margin around) the reference dataset, out to the maximum distance.
1. Run a spatial relationship query to find all focal features that intersect (or are within) the buffer.

---------------------------------

Let's read in our bike boulevard data again.

Then we'll find out which of our Berkeley schools are within a block's distance (200 m) of the boulevards.

bike_blvds = gpd.read_file('notebook_data/transportation/BerkeleyBikeBlvds.geojson')
bike_blvds.plot()

Of course, we need to reproject the boulevards to our projected CRS.

bike_blvds_utm10 = bike_blvds.to_crs( "epsg:26910")

Now we can create our 200 meter bike boulevard buffers.

bike_blvds_buf = bike_blvds_utm10.buffer(distance=200)

Now let's overlay everything.

fig, ax = plt.subplots(figsize=(10,10))
berkeley_utm10.plot(color='lightgrey', ax=ax)
bike_blvds_buf.plot(color='pink', ax=ax, alpha=0.5)
bike_blvds_utm10.plot(ax=ax)
schools_gdf_utm10.plot(color='purple',ax=ax)

Great! Looks like we're all ready to run our intersection to complete the proximity analysis.


**NOTE**: In order to subset with our buffers we need to call the `unary_union` attribute of the buffer object.
This gives us a single unified polygon, rather than a series of multipolygons representing buffers around each of the points in our multilines.

schools_near_blvds = berkeley_schools.within(bike_blvds_buf.unary_union)
blvd_schools = berkeley_schools[schools_near_blvds]

Now let's overlay again, to see if the schools we subsetted make sense.

fig, ax = plt.subplots(figsize=(10,10))
berkeley_utm10.plot(color='lightgrey', ax=ax)
bike_blvds_buf.plot(color='pink', ax=ax, alpha=0.5)
bike_blvds_utm10.plot(ax=ax)
berkeley_schools.plot(color='purple',ax=ax)
blvd_schools.plot(color='yellow', markersize=50, ax=ax)

If we want to find the shortest distance from one school to the bike boulevards, we can use the `distance` function.

berkeley_schools.distance(bike_blvds_utm10.unary_union)

# Exercise: Proximity Analysis

Now it's your turn to try out a proximity analysis!

Run the next cell to load our BART-system data, reproject it to EPSG: 26910, and subset it to Berkeley.

Then in the following cell, write your own code to find all schools within walking distance (1 km) of a BART station.

As a reminder, let's break this into steps:
1. buffer your Berkeley BART stations to 1 km (**HINT**: remember your units!)
2. use the schools' `within` attribute to check whether or not they're within the buffers (**HINT**: don't forget the `unary_union`!)
3. subset the Berkeley schools using the object returned by your spatial relationship query

4. as always, plot your results for a good visual check!

To see the solution, double-click the Markdown cell below.

# load the BART stations from CSV
bart_stations = pd.read_csv('notebook_data/transportation/bart.csv')
# coerce to a GeoDataFrame
bart_stations_gdf = gpd.GeoDataFrame(bart_stations, 
                               geometry=gpd.points_from_xy(bart_stations.lon, bart_stations.lat))
# define its unprojected (EPSG:4326) CRS
bart_stations_gdf.crs = "epsg:4326"
# transform to UTM Zone 10 N (EPSG:26910)
bart_stations_gdf_utm10 = bart_stations_gdf.to_crs( "epsg:26910")
# subset to Berkeley
berkeley_bart = bart_stations_gdf_utm10[bart_stations_gdf_utm10.within(berkeley_utm10.unary_union)]

# YOUR CODE HERE:







## Double-click to see solution!

<!--

# SOLUTION

# buffer the BART stations to 1 km
bart_buf = berkeley_bart.buffer(distance=1000)
# check whether or not each school is within a buffer
schools_near_bart = berkeley_schools.within(bart_buf.unary_union)
# subset the schools using the boolean Series you just produced
bart_schools = berkeley_schools[schools_near_bart]

# create a fig with one Axes object
fig, ax = plt.subplots(figsize=(10,10))
# plot the Berkeley boundary (for reference)
berkeley_utm10.plot(color='lightgrey', ax=ax)
# plot the BART stations (for reference)
berkeley_bart.plot(color='green', ax=ax)
# add the BART buffers (for check)
bart_buf.plot(color='lightgreen', ax=ax, alpha=0.5)
# add all Berkeley schools (for reference)
berkeley_schools.plot(ax=ax)
# add the schools near BART (for check)
bart_schools.plot(color='yellow', markersize=50, ax=ax)

-->

----------------------------------

## 6.4 Recap
Leveraging what we've learned in our earlier lessons, we got to work with map overlays and start answering questions related to proximity. Key concepts include:
- Measuring area and length
	- `.area`, 
	- `.length`
- Relationship Queries
	- `.intersects()`
	- `.within()`
- Buffer analysis
	- `.buffer()`
	- `.distance()`

---
<div style="display:inline-block;vertical-align:middle;">
<a href="https://dlab.berkeley.edu/" target="_blank"><img src ="assets/images/dlab_logo.png" width="75" align="left">
</a>
</div>

<div style="display:inline-block;vertical-align:middle;">
    <div style="font-size:larger">&nbsp;D-Lab @ University of California - Berkeley</div>
    <div>&nbsp;Team Geo<div>
</div>
        


