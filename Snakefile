import yaml

conda: "requirements.yaml"
configfile: "conf/config.yaml"

year=config["shapefile_year"]
polygon_name=config["shapefile_polygon_name"]

rule all:
    input:
        f"data/intermediate/climate_pcts/climate_pcts_{polygon_name}_{year}.json", 
        f"data/intermediate/climate_pcts/climate_types_{polygon_name}_{year}.csv",
        f"data/output/climate_types_raster2polygon/climate_types_{polygon_name}_{year}.parquet"

rule download_climate_types:
    output:
        f"data/input/climate_types/{config['climate_types_file']}"
    shell:
        "python src/download_climate_types.py"

rule download_shapefiles:
    output:
        f"data/input/shapefiles/shapefile_{polygon_name}_{year}/shapefile.shp" #ext = ["shp", "shx", "dbf", "prj", "cpg", "xml"]
    shell:
        "python src/download_shapefile.py"

rule aggregate_climate_types:
    input:
        f"data/input/climate_types/{config['climate_types_file']}", 
        f"data/input/shapefiles/shapefile_{polygon_name}_{year}/shapefile.shp"
    output:
        f"data/intermediate/climate_pcts/climate_pcts_{polygon_name}_{year}.json", 
        f"data/intermediate/climate_pcts/climate_types_{polygon_name}_{year}.csv", 
        f"data/output/climate_types_raster2polygon/climate_types_{polygon_name}_{year}.parquet"
    shell:
        "python src/aggregate_climate_types.py"
