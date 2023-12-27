rule all:
    input:
        expand("data/output/climate_types_raster2polygon/climate_types_{polygon_name}_{year}.csv", 
               polygon_name=config["shapefile_polygon_name"], 
               year=config["shapefile_year"])

rule download_climate_types:
    output:
        expand("data/input/climate_types/{climate_types_file}", 
               climate_types_file=config["climate_types_file"])
    shell:
        "python src/download_climate_types.py"

rule download_shapefiles:
    output:
        # for simplification, only the geometric data .shp file is listed
        # but the shape index .shx, attribute dara .dbf, and 
        # other shapefile accompanying files are required
        expand("data/input/shapefiles/shapefile_{polygon_name}_{year}/shapefile.shp", 
               polygon_name=config["shapefile_polygon_name"], 
               year=config["shapefile_year"]) 
    shell:
        "python src/download_shapefile.py"

rule aggregate_climate_types:
    input:
        expand("data/input/climate_types/{climate_types_file}", 
               climate_types_file=config["climate_types_file"]),
        expand("data/input/shapefiles/shapefile_{polygon_name}_{year}/shapefile.shp", 
               polygon_name=config["shapefile_polygon_name"], 
               year=config["shapefile_year"])
    output:
        expand("data/intermediate/climate_pcts/climate_pcts_{polygon_name}_{year}/pcts_file.json", 
               polygon_name=config["shapefile_polygon_name"], 
               year=config["shapefile_year"]),
        expand("data/intermediate/climate_pcts/climate_pcts_{polygon_name}_{year}/class_file.csv", 
               polygon_name=config["shapefile_polygon_name"], 
               year=config["shapefile_year"]),
        expand("data/output/climate_types_raster2polygon/climate_types_{polygon_name}_{year}.csv", 
               polygon_name=config["shapefile_polygon_name"], 
               year=config["shapefile_year"])
    shell:
        "python src/aggregate_climate_types.py"
