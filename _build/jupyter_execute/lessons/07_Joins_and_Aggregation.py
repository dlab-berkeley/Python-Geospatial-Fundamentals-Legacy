# Lesson 7. Attribute and Spatial Joins

Now that we understand the logic of spatial relationship queries,
let's take a look at another fundamental spatial operation that relies on them.

This operation, called a **spatial join**, is the process by which we can
leverage the spatial relationships between distinct datasets to merge
their information into a new, synthetic dataset.

This operation can be thought as the spatial equivalent of an
**attribute join**, in which multiple tabular datasets can be merged by
aligning matching values in a common column that they both contain.
Thus, we'll start by developing an understanding of this operation first!

- 7.0 Data Input and Prep
- 7.1 Attribute Joins
- **Exercise**: Choropleth Map
- 7.2 Spatial Joins
- 7.3 Aggregation
- **Exercise**: Aggregation
- 7.4 Recap

<br>
<font color='grey'>
    <b>Instructor Notes</b>

- Datasets used
    - 'notebook_data/census/ACS5yr/census_variables_CA.csv'
    - 'notebook_data/census/Tracts/cb_2013_06_tract_500k.zip'
    - 'notebook_data/alco_schools.csv'
    
- Expected time to complete
    - Lecture + Questions: 45 minutes
    - Exercises: 20 minutes
</font>

import pandas as pd
import geopandas as gpd

import matplotlib # base python plotting library
import matplotlib.pyplot as plt # submodule of matplotlib

# To display plots, maps, charts etc in the notebook
%matplotlib inline  

## 7.0 Data Input and Prep

Let's read in a table of data from the US Census' 5-year American Community Survey (ACS5).

# Read in the ACS5 data for CA into a pandas DataFrame.
# Note: We force the FIPS_11_digit to be read in as a string to preserve any leading zeroes.
acs5_df = pd.read_csv("notebook_data/census/ACS5yr/census_variables_CA.csv", dtype={'FIPS_11_digit':str})
acs5_df.head()


**Brief summary of the data**:

Below is a table of the variables in this table. They were combined from 
different ACS 5 year tables.

<u>NOTE</u>:
- variables that start with `c_` are counts
- variables that start with `med_` are medians
- variables that end in `_moe` are margin of error estimates
- variables that start with `_p` are proportions calcuated from the counts divided by the table denominator (the total count for whom that variable was assessed)


| Variable        | Description                                     |
|-----------------|-------------------------------------------------|
|`c_race`         |Total population                                 
|`c_white`        |Total white non-Latinx
| `c_black`       | Total black and African American non-Latinx
| `c_asian`       | Total Asian non-Latinx
| `c_latinx`      | Total Latinx
| `state_fips`    | State level FIPS code
| `county_fips`   | County level FIPS code
| `tract_fips`    |Tracts level FIPS code
| `med_rent`      |Median rent
| `med_hhinc`     |Median household income
| `c_tenants`     |Total tenants
| `c_owners`      |Total owners
| `c_renters`     |Total renters
| `c_movers`      |Total number of people who moved
| `c_stay`        |Total number of people who stayed
| `c_movelocal`   |Number of people who moved locally
| `c_movecounty`  |Number of people who moved counties
| `c_movestate`   | Number of people who moved states
| `c_moveabroad`  |Number of people who moved abroad
| `c_commute`     |Total number of commuters
| `c_car`         | Number of commuters who use a car
| `c_carpool`     | Number of commuters who carpool
| `c_transit`     |Number of commuters who use public transit
| `c_bike`        |Number of commuters who bike
| `c_walk`        |Number of commuters who bike
| `year`          | ACS data year
| `FIPS_11_digit` | 11-digit FIPS code


We're going to drop all of our `moe` columns by identifying all of those that end with `_moe`. We can do that in two steps, first by using `filter` to identify columns that contain the string `_moe`.

moe_cols = acs5_df.filter(like='_moe',axis=1).columns
moe_cols

acs5_df.drop(moe_cols, axis=1, inplace=True)

And lastly, let's grab only the rows for year 2018 and county FIPS code 1 (i.e. Alameda County)

acs5_df_ac = acs5_df[(acs5_df['year']==2018) & (acs5_df['county_fips']==1)]

---------------------------------
Now let's also read in our census tracts again!

tracts_gdf = gpd.read_file("zip://notebook_data/census/Tracts/cb_2013_06_tract_500k.zip")

tracts_gdf.head()

