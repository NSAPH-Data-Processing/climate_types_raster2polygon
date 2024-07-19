import geopandas as gpd
import os
import argparse
import fiona

def convert_gpkg_to_shp(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".gpkg"):
            gpkg_path = os.path.join(input_dir, filename)
            layers = fiona.listlayers(gpkg_path)
            
            for layer_name in layers:
                layer_gdf = gpd.read_file(gpkg_path, layer=layer_name)
                layer_output_dir = os.path.join(output_dir, os.path.splitext(filename)[0])
                if not os.path.exists(layer_output_dir):
                    os.makedirs(layer_output_dir)
                layer_output_path = os.path.join(layer_output_dir, f"{layer_name}.shp")
                layer_gdf.to_file(layer_output_path, driver='ESRI Shapefile')
                print(f"Saved {layer_name} to {layer_output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert GeoPackage files to Shapefiles")
    parser.add_argument("--input_dir", help="Directory containing .gpkg files")
    parser.add_argument("--output_dir", help="Directory to save the converted .shp files")
    args = parser.parse_args()

    convert_gpkg_to_shp(args.input_dir, args.output_dir)
