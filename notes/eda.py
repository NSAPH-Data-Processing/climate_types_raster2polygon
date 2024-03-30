# %%
import matplotlib.pyplot as plt
import rasterio
import geopandas as gpd
import pandas as pd

# %%
# Open the raster file
file_path = 'data/input/climate_types/Beck_KG_V1_present_0p083.tif'
raster = rasterio.open(file_path)

# Read the raster data
data = raster.read(1)

# Plot the map
plt.imshow(data, cmap='viridis')
plt.title('Climate Types')
plt.show()


# %%
! conda list

# %%
# Read the shapefile
shapefile_path = 'data/input/shapefiles/shapefile_cb_zcta_2015/shapefile.shp'
shapefile = gpd.read_file(shapefile_path)
shapefile.ZCTA5CE10 = shapefile.ZCTA5CE10.astype(int)
shapefile.rename(columns={'ZCTA5CE10': 'ZCTA5'}, inplace=True)

# Read the aggregated climate types file
climate_types_path = 'data/output/climate_types_raster2polygon/climate_types_cb_zcta_2015.csv'
climate_types_df = pd.read_csv(climate_types_path)
climate_types_df.rename(columns={'id': 'ZCTA5'}, inplace=True)

# Merge the shapefile and CSV based on a common column
merged_data = shapefile.merge(climate_types_df, on='ZCTA5')

# %%
# Plot the merged data
merged_data.plot(column='climate_type_short', cmap='viridis', legend=True)


