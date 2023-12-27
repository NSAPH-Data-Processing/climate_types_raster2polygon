# climate_types_raster2polygon

Code to produce spatial aggregations of [Koppen-Geiger climate types](https://www.nature.com/articles/sdata2018214). The spatial aggregation are performed from climate type information from grid/raster (tiff) to polygons (shp).

---

# Codebook

## Dataset Columns:

1. **id**: Represents the id of a given polygon in a shp file.
2. **climate_type_short**: The abbreviated code for each specific climate type.
3. **climate_type_long**: The detailed description of each specific climate type.
4. **Af - EF**: Each of these columns represents a specific climate type. The values within these columns will represent the percentage area corresponding to each climate type for a specific polygon.

## Climate Types (Keys and Descriptions):

- **Af**: Tropical, rainforest
- **Am**: Tropical, monsoon
- **Aw**: Tropical, savannah
- **BWh**: Arid, desert, hot
- **BWk**: Arid, desert, cold
- **BSh**: Arid, steppe, hot
- **BSk**: Arid, steppe, cold
- **Csa**: Temperate, dry summer, hot summer
- **Csb**: Temperate, dry summer, warm summer
- **Csc**: Temperate, dry summer, cold summer
- **Cwa**: Temperate, dry winter, hot summer
- **Cwb**: Temperate, dry winter, warm summer
- **Cwc**: Temperate, dry winter, cold summer
- **Cfa**: Temperate, no dry season, hot summer
- **Cfb**: Temperate, no dry season, warm summer
- **Cfc**: Temperate, no dry season, cold summer
- **Dsa**: Cold, dry summer, hot summer
- **Dsb**: Cold, dry summer, warm summer
- **Dsc**: Cold, dry summer, cold summer
- **Dsd**: Cold, dry summer, very cold winter
- **Dwa**: Cold, dry winter, hot summer
- **Dwb**: Cold, dry winter, warm summer
- **Dwc**: Cold, dry winter, cold summer
- **Dwd**: Cold, dry winter, very cold winter
- **Dfa**: Cold, no dry season, hot summer
- **Dfb**: Cold, no dry season, warm summer
- **Dfc**: Cold, no dry season, cold summer
- **Dfd**: Cold, no dry season, very cold winter
- **ET**: Polar, tundra
- **EF**: Polar, frost

---

# Run

### Conda environment

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

### Input and output paths

Determine the configuration file to be used in `cfg.datapaths`. The `input`, `intermediate`, and `output` arguments are used in `utils/create_dir_paths.py` to fix the paths or directories from which a step in the pipeline reads/writes its input/output data inside the corresponding `/data` subfolders.

If `cfg.datapaths` points to `<input_path>` or `<output_path>`, then `utils/create_dir_paths.py` will automatically create a symlink as in the following example:

```bash
export HOME_DIR=$(pwd)

cd $HOME_DIR/data/input/ .
ln -s <input_path> . 

cd $HOME_DIR/data/output/
ln -s <output_path> . 
```

### Pipeline

You can run the pipeline steps manually or run the snakemake pipeline described in the Snakefile.

**run pipeline steps manually**

```bash
python src/download_shapefile.py
python src/download_climate_types.py
python src/aggregate_climate_types.py
```

**run snakemake pipeline**
or run the pipeline:

```bash
snakemake --cores 1 --configfile conf/config.yaml
```

## Dockerized Pipeline

Create the folder where you would like to store the output dataset.

```bash 
mkdir <path>/climate_types_raster2polygon
```

### Pull and Run:

```bash
docker pull nsaph/climate_types_raster2polygon
docker run -v <path>/climate_types_raster2polygon/:/app/data/output/climate_types_raster2polygon nsaph/climate_types_raster2polygon
```
