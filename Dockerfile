FROM condaforge/mambaforge:23.3.1-1

# install build essentials
RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

# Clone your repository
RUN git clone https://github.com/NSAPH-Data-Processing/climate_types_raster2polygon . 

# Update the base environment
RUN mamba env update -n base -f requirements.yml 
#&& mamba clean -a

RUN apt update && apt install -y libsm6 libxext6
RUN apt-get install -y libxrender-dev

# Create paths to data placeholders
RUN python utils/create_dir_paths.py datapaths=datapaths.yaml

# snakemake --configfile conf/config.yaml --cores 4 -C shapefile_polygon_name=zcta
ENTRYPOINT ["snakemake"]
CMD ["--cores", "1", "--configfile", "conf/config.yaml"]
