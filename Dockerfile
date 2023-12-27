FROM condaforge/mambaforge:23.3.1-1

# install build essentials
RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

# Clone your repository
RUN git clone https://github.com/NSAPH-Data-Processing/climate_types_raster2polygon . 

# Update the base environment
RUN mamba env update -n base -f requirements.yml 
#&& mamba clean -a

# Create paths to data placeholders
RUN python utils/create_dir_paths.py

CMD ["bash", "/app/pipeline.sh"]
