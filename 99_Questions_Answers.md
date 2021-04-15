# Common questions and answers

This document lists comment questions and their respective answers pointing to specific parts of the workshop files. 

I’m having trouble installing `GeoPandas` on a Windows computer.
- I’m having trouble installing `GeoPandas` on a Mac and I usually use pip install.
- When using pip to install GeoPandas, you need to make sure that all dependencies are installed correctly. Fiona provides binary wheels with the dependencies included for Mac and Linux. The easiest way to attempt to fix this, first order, is to uninstall geopandas and it’s dependencies and reinstall. 
I’m having trouble with packages versions not working with each other.
- You can try creating a virtual environment, see the bottom of the [README](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/README.md)
What’s the difference between `GeoPandas` and `Pandas`?
- [Lesson 2.1](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/02_Introduction_to_GeoPandas.ipynb)
How do I read in geospatial data vector file formats?
- `gpd.read_file` is a great function that reads in multiple vector data file formats.
- [Lesson 2.2 and 2.6](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/02_Introduction_to_GeoPandas.ipynb)
How do I save geospatial data file formats?
- [Lesson 2.6](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/02_Introduction_to_GeoPandas.ipynb)
What are Coordinate Reference Systems
- [Lesson 1](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/01.Overview_Geospatial_Data.pdf)
- [Lesson 3.4](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/03_CRS_Map_Projections.ipynb)
I’m trying to plot two shapefile together but they’re not showing up
- This is the #1 folks run into! It’s most likely that the CRS for your two datasets are different.
- [Lesson 3.1-3.3](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/03_CRS_Map_Projections.ipynb)
How do I get the CRS of my data and transform it?
- [Lesson 3.5, 3.7](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/03_CRS_Map_Projections.ipynb)
How do I set the CRS of my data if it’s missing?
- [Lesson 3.6](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/03_CRS_Map_Projections.ipynb)
I have a CSV that has latitude and longitude values, how do I coerce it to be a GeoDataFrame?
- [Lesson 4.2](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/04_More_Data_More_Maps.ipynb)
How do I find the geospatial extent of my data?
- Use `total_bounds`
- [Lesson 4.3](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/04_More_Data_More_Maps.ipynb)
How do I create a choropleth map?
- [Lesson 5.1](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/05_Data-Driven_Mapping.ipynb)
What kinds of color maps are there?
- [Lesson 5.1](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/05_Data-Driven_Mapping.ipynb)
What types of data is best for choropleth mapping?
- [Lesson 5.2](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/05_Data-Driven_Mapping.ipynb)
What is a classification scheme and how do I use different ones in Python?
- [Lesson 5.3](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/05_Data-Driven_Mapping.ipynb)
Can I define my own classification scheme?
- Yes! 
- [Lesson 5.3](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/05_Data-Driven_Mapping.ipynb)
How do I create a point map?
- [Lesson 5.4](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/05_Data-Driven_Mapping.ipynb)
How does mapping categorical data different from mapping quantitative data?
- It’s basically the same except you’ll have to specify that it’s categorical.
- [Lesson 5.5](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/05_Data-Driven_Mapping.ipynb)
How do I calculate the area or length of my GeoDataFrame?
- [Lesson 6.1](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/06_Spatial_Queries.ipynb)
What is a relationship query?
- [Lesson 6.2](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/06_Spatial_Queries.ipynb)
How do I do a proximity analysis?
- [Lesson 6.3](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/06_Spatial_Queries.ipynb)
How do I know what units my buffer size is in?
- The units are what your CRS says they are.
- [Lesson 6.3](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/06_Spatial_Queries.ipynb)
Can I do a merge like I do in Pandas for GeoDataFrames?
- Yes!
- [Lesson 7.1](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/07_Joins_and_Aggregation.ipynb)
What is a spatial join and how do I do it?
- [Lesson 7.2](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/07_Joins_and_Aggregation.ipynb)
What’s the best way to aggregate my geospatial data (for example, after doing a join)?
- Using `.dissolve` is better than a `groupby` since it’ll preserve your geometries.
- [Lesson 7.3](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/07_Joins_and_Aggregation.ipynb)
Do you have any full workflows we can work through and ask questions about?
- Yes, we have two!
- [Lesson 8](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/08_Pulling_It_All_Together.ipynb)
- [Lesson 9](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/09_ON_YOUR_OWN_A_Full_Workflow.ipynb)
How do I fetch and use geospatial data without downloading it as a file?
- [Lesson 10](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/10_OPTIONAL_Fetching_Data.ipynb)
How do I create maps with basemaps?
- [Lesson 11](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/11_OPTIONAL_Basemap_with_Contextily.ipynb) 
How do I create interactive maps?
- [Lesson 12](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/12_OPTIONAL_Interactive_Mapping_with_Folium.ipynb)
How do I geocode address in Python?
- [Lesson 13](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/13_OPTIONAL_geocoding.ipynb) 
Is there a package to do both panda and geopandas plots with some interactive functionality?
- Try `Altair`!
- [Lesson 14](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/14_OPTIONAL_Plotting_and_Mapping_with_Altair.ipynb)
How do I do a Voronoi Tessellation?
- [Lesson 15](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/14_OPTIONAL_Plotting_and_Mapping_with_Altair.ipynb)
I want to start using raster data. Where’s a good place ot start?
- [Lesson 16](https://github.com/dlab-berkeley/Geospatial-Fundamentals-in-Python/blob/master/16_OPTIONAL_Introduction_to_Raster_Data.ipynb) 

---
<div style="display:inline-block;vertical-align:middle;">
<a href="https://dlab.berkeley.edu/" target="_blank"><img src ="assets/images/dlab_logo.png" width="75" align="left">
</a>
</div>

<div style="display:inline-block;vertical-align:middle;">
    <div style="font-size:larger">&nbsp;D-Lab @ University of California - Berkeley</div>
    <div>&nbsp;Team Geo<div>
</div>

