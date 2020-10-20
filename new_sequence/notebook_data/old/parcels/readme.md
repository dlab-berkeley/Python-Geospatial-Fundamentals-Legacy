# Parcels Data

The Parcels data provides information regarding the location of a particular parcel that can be mapped out geospatially. It's APN identifier may correspond to the Permit dataset, which can then be used to show the distribution of affordable housing.

## Variable Information:

If you have worked with housing datasets before many of these values may look familiar. If not, please ask for clarification if the descriptions below do not answer all of your questions.

* `APN` and `APN2` are different forms of the assessor's parcel number (APN). It is a number assigned to parcels of  property by the jurisdiction's tax assessor.


* `STATE` and `COUNTY` are pretty straight forward descriptions, as these columns contain strings with the state (2 letter abbreviation) and county that the parcel is in.


* `FIPS` stands for Federal Information Processing Standards and should be familiar because we have been using them to identify records in the ACS dataset. The FIPS code in this dataframe only contains the 5 number code for the state and county.
    * e.g. `06001` stands for `06`=California and `001`=Alameda County


* All of the fields that begin with `SIT_` describe the specific address for the parcel. `SIT_FULL_S`, `SIT_CITY`, `SIT_STATE`, and `SIT_ZIP` together represent the full address for the parcel. The other fields are either subsets of that address (`SIT_HSE_NU`, `SIT_DIR`, `SIT_STR_NA`, `SIT_STR_SF`) or contain additional location descriptions (`SIT_ZIP4`, `SIT_POST`).


* `LAND_VALUE` is the value of the parcel in 2016 USD
* `IMPR_VALUE` is the value of the market improvement value on the parcel in 2016 USD
* `TOT_VALUE` is the sum of `LAND_VALUE` and `IMPR_VALUE`


* `OWNER` is the name of the owner of the parcel. `OWNADDRESS` and `OWNCTYSTZP` together represent the full address for the listed owner of the parcel.


* `geometry` is a column associated with geospatial data. Do not delete this column. We will discuss details on this column in more detail in subsequent notebooks.


Original Locations: I'm actually not sure where these files originated from.