tracts_gdf_ac = tracts_gdf[tracts_gdf['COUNTYFP']=='001']
tracts_gdf_ac.plot()
plt.show()

## 7.1 Attribute Joins

**Attribute Joins  between Geodataframes and  Dataframes**

*We just mapped the census tracts. But what makes a map powerful is when you map the data associated with the locations.*

- `tracts_gdf_ac`: These are polygon data in a GeoDataFrame. However, as we saw in the `head` of that dataset, they no attributes of interest!

- `acs5_df_ac`: These are 2018 ACS data from a CSV file ('census_variables_CA.csv'), imported and read in as a `pandas` DataFrame. However, they have no geometries!

In order to map the ACS data we need to associate it with the tracts. Let's do that now, by joining the columns from `acs5_df_ac` to the columns of `tracts_gdf_ac` using a common column as the key for matching rows. This process is called an **attribute join**.






--------------------------

<img src="https://shanelynnwebsite-mid9n9g1q9y8tt.netdna-ssl.com/wp-content/uploads/2017/03/join-types-merge-names.jpg">


<div style="display:inline-block;vertical-align:top;">
    <img src="http://www.pngall.com/wp-content/uploads/2016/03/Light-Bulb-Free-PNG-Image.png" width="30" align=left > 
</div>  
<div style="display:inline-block;">

#### Question
</div>

The image above gives us a nice conceptual summary of the types of joins we could run.

1. In general, why might we choose one type of join over another?
1. In our case, do we want an inner, left, right, or outer (AKA 'full') join? 

