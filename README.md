# climate_types_zip_zcta

Code to produce a spatial aggregation from 1km tiff raster to zcta (tiger polygons) of [Koppen-Geiger climate types](https://www.nature.com/articles/sdata2018214).

Spatial aggregation of climate type information from grid (tiff) to zcta polygons (shp). In addition the information is merged with a zip2zcta crosswalk to allow mapping to either postal zipcode of census zcta.

# Codebook Description

---

## Dataset Columns:

1. **zip**: Represents the ZIP code.
2. **zcta**: Represents the ZIP Code Tabulation Area.
3. **climate_type_short**: The abbreviated code for each specific climate type.
4. **climate_type_long**: The detailed description of each specific climate type.
5. **Af - EF**: Each of these columns represents a specific climate type. The values within these columns will represent the percentage area corresponding to each climate type for a specific ZIP or ZCTA.

---

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
## Dockerized Pipeline

Create the folder where you would like to store the output dataset.

```bash 
mkdir <path>/climate_types_zip_zcta
```

### Pull and Run:

```bash
docker pull nsaph/climate_types_zip_zcta:v1
docker run -v <path>/climate_types_zip_zcta/:/app/data/output/climate_types_zip_zcta nsaph/climate_types_zip_zcta:v1
```
