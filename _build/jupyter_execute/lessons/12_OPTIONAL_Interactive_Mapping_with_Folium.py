# 12. Interactive Mapping with Folium

In previous lessons we  used `Geopandas` and `matplotlib` to create choropleth and point maps of our data. In this notebook we will take it to the next level by creating `interactive maps` with the **folium** library. 



>### References
>
>This notebook provides an introduction to `folium`. To see what else you can do, check out the references listed below.
>
> - [Folium web site](https://github.com/python-visualization/folium)
>
> - [Folium notebook examples](https://nbviewer.jupyter.org/github/python-visualization/folium/tree/master/examples/)

### Import Libraries

import pandas as pd
import geopandas as gpd
import numpy as np

import matplotlib # base python plotting library
import matplotlib.pyplot as plt # submodule of matplotlib

# To display plots, maps, charts etc in the notebook
%matplotlib inline  

import folium # popular python web mapping tool for creating Leaflet maps
import folium.plugins

# Supress minor warnings about the syntax of CRS definitions, 
# ie "init=epsg:4269" vs "epsg:4269"
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#### Check your version of `folium` and `geopandas`.

Folium is a new and evolving Python library so make sure you have version 0.10.1 or later installed.

print(folium.__version__) # Make sure you have version 0.10.1 or later of folium!

print(gpd.__version__) # Make sure you have version 0.7.0 or later of GeoPandas!

## 12.1 Introduction

Interactive maps serve two very important purposes in geospatial analysis. First, they provde new tools for exploratory data analysis. With an interactive map you can:
- `pan` over the mapped data, 
- `zoom` into a smaller arear that is not easily visible when the full extent of the map is displayed, and 
- `click` on or `hover` over a feature to see more information about it.

Second, when saved and shared, interactive maps provide a new tool for communicating the results of your analysis and for inviting your online audience to actively explore your work.

For those of you who work with tools like ArcGIS or QGIS, interactive maps also make working in the jupyter notebook environment a bit more like working in a desktop GIS.

The goal of this notebook is to show you how to create an interactive map with your geospatial data so that you can better analyze your data and save your output to share with others. 

After completing this lesson you will be able to create an interactive map like the one shown below.

%%html
<iframe src="notebook_data/bartmap_example.html" width="1000" height="600"></iframe>

<a id="section2"></a>
## 12.2 Interactive Mapping with Folium

Under the hood, `folium` is a Python package for creating interactive maps with [Leaflet](https://leafletjs.com), a popular javascript web mapping library.  

Let's start by creating a interactive map with the `folium.Map` function and display it in the notebook.

# Create a new folium map and save it to the variable name map1
map1 = folium.Map(location=[37.8721, -122.2578],   # lat, lon around which to center the map
                 width="100%",                     # the width & height of the output map
                 height=500,                       # in pixels (int) or in percent of available space (str)
                 zoom_start=13)                    # the zoom level for the data to be displayed (3-20)

map1  # display the map in the notebook

Let's discuss the map above and the code we used to generate it.

At any time you can enter the following command to get help with `folium.Map`:


# uncomment to see help docs
?folium.Map

Let's make another folium map using the code below:

# Create a new folium map and save it to the variable name map1
#
map1 = folium.Map(location=[37.8721, -122.2578],   # lat, lon around which to center the map
                 tiles='CartoDB Positron',
                 #width=800,                        # the width & height of the output map
                 #height=600,                       # in pixels or in percent of available space
                 zoom_start=13)                    # the zoom level for the data to be displayed

<div style="display:inline-block;vertical-align:top;">
    <img src="https://image.flaticon.com/icons/svg/87/87705.svg" width="30" align=left > 
</div>  
<div style="display:inline-block;">

#### Questions
</div>

- What's new in the code?

- How do you think that will change the map?

Let's display the map and see what changes...

map1  # display map in notebook

Notice how the map changes when you change the underlying **tileset** from the default, which is `OpenStreetMap`, to `CartoDB Positron`. 
> [OpenStreetMap](https://www.openstreetmap.org/#map=5/38.007/-95.844) is the largest free and open source dataset of geographic information about the world. So it is the default basemap for a lot of mapping tools and libraries.

- You can find a list of the available tilesets you can use in the help documentation (`folium.Map?`), a snippet of which is shown below:

<pre>
Generate a base map of given width and height with either default
tilesets or a custom tileset URL. The following tilesets are built-in
to Folium. Pass any of the following to the "tiles" keyword:

    - "OpenStreetMap"
    - "Mapbox Bright" (Limited levels of zoom for free tiles)
    - "Mapbox Control Room" (Limited levels of zoom for free tiles)
    - "Stamen" (Terrain, Toner, and Watercolor)
    - "Cloudmade" (Must pass API key)
    - "Mapbox" (Must pass API key)
    - "CartoDB" (positron and dark_matter)
</pre>


#### Exercise

Take a few minutes to try some of the different tilesets in the code below and see how they change the output map. *Avoid the ones that don't require an API key*.

# Make changes to the code below to change the folium Map
## Try changing the values for the zoom_start and tiles parameters.
map1 = folium.Map(location=[37.8721, -122.2578],   # lat, lon around which to center the map
                 tiles='Stamen Watercolor',         # basemap aka baselay or tile set
                 width=800,                        # the width & height of the output map
                 height=500,                       # in pixels or percent of available space
                 zoom_start=13)                    # the zoom level for the data to be displayed

#display the map
map1

<a id="section3"></a>
## 12.3 Adding a Map Layer

Now that we have created a folium map, let's add our California County data to the map. 

First, let's read that data into a Geopandas geodataframe.

# Alameda county census tract data with the associated ACS 5yr variables.
ca_counties_gdf = gpd.read_file("notebook_data/california_counties/CaliforniaCounties.shp")

Take another brief look at the geodataframe to recall the contents.

# take a look at first two rows
ca_counties_gdf.head(2)

# take a look at all column names
ca_counties_gdf.columns

### Adding a layer with folium.GeoJson

Folium provides a number of ways to add vector data - points, lines, and polygons - to a map. 

The data we are working with are in Geopandas geodataframes. The main folium function for adding these to the map is `folium.GeoJson`.

Let's build on our last map and add the census tracts as a `folium.GeoJson` layer. 

map1 = folium.Map(location=[37.8721, -122.2578],   # lat, lon around which to center the map
                 tiles='CartoDB positron',         # basemap aka baselay or tile set
                 width=800,                       # the width & height of the output map
                 height=600,                      # in pixels or in percent of available space
                 zoom_start=6)                    # the zoom level for the data to be displayed

# Add the census tracts to the map
folium.GeoJson(ca_counties_gdf).add_to(map1)

#display the map
map1

That was pretty straight-forward, but `folium.GeoJSON` provides a lot of arguments for customizing the display of the data in the map. We will review some of these soon. However, at any time you can get more information about `folium.GeoJSON` by taking a look at the function documentation.

# Uncomment to view documentation
# folium.GeoJson?

### Checking and Transforming the CRS

It's always a good idea to check the **CRS** of your geodata before doing anything with that data. This is true when we use `folium` to make an interactive map. 

Here is how folium deals with the CRS of a geodataframe before mapping it:
- Folium checks to see if the gdf has a defined CRS
  - If the CRS is not defined, it assumes the data to be in the WGS84 CRS (epsg=4326).
  - If the CRS is defined, it will be transformed dynamically to WGS84 before mapping.


So, if your map data doesn't show up where at all or where you think it should, check the CRS of your data!
- If it is not defined, define it.

<div style="display:inline-block;vertical-align:top;">
    <img src="https://image.flaticon.com/icons/svg/87/87705.svg" width="30" align=left > 
</div>  
<div style="display:inline-block;">

#### Questions
</div>

- What is the CRS of the tract data?
- How is folium dealing with the CRS of this gdf?

# Check the CRS of the data 
print(...)

*Click here for answers*

<!---
# What is the CRS of the tract data?
tracts_gdf.crs

# How is folium dealing with the CRS of this gdf?
# Dynamically transformed to WGS84 (but it already is in that projection so no change)
--->

### Styling features with `folium.GeoJson`

Let's dive deeper into the `folium.GeoJson` function. Below is an excerpt from the help documentation for the function that shows all the available function arguments that we can set.

<div style="display:inline-block;vertical-align:top;">
    <img src="http://www.pngall.com/wp-content/uploads/2016/03/Light-Bulb-Free-PNG-Image.png" width="20" align=left > 
</div>  
<div style="display:inline-block;">

#### Question
</div>
What argument do we use to style the color for our polygons?

<pre>
folium.GeoJson(
    data,
    style_function=None,
    highlight_function=None,
    name=None,
    overlay=True,
    control=True,
    show=True,
    smooth_factor=None,
    tooltip=None,
    embed=True,
)
</pre>

Let's examine the options for the `style_function` in more detail since we will use these to change the style of our mapped data.


`style_function = lambda x: {` apply to all features being mapped (ie, all rows in the geodataframe)  
`'weight': line_weight,` set the thickness of a line or polyline where <1 is thin, >1 thick, 1 = default  
`'opacity': line_opacity,` set opacity where 1 is solid, 0.5 is semi-opaque and 0 is transparent  
`'color': line_color` set the color of the line, eg "red" or some hexidecimal color value
`'fillOpacity': opacity,` set opacity of the fill of a polygon  
`'fillColor': color` set color of the fill of a polygon  
`'dashArray': '5, 5'` set line pattern to a dash of 5 pixels on, off  
`}`



Ok! Let's try setting the style of our census tract by defining a style function.

# Define the basemap
map1 = folium.Map(location=[37.8721, -122.2578],           # lat, lon around which to center the map
                 tiles='CartoDB Positron',
                 width=1000,                       # the width & height of the output map
                 height=600,                       # in pixels
                 zoom_start=6)                    # the zoom level for the data to be displayed

# Add  the census tracts gdf layer
# setting the style of the data
folium.GeoJson(ca_counties_gdf,
               style_function = lambda x: {
                   'weight':2,
                   'color':"white",
                   'opacity':1,
                   'fillColor':"red",
                   'fillOpacity':0.6
               }
              ).add_to(map1)


map1

#### Exercise
Copy the code from our last map and paste it below. Take a few minutes edit the code to change the style of the census tract polygons.


# Your code here
map1 = folium.Map(location=[37.8721, -122.2578],           # lat, lon around which to center the map
                 tiles='Stamen Watercolor',
                 width=1000,                       # the width & height of the output map
                 height=600,                       # in pixels
                 zoom_start=10)                    # the zoom level for the data to be displayed

# Add  the census tracts gdf layer
# setting the style of the data
folium.GeoJson(ca_counties_gdf,
               style_function = lambda x: {
                   'weight':3,
                   'color':"black",
                   'opacity':1,
                   'fillColor':"none",
                   'fillOpacity':0.6
               }
              ).add_to(map1)


map1

### Adding a Tooltip

A `tooltip` can be added to a folium.GeoJson map layer to display data values when the mouse hovers over a feature.


# Double check what columns we have
ca_counties_gdf.columns

?folium.GeoJsonTooltip

# Define the basemap
map1 = folium.Map(location=[37.8721, -122.2578],           # lat, lon around which to center the map
                 tiles='CartoDB Positron',
                 width=1000,                       # the width & height of the output map
                 height=600,                       # in pixels
                 zoom_start=6)                    # the zoom level for the data to be displayed

# Add  the census tracts gdf layer
folium.GeoJson(ca_counties_gdf,
               style_function = lambda x: {
                   'weight':2,
                   'color':"white",
                   'opacity':1,
                   'fillColor':"red",
                   'fillOpacity':0.6
               },
               
               tooltip=folium.GeoJsonTooltip(
                   fields=['NAME','POP2012','POP12_SQMI' ], 
                   aliases=['County', 'Population', 'Population Density (mi2)'],
                   labels=True,
                   localize=True
               ),
              ).add_to(map1)


map1

As always, you can get more help by reading the documentation.

# Uncomment to view help
#folium.GeoJsonTooltip?

#### Exercise

Edit the code in the cell below to `add` the median age(`MED_AGE`) to the tooltip.

# Define the basemap
map1 = folium.Map(location=[37.8721, -122.2578],           # lat, lon around which to center the map
                 tiles='CartoDB Positron',
                 width=1000,                       # the width & height of the output map
                 height=600,                       # in pixels
                 zoom_start=6)                    # the zoom level for the data to be displayed

# Add  the census tracts gdf layer
folium.GeoJson(ca_counties_gdf,
               style_function = lambda x: {
                   'weight':2,
                   'color':"white",
                   'opacity':1,
                   'fillColor':"red",
                   'fillOpacity':0.6
               },
               
               tooltip=folium.GeoJsonTooltip(
                   fields=['NAME','POP2012','POP12_SQMI','MED_AGE' ], 
                   aliases=['County', 'Population', 'Population Density (mi2)', 'Median Age'],
                   labels=True,
                   localize=True
               ),
              ).add_to(map1)


map1

*Click here for answers*

<!---
# Define the basemap
map1 = folium.Map(location=[37.8721, -122.2578],           # lat, lon around which to center the map
                 tiles='CartoDB Positron',
                 width=1000,                       # the width & height of the output map
                 height=600,                       # in pixels
                 zoom_start=6)                    # the zoom level for the data to be displayed

# Add  the census tracts gdf layer
folium.GeoJson(ca_counties_gdf,
               style_function = lambda x: {
                   'weight':2,
                   'color':"white",
                   'opacity':1,
                   'fillColor':"red",
                   'fillOpacity':0.6
               },
               
               tooltip=folium.GeoJsonTooltip(
                   fields=['FID_','POP2012','POP12_SQMI','MED_AGE' ], 
                   aliases=['County ID', 'Population', 'Population Density (mi2)', 'Median Age'],
                   labels=True,
                   localize=True
               ),
              ).add_to(map1)


map1
--->

<a id="section4"></a>
## 12.4 Data Mapping

Above, we set the style for all of the census tracts to the same fill and outline colors and opacity values. 

Let's take a look at how we would use the `data values` to set the color values for the polygons. This is called a `choropleth` map or, more generally, a `thematic map`.

The `folium.Choropleth` function can be used for this.

# Uncomment to view help docs
## folium.Choropleth?

With `folium.Choropleth`, we will use some of the same style parameters that we used with `folium.GeoJson`.

We will also use some new parameters, as shown below.

First, let's take a look at the data we will map to refresh our knowledge.

print(ca_counties_gdf.columns)
ca_counties_gdf.head(2)

Now let's create a choropleth map of total population, which is in the `c_race` column.

ca_counties_gdf.head()

# Define the basemap
map2 = folium.Map(location=[37.8721, -122.2578],           # lat, lon around which to center the map
                 tiles='CartoDB Positron',
                 width=1000,                       # the width & height of the output map
                 height=600,                       # in pixels
                 zoom_start=6)                    # the zoom level for the data to be displayed


# Add the Choropleth layer
folium.Choropleth(geo_data=ca_counties_gdf.set_index('NAME'),   # The object with the geospatial data
           data=ca_counties_gdf,                                 # The object with the attribute data (can be same)
           columns=['NAME','POP2012'],                      # the ID and data columns in the data objects
           key_on="feature.id",                             # the ID in the geo_data object (don't change)
           fill_color="Reds",                               # The color palette (or color map) - see help
           fill_opacity=0.65,
           line_color="grey",
           legend=True,
           legend_name="Population",
          ).add_to(map2)

# Display the map
map2  

### Choropleth Mapping with Folium - discussion

Let's discuss the following lines from the code above in more detail.

<pre>
# Add the Choropleth layer
folium.Choropleth(geo_data=ca_counties_gdf.set_index('NAME'),
           data=ca_counties_gdf, 
           columns=['NAME','POP2012'],
           key_on="feature.id",
           fill_color="Reds",                               
           ...)


</pre>

`geo_data` and the `data`: we need to identify the objects that contains both because they could be different objects. In our example they are in the same object.

`ca_counties_gdf.set_index('NAME')`: We need to **set_index('NAME')** in order to identify the column in `geo_data` that will be used to `join` the geometries in the `geo_data` to the data values in `data`.

`columns=['NAME','POP2012']`: we identify in `data` (1) the column that will join these `data` to  `geo_data` and (2) the second column is the column with the values that will determine the color.

`fill_color="Reds":` Here we identify the name of the color palette that we will use to style the polygons. These will be the same as the `matplotlib` colormaps.


#### Question
Recall our discussion about best practices for choropleth maps. Is population count an appropriate variable to plot as a choropleth? 

# Write your thoughts here

#### Exercise

Copy and paste the code from above into the cell below to create a choropleth map of population density (`POP12_SQMI`).

Feel free to experiment with any of the `folium.Choropleth` style parameters, especially the `fill_color` which needs to be one of the `color brewer palettes` listed below:

<pre>
fill_color: string, default 'blue'
    Area fill color. Can pass a hex code, color name, or if you are
    binding data, one of the following color brewer palettes:
    'BuGn', 'BuPu', 'GnBu', 'OrRd', 'PuBu', 'PuBuGn', 'PuRd', 'RdPu',
    'YlGn', 'YlGnBu', 'YlOrBr', and 'YlOrRd'.
</pre>

# Your code here
# Define the basemap
map2 = folium.Map(location=[37.7749, -122.4194],           # lat, lon around which to center the map
                 tiles='Stamen Toner',
                 width=1000,                       # the width & height of the output map
                 height=600,                       # in pixels
                 zoom_start=10)                    # the zoom level for the data to be displayed


# Add the Choropleth layer 
folium.Choropleth(geo_data=ca_counties_gdf.set_index('NAME'),   # The object with the geospatial data
           data=ca_counties_gdf,                                 # The object with the attribute data (can be same)
           columns=['NAME','POP12_SQMI'],                      # the ID and data columns in the data objects
           key_on="feature.id",                             # the ID in the geo_data object (don't change)
           fill_color="RdPu",                               # The color palette (or color map) - see help
           fill_opacity=0.8).add_to(map2)

map2

*Click here for answers*

<!---
    # SOLUTION
    # Get our map center
    ctrX = (tracts_gdf.total_bounds[0] + tracts_gdf.total_bounds[2])/2
    ctrY = (tracts_gdf.total_bounds[1] + tracts_gdf.total_bounds[3])/2

    # Create our base map
    map2 = folium.Map(location=[ctrY, ctrX], 
                      tiles='CartoDB Positron',
                      width=800,height=600,
                      zoom_start=10)

    # Add the Choropleth layer
    folium.Choropleth(geo_data=tracts_gdf.set_index('GEOID'), 
               data=tracts_gdf,
               columns=['GEOID','pop_dens_km2'],
               key_on="feature.id",
               fill_color="PuBu",
               fill_opacity=0.65,
               line_color="grey",
               legend=True,
               legend_name="Population Density per km2",
              ).add_to(map2)

    # Display 
    map2
--->

### Choropleth Maps with Tooltips

You can add a `tooltip` to a folium.Choropleth map but the process is not straigthforward. The `folium.Choropleth` function does not have a tooltip argument the way `folium.GeoJson` does.

The workaround is to add the layer as both a `folium.Choropleth` layer and as a `folium.GeoJson` layer and bind the tooltip to the GeoJson layer.

Let's check it out below.

# Define the basemap
map3 = folium.Map(location=[37.8721, -122.2578],           # lat, lon around which to center the map
                 tiles='CartoDB Positron',
                 width=1000,                       # the width & height of the output map
                 height=600,                       # in pixels
                 zoom_start=6)                    # the zoom level for the data to be displayed


# Add the Choropleth layer
folium.Choropleth(geo_data=ca_counties_gdf.set_index('NAME'),   # The object with the geospatial data
           data=ca_counties_gdf,                                 # The object with the attribute data (can be same)
           columns=['NAME','POP2012'],                      # the ID and data columns in the data objects
           key_on="feature.id",                             # the ID in the geo_data object (don't change)
           fill_color="Reds",                               # The color palette (or color map) - see help
           fill_opacity=0.65,
           line_color="grey",
           legend=True,
           legend_name="Population",
          ).add_to(map3)

# ADD the same geodataframe to the map to display a tooltip
layer2 = folium.GeoJson(ca_counties_gdf,
    style_function=lambda x: {'color':'transparent','fillColor':'transparent'},
    tooltip=folium.GeoJsonTooltip(
        fields=['NAME','POP2012'], 
        aliases=['County', 'Population'],
        labels=True,
        localize=True
    ),
    highlight_function=lambda x: {'weight':3,'color':'white'}
).add_to(map3)



map3  # show map

#### Question  
Do you notice anything different about the `style_function` for layer2 above?

#### Exercise
Redo the above choropleth map code to map population density. Add both population and population density to the tooltip. Don't forget to update the legend name.

# Your code here

<a id="section5"></a>
## 12.5 Overlays

We can overlay other geospatial data on our folium maps.

Let's say we want to focus the previous choropleth map with tooltips (`map3`) on the City of Berkeley. We can fetch the border of the city from our census Places dataset. These data can be downloaded from the Census website. We use the cartographic boundary files not the TIGER line files as these look better on a map (clipped to shoreline).  

Specifically, we will fetch the city boundaries from the following census cartographic boundary file:

- https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_06_place_500k.zip

Then we can overlay the border of the city on the map and set the initial zoom to the center of the Berkeley boundary.

Let's try that.


First we need to read in the census places data and create a subset geodataframe for our city of interest, here Berkeley.

places = gpd.read_file("zip://notebook_data/census/Places/cb_2018_06_place_500k.zip")

places.head(2)

berkeley = places[places.NAME=='Berkeley'].copy()
berkeley.head(2)

Plot the Berkeley geodataframe to make sure it looks ok.

berkeley.plot()

# Create a new map centered on Berkeley
berkeley_map = folium.Map(location=[berkeley.centroid.y.mean(), 
                                    berkeley.centroid.x.mean()], 
                  tiles='CartoDB Positron',
                  width=800,height=600,
                  zoom_start=13)


# Add the census tract polygons as a choropleth map
layer1=folium.Choropleth(geo_data=ca_counties_gdf.set_index('NAME'),
           data=ca_counties_gdf,
           columns=['NAME','POP2012'],
           fill_color="Reds",
           fill_opacity=0.65,
           line_color="grey", #"white",
           line_weight=1,
           line_opacity=1,
           key_on="feature.id",
           legend=True,
           legend_name="Population",
           highlight=True
          ).add_to(berkeley_map)

# Add the berkeley boundary - note the fill color
layer2 = folium.GeoJson(data=berkeley,
               name='Berkeley',smooth_factor=2,
               style_function=lambda x: {'color':'black',
                                         'opacity':1,
                                         'fillColor':
                                         'transparent',
                                         'weight':3},
               ).add_to(berkeley_map)

# Add the tooltip for the census tracts as its own layer
layer3 = folium.GeoJson(ca_counties_gdf,
    style_function=lambda x: {'color':'transparent','fillColor':'transparent'},
    tooltip=folium.features.GeoJsonTooltip(
        fields=['NAME','POP2012'], 
        aliases=['County', 'Population'],
        labels=True,
        localize=True
    ),
    highlight_function=lambda x: {'weight':3,'color':'white'}
).add_to(berkeley_map)

berkeley_map  # show map

<div style="display:inline-block;vertical-align:top;">
    <img src="http://www.pngall.com/wp-content/uploads/2016/03/Light-Bulb-Free-PNG-Image.png" width="30" align=left > 
</div>  
<div style="display:inline-block;">

#### Questions
</div>

Any questions about the above map?

Does the code for the Berkeley map above differ from our previous choropleth map code?

Does the order of layer2 & layer3 matter (can they be switched?)

#### Exercise

Redo the above map with population density. Create and display the Oakland city boundary on the map instead of Berkeley and center the map on Oakland.

# Your code here

*Click here for solution*

<!---
    # SOLUTION
    oakland = places[places.NAME=='Oakland'].copy()
    oakland.plot()

    # SOLUTION
    oakland_map = folium.Map(location=[oakland.centroid.y.mean(), oakland.centroid.x.mean()], 
                      tiles='CartoDB Positron',
                      width=800,height=600,
                      zoom_start=12)

    # Add the census tract polygons as a choropleth map
    layer1=folium.Choropleth(geo_data=ca_counties_gdf.set_index('NAME'),
           data=ca_counties_gdf,
           columns=['NAME','POP2012'],
           fill_color="Reds",
           fill_opacity=0.65,
           line_color="grey", #"white",
           line_weight=1,
           line_opacity=1,
           key_on="feature.id",
           legend=True,
           legend_name="Population",
           highlight=True
          ).add_to(oakland_map)


    # Add the oakland boundary
    layer2 = folium.GeoJson(data=oakland,
                   name='Oakland',smooth_factor=2,
                   style_function=lambda x: {'color':'black','opacity':1,'fillColor':'transparent','weight':3},
                   ).add_to(oakland_map)

    # Add the tooltip
    layer3 = folium.GeoJson(ca_counties_gdf,
        style_function=lambda x: {'color':'transparent','fillColor':'transparent'},
        tooltip=folium.features.GeoJsonTooltip(
            fields=['NAME','POP2012'], 
            aliases=['County', 'Population'],
            labels=True,
            localize=True
        ),
        highlight_function=lambda x: {'weight':3,'color':'white'}
    ).add_to(oakland_map)


    oakland_map  # show map
--->

<a id="section6"></a>
## 12.6 Mapping Points and Lines

We can also add points and lines to a folium map.

Let's overlay BART stations as points and BART lines as lines to the interactive map. For the Bay Area these are data are available from the [Metropoliton Transportation Commission (MTC) Open Data portal](http://opendata.mtc.ca.gov/datasets).

We're going to try pulling in BART station data that we downloaded from the website and subsetted from the passenger-rail-stations. You can learn more about the dataset through here: http://opendata.mtc.ca.gov/datasets/passenger-rail-stations-2019

As usual, let's try pulling in the data and inspect the first couple of rows.

# Load light rail stop data
railstops = gpd.read_file("zip://notebook_data/transportation/Passenger_Rail_Stations_2019.zip")  
railstops.tail()

# Subset to keep just bart stations
bart_stations = railstops[railstops['agencyname']=='BART'].sort_values(by="station_na")
bart_stations.head()

# Repeat for the rail lines
rail_lines = gpd.read_file("zip://notebook_data/transportation/Passenger_Railways_2019.zip")  
rail_lines.head()

rail_lines.operator.value_counts()

# subset by operator to get the bart lines
bart_lines = rail_lines[rail_lines['operator']=='BART']

# Check the CRS of the geodataframes
print(bart_stations.crs)
print(bart_lines.crs)

# Quick plot
bart_stations.plot()
bart_lines.plot()

Now that we have fetched and checked the Bart data, let's do a quick folium map with it.

We will use `folium.GeoJson` to add these data to the map, just as we used it previously for the census tract polygons.

# Bart Map
map4 = folium.Map(location=[bart_stations.centroid.y.mean(), bart_stations.centroid.x.mean()], 
                  tiles='CartoDB Positron',
                  width=800,height=600,
                  zoom_start=10)


folium.GeoJson(bart_lines).add_to(map4)

folium.GeoJson(bart_stations).add_to(map4)


map4  # show map

We can also add tooltips, just as we did previously.

# Bart Map
map4 = folium.Map(location=[bart_stations.centroid.y.mean(), bart_stations.centroid.x.mean()], 
                  tiles='CartoDB Positron',
                  #width=800,height=600,
                  zoom_start=10)

# Add Bart lines
folium.GeoJson(bart_lines,
               tooltip=folium.GeoJsonTooltip(
                   fields=['operator' ],
                   aliases=['Line operator'],
                   labels=True,
                   localize=True
               ),
              ).add_to(map4)

# Add Bart stations
folium.GeoJson(bart_stations,
              tooltip=folium.GeoJsonTooltip(fields=['ts_locatio'], 
                   aliases=['Stop Name'],
                   labels=True,
                   localize=True
               ),
              ).add_to(map4)


map4  # show map

That's pretty cool, but don't you just want to click on those marker points to get a `popup` rather than hovering over for a `tooltip`?

### Mapping Points

So far we have used `folium.GeoJson` to map our BART points. By default this uses the push-pin marker symbology made popular by Google Maps. 

Under the hood, folium.GeoJson uses the default object type `folium.Marker` when the input data are points.

This is helpful to know because `folium.Marker` has a few options that allow further customization of our points.

# Uncomment to view help docs
folium.Marker?

Let's explicitly add the Bart Stations as points so we can change the `tooltips` to `popups`.

# Bart Map
map4 = folium.Map(location=[bart_stations.centroid.y.mean(), bart_stations.centroid.x.mean()], 
                  tiles='CartoDB Positron',
                  #width=800,height=800,
                  zoom_start=10)

# Add Bart lines
folium.GeoJson(bart_lines,
               tooltip=folium.GeoJsonTooltip(
                   fields=['operator' ],
                   aliases=['Line operator'],
                   labels=True,
                   localize=True
               ),
              ).add_to(map4)

# Add Bart stations
bart_stations.apply(lambda row:
                        folium.Marker(
                                  location=[row['geometry'].y, row['geometry'].x],
                                  popup=row['ts_locatio'],
                                 ).add_to(map4), axis=1)

map4  # show map

That `folium.Marker` code is a bit more complex than `folium.GeoJson` and may not be worth it unless you really want that popup behavior.

But let's see what else we can do with a `folium.Marker` by viewing the next map.

# Bart Map
map4 = folium.Map(location=[bart_stations.centroid.y.mean(), bart_stations.centroid.x.mean()], 
                  tiles='CartoDB Positron',
                  #width=800,height=600,
                  zoom_start=10)

# Add BART lines
folium.GeoJson(bart_lines,
               tooltip=folium.GeoJsonTooltip(
                   fields=['operator' ],
                   aliases=['Line operator'],
                   labels=True,
                   localize=True
               ),
              ).add_to(map4)

# Add BART Stations
icon_url = "https://gomentumstation.net/wp-content/uploads/2018/08/Bay-area-rapid-transit-1000.png"
bart_stations.apply(lambda row:
                        folium.Marker(
                                  location=[row['geometry'].y,row['geometry'].x],
                                  popup=row['ts_locatio'],
                                  icon=folium.features.CustomIcon(icon_url,icon_size=(20, 20)),
                                 ).add_to(map4), axis=1)

map4  # show map

#### Exercise

Copy and paste the code for the previous cell into the next cell and 
1. change the bart icon to "https://ya-webdesign.com/transparent450_/train-emoji-png-14.png"
2. change the popup back to a tooltip.

# Your code here

*Click here for solution*

<!---
# Bart Map
map4 = folium.Map(location=[bart_stations.centroid.y.mean(), bart_stations.centroid.x.mean()], 

                  tiles='CartoDB Positron',
                  #width=800,height=600,
                  zoom_start=10)

# Add BART lines
folium.GeoJson(bart_lines,
               tooltip=folium.GeoJsonTooltip(
                   fields=['operator' ],
                   aliases=['Line operator'],
                   labels=True,
                   localize=True
               ),
              ).add_to(map4)

# Add BART Stations
icon_url = "https://ya-webdesign.com/transparent450_/train-emoji-png-14.png"
bart_stations.apply(lambda row:
                        folium.Marker(
                                  location=[row['geometry'].y,row['geometry'].x],
                                  tooltip=row['ts_locatio'],
                                  icon=folium.features.CustomIcon(icon_url,icon_size=(20, 20)),
                                 ).add_to(map4), axis=1)

map4  # show map
--->

### folium.CircleMarkers

You may prefer to customize points as `CircleMarkers` instead of the icon or pushpin Marker style. This allows you to set size and color of a marker, either manually or as a function of a data variable.

Let's look at some code for doing this.

# Define the basemap
map5 = folium.Map(location=[bart_stations.centroid.y.mean(), bart_stations.centroid.x.mean()],   # lat, lon around which to center the map
                 tiles='CartoDB Positron',
                 #width=1000,                        # the width & height of the output map
                 #height=600,                       # in pixels
                 zoom_start=10)                    # the zoom level for the data to be displayed

# Add BART Lines
folium.GeoJson(bart_lines).add_to(map5)


# Add BART Stations
bart_stations.apply(lambda row:
                        folium.CircleMarker(
                                  location=[row['geometry'].y, row['geometry'].x],
                                  radius=10,
                                  color='purple',
                                  fill=True,
                                  fill_color='purple',
                                  popup=row['ts_locatio'],
                                 ).add_to(map5), 
                         axis=1)


map5


### folium.Circle 

You can also set the size of your circles to a fixed radius, in meters, using `folium.Circle`.  This is great for exploratory data analysis. For example, you can see what the census tract values are within 500 meters of a BART station.

# Uncomment to view
#?folium.Circle

# Define the basemap
map5 = folium.Map(location=[bart_stations.centroid.y.mean(), bart_stations.centroid.x.mean()],   # lat, lon around which to center the map
                 tiles='CartoDB Positron',
                 #width=1000,                        # the width & height of the output map
                 #height=600,                       # in pixels
                 zoom_start=10)                    # the zoom level for the data to be displayed

# Add BART Lines
folium.GeoJson(bart_lines).add_to(map5)


# Add BART Stations
bart_stations.apply(lambda row:
                        folium.Circle(
                                  location=[row['geometry'].y, row['geometry'].x],
                                  radius=500,
                                  color='purple',
                                  fill=True,
                                  fill_color='purple',
                                  popup=row['ts_locatio'],
                                 ).add_to(map5), 
                         axis=1)


map5


<div style="display:inline-block;vertical-align:top;">
    <img src="http://www.pngall.com/wp-content/uploads/2016/03/Light-Bulb-Free-PNG-Image.png" width="30" align=left > 
</div>  
<div style="display:inline-block;">

#### Question
</div>

What do you notice about the size of the circles as you zoom in/out when you compare folium.Circles and folium.CircleMarkers?

### Proportional Symbol Maps

One of the advantages of the `folium.CircleMarker` is that we can set the size of the map to vary based on a data value.

To give this a try, let's add a fake column to the `bart_stations` gdf called millions_served and set it to a value between 1 and 10.

# add a column to the bart stations gdf
bart_stations['millions_served'] = np.random.randint(1,10, size=len(bart_stations))
bart_stations.head()

# Define the basemap
map5 = folium.Map(location=[bart_stations.centroid.y.mean(), bart_stations.centroid.x.mean()],
                 tiles='CartoDB Positron',
                 #width=1000,                        # the width & height of the output map
                 #height=600,                       # in pixels
                 zoom_start=10)                    # the zoom level for the data to be displayed

folium.GeoJson(bart_lines).add_to(map5)

# Add BART Stations as CircleMarkers
# Here, some knowlege of Python string formatting is useful
bart_stations.apply(lambda row:
                        folium.CircleMarker(
                                  location=[row['geometry'].y, row['geometry'].x],
                                  radius=row['millions_served'],
                                  color='purple',
                                  fill=True,
                                  fill_color='purple',
                                  tooltip = "Bart Station: %s<br>Millions served: %s" % (row['ts_locatio'], row['millions_served'])
                    
                                 ).add_to(map5), axis=1)
map5


So if you hover over our BART stations, you see that we've formatted it nicely! Using some HTML and Python string formatting we can make our `tooltip` easier to read. 

If you want to learn more about customizing these, you can [go check this out to learn HTML basics](https://www.w3schools.com/html/html_basic.asp).  You can then [go here to learn about Python string formatting](https://python-reference.readthedocs.io/en/latest/docs/str/formatting.html).

<a id="section7"></a>
## 12.7 Creating and Saving a folium Interactive Map

Now that you have seen most of the ways you can add a geodataframe to a folium map, let's create one big map that includes several of our geodataframes.

To control the display of the data layers, we will add a `folium.LayerControl`

- A `folium.LayerControl` will allow you to toggle on/off a map's visible layers. 

- In order to add a layer to the LayerControl, the layer must have value set for its `name`.

Let's take a look. 

# Create a new map centered on the census tract data
map6 = folium.Map(location=[bart_stations.centroid.y.mean(), bart_stations.centroid.x.mean()], 
                  tiles='CartoDB Positron',
                  #width=800,height=600,
                  zoom_start=10)

# Add the counties polygons as a choropleth map
layer1=folium.Choropleth(geo_data=ca_counties_gdf.set_index('NAME'),
           data=ca_counties_gdf,
           columns=['NAME','POP2012'],
           fill_color="Reds",
           fill_opacity=0.65,
           line_color="grey", #"white",
           line_weight=1,
           line_opacity=1,
           key_on="feature.id",
           legend=True,
           legend_name="Population",
           highlight=True,
           name="Counties"
          ).add_to(map6)

# Add the tooltip for the counties as its own layer
# Don't display in the Layer control!
layer2 = folium.GeoJson(ca_counties_gdf,
    style_function=lambda x: {'color':'transparent','fillColor':'transparent'},
    tooltip=folium.features.GeoJsonTooltip(
        fields=['NAME','POP2012'], 
        aliases=['Name', 'Population'],
        labels=True,
        localize=True
    ),
    highlight_function=lambda x: {'weight':3,'color':'white'}
).add_to(layer1.geojson)

# Add Bart lines
folium.GeoJson(bart_lines,
               name="Bart Lines",
               tooltip=folium.GeoJsonTooltip(
                   fields=['operator' ],
                   aliases=['Line operator'],
                   labels=True,
                   localize=True
               ),
              ).add_to(map6)


# Add Bart stations
folium.GeoJson(bart_stations,
               name="Bart stations",
              tooltip=folium.GeoJsonTooltip(fields=['ts_locatio' ], 
                   aliases=['Stop Name'],
                   labels=True,
                   localize=True
               ),
              ).add_to(map6)

# ADD LAYER CONTROL
folium.LayerControl(collapsed=False).add_to(map6)

map6  # show map

<div style="display:inline-block;vertical-align:top;">
    <img src="https://image.flaticon.com/icons/svg/87/87705.svg" width="30" align=left > 
</div>  
<div style="display:inline-block;">

#### Questions
</div>

1. Take a look at the help docs `folium.LayerControl?`. What parameter would move the location of the LayerControl? What parameter would allow it to be closed by default?

2. Take a look at the way we added `layer2` above (this has the census tract tooltips). How has the code we use to add the layer to the map changed? Why do you think we made this change?

# Uncomment to view
#folium.LayerControl?

### Saving to an html file

By saving our map to a html we can use it later as something to add to a website or email to a colleague.

You can save any of the maps you have in the notebook using this syntax:

> map_name.save("file_name.html")

Let's try that.

map6.save('outdata/bartmap.html')

Find your html file on your computer and double-click on it to open it in a browser.

#### Extra Challenge

Check out the notebook examples and find one to try with the data we have used in this notebook. I recommend the following.

- [Mini-maps](https://nbviewer.jupyter.org/github/python-visualization/folium/blob/master/examples/MiniMap.ipynb)
- [Dual-map](https://nbviewer.jupyter.org/github/python-visualization/folium/blob/master/examples/plugin-DualMap.ipynb) (choropleth maps two census tract vars)
- [Search](https://nbviewer.jupyter.org/github/python-visualization/folium/blob/master/examples/plugin-Search.ipynb) (e.g., for a Bart Station by name)

<a id="section6"></a>
## 12.8 Recap
Here we learned about the wonderful world of `Folium`! We created interactive maps-- whether it be choropleth, points, lines, symbols... we mapped it all. 

Below you'll find a list of key functionalities we learned:
- Interactive mapping
	- `folium.Map()`
- Adding a map layer
	- `.add_to()`
	- `folium.Choropleth()`
		- `geo_data`
		- `columns`
		- `fill_color`
	- `folium.GeoJson()`
		- `style_function`
	- `folium.Marker()`
		- `icon`
	- `folium.CircleMarker()`
		- `radius`
- Adding a Tooltip
	- `folium.GeoJsonTooltip`
	- `folium.features.GeoJsonTooltip`
- Adding layer control
	- `folium.LayerControl()`

## Important note

The folium library changes often so I recommend you update your package frequently. This will give you increased functionality and may make future code easier to write. However, it might cause your existing code to break.

### References

This notebook provides an introduction to `folium`. To see what else you can do, check out the references listed below.

- [Folium web site](https://github.com/python-visualization/folium)

- [Folium notebook examples](https://nbviewer.jupyter.org/github/python-visualization/folium/tree/master/examples/)



---
<div style="display:inline-block;vertical-align:middle;">
<a href="https://dlab.berkeley.edu/" target="_blank"><img src ="assets/images/dlab_logo.png" width="75" align="left">
</a>
</div>

<div style="display:inline-block;vertical-align:middle;">
    <div style="font-size:larger">&nbsp;D-Lab @ University of California - Berkeley</div>
    <div>&nbsp;Team Geo<div>
</div>
        



