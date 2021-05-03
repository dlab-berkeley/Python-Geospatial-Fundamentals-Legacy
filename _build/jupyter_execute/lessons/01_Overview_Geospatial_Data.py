# Lesson 1. Overview of Geospatial Data

Before diving into any coding, let's first go over some core concepts.

- 1.1 Geospatial Data
- 1.2 Coordinate Reference Systems
- 1.3 Types of Spatial Data
- 1.4 Other Resources

Note that this Jupyterbook covers *a lot*! There's so much to learn and understand about the world of doing geospatial work. But we want you to keep in mind that this really only the start of your journey. All the authors who contributed to this are still learning too :)

<img src="https://pbs.twimg.com/media/EIEHbKvXUAATXhi?format=jpg&name=large" width=500>

## 1.1 Geospatial Data

So there are a couple of terms that get confused when we're trying to talk about work in this area:
- *Geographic Information Systems (GIS)*
- *Geographic Data*
- *Geospatial Data*
We'll walk through each of these term-by-term.

**Geographic Information Systems (GIS)** is probably a term that you've heard of before and it integrates many types of data, which includes spatial location. You can think of it as a framework to analyze spatial and geographic data.
> **Note**: GIS can also be an acronym for Geographic Information Science, which is the study of the study of geographic systems.

**Geographic data** can answer the questions "where" and "what". To make this a little bit more concrete, let's use this sign in Anatone, WA, USA as an example.

<img src ="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Anatone_WA.jpg/640px-Anatone_WA.jpg" width=400>

<small><center><i>Image Credit: <a href="https://commons.wikimedia.org/wiki/File:Anatone_WA.jpg"> Dsdugan at English Wikipedia </a></i></small></center>


Dsdugan at English Wikipedia

Here, our answer to the question to "where" is Anatone, WA. The "what" question is answered by all the details on the sign, for example we know that the number of dogs in Anatone is 22. These types of details are also called *attributes*.

Another component of geographic data is *metadata*. This component includes things such as when the data was taken, by whom, how, the quality, as wel as other information about the geographic data itself. 

**Geospatial Data** is a location that is given by a set of coordinates. For example, the location for Anatone could be specified with a specific latitude and longitude ($46.135570$, $-117.132659$). 

<img src = 'assets/images/Anatone Google.png' width=500>

## 1.2 Coordinate Reference Systems

A **Coordinate Reference System** or **CRS** is a system for associating specific numerical coordinates with a position on earth. So depending on the CRS that is used the numbers for the latitude and longitude could differ.

<img src ="https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Latitude_and_Longitude_of_the_Earth.svg/1304px-Latitude_and_Longitude_of_the_Earth.svg.png" width=500>

<small><center><i>Image Credit: Wikimedia Commons</i></small></center>


There are many CRSs because our understanding and ability to measure the surface of the earth has evolved over time. We can think of these different reasonings as an orange peel or a lamp.

Think if we take a regular orange as our earth:

<img src="https://www.esri.com/arcgis-blog/wp-content/uploads/2020/03/BlogOrange.jpg" width=300>

<small><center><i>Image Credit: <a href="https://nation.maps.arcgis.com/home/item.html?id=c4d4448b28a54df09b43642719373dc3">ESRI project package by j_nelson</a></i></small></center>


And the first assumption we make is that it is spherical: 

<img src="https://www.esri.com/arcgis-blog/wp-content/uploads/2020/03/OrangePeelProGlobe.jpg" width=300>

<small><center><i>Image Credit: <a href="https://nation.maps.arcgis.com/home/item.html?id=c4d4448b28a54df09b43642719373dc3">ESRI project package by j_nelson</a></i></small></center>


Assuming that it's spherical will introduce some distortion, as well as how I choose to draw all of my continents on it. Plus when I decide to peel it, depending on how I do that, It'll look like different maps on a flat surface:

<img src="https://www.esri.com/arcgis-blog/wp-content/uploads/2020/03/OrangePeelProGoode.jpg" width=300>

<img src="https://www.esri.com/arcgis-blog/wp-content/uploads/2020/03/OrangePeelProFuller.jpg" width=300>


<small><center><i>Image Credit: <a href="https://nation.maps.arcgis.com/home/item.html?id=c4d4448b28a54df09b43642719373dc3">ESRI project package by j_nelson</a></i></small></center>


Another way to think about this is by thinking about our planet earth as a lamp in a dark room.

<img src ="https://lifestyle.brando.com/prod_img/EEHOMD005500_1_640.jpg" width=400>

<small><center><i>Image Credit: <a href="https://lifestyle.brando.com/led-world-earth-globe-lamp_p18265c1764d132.html"> Brando </a></i></small></center>



Depending on factors such as how we tilt the lamp and if our walls our flat the image that we project onto the wall will be different.

*In short, since our earth isn't flat, our earth is distorted to make it feasible to show it on a flat surface*.


There are two types of coordinate reference systems.
- *Geographic CRS*
- *Projected CRS*

*Geographic CRS* are great for storing data and has units of degrees and are widely used. WGS84 is the most commonly used CRS and is basd on satellites and used by cellphones and GPS. It has the best overall fir for most places on earth. Another common one is NAD83 which is based on both satellite and survey data. It's a great fit for USA based work and is utilized in a lot of federal data products such as the census data. Both of these CRS have *EPSG codes*, which a 4+ digit number used to reference a CRs. For WGS84 the code is 4326, while for NAD83 its 4269. You'll be using these codes when you're using CRS in Python.

