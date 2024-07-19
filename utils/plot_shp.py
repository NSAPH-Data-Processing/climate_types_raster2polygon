import geopandas as gpd
import matplotlib.pyplot as plt
import os
import argparse

def plot_shapefiles(input_dir):
    fig, ax = plt.subplots(figsize=(10, 10))

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".shp"):
                shapefile_path = os.path.join(root, file)
                gdf = gpd.read_file(shapefile_path)
                gdf.plot(ax=ax, label=file)
    
    plt.legend()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot multiple shapefiles")
    parser.add_argument("input_dir", help="Directory containing .shp files")
    args = parser.parse_args()

    plot_shapefiles(args.input_dir)