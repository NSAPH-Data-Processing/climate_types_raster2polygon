# climate_types_zip_zcta

Code to produce a spatial aggregation from 1km tiff raster to zcta (tiger polygons) of [Koppen-Geiger climate types](https://www.nature.com/articles/sdata2018214).

Spatial aggregation of climate type information from grid (tiff) to zcta polygons (shp). In addition the information is merged with a zip2zcta crosswalk to allow mapping to either postal zipcode of census zcta.

## Run

Clone the repository and create a conda environment.

```bash
git clone <https://github.com/<user>/repo>
cd <repo>

conda env create -f requirements.yml
conda activate <env_name> #environment name as found in requirements.yml
```

It is also possible to use `mamba`.

```bash
mamba env create -f requirements.yml
mamba activate <env_name>
```

### Entrypoints

Add symlinks to input, intermediate and output folders inside the corresponding `/data` subfolders.

For example:

```bash
export HOME_DIR=$(pwd)

cd $HOME_DIR/data/input/ .
ln -s <input_path> . #paths as found in data/input/README.md

cd $HOME_DIR/data/output/
ln -s <output_path> . #paths as found in data/output/README.md
```

The README.md files inside the `/data` subfolders contain path documentation for NSAPH internal purposes.

git clone <https://github.com/<user>/repo>
cd <repo>
conda env create -f requirements.yaml
conda activate sectors_pollution_env

### Pipeline

You can run the pipeline steps manually or run the snakemake pipeline described in the Snakefile.

**run pipeline steps manually**

* step 1: download shapefiles

```bash
python ./src/generate_counts.py --year <year>
```

**run snakemake pipeline**
or run the pipeline:

```bash
snakemake --cores
```
