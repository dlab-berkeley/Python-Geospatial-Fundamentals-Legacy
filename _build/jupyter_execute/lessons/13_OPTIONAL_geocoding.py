# Geocoding Addresses in Python

This notebook demonstrates how to geocode a dataframe of addresses

# import our packages
import numpy as np
import pandas as pd
import geopandas as gpd
import contextily as cx
import matplotlib.pyplot as plt
import folium

# FOR geocoding
import geopy


## Sample Data
Let's use as our sample data a CSV file of Alameda County Schools.

df0 = pd.read_csv("./notebook_data/alco_schools.csv")
df0.head()

We can see that this datafile already has coordinates, but we will ignore those columns and subset it to Berkeley schools only for our geocoding example. We will also only keep public schools to limit the number of addresses to be geocoded.

df = df0[(df0['City']=='Berkeley' )& (df0['Org']== 'Public')][['Site','Address','City','State']].reset_index(drop=True)
df.head()

df.shape  # SEE HOW MANY SCHOOLS WILL BE GEOCODED

Next we create a column that has all address components as this format is favored by many geocoders.

df['full_address'] =  df['Address'] +' '+ df['City']+ ' '+ df['State']
df.head()

## Create a GeoDataFrame
We will create a Geopandas Geodataframe that has no geometry so that we can use GeoPandas functionality for geocoding.

gdf =  gpd.GeoDataFrame(data=df, 
                        geometry=None)

gdf.head()

gdf.info()

## Define Geocoders and associated parameters


##################################################################
## Geocoder to use 
## see https://geopy.readthedocs.io/en/latest/
## and https://geopandas.org/geocoding.html
##################################################################

# By default, the geocode function uses the GeoCode.Farm geocoding API with a rate limitation applied. 
# But a different geocoding service can be specified (we really like the google geocoder!)
# Set your Google geocoding API Key if you want to geocode using that API
geocoder_name =  'Nominatim'   # or "GoogleV3" or None to skip geocoding step
geocoder_apikey = None           # None if not required or google api key, or other api key
geopy.geocoders.options.default_user_agent = 'D-Lab GeoFUN Workshop at UC Berkeley'

## Test the geocoder

# test the geocoder
if geocoder_name is not None: 
    print("Geocoding is enabled with this geocoder:", geocoder_name)
    
    if geocoder_apikey is None:      
        x= gpd.tools.geocode('1600 pennsylvania ave. washington, dc', provider=geocoder_name)['geometry'].squeeze()
    
    else:
        x=gpd.tools.geocode('1600 pennsylvania ave. washington, dc', provider=geocoder_name, api_key=geocoder_apikey)['geometry'].squeeze()
else:
    print("Geocoding is NOT enabled.")
    
print(x)

## Make a Geocoding Function

We can apply a geocoding function to a pandas dataframe to geocode all rows

def geocode_one_address(addr, geocoder_name=geocoder_name, geocoder_apikey=geocoder_apikey):
    '''
    Function to geocode an input address IFF geom is None
    Use geopy with google geocoder to geocode addresses.
    Requires the api_key value to be set prior to running this function
    
    Parameters:
        addr (str): address to geocode, eg "1 Main St, Oakland, CA"
        geocoder_name (str): name of geocoder ("nominatim" or "GoogleV3")
        geocoder_apikey (str): api_key if needed by geocoder
    Returns: 
        geom (POINT): a point geometry or None if unsuccessful
        
    '''   
    
    if addr != None:
        tempaddr = addr
    
        print("...geocoding this address: [%s]" % tempaddr)
        
        try:
            if geocoder_apikey == None:
                return gpd.tools.geocode(tempaddr, provider=geocoder_name)['geometry'].squeeze()
            else:
                return gpd.tools.geocode(tempaddr, provider=geocoder_name, api_key=geocoder_apikey)['geometry'].squeeze()
        except:
            print("...Problem with address: ", tempaddr)
            return None

    else: 
        print("No address to geocode")
        return None

# test geocoding function on one address
x = geocode_one_address('1600 pennsylvania ave. washington, dc')
print(x)

#batch geocode addresses in a data frame
if geocoder_name is None:
    print("Geocoding is NOT enabled.")
    print("Will NOT geocode addresses")
else:
    print("Geocoding is enabled with this geocoder:", geocoder_name)
    print("Ready to Geocode addresses")
        
    if geocoder_apikey is None:  
        gdf['geometry'] = gdf.apply(lambda x: geocode_one_address(x['full_address']), axis=1)
    else:
        gdf['geometry'] = gdf.apply(lambda x: geocode_one_address(x['full_address']), axis=1)


gdf.head()

## Set the CRS
Since we now have geographic coordinates we need to set the Coordinate Reference System of the data (WGS84)

gdf = gdf.set_crs(epsg=4326)

## Map the geocoded Addresses

gdf.plot();

## Add basemap with Contextily
We can map the schools that were successfully geocoded, i.e. where the geometry is not equal to None.

ax = gdf[gdf.geometry!=None].to_crs('EPSG:3857').plot(figsize=(9, 9), color="red")
cx.add_basemap(ax)

## Interactive Map with Folium

We can create an interactive map of the schools that were successfully geocoded.


map1 = folium.Map(location=[gdf.geometry.y.mean(), gdf.geometry.x.mean()], 
                  tiles='CartoDB Positron',
                  zoom_start=12)

folium.GeoJson(gdf[gdf.geometry!=None],
               tooltip=folium.GeoJsonTooltip(
                   fields=['Site'], 
                   aliases=[""],
                   #labels=True,
                   localize=True)
              ).add_to(map1)

map1  # show map

## Save output to GeoJson File

# Save Geodataframe to file
#gdf.to_file("my_geocoded_schools.geojson", driver='GeoJSON')

