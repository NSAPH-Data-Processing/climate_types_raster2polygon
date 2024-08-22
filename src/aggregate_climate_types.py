import json
import logging
import hydra
import numpy as np
import rasterio
import rasterstats
import pandas as pd
import geopandas as gpd

# configure logger to print at info level
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

@hydra.main(config_path="../conf", config_name="config", version_base=None)
def main(cfg):
    LOGGER.info("""
        # Extract transform, crs, nodata from raster
    """)
    raster_path = f"data/input/climate_types/{cfg.climate_types_file}"
    LOGGER.info(f"Reading raster {raster_path}")
    with rasterio.open(raster_path) as src:
        transform = src.transform
        crs = src.crs
        layer = src.read(1)
        nodata = src.nodata
        num_layers = src.count

    # # debugger notes: show the raster
    # import matplotlib.pyplot as plt
    # plt.imshow(layer == 0) #modify layer value to see different climate types
    # plt.show()

    LOGGER.info("Read file with characteristics:\n"
        f"Transform:\n{transform}\n"
        f"CRS: {crs}\n"
        f"NoData: {nodata}\n"
        f"Shape: {layer.shape}\n"
        f"Number of layers: {num_layers}"
    )

    # read shapefile
    for shapefile_name in cfg.shapefiles:
        LOGGER.info(f"Shapefile: {shapefile_name}")
        idvar = cfg.shapefiles[shapefile_name].idvar
        shp_path = f"data/input/shapefiles/{shapefile_name}/{shapefile_name}.shp"
        LOGGER.info(f"Reading shapefile {shp_path}")
        shp = gpd.read_file(shp_path)
        LOGGER.info(f"Read shapefile with head\n: {shp.drop(columns='geometry').head()}")
        ids = shp[idvar]

        # compute zonal stats
        LOGGER.info(f"Computing zonal stats")
        stats = rasterstats.zonal_stats(
            shp_path,
            raster_path,
            stats="count",
            all_touched=True,
            geojson_out=False,
            categorical=True,
            nodata=nodata,
        )
        LOGGER.info(f"Done.")

        # for each entry in stats count the unique values
        avs = {}
        for i, s in enumerate(stats):
            n0 = s.get(0, 0)
            if n0 == s["count"]:
                # Print the polygon id if it has no climate intersection, that is
                # if the number of pixels with climate type 0 is equal to the total number of pixels.
                # This is the case for some polygons with area intersecting raster grids classified as 0 only
                # climate class 0 is body of water
                LOGGER.info(f"Polygon {ids[i]} has {n0} pixels with climate type 0")
                avs[ids[i]] = {0: 1.0}
            else:
                n = s["count"] - n0
                avs[ids[i]] = {k: v / n for k, v in s.items() if (k != "count" and k != 0)} # do not include the counts that correspond to intersections with a body of water

        # log some statistics of what ran
        m0 = np.mean([len(m) == 1 for m in avs.values()])
        m1 = np.mean([len(m) > 1 for m in avs.values()])
        m2 = np.mean([len(m) > 2 for m in avs.values()])
        frac_ties = 0
        for m in avs.values():
            if len(m) > 1:
                x = np.array(sorted(m.values(), reverse=True))
                if x[0] == x[1]:
                    frac_ties += 1 / len(avs)

        LOGGER.info(f"Fraction of locations with only one climate: {100 * m0:.2f}%")
        LOGGER.info(f"Fraction of locations more than one climate: {100 * m1:.2f}%")
        LOGGER.info(f"Fraction of locations more than two climates: {100 * m2:.2f}%")
        LOGGER.info(f"Fraction of locations with ties: {100 * frac_ties:.2f}%")

        intermediate_dir = f"data/intermediate/climate_pcts"
        pcts_file = f"{intermediate_dir}/climate_pcts_{shapefile_name}.json"
        LOGGER.info(f"Saving pcts to {pcts_file}")
        with open(pcts_file, "w") as f:
            json.dump(avs, f)

        # pick the climate with the highest percentage
        clkey = cfg.climate_keys

        modes = [max(m.keys(), key=m.get) for m in avs.values()]
        class_df = pd.DataFrame({"climate_type_num": modes, "id": ids}) 
        codedict_short = {k: v[0] for k, v in clkey.items()}
        codedict_long = {k: v[1] for k, v in clkey.items()}
        class_df["climate_type_short"] = class_df["climate_type_num"].map(codedict_short) # if a polygon intersects only with water then there is no assignment
        class_df["climate_type_long"] = class_df["climate_type_num"].map(codedict_long) # if a polygon intersects only with water then there is no assignment
        class_df = class_df.drop(columns="climate_type_num")

        class_file = f"{intermediate_dir}/climate_types_{shapefile_name}.csv"
        LOGGER.info(f"Saving classification to {class_file}")
        class_df.to_csv(class_file, index=False)

        # transform the percentages into a sparse dataframe
        output_df = []
        for k, v in avs.items():
            row = {"id": k}
            for c in clkey.keys():
                short_name = clkey[c][0]
                row[short_name] = v.get(c, 0.0)
            output_df.append(row)
        output_df = pd.DataFrame(output_df)

        output_df = pd.merge(class_df, output_df, on="id")

        output_file = f"data/output/climate_types_raster2polygon/climate_types_{shapefile_name}.parquet"
        LOGGER.info(f"Saving output to {output_file}")
        output_df.rename(columns={"id": cfg.shapefiles[shapefile_name].output_idvar}, inplace=True)
        output_df.to_parquet(output_file)

if __name__ == "__main__":
    main()
