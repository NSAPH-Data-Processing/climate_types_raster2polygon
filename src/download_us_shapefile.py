import logging
import os
import zipfile
import hydra
import wget

@hydra.main(config_path="../conf", config_name="config", version_base=None)
def main(cfg):
    url = cfg.shapefiles[cfg.shapefile_name].url

    tgt = f"data/input/shapefiles/{cfg.shapefile_name}"

    tgtdir = os.path.dirname(tgt)
    tgtfile = os.path.basename(tgt)

    tgt = f"{tgtdir}/{tgtfile}"
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

    logging.info(f"Rename files within zip folder ")
    files = os.listdir(tgt)
    for f in files:
        _, ext = os.path.splitext(f)
        os.rename(f"{tgt}/{f}", f"{tgt}/{cfg.shapefile_name}{ext}")


if __name__ == "__main__":
    main()
