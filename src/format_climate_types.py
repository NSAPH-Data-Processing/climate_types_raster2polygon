import json
import logging
import hydra
import pandas as pd

# configure logger to print at info level
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

@hydra.main(config_path="../conf", config_name="config", version_base=None)
def main(cfg):
    intermediate_dir = f"{cfg.datapaths.base_path}/intermediate/climate_pcts"
    
    # read shapefile
    for shapefile in cfg.shapefiles: #loops through all shapefiles in the config
        pcts_file = f"{intermediate_dir}/climate_pcts_{shapefile.name}.json"
        LOGGER.info(f"Reading {pcts_file}")
        with open(pcts_file, "r") as f:
            avs = json.load(f)
            
        class_file = f"{intermediate_dir}/climate_types_{shapefile.name}.csv"
        LOGGER.info(f"Reading {class_file}")
        class_df = pd.read_csv(class_file, index=False)

        clkey = cfg.climate_keys

        # transform the percentages into a sparse dataframe
        output_df = []
        for k, v in avs.items():
            row = {shapefile.output_idvar: k}
            for c in clkey.keys():
                short_name = clkey[c][0]
                #convert to smallcap
                short_name = f"pct_{short_name.lower()}"
                row[short_name] = v.get(c, 0.0)
            output_df.append(row)
        output_df = pd.DataFrame(output_df)

        output_df = pd.merge(class_df, output_df, on=shapefile.output_idvar)

        output_file = f"{cfg.datapaths.base_path}/output/present/climate_types__koppen_geiger__{shapefile.name}.parquet"
        LOGGER.info(f"Saving output to {output_file}")
        output_df.rename(columns={"id": shapefile.output_idvar}, inplace=True)
        output_df.to_parquet(output_file)
        LOGGER.info(f"Done.")

if __name__ == "__main__":
    main()
