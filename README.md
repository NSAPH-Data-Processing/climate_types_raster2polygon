# climate_types_raster2polygon

Code to produce spatial aggregations of [Koppen-Geiger climate types](https://www.nature.com/articles/sdata2018214). The spatial aggregation are performed from climate type information from grid/raster (tiff) to polygons (shp).

---

# Climate Types

Raw climate type maps are referenced to the World Geodetic Reference System 1984 (WGS 84) ellipsoid and made available at three resolutions (0.0083°, 0.083°, and 0.5°; approximately 1 km, 10 km, and 50 km at the equator, respectively).

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

### Create input and output data placeholders 

Run

```bash
python utils/create_dir_paths.py 
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
# to generate county aggregations
snakemake --cores 1 
# to generate zcta aggregations
snakemake --cores 1 -C shapefile_polygon_name=zcta
```

## Dockerized Pipeline

Create the folder where you would like to store the output dataset.

```bash 
mkdir <path>/climate_types_raster2polygon
```

### Pull and Run:

```bash
docker pull nsaph/climate_types_raster2polygon
# to generate county aggregations
docker run -v <test_path>:/app/data/output/climate_types_raster2polygon -t nsaph/climate_types_raster2polygon
# to generate zcta aggregations
docker run -v <test_path>:/app/data/output/climate_types_raster2polygon -t nsaph/climate_types_raster2polygon --cores 1 -C shapefile_polygon_name=zcta
```

### If you want to build your own image use

```
docker build -t <image_name> .
```

To dev or test do 
```
docker run --entrypoint /bin/bash -v $(pwd)/:/app -it <image> 
```

For a multiplatform built use
```
docker buildx build --platform linux/amd64,linux/arm64 -t <user>/<image>:<version> . --push
```
Remember this step is unnecessary as the built image is availabe under `nsaph/climate_types_raster2polygon:latest`.
