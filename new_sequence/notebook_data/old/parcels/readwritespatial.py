# ==========================================================================
# Read, write spatial
# ==========================================================================

import geopandas as gpd

#
# Read, filter, and write shapefile to geojson
# --------------------------------------------------------------------------

alameda = gpd.read_file("/Volumes/GoogleDrive/My Drive/Data for Housing/data/raw/CA_ParcelData_2016/06001/Parcels.shp")   

### Filter out Oakland 

oakland = alameda[alameda['SIT_CITY']=='Oakland'] 

### Write to geojson
oakland.to_file('/Users/timothythomas/git/curriculum_dev/notebook_data/parcels/Oakland_parcels_2016_raw2.geojson', driver = 'GeoJSON')