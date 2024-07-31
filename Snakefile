import yaml

conda: "requirements.yaml"
configfile: "conf/config.yaml"

tag=config["shapefile_tag"]
polygon_name=config["shapefile_polygon_name"]

rule all:
    input:
        f"data/output/climate_types_raster2polygon/climate_types_{polygon_name}_{tag}.parquet"

rule download_climate_types:
    output:
        f"data/input/climate_types/{config['climate_types_file']}"
    shell:
        "python src/download_climate_types.py"

# temporarily removing download step in snakemake
# rule download_shapefiles:
#     output:
#         f"data/input/shapefiles/shapefile_{polygon_name}_{tag}/shapefile.shp" #ext = ["shp", "shx", "dbf", "prj", "cpg", "xml"]
#     shell:
#         f"python src/download_shapefile.py shapefile_tag={tag} shapefile_polygon_name={polygon_name}"

rule aggregate_climate_types:
    input:
        f"data/input/climate_types/{config['climate_types_file']}", 
        f"data/input/shapefiles/shapefile_{polygon_name}_{tag}/shapefile.shp"
    output:
        f"data/output/climate_types_raster2polygon/climate_types_{polygon_name}_{tag}.parquet",
        f"data/intermediate/climate_pcts/climate_pcts_{polygon_name}_{tag}.json",
        f"data/intermediate/climate_pcts/climate_types_{polygon_name}_{tag}.csv"
    shell:
        f"python src/aggregate_climate_types.py shapefile_tag={tag} shapefile_polygon_name={polygon_name}"
