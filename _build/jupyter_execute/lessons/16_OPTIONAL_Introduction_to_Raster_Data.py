# 16. Introduction to Raster Data

This is a very brief introduction to reading raster data and basic manipulations in Python. We'll walk through one of the most commonly used raster python packages, `rasterio`. We'll be using the [National Land Cover Database (NLCD)](https://www.mrlc.gov/data/legends/national-land-cover-database-2016-nlcd2016-legend) from 2011 that was downloaded from [here](https://viewer.nationalmap.gov/basic).

<img src="https://www.mdpi.com/remotesensing/remotesensing-11-02971/article_deploy/html/images/remotesensing-11-02971-g004.png" width="600">

> Note: They also have a [cool online viewer](https://www.mrlc.gov/viewer/) that is free and open access.

import pandas as pd
import geopandas as gpd

import matplotlib # base python plotting library
import matplotlib.pyplot as plt # submodule of matplotlib
from matplotlib.patches import Patch

import json
import numpy as np

# To display plots, maps, charts etc in the notebook
%matplotlib inline  

To use raster data we'll be using the `rasterio` package, which is a popular package that helps you read, write, and manipulate raster data. We'll also be using `rasterstats`.

import rasterio
from rasterio.plot import show, plotting_extent
from rasterio.mask import mask

from rasterstats import zonal_stats

## 16.1 Import data and plot

To open our NLCD subset data, we'll use the `rasterio.open` function

nlcd_2011 = rasterio.open('notebook_data/raster/nlcd2011_sf.tif')

Let's check out what we get.

nlcd_2011

Let's dissect this output here. We can look at the helper documentation for clues.

?rasterio.open

Which reads that the function returns a ``DatasetReader`` or ``DatasetWriter`` object. Unlike in `GeoPandas` which we've been utilizing a lot of, we don't have a directly editable object here. However, `rasterio` does have functions in place where we can still use this returned object directly.

For example, we can easily plot our NLCD data using `rasterio.plot.show`.

rasterio.plot.show(nlcd_2011)

And just like how we formatted our `matplotlib` plots when we were using GeoDataFrames, we can still do that with this raster plotting function.

?rasterio.plot.show

fig, ax = plt.subplots(figsize=(8,8))
plt_nlcd = rasterio.plot.show(nlcd_2011, cmap='Pastel2', ax=ax)

(Take note of what you think could be improved here... we'll come back to this)

We can also plot a histogram of our data in a very similar way.

rasterio.plot.show_hist(nlcd_2011, bins=30)

We can see that we have more values on the lower end than on the higher end. To really understand the values that we see here let's [take a look at the legend](https://www.mrlc.gov/data/legends/national-land-cover-database-2016-nlcd2016-legend).

<img src ="assets/images/NLCD_Colour_Classification_Update.jpg" width="200" align="center">

## 16.2 Raster data structure

> *Note:* If you need a refresher on what raster data is and relevant terminology. Check out the first lesson that covers geospatial topics

Now that we have a basic grasp on how to pull in and plot raster data, we can dig a little deeper to see what information we have.

First let's check the number of bands there are in our dataset.

nlcd_2011.count

In this case we only have 1 band. If you're pulling in aerial image, you might have 3 bands (red, green, blue). In the case you're bringing in remote sensing data like Landsat or MODIS you might have more!

Not let's check out what meta data we have.

nlcd_2011.meta

So we have a lot of good information here. Let's unpack it:

- `driver`: the file type (simialr to what we see in `open` and Geopandas `open`)
- `dtype`: the data type of each of your pixels
- `nodata`: the value that is set for no data pixels
- `width`: the number of pixels wide your dataset is
- `height`: the number of pixels high your dataset is
- `count`: the number of bands in your dataset
- `crs`: the coordiante reference system (CRS) of your data
- `transform`: the affine transform matrix that tell us which pixel locations in each row and column align with spatial locations (longitude, latitude).

We can also get similar information by calling `profile`.

nlcd_2011.profile

nlcd_2011.crs

Okay, but now we want to actually access our data. We can read in our data as a Numpy ndarray.

nlcd_2011_array = nlcd_2011.read()
nlcd_2011_array

And we can call shape and see we have a 3D array.

nlcd_2011_array.shape

Much like other Numpy arrays, we can look at the min, mean, and max of our data

print("Minimum: ", np.nanmin(nlcd_2011_array))
print("Max: ", np.nanmean(nlcd_2011_array))
print("Mean: ", np.nanmax(nlcd_2011_array))

And since we have our data in an array form now, we can plot it using not a `rasterio` function, but simply `plt.imshow`.

plt.imshow(nlcd_2011_array[0,:,:])

Notice that we specified this plotting by making our array 2D. This gives us more flexibility about how we want to create our plots. You can do something like this:

> This definitely looks more scary than it actually is. Essentially we are:
> 1. constructing a full color spectrum with all the colors we want
> 2. If values are outside of this range, we set the color tot white
> 3. we set the boudnaries for each of these colors so we know which color to assign to what value
> 4. we create legend labels for our legend
>
> This process is only really needed if we want to have a color map for specific values outside of a specific named `matplotlib` named color map.

# Define the colors you want
cmap = matplotlib.colors.ListedColormap(['royalblue', #11
                                        'white', #12
                                        'beige', #21
                                        'salmon', #22
                                        'red', #23
                                        'darkred', #24
                                        'grey', #31
                                        'yellowgreen', #41
                                        'darkgreen', #42
                                        'lightgreen', # 43
                                        'darkgoldenrod', #51
                                        'tan', # 52
                                        'wheat', # 71
                                        'darkkhaki', #72
                                        'darkseagreen', #73
                                         'mediumseagreen', #74
                                         'gold', #81
                                         'chocolate', #82
                                         'lightsteelblue', #90
                                         'steelblue', #95
                                        ])
cmap.set_under('#FFFFFF')
cmap.set_over('#FFFFFF')
# Define a normalization from values -> colors
norm = matplotlib.colors.BoundaryNorm([10.5,
                                       11.5,
                                       12.5,
                                       21.5,
                                       22.5,
                                       23.5,
                                       24.5,
                                       31.5,
                                       41.5, 
                                       42.5,
                                       43.5,
                                       51.5,
                                       52.5,
                                       71.5,
                                       72.5,
                                       73.5,
                                       74.5,
                                       81.5,
                                       82.5,
                                       90.5,
                                       95.5,
                                      ],20)


legend_labels = { 'royalblue':'Open Water', 
                  'white':'Perennial Ice/Snow',
                  'beige':'Developed, Open Space',
                  'salmon':'Developed, Low Intensity',
                  'red':'Developed, Medium Intensity',
                  'darkred':'Developed High Intensity',
                  'grey':'Barren Land (Rock/Sand/Clay)',
                  'yellowgreen':'Deciduous Forest',
                  'darkgreen':'Evergreen Forest',
                  'lightgreen':'Mixed Forest',
                  'darkgoldenrod':'Dwarf Scrub',
                  'tan':'Shrub/Scrub',
                  'wheat':'Grassland/Herbaceous',
                  'darkkhaki':'Sedge/Herbaceous',
                  'darkseagreen':'Lichens',
                  'mediumseagreen':'Moss',
                  'gold':'Pasture/Hay',
                  'chocolate':'Cultivated Crops',
                  'lightsteelblue':'Woody Wetlands',
                  'steelblue':'Emergent Herbaceous Wetlands'}

fig, ax = plt.subplots(figsize=(8, 8))
plt_nlcd = ax.imshow(nlcd_2011_array[0,:,:], cmap=cmap, norm=norm)
ax.set_title('NLCD 2011', fontsize=30)

# Remove axes
ax.set_frame_on(False)
plt.setp(ax.get_xticklabels(), visible=False)
plt.setp(ax.get_yticklabels(), visible=False)
ax.set_xticks([])
ax.set_yticks([])

# Add color bar
patches = [Patch(color=color, label=label)
           for color, label in legend_labels.items()]

fig.legend(handles=patches, facecolor="white",bbox_to_anchor=(1.1, 1.05))




## 16.2 Mask raster data

*Masking* is a common action that is done with raster data where you "mask" everything outside of a certain geometry.

To do this let's first bring in the san francisco county data.

# Bring in census tracts
tracts_gdf = gpd.read_file("zip://notebook_data/census/Tracts/cb_2013_06_tract_500k.zip").to_crs('epsg:4326')

# Narrow it down to San Francisco County
tracts_gdf_sf = tracts_gdf[tracts_gdf['COUNTYFP']=='075']

tracts_gdf_sf.plot()
plt.show()

We forgot about the Farollon islands! Let's crop those out.

# Crop out Farallon
tracts_gdf_sf = tracts_gdf_sf.cx[-122.8:-122.35, 37.65:37.85].copy().reset_index(drop=True)

tracts_gdf_sf.plot()
plt.show()

We'll want to check the crs of our GeoDataFrame

tracts_gdf_sf.crs

Now we will call the `mask` function from `rasterio`. Let's look at the documentation first.

?mask

We actually recommend using the `rioxarray` method instesd. So we'll import a new package.

import rioxarray as rxr

Open our same NLCD data...

nlcd_2011 = rxr.open_rasterio('notebook_data/raster/nlcd2011_sf.tif',
                              masked=True).squeeze()

Reproject our NLCD to be in the same coordinate reference system as the san francisco data

from rasterio.crs import CRS

!rio --version

# Currently doesn't work
# Issue: https://github.com/mapbox/rasterio/issues/2103
test = nlcd_2011.rio.reproject(tracts_gdf_sf.crs)

And clip our data to the san francisco geometry

clipped = test.rio.clip(tracts_gdf_sf.geometry, tracts_gdf_sf.crs, drop=False, invert=False)

We can easily plot this using `.plot()`

clipped.plot()

And we can also make a pretty map like we did before.

fig, ax = plt.subplots(figsize=(8, 8))
clipped.plot(cmap=cmap, norm=norm, ax=ax,  add_colorbar=False)
ax.set_title('NLCD 2011 (Cropped)', fontsize=30)

# Add color bar
patches = [Patch(color=color, label=label)
           for color, label in legend_labels.items()]

fig.legend(handles=patches, facecolor="white",bbox_to_anchor=(1.1, 1.05))

# Remove axes
ax.set_frame_on(False)
plt.setp(ax.get_xticklabels(), visible=False)
plt.setp(ax.get_yticklabels(), visible=False)
ax.set_xticks([])
ax.set_yticks([])



and you can save your work out to a new file!

clipped.rio.to_raster("outdata/nlcd2011_sf_cropped.tif", tiled=True)

## 16.3 Aggregate raster to vector

Another common step we see in a lot of raster work flows is questions that go along the lines of "How do I find the average of my raster within my vector data shapes"?

We can do this by *aggregating* to our vector data. For this example we'll ask the question, "What is the majority class I have in each of the census tracts in San Francisco?"

For this we'll turn to the `rasterstas` pacakge which has a handy function called `zonal_stats`. By default, the function will give us the minimum, maximum, mean, and count. But there also a lot more statistics that the function can return beyond this:
- sum
- std
- median
- majority
- minority
- unique
- range
- nodata
- percentile

So we'll first bring back our clipped census tracts shapefile we have for san francisco.

tracts_gdf_sf.plot()
plt.show()

And we'll check out the `zonal_stats` documentation to get a better sense of how we can customize the arguments to better fit our needs.

?zonal_stats

Which doesn't tell us a ton. Since we don't have `gen_zonal_stas` loaded, we can go look at the documentation online: https://pythonhosted.org/rasterstats/rasterstats.html

After we check that out, let's get on rolling and actually get our zonal stats by census tract.

with rasterio.open('notebook_data/raster/nlcd2011_sf.tif') as src:
    affine = src.transform
    array = src.read(1)
    df_zonal_stats = pd.DataFrame(zonal_stats(tracts_gdf_sf, array, affine=affine, stats=['majority', 'unique']))

There's a lot going on in the cell above, let's break it down:
- `affine` object grabbed the transform of our raster data
- `array` object read the first band we have in our raster dataset
- `df_zonal_stats` has the results of our `zonal_stats` and then coerced it to be a dataframe.

So from that caell, we get `df_zonal_stats` which looks like:

df_zonal_stats

So now, we can merge this back onto our geodataframe so we can add the majority classes and unique number of classes as attributes.

tracts_gdf_sf_zs = pd.concat([tracts_gdf_sf, df_zonal_stats[['majority','unique']]], axis=1) 

And we can make a map that shows, for example, the majority class we have in each census tract.

fig, ax = plt.subplots(figsize=(8,8))
tracts_gdf_sf_zs.plot(column='majority', cmap=cmap, norm=norm, ax=ax)

# Add color bar
patches = [Patch(color=color, label=label)
           for color, label in legend_labels.items()]

fig.legend(handles=patches, facecolor="white",bbox_to_anchor=(1.1, 1.05))

plt.show()

## 16.4 Other resources
We really only grazed the surface here. We've linked a couple of resources that dive into raster data.

- [EarthLab](https://www.earthdatascience.org)
- [Software Carpentry](https://carpentries-incubator.github.io/geospatial-python/aio/index.html)
- [Intro to Python GIS](https://automating-gis-processes.github.io/CSC/index.html)

---
<div style="display:inline-block;vertical-align:middle;">
<a href="https://dlab.berkeley.edu/" target="_blank"><img src ="assets/images/dlab_logo.png" width="75" align="left">
</a>
</div>

<div style="display:inline-block;vertical-align:middle;">
    <div style="font-size:larger">&nbsp;D-Lab @ University of California - Berkeley</div>
    <div>&nbsp;Team Geo<div>
</div>
        

