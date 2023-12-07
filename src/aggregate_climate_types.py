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
    raster_path = f"data/input/climate_types/{cfg.raster}.tif"
    logging.info(f"Reading raster {raster_path}")
    with rasterio.open(raster_path) as src:
        transform = src.transform
        crs = src.crs
        layer = src.read(1)
        nodata = src.nodata
        num_layers = src.count

    logging.info(
        "Read file with characteristics:\n"
        f"Transform:\n{transform}\n"
        f"CRS: {crs}\n"
        f"NoData: {nodata}\n"
        f"Shape: {layer.shape}\n"
        f"Number of layers: {num_layers}"
    )

    # read shapefile
    idvar = cfg.shapefiles.idvar[cfg.year]
    shp_path = f"data/input/shapefiles/shapefile_{cfg.year}/shapefile.shp"
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
        all_touched=cfg.all_touched,
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
    tgtdir = f"data/intermediate/climate_pcts/climate_pcts_{cfg.year}"
    os.makedirs(tgtdir, exist_ok=True)
    pcts_file = f"{tgtdir}/pcts_file.json"
    class_file = f"{tgtdir}/class_file.csv"
    class_file_dense = f"{tgtdir}/class_file_dense.csv"

    logging.info(f"Saving pcts to {pcts_file} and classification to {class_file}")
    with open(pcts_file, "w") as f:
        json.dump(avs, f)

    # make the above sparse file into a dense file
    clkey = cfg.climate_keys
    sparse = []
    for k, v in avs.items():
        row = {"id": k}
        for c in clkey.keys():
            short_name = clkey[c][0]
            row[short_name] = v.get(c, 0.0)
        sparse.append(row)
    sparse = pd.DataFrame(sparse)
    logging.info(f"Saving full pcts df to data/output/climate_types_zip_zcta\n{sparse.head()}")
    sparse.to_csv("data/output/climate_types_zip_zcta/climate_types_zip_zcta.csv", index=False)

    # pick the climate with the highest percentage
    modes = [max(m.keys(), key=m.get) for m in avs.values()]
    df = pd.DataFrame({"climate_type_num": modes, "zcta": ids})
    codedict_short = {k: v[0] for k, v in clkey.items()}
    codedict_long = {k: v[1] for k, v in clkey.items()}
    df["climate_type_short"] = df["climate_type_num"].map(codedict_short)
    df["climate_type_long"] = df["climate_type_num"].map(codedict_long)
    df = df.drop(columns="climate_type_num")
    df.to_csv(class_file, index=False)

if __name__ == "__main__":
    main()
