# 14. Making Plots and Maps with Altair

The Python Altair library is great because it works with both pandas dataframes and geopandas geodataframes. It allows you to create all kinds of plots and also to make makes. Moreover the plots can be linked to the maps (but not vice versa) so that selecting data on the plot in turn highlights the geographies for related areas. We demonstrate this below with census data.

This is powerful because you can do all this with just one Python library - instead of learning one for plotting and one for mapping.  You can do this with matplotlib as well but the Altair syntax is a bit less complex.


For more information see the Altair website: https://altair-viz.github.io/

#Import libraries including altair
import numpy as np
import pandas as pd
import altair as alt

# Uncomment & Install or Upgrade geopandas if necessary
#!pip install GeoPandas==0.8.2

import geopandas as gpd

!ls notebook_data/census/ACS5yr/

## Load ACS 5 year (2014 - 2018) data

df = pd.read_csv("notebook_data/census/ACS5yr/census_variables_CA_2018.csv", dtype={'FIPS_11_digit':str})

# Take a look at the data
df.head()

# See what columns we have complete data for (no nulls) and what the datatypes are
df.info()

## Subset the data so we are only looking at Alameda County (fips code == 1)

df2 = df[df.county_fips==1]

df2.head(2)

## Make an Altair scatter plot 

that visualizes the relationship between median household income and the percent of households that are owner-occupied.


alt.Chart(df2).mark_circle(size=50).encode(
   x='med_hhinc',
   y='p_owners'
).properties(
   height=350, width=500
)

df2.shape

!ls notebook_data/census/Tracts

## Read in the Census Tract geographic data

into a GeoPandas GeoDataFrame

tracts = gpd.read_file('zip://./notebook_data/census/Tracts/cb_2018_06_tract_500k.zip')

tracts.head(2)

tracts.plot()

## Subset to keep only the tracts for Alameda County

tracts=tracts[tracts.COUNTYFP=='001']

tracts.plot()

## Merge the ACS dataframe into the census tracts geodataframe

tracts2 = tracts.merge(df2, how='left', left_on="GEOID", right_on="FIPS_11_digit")

tracts2.head(2)

## Create a Thematic Map

Use the Geopandas Plot method to create a map of tracts colored by median household income values.

tracts2.plot(column='med_hhinc', legend=True)

## Make the same map with Altair

alt.Chart(tracts2).mark_geoshape().encode(
    color='med_hhinc'
).properties(
    width=500,
    height=300
)

## Link Atair Scatterplot and Map

# First create a selection object
my_selection = alt.selection_interval()

# Create a background map
background_map = alt.Chart(tracts2).mark_geoshape(
    fill= 'lightgray',
    stroke = 'white'
).properties(
    width=400,
    height=300
)

# Create the interactive scatterplot
# by addng the selection object
the_scatterplot = alt.Chart(tracts2).mark_circle(size=50).encode(
   x='med_hhinc',
   y='p_owners'
).properties(
   width=375,
   height=300
).add_selection(
    my_selection
)

# Create the interactive map
# by adding the selection object
income_map = alt.Chart(tracts2).mark_geoshape().encode(
    color='med_hhinc'
).properties(
    width=400,
    height=350
).transform_filter(
    my_selection
)

# Link the maps (background_map and income_map)
# to the scatterplot (the_scatterplot)
the_scatterplot | (background_map + income_map)

## Try dragging a box around a subset of the points on the scatterplot and see what happens to the map.

