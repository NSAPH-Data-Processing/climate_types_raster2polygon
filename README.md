# raster2zcta_climate_types
raster2zcta for climate types

## Motivation

**zcta** 

* In theory, zctas change every 10 years and there are currently three editions: zcta500, zcta510 and zcta520
* In practice, there are yearly zcta shp file realeases. For the same editions there might be small differences between the releases.

**zipcode**

* In theory, zipcodes change yearly. There are several providers of shapefiles for zipcodes, there is not an official USPS realease.
* ESRI provides yearly releases of zipcode shapefiles which exclude poboxes.

**xwalks**

* Zipcodes are "smaller" than zctas. Zipcode to zcta crosswalks have a single entry per zipcode. There might be zctas that point to multiple zipcodes. 
* There is no official zip2zcta xwalk.
* USD provides xwalks 2009 onwards. The yearly releases are not harmonized: there are changes in column names and other file format changes.
* Within a single zcta edition, there are small differences in the xwalks across years.

**Questions**

* Is it worth using yearwise crosswalks?

For the most part, the crosswalk entries will have the same mapping every year. Also, when merging by year-zip to year-zcta, a different logic would have to be applied for years prior to 2009. 

**Conclusion**
It make sense to have a single master zip2zcta crosswalk and shapefile that applies to all zcta editions that incorporate all retired zipcodes and retired zctas.

