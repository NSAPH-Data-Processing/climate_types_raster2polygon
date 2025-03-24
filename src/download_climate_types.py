import logging
import os
import zipfile
import hydra
import wget


@hydra.main(config_path="../conf", config_name="config", version_base=None)
def main(cfg):
    url = cfg.climate_types_url

    tgt = "{cfg.datapaths.base_path}/input/climate_types"

    logging.info(f"Downloading {url}")
    wget.download(url, f"{tgt}.zip")
    logging.info(f"Done.")

    # unzip with unzip library
    with zipfile.ZipFile(f"{tgt}.zip", "r") as zip_ref:
        zip_ref.extractall(tgt)
    logging.info(f"Unzipped {tgt} with files:\n {os.listdir(tgt)}")

    # remove dirty zip file
    os.remove(f"{tgt}.zip")
    logging.info(f"Removed {tgt}.zip")


if __name__ == "__main__":
    main()