(**NOTE**: You can read more about merging in `geopandas` [here](http://geopandas.org/mergingdata.html#attribute-joins).)

Your responses here:







Okay, here we go!

Let's take a look at the common column in both our DataFrames.


tracts_gdf_ac['GEOID'].head()

acs5_df_ac['FIPS_11_digit'].head()


Note that they are **not named the same thing**. 
        
        That's okay! We just need to know that they contain the same information.

Also note that they are **not in the same order**. 
        
        That's not only okay... That's the point! (If they were in the same order already then we could just join them side by side, without having Python find and line up the matching rows from each!)

-------------------------------

Let's do a `left` join to keep all of the census tracts in Alameda County and only the ACS data for those tracts.

**NOTE**: To figure out how to do this we could always take a peek at the documentation by calling
`?tracts_gdf_ac.merge`, or `help(tracts_gdf_ac)`.

# Left join keeps all tracts and the acs data for those tracts
tracts_acs_gdf_ac = tracts_gdf_ac.merge(acs5_df_ac, left_on='GEOID',
                                        right_on="FIPS_11_digit", how='left')
tracts_acs_gdf_ac.head(2)

Let's check that we have all the variables we have in our dataset now.

list(tracts_acs_gdf_ac.columns)

<div style="display:inline-block;vertical-align:top;">
    <img src="http://www.pngall.com/wp-content/uploads/2016/03/Light-Bulb-Free-PNG-Image.png" width="30" align=left > 
</div>  
<div style="display:inline-block;">

#### Question
</div>

It's always important to run sanity checks on our results, at each step of the way!

In this case, how many rows and columns should we have?


Your response here:







print("Rows and columns in the Alameda County Census tract gdf:\n\t", tracts_gdf_ac.shape)
print("Row and columns in the ACS5 2018 data:\n\t", acs5_df_ac.shape)
print("Rows and columns in the Alameda County Census tract gdf joined to the ACS data:\n\t", tracts_acs_gdf_ac.shape)

Let's save out our merged data so we can use it in the final notebook.

tracts_acs_gdf_ac.to_file('outdata/tracts_acs_gdf_ac.json', driver='GeoJSON')

## Exercise: Choropleth Map
We can now make choropleth maps using our attribute joined geodataframe. Go ahead and pick one variable to color the map, then map it. You can go back to lesson 5 if you need a refresher on how to make this!

To see the solution, double-click the Markdown cell below.

# YOUR CODE HERE


### Double-click to see solution!

<!--

# SOLUTION:
fig, ax = plt.subplots(figsize = (10,5)) 
tracts_acs_gdf_ac.plot(column='p_renters', 
                   scheme="quantiles",
                   legend=True,
                   ax=ax,cmap='magma'
                   )
ax.set_title("Percentage of Renters")

-->

-------------------
## 7.2 Spatial Joins

Great! We've wrapped our heads around the concept of an attribute join.

Now let's extend that concept to its spatially explicit equivalent: the **spatial join**!


<br>

To start, we'll read in some other data: The Alameda County schools data.

Then we'll work with that data and our `tracts_acs_gdf_ac` data together.

schools_df = pd.read_csv('notebook_data/alco_schools.csv')
schools_gdf = gpd.GeoDataFrame(schools_df, 
                               geometry=gpd.points_from_xy(schools_df.X, schools_df.Y))
schools_gdf.crs = "epsg:4326"

Let's check if we have to transform the schools to match the`tracts_acs_gdf_ac`'s CRS.

print('schools_gdf CRS:', schools_gdf.crs)
print('tracts_acs_gdf_ac CRS:', tracts_acs_gdf_ac.crs)

Yes we do! Let's do that.

**NOTE**: Explicit syntax aiming at that dataset's CRS leaves less room for human error!

schools_gdf = schools_gdf.to_crs(tracts_acs_gdf_ac.crs)

print('schools_gdf CRS:', schools_gdf.crs)
print('tracts_acs_gdf_ac CRS:', tracts_acs_gdf_ac.crs)

Now we're ready to combine the datasets in an analysis.

**In this case, we want to get data from the census tract within which each school is located.**

But how can we do that? The two datasets don't share a common column to use for a join.

tracts_acs_gdf_ac.columns

schools_gdf.columns

However, they do have a shared relationship by way of space! 

So, we'll use a spatial relationship query to figure out the census tract that
each school is in, then associate the tract's data with that school (as additional data in the school's row).
This is a **spatial join**!

---------------------------------

### Census Tract Data Associated with Each School

In this case, let's say we're interested in the relationship between the median household income
in a census tract (`tracts_acs_gdf_ac['med_hhinc']`) and a school's Academic Performance Index
(`schools_gdf['API']`).

To start, let's take a look at the distributions of our two variables of interest.

tracts_acs_gdf_ac.hist('med_hhinc')

schools_gdf.hist('API')

Oh, right! Those pesky schools with no reported APIs (i.e. API == 0)! Let's drop those.

schools_gdf_api = schools_gdf.loc[schools_gdf['API'] > 0, ]

schools_gdf_api.hist('API')

Much better!

Now, maybe we think there ought to be some correlation between the two variables?
As a first pass at this possibility, let's overlay the two datasets, coloring each one by
its variable of interest. This should give us a sense of whether or not similar values co-occur.

ax = tracts_acs_gdf_ac.plot(column='med_hhinc', cmap='cividis', figsize=[18,18],
                            legend=True, legend_kwds={'label': "median household income ($)",
                                                      'orientation': "horizontal"})
schools_gdf_api.plot(column='API', cmap='cividis', edgecolor='black', alpha=1, ax=ax,
                     legend=True, legend_kwds={'label': "API", 'orientation': "horizontal"})

### Spatially Joining our Schools and Census Tracts

Though it's hard to say for sure, it certainly looks possible.
It would be ideal to scatterplot the variables! But in order to do that, 
we need to know the median household income in each school's tract, which
means we definitely need our **spatial join**!

We'll first take a look at the documentation for the spatial join function, `gpd.sjoin`.

help(gpd.sjoin)

Looks like the key arguments to consider are:
- the two GeoDataFrames (**`left_df`** and **`right_df`**)
- the type of join to run (**`how`**), which can take the values `left`, `right`, or `inner`
- the spatial relationship query to use (**`op`**)

**NOTE**:
- By default `sjoin` is an inner join. It keeps the data from both geodataframes only where the locations spatially intersect.

- By default `sjoin` maintains the geometry of first geodataframe input to the operation. 


<div style="display:inline-block;vertical-align:top;">
    <img src="http://www.pngall.com/wp-content/uploads/2016/03/Light-Bulb-Free-PNG-Image.png" width="30" align=left > 
</div>  
<div style="display:inline-block;">

#### Questions
</div>

1. Which GeoDataFrame are we joining onto which (i.e. which one is getting the other one's data added to it)?
1. What happened to 'outer' as a join type?
1. Thus, in our operation, which GeoDataFrame should be the `left_df`, which should be the `right_df`, and `how` do we want our join to run?

Your responses here:









Alright! Let's run our join!

schools_jointracts = gpd.sjoin(schools_gdf_api, tracts_acs_gdf_ac, how='left')

schools_jointracts.head()

### Checking Our Output

<br>

<div style="display:inline-block;vertical-align:top;">
    <img src="http://www.pngall.com/wp-content/uploads/2016/03/Light-Bulb-Free-PNG-Image.png" width="30" align=left > 
</div>  
<div style="display:inline-block;">

#### Questions
</div>

As always, we want to sanity-check our intermediate result before we rush ahead.

One way to do that is to introspect the structure of the result object a bit.

1. What type of object should that have given us?
1. What should the dimensions of that object be, and why?
1. If we wanted a visual check of our results (i.e. a plot or map), what could we do?

Your responses here:








print(schools_jointracts.shape)
print(schools_gdf.shape)
print(tracts_acs_gdf_ac.shape)

schools_jointracts.head()

Confirmed! The output of the our `sjoin` operation is a GeoDataFrame (`schools_jointracts`) with:
- a row for each school that is located inside a census tract (all of them are)
- the **point geometry** of that school
- all of the attribute data columns (non-geometry columns) from both input GeoDataFrames

----------------------------

Let's also take a look at an overlay map of the schools on the tracts.
If we color the schools categorically by their tracts IDs, then we should see
that all schools within a given tract polygon are the same color.

ax = tracts_acs_gdf_ac.plot(color='white', edgecolor='black', figsize=[18,18])
schools_jointracts.plot(column='GEOID', ax=ax)

### Assessing the Relationship between Median Household Income and API

Fantastic! That looks right!

Now we can create that scatterplot we were thinking about!

fig, ax = plt.subplots(figsize=(6,6))
ax.scatter(schools_jointracts.med_hhinc, schools_jointracts.API)
ax.set_xlabel('median household income ($)')
ax.set_ylabel('API')

Wow! Just as we suspected based on our overlay map,
there's a pretty obvious, strong, and positive correlation
between median household income in a school's tract
and the school's API.

## 7.3. Aggregation

We just saw that a spatial join in one way to leverage the spatial relationship
between two datasets in order to create a new, synthetic dataset.

An **aggregation** is another way we can generate new data from this relationship.
In this case, for each feature in one dataset we find all the features in another
dataset that satisfy our chosen spatial relationship query with it (e.g. within, intersects),
then aggregate them using some summary function (e.g. count, mean).

------------------------------------

### Getting the Aggregated School Counts

Let's take this for a spin with our data. We'll count all the schools within each census tract.

Note that we've already done the first step of spatially joining the data from the aggregating features
(the tracts) onto the data to be aggregated (our schools).

The next step is to group our GeoDataFrame by census tract, and then summarize our data by group.
We do this using the DataFrame method `groupy`.

To get the correct count, lets rejoin our schools on our tracts, this time keeping all schools
(not just those with APIs > 0, as before).

schools_jointracts = gpd.sjoin(schools_gdf, tracts_acs_gdf_ac, how='left')

Now for the `groupy` operation.

**NOTE**: We could really use any column, since we're just taking a count. For now we'll just use the school names ('Site').

schools_countsbytract = schools_jointracts[['GEOID','Site']].groupby('GEOID', as_index=False).count()
print("Counts, rows and columns:", schools_countsbytract.shape)
print("Tracts, rows and columns:", tracts_acs_gdf_ac.shape)

# take a look at the data
schools_countsbytract.head()

### Getting Tract Polygons with School Counts

The above `groupby` and `count` operations give us the counts we wanted.
- We have the 263 (of 361) census tracts that have at least one school
- We have the number of schools within each of those tracts

But the output of `groupby` is a plain DataFrame not a GeoDataFrame.

If we want a GeoDataFrame then we have two options:
1. We could join the `groupby` output to `tracts_acs_gdf_ac` by the attribute `GEOID`
or
2. We could start over, using the GeoDataFrame `dissolve` method, which we can think of as a spatial `groupby`. 


---------------------------

Since we already know how to do an attribute join, we'll do the `dissolve`!

First, let's run a new spatial join.

tracts_joinschools = gpd.sjoin(schools_gdf, tracts_acs_gdf_ac, how='right')

tracts_joinschools.geometry

Now, let's run our dissolve!

tracts_schoolcounts = tracts_joinschools[['GEOID', 'Site', 'geometry']].dissolve(by='GEOID', aggfunc='count')
print("Counts, rows and columns:", tracts_schoolcounts.shape)

# take a look
tracts_schoolcounts.head()

Nice! Let's break that down.

- The `dissolve` operation requires a geometry column and a grouping column (in our case, 'GEOID'). Any geometries within the **same group** will be dissolved if they have the same geometry or nested geometries. 
 
- The `aggfunc`, or aggregation function, of the dissolve operation will be applied to all numeric columns in the input geodataframe (unless the function is `count` in which case it will count rows.)  

Check out the Geopandas documentation on [dissolve](https://geopandas.org/aggregation_with_dissolve.html?highlight=dissolve) for more information.


<div style="display:inline-block;vertical-align:top;">
    <img src="http://www.pngall.com/wp-content/uploads/2016/03/Light-Bulb-Free-PNG-Image.png" width="30" align=left > 
</div>  
<div style="display:inline-block;">

#### Questions
</div>

1. Above we selected three columns from the input GeoDataFrame to create a subset as input to the dissolve operation. Why?
1. Why did we run a new spatial join? What would have happened if we had used the `schools_jointracts` object instead?
1. What explains the dimensions of the new object (361, 2)?

You responses here:








### Mapping our Spatial Join Output

Also, because our `sjoin` plus `dissolve` pipeline outputs a GeoDataFrame, we can now easily map the school count by census tract!

fig, ax = plt.subplots(figsize = (14,8)) 

# Display the output of our spatial join
tracts_schoolcounts.plot(ax=ax,column='Site', 
                         scheme="user_defined",
                         classification_kwds={'bins':[*range(9)]},
                         cmap="PuRd_r",
                         edgecolor="grey",
                         legend=True, 
                         legend_kwds={'title':'Number of schools'})
schools_gdf.plot(ax=ax, color='black', markersize=2)

---------------------

## Exercise: Aggregation

#### What is the mean API of each census tract?

As we mentioned, the spatial aggregation workflow that we just put together above
could have been used not to generate a new count variable, but also
to generate any other new variable the results from calling an aggregation function
on an attribute column.

In this case, we want to calculate and map the mean API of the schools in each census tract.

Copy and paste code from above where useful, then tweak and/or add to that code such that your new code:
1. joins the schools onto the tracts (**HINT**: make sure to decide whether or not you want to include schools with API = 0!)
1. dissolves that joined object by the tract IDs, giving you a new GeoDataFrame with each tract's mean API (**HINT**: because this is now a different calculation, different problems may arise and need handling!)
1. plots the tracts, colored by API scores (**HINT**: overlay the schools points again, visualizing them in a way that will help you visually check your results!)

To see the solution, double-click the Markdown cell below.

# YOUR CODE HERE:






### Double-click to see solution!

<!--

# SOLUTION:

# join the schools onto the tracks (excluding 0-API schools so that they don't skew our results!)
tracts_joinschools_api = gpd.sjoin(schools_gdf_api, tracts_acs_gdf_ac, how='right')

# dissolve the tracts by GEOID, using 'API' as the column we'll aggregate and 'mean' as our aggfunc
tracts_meanAPI = tracts_joinschools_api[['GEOID', 'API', 'geometry']].dropna(how='any').dissolve(by='GEOID',
                                                                                                 aggfunc='mean')

# plot the tracts, coloring them by mean API
fig, ax = plt.subplots(figsize = (20,20)) 
tracts_meanAPI.plot(ax=ax,column='API', 
                    scheme='equalinterval',
                    cmap="cool_r",
                    edgecolor="grey",
                    legend=True, legend_kwds={'title': 'mean API (tracts)'})
# add the schools, coloring them by API (so we can check that the mean APIs we calculated are resonable)
schools_gdf_api.plot(ax=ax, column='API', cmap='cool_r', edgecolor='black', linewidth=0.3, markersize=25,
                 legend=True, legend_kwds={'label': "API (schools)", 'orientation': "horizontal"})

-->

----------------------------

## 7.4 Recap
We discussed how we can combine datasets to enhance any geospatial data analyses you could do. Key concepts include:
-  Attribute joins
	- `.merge()`
- Spatial joins (order matters!)
	- `gpd.sjoin()`
- Aggregation
	-`.groupby()`
	- `.dissolve()` (preserves geometry)

---
<div style="display:inline-block;vertical-align:middle;">
<a href="https://dlab.berkeley.edu/" target="_blank"><img src ="assets/images/dlab_logo.png" width="75" align="left">
</a>
</div>

<div style="display:inline-block;vertical-align:middle;">
    <div style="font-size:larger">&nbsp;D-Lab @ University of California - Berkeley</div>
    <div>&nbsp;Team Geo<div>
</div>
        


