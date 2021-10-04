# Lesson 5. Data-driven Mapping

*Data-driven mapping* refers to the process of using data values to determine the symbology of mapped features. Color, shape, and size are the three most common symbology types used in data-driven mapping.
Data-driven maps are often refered to as thematic maps.


- 5.1 Choropleth Maps
- 5.2 Issues with Visualization
- 5.3 Classification Schemes
- 5.4 Point Maps
- 5.5 Mapping Categorical Data
- 5.6 Recap
- **Exercise**: Data-Driven Mapping

<br>
<font color='grey'>
    <b>Instructor Notes</b>

- Datasets used
    - 'notebook_data/california_counties/CaliforniaCounties.shp'
    - 'notebook_data/alco_schools.csv'
    - 'notebook_data/transportation/BerkeleyBikeBlvds.geojson'
- Expected time to complete
    - Lecture + Questions: 30 minutes
    - Exercises: 15 minutes
</font>


### Types of Thematic Maps

There are two primary types of maps used to convey data values:

- `Choropleth maps`: set the color of areas (polygons) by data value
- `Point symbol maps`: set the color or size of points by data value

We will discuss both of these types of maps in more detail in this lesson. But let's take a quick look at choropleth maps. 

import pandas as pd
import geopandas as gpd

import matplotlib # base python plotting library
import matplotlib.pyplot as plt # submodule of matplotlib

# To display plots, maps, charts etc in the notebook
%matplotlib inline  

# 5.1 Choropleth Maps
Choropleth maps are the most common type of thematic map.

Let's take a look at how we can use a geodataframe to make a choropleth map.

We'll start by reloading our counties dataset from Day 1.

counties = gpd.read_file('notebook_data/california_counties/CaliforniaCounties.shp')

counties.head()

counties.columns

Here's a plain map of our polygons.

counties.plot()

Now, for comparison, let's create a choropleth map by setting the color of the county based on the values in the population per square mile (`POP12_SQMI`) column.

counties.plot(column='POP12_SQMI', figsize=(10,10))

That's really the heart of it. To set the color of the features based on the values in a column, set the `column` argument to the column name in the gdf.
> **Protip:** 
- You can quickly right-click on the plot and save to a file or open in a new browser window.

By default map colors are linearly scaled to data values. This is called a `proportional color map`.

- The great thing about `proportional color maps` is that you can visualize the full range of data values.



We can also add a legend, and even tweak its display.

counties.plot(column='POP12_SQMI', figsize=(10,10), legend=True)
plt.show()

counties.plot(column='POP12_SQMI', figsize=(10,10), legend=True,
                    legend_kwds={'label': "Population Density per mile$^2$",
                                 'orientation': "horizontal"},)
plt.show()

<div style="display:inline-block;vertical-align:top;">
    <img src="http://www.pngall.com/wp-content/uploads/2016/03/Light-Bulb-Free-PNG-Image.png" width="30" align=left > 
</div>  
<div style="display:inline-block;">

#### Question
</div>

Why are we plotting `POP12_SQMI` instead of `POP2012`?

Your response here:






### Note: Types of Color Maps

There are a few different types of color maps (or color palettes), each of which has a different purpose:
- *diverging* - a "diverging" set of colors are used so emphasize mid-range values as well as extremes.
- *sequential* - usually with a single color hue to emphasize changes in magnitude, where darker colors typically mean higher values
- *qualitative* - a diverse set of colors to identify categories and avoid implying quantitative significance.

<img src="http://www.gnuplotting.org/figs/colorbrewer.png"></img>

<small><center><i>Image Credit: <a href="https://commons.wikimedia.org/wiki/File:Anatone_WA.jpg"> Dsdugan at English Wikipedia </a></i></small></center>

> **Pro-tip**: You can actually see all your color map options if you misspell what you put in `cmap` and try to run-in. Try it out!