*Projected CRS* are good for mapping and spatial analysis. They transform the geographic coordinates (latitude, longitude) to be 2D (X, Y) with units such as meters. All map projections include some type of distortion, whether that be in area, shape, distance or direction. Depending on the CRS it'll probably be minimizing distortion for one of these characteristics. For example, the Mercator projection places importance on shape and direction, but in turn has distorted area as you move away from the equator.

<img src="https://docs.qgis.org/3.10/en/_images/mercator_projection.png" width=400>

<small><center><i>Image Credit: <a href="https://docs.qgis.org/3.10/en/docs/index.html"> QGIS Documentation </a></i></small></center>



Of course some projections are worse than others. This <u>joke</u> projection has somehow made all continents look like South America! This story of distortion tells us that some projections are better than others.

<img src ="https://imgs.xkcd.com/comics/bad_map_projection_south_america_2x.png" width=400>

<small><center><i>Image Credit: <a href="https://xkcd.com/2256/"> xkcd comics </a></i></small></center>





> **Note**: Here are some videos related to the concept of CRS. 
> - Drawing projections on fruits: [Link](https://www.youtube.com/watch?v=wkK_HsY7S_4&t=399s)
> - West Wing discussion on using specific projections: [Link](https://www.youtube.com/watch?v=vVX-PrBRtTY&t=55s)
> - Vox on why world maps are wrong: [Link](https://www.youtube.com/watch?v=kIID5FDi2JQ)

## 1.3 Types of Spatial Data

As you start to gather geospatial data, you'll encounter two types: **vector** and **raster** data.

**Vector data** can be thought of as that that you can connect the dots with. This type of data includes points, lines, and polygons.

<img src ="assets/images/fig_create4.png" width=600>

As an example, we can look at these different types of vector data by looking at different data in San Francisco.

<img src = 'assets/images/vector_data.png' width=700>

Each of these geometry types can be used for different types of information. Point geometries are great for showing where crimes have occurred historically. Lines can show us the location and length of the freeways in the city. Polygons could help us show information such as population per square mile in different neighborhoods.

Now let's think about what this vector data could look like when you open it up.

<img src ="assets/images/fig_create5.png" width=600>

You might get something like this. Each row represents one geospatial feature. So for our second attribute we have the ID number 2, the plot size 20, vegetation type, and a vegetation class of deciduous. Those additional information like the plot size, are **attributes**. These help describe our features. 

Furthermore, each of these features have an associated geometry or geometry collection. So in our first table our geometry is a point,

One last thing about vector data-- each group of features is called a layer. So you could have all three of these data, and each dataset would be its own layer. 


**Raster data** on the other hand is continous. Each location is represented by a grid cell, which are usually all the same size. There a fixed number of rows and columns, and each cell has a value that represents the attribute of interest. 

<img src = "http://gsp.humboldt.edu/OLM_2017/Lessons/GIS/04%20CreatingSpatialData/Images/rasterdatamodel.png" width=400>

<small><center><i>Image Credit: <a href="https://xkcd.com/2256/"> Humboldt GSP </a></i></small></center>



Raster data should feel familiar to you since images are basically raster data! 

Now that we know we have these two types of datasets, we can talk about when to use each. Vector data are better for when you have discreetly bounded data. This could be for counties, rivers, etc. On the other hand, raster data is better for continuous data (like the image we just looked at), or maybe something like temperature, elevation or rainfall.

Now these two datasets come in different file formats, so you’ll know what it is before you pull it in for whatever GIS software you’re using. Some common ones I use are shapefile and geojsons for vector data, and geotiffs for raster data. 

| Vector    | Raster |
| ----------- | ----------- |
| Shapefile (.shp…)      | GeoTIFF       |
| GeoJSON, JSON   | netCDF        |
| KML   | DEM       |
| GeoPackage   |       |

Although these two types of data look different, and come in different formats, you can still use a combination of raster and vector data to answers questions that you’re probably aiming to answer through your own work.


## 1.4 Other Resources

This is really only a brief introduction to geospatial concepts! If you want to dive a little deeper, here are a couple of resources you can check out:

- [Kaggle Learn: Geospatial Analysis in Python](https://www.kaggle.com/learn/geospatial-analysis), an online interactive tutorial

- [Campbell & Shin, Geographic Information System Basics, v1.0](https://2012books.lardbucket.org/books/geographic-information-system-basics/index.html)

- [ESRI Introduction to Map Design](https://www.esri.com/industries/k-12/education/~/media/Files/Pdfs/industries/k-12/pdfs/intrcart.pdf)

- [AxisMaps Cartography Guide](https://www.axismaps.com/guide/)

- [Gentle Introduction to GIS (QGIS)](https://docs.qgis.org/3.16/en/docs/gentle_gis_introduction/index.html)

---
<div style="display:inline-block;vertical-align:middle;">
<a href="https://dlab.berkeley.edu/" target="_blank"><img src ="assets/images/dlab_logo.png" width="75" align="left">
</a>
</div>

<div style="display:inline-block;vertical-align:middle;">
    <div style="font-size:larger">&nbsp;D-Lab @ University of California - Berkeley</div>
    <div>&nbsp;Team Geo<div>
</div>