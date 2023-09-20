FROM condaforge/mambaforge:23.3.1-1

# install build essentials
RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

# Clone your repository
RUN git clone https://github.com/NSAPH-Data-Processing/climate_types_zip_zcta . 

# Update the base environment
RUN mamba env update -n base -f requirements.yml 
#&& mamba clean -a

# Create symlinks to data placeholders
RUN python src/create_data_symlinks.py

CMD ["pipeline.sh"]
