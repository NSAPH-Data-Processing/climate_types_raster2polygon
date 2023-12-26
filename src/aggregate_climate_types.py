import json
import logging
import os
import hydra
import numpy as np
import rasterio
import rasterstats
import pandas as pd
import geopandas as gpd

@hydra.main(config_path="../conf", config_name="config", version_base=None)
def main(cfg):
    # log statistics (transform, crs, nodata)
    raster_path = f"data/input/climate_types/{cfg.climate_types_file}"
    logging.info(f"Reading raster {raster_path}")
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


    logging.info(
        "Read file with characteristics:\n"
        f"Transform:\n{transform}\n"
        f"CRS: {crs}\n"
        f"NoData: {nodata}\n"
        f"Shape: {layer.shape}\n"
        f"Number of layers: {num_layers}"
    )

    # read shapefile
    idvar = cfg.shapefiles[cfg.shapefile_polygon_name][cfg.shapefile_year].idvar
    shp_path = f"data/input/shapefiles/shapefile_{cfg.shapefile_polygon_name}_{cfg.shapefile_year}/shapefile.shp"
    logging.info(f"Reading shapefile {shp_path}")
    shp = gpd.read_file(shp_path)
    logging.info(f"Read shapefile with head\n: {shp.drop(columns='geometry').head()}")
    ids = shp[idvar]

    # compute zonal stats
    logging.info(f"Computing zonal stats")
    stats = rasterstats.zonal_stats(
        shp_path,
        raster_path,
        stats="count",
        all_touched=True,
        geojson_out=False,
        categorical=True,
        nodata=nodata,
    )
    logging.info(f"Done.")

    # for each entry in stats count the unique values
    avs = {}
    for i, s in enumerate(stats):
        n = s["count"] - s.get(0, 0)
        avs[ids[i]] = {k: v / n for k, v in s.items() if k != "count"}

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

    logging.info(f"Fraction of locations with only one climate: {100 * m0:.2f}%")
    logging.info(f"Fraction of locations more than one climate: {100 * m1:.2f}%")
    logging.info(f"Fraction of locations more than two climates: {100 * m2:.2f}%")
    logging.info(f"Fraction of locations with ties: {100 * frac_ties:.2f}%")

    # save files
    intermediate_dir = f"data/intermediate/climate_pcts/climate_pcts_{cfg.shapefile_polygon_name}_{cfg.shapefile_year}"
    os.makedirs(intermediate_dir, exist_ok=True)
    pcts_file = f"{intermediate_dir}/pcts_file.json"
    class_file = f"{intermediate_dir}/class_file.csv"
    output_file = f"data/output/climate_types_raster2polygon/climate_types_{cfg.shapefile_polygon_name}_{cfg.shapefile_year}.csv"

    logging.info(f"Saving pcts to {pcts_file}")
    with open(pcts_file, "w") as f:
        json.dump(avs, f)

    # pick the climate with the highest percentage
    clkey = cfg.climate_keys

    modes = [max(m.keys(), key=m.get) for m in avs.values()]
    class_df = pd.DataFrame({"climate_type_num": modes, "id": ids})
    codedict_short = {k: v[0] for k, v in clkey.items()}
    codedict_long = {k: v[1] for k, v in clkey.items()}
    class_df["climate_type_short"] = class_df["climate_type_num"].map(codedict_short)
    class_df["climate_type_long"] = class_df["climate_type_num"].map(codedict_long)
    class_df = class_df.drop(columns="climate_type_num")
    logging.info(f"Saving classification to {class_file}")
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

    logging.info(f"Saving output into data/output/climate_types_zip_zcta \n {output_df.head()}")
    output_df.to_csv(output_file , index=False)

if __name__ == "__main__":
    main()
