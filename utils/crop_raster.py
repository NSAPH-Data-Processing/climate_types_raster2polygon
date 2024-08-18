import geopandas as gpd
import rasterio
from rasterio.mask import mask
import os
import argparse

def crop_tif(input_shapefile, input_raster, output_tif):
    shapefile = gpd.read_file(input_shapefile)

    with rasterio.open(input_raster) as src:
        # Crop the raster with the shapefile
        out_image, out_transform =mask(src, shapefile.geometry, crop=True)

        # Update the metadata with the new dimensions, transform, and CRS
        out_meta = src.meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform
        })

        # Write the cropped raster to a new file
        with rasterio.open(output_tif, "w", **out_meta) as dest:
            dest.write(out_image)

        print(f"Raster cropped to {input_shapefile} and saved as {output_tif}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crop raster to bounding box and mask values outside shapefiles")
    parser.add_argument("--input_shapefile", 
                        default="data/example/MEX_ADM2/MEX_ADM2.shp",
                        help="Input .shp file")
    parser.add_argument("--input_raster",
                        default="data/input/climate_types/Beck_KG_V1_present_0p0083.tif",
                        help="Raster file to crop")
    parser.add_argument("--output_tif", 
                        default="data/example/climate_types_MEX_ADM2.tif",
                        help="Output .tif file")
    args = parser.parse_args()

    crop_tif(args.input_dir, args.input_raster, args.output_dir)