> **Pro-tip**: Sites like [ColorBrewer](https://colorbrewer2.org/#type=sequential&scheme=Blues&n=3) let's you play around with different types of color maps. If you want to create your own, [The Python Graph Gallery](https://python-graph-gallery.com/python-colors/) is a way to see what your Python color options are.


# 5.2 Issues with Visualization

### Types of choropleth data

There are several types of quantitative data variables that can be used to create a choropleth map. Let's consider these in terms of our ACS data.

- **Count**
    - counts, aggregated by feature
        - *e.g. population within a census tract*

- **Density**
    - count, aggregated by feature, normalized by feature area
        - *e.g. population per square mile within a census tract*

- **Proportions / Percentages**
    - value in a specific category divided by total value across in all categories
        - *e.g. proportion of the tract population that is white compared to the total tract population*

- **Rates / Ratios**
    - value in one category divided by value in another category
        - *e.g. homeowner-to-renter ratio would be calculated as the number of homeowners (c_owners/ c_renters)*

### Interpretability of plotted data
The goal of a choropleth map is to use color to visualize the spatial distribution of a quantitative variable.

Brighter or richer colors are typically used to signify higher values.

A big problem with choropleth maps is that our eyes are drawn to the color of larger areas, even if the values being mapped in one or more smaller areas are more important.



We see just this sort of problem in our population-density map. 

***Why does our map not look that interesting?*** Take a look at the histogram below, then consider the following question.

plt.hist(counties['POP12_SQMI'],bins=40)
plt.title('Population Density per mile$^2$')
plt.show()

<div style="display:inline-block;vertical-align:top;">
    <img src="http://www.pngall.com/wp-content/uploads/2016/03/Light-Bulb-Free-PNG-Image.png" width="30" align=left > 
</div>  
<div style="display:inline-block;">

#### Question
</div>

What county does that outlier represent? What problem does that pose?

Your response here:






# 5.3 Classification schemes

Let's try to make our map more interpretable!

The common alternative to a proportionial color map is to use a **classification scheme** to create a **graduated color map**. This is the standard way to create a **choropleth map**.

A **classification scheme** is a method for binning continuous data values into 4-7 classes (the default is 5) and map those classes to a color palette. 

### The commonly used classifications schemes:

- **Equal intervals**
    - equal-size data ranges (e.g., values within 0-10, 10-20, 20-30, etc.)
    - <u>pros</u>:
        - best for data spread across entire range of values
        - easily understood by map readers
    - <u>cons</u>:
        - but avoid if you have highly skewed data or a few big outliers
 
 
- **Quantiles**
    - equal number of observations in each bin
    - <u>pros</u>:
        - looks nice, becuase it best spreads colors across full set of data values
        - thus, it's often the default scheme for mapping software
    - <u>cons</u>:
        - bin ranges based on the number of observations, not on the data values
        - thus, different classes can have very similar or very different values.
 
 
- **Natural breaks**
    - minimize within-class variance and maximize between-class differences
    - e.g. 'fisher-jenks'
    - </u>pros</u>:
        - great for exploratory data analysis, because it can identify natural groupings
    - <u>cons</u>:
        - class breaks are best fit to one dataset, so the same bins can't always be used for multiple years
 
 
- **Manual** 
    - classifications are user-defined
    - <u>pros</u>: 
        - especially useful if you want to slightly change the breaks produced by another scheme
        - can be used as a fixed set of breaks to compare data over time
    - <u>cons</u>:
        - more work involved

### Classification schemes and GeoDataFrames

Classification schemes can be implemented using the geodataframe `plot` method by setting a value for the **scheme** argument. This requires the [pysal](https://pysal.org/) and [mapclassify](https://pysal.org/mapclassify) libraries to be installed in your Python environment. 

Here is a list of the `classification schemes` names that we will use:
-  `equalinterval`, `quantiles`,`fisherjenks`,`naturalbreaks`, and `userdefined`.

For more information about these classification schemes see the [pysal mapclassifiers web page](https://pysal.org/mapclassify/api.html) or check out the help docs.

--------------------------

### Classification schemes in action

Let's redo the last map using the `quantile` classification scheme.

- What is different about the code? About the output map?

# Plot population density - mile^2
fig, ax = plt.subplots(figsize = (10,5)) 
counties.plot(column='POP12_SQMI', 
                   scheme="quantiles",
                   legend=True,
                   ax=ax
                   )
ax.set_title("Population Density per Sq Mile")

Note: For interval notation
- A square bracket is *inclusive*
- A parentheses is *exclusive*

### User Defined Classification Schemes

You may get pretty close to your final map without being completely satisfied. In this case you can manually define a classification scheme.

Let's customize our map with a `user-defined` classification scheme where we manually set the breaks for the bins using the `classification_kwds` argument.

fig, ax = plt.subplots(figsize = (14,8)) 
counties.plot(column='POP12_SQMI',
                    legend=True, 
                    cmap="RdYlGn", 
                    scheme='user_defined', 
                    classification_kwds={'bins':[50,100,200,300,400]},
                    ax=ax)
ax.set_title("Population Density per Sq Mile")

Since we are customizing our plot, we can also edit our legend to specify and format the text so that it's easier to read.

- We'll use `legend_labels_list` to customize the labels for group in the legend.

fig, ax = plt.subplots(figsize = (14,8)) 
counties.plot(column='POP12_SQMI',
                    legend=True, 
                    cmap="RdYlGn", 
                    scheme='user_defined', 
                    classification_kwds={'bins':[50,100,200,300,400]},
                    ax=ax)

# Create the labels for the legend
legend_labels_list = ['<50','50 to 100','100 to 200','200 to 300','300 to 400','>400']

# Apply the labels to the plot
for j in range(0,len(ax.get_legend().get_texts())):
        ax.get_legend().get_texts()[j].set_text(legend_labels_list[j])

ax.set_title("Population Density per Sq Mile")

### Let's plot a ratio

If we look at the columns in our dataset, we see we have a number of variables
from which we can calculate proportions, rates, and the like.

Let's try that out:

counties.head()

fig, ax = plt.subplots(figsize = (15,6)) 

# Plot percent hispanic as choropleth
counties.plot(column=(counties['HISPANIC']/counties['POP2012'] * 100), 
                        legend=True, 
                        cmap="Blues", 
                        scheme='user_defined', 
                        classification_kwds={'bins':[20,40,60,80]},
                        edgecolor="grey",
                        linewidth=0.5,
                        ax=ax)

legend_labels_list = ['<20%','20% - 40%','40% - 60%','60% - 80%','80% - 100%']
for j in range(0,len(ax.get_legend().get_texts())):
        ax.get_legend().get_texts()[j].set_text(legend_labels_list[j])

ax.set_title("Percent Hispanic Population")
plt.tight_layout()

<div style="display:inline-block;vertical-align:top;">
    <img src="http://www.pngall.com/wp-content/uploads/2016/03/Light-Bulb-Free-PNG-Image.png" width="30" align=left > 
</div>  
<div style="display:inline-block;">

#### Questions
</div>

1. What new options and operations have we added to our code?
1. Based on our code, what title would you give this plot to describe what it displays?
1. How many bins do we specify in the `legend_labels_list` object, and how many bins are in the map legend? Why?

Your responses here:






# 5.4 Point maps

Choropleth maps are great, but mapping using point symbols enables us to visualize our spatial data in another way. 

If you know both mapping methods you can expand how much information you can show in one map. 

For example, point maps are a great way to map `counts` because the varying sizes of areas are deemphasized.



-----------------------
Let's read in some point data on Alameda County schools.

schools_df = pd.read_csv('notebook_data/alco_schools.csv')
schools_df.head()

We got it from a plain CSV file, let's coerce it to a GeoDataFrame.

schools_gdf = gpd.GeoDataFrame(schools_df, 
                               geometry=gpd.points_from_xy(schools_df.X, schools_df.Y))
schools_gdf.crs = "epsg:4326"

Then we can map it.

schools_gdf.plot()
plt.title('Alameda County Schools')

### Proportional Color Maps
**Proportional color maps** linearly scale the `color` of a point symbol by the data values.

Let's try this by creating a map of `API`. API stands for *Academic Performance Index*, which is a measurement system that looks at the performance of an individual school.

schools_gdf.plot(column="API", cmap="gist_heat", 
                 edgecolor="grey", figsize=(10,8), legend=True)
plt.title("Alameda County, School API scores")

When you see that continuous color bar in the legend you know that the mapping of data values to colors is not classified.


### Graduated Color Maps

We can also create **graduated color maps** by binning data values before associating them with colors. These are just like choropleth maps, except that the term "choropleth" is only used with polygon data. 

Graduated color maps use the same syntax as the choropleth maps above - you create them by setting a value for `scheme`. 

Below, we copy the code we used above to create a choropleth, but we change the name of the geodataframe to use the point gdf. 

fig, ax = plt.subplots(figsize = (15,6)) 

# Plot percent non-white with graduated colors
schools_gdf.plot(column='API', 
                        legend=True, 
                        cmap="Blues",
                        scheme='user_defined', 
                        classification_kwds={'bins':[0,200,400,600,800]},
                        edgecolor="grey",
                        linewidth=0.5,
                        #markersize=60,
                        ax=ax)

# Create a custom legend
legend_labels_list = ['0','< 200','< 400','< 600','< 800','>= 800']

# Apply the legend to the map
for j in range(0,len(ax.get_legend().get_texts())):
        ax.get_legend().get_texts()[j].set_text(legend_labels_list[j])

# Create the plot
plt.tight_layout()
plt.title("Alameda County, School API scores")

schools_gdf['API'].describe()

As you can see, the syntax for a choropleth and graduated color map is the same,
although some options only apply to one or the other.

For example, uncomment the `markersize` parameter above to see how you can further customize a graduated color map.

### Graduated symbol maps

`Graduated symbol maps` are also a great method for mapping points.  These are just like graduated color maps but instead of associating symbol color with data values they associate point size. Similarly,graduated symbol maps use `classification schemes` to set the size of point symbols. 

> We demonstrate how to make graduated symbol maps along with some other mapping techniques in the `Optional Mapping notebook` which we encourage you to explore on your own. (***Coming Soon***)

## 5.5 Mapping Categorical Data

Mapping categorical data, also called qualitative data, is a bit more straightforward. There is no need to scale or classify data values. The goal of the color map is to provide a contrasting set of colors so as to clearly delineate different categories. Here's a point-based example:

schools_gdf.plot(column='Org', categorical=True, legend=True)

## 5.6 Recap
We learned about important data driven mapping strategies and mapping concepts and can leverage what many of us know about `matplotlib`
- Choropleth Maps
- Point maps
- Color schemes 
- Classifications

# Exercise: Data-Driven Mapping

Point and polygons are not the only geometry-types that we can use in data-driven mapping!

Run the next cell to load a dataset containing Berkeley's bicycle boulevards (which we'll be using more in the following notebook).

Then in the following cell, write your own code to:
1. plot the bike boulevards;
2. color them by status (find the correct column in the head of the dataframe, displayed below);
3. color them using a fitting, good-looking qualitative colormap that you choose from [The Matplotlib Colormap Reference](https://matplotlib.org/3.1.1/gallery/color/colormap_reference.html);
4. set the line width to 5 (check the plot method's documentation to find the right argument for this!);
4. add the argument `figsize=[20,20]`, to make your map nice and big and visible!
    
Then answer the questions posed in the last cell.

<br>


To see the solution, double-click the Markdown cell below.


bike_blvds = gpd.read_file('notebook_data/transportation/BerkeleyBikeBlvds.geojson')
bike_blvds.head()

# YOUR CODE HERE:


## Double-click to see solution!

<!--

# SOLUTION:

bike_blvds.plot(column='Status', cmap='Dark2', linewidth=5, legend=True, figsize=[20,20])

-->

-------------------------------------

<div style="display:inline-block;vertical-align:top;">
    <img src="http://www.pngall.com/wp-content/uploads/2016/03/Light-Bulb-Free-PNG-Image.png" width="30" align=left > 
</div>  
<div style="display:inline-block;">

#### Questions
</div>

1. What does that map indicate about the status of the Berkeley bike boulevards?
1. What does that map indicate about the status of your Berkeley bike-boulevard *dataset*?

Your responses here:







---
<div style="display:inline-block;vertical-align:middle;">
<a href="https://dlab.berkeley.edu/" target="_blank"><img src ="assets/images/dlab_logo.png" width="75" align="left">
</a>
</div>

<div style="display:inline-block;vertical-align:middle;">
    <div style="font-size:larger">&nbsp;D-Lab @ University of California - Berkeley</div>
    <div>&nbsp;Team Geo<div>
</div>
        


