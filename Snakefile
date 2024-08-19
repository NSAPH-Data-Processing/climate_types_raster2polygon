import yaml

conda: "requirements.yaml"
configfile: "conf/config.yaml"

# == Load configuration ==

# dynamic config files
defaults_dict = {key: value for d in config['defaults'] if isinstance(d, dict) for key, value in d.items()}
shapefiles_cfg = yaml.safe_load(open(f"conf/shapefiles/{defaults_dict['shapefiles']}.yaml", 'r'))
# == Define variables ==
shapefile_list = shapefiles_cfg.keys()

rule all:
    input:
        expand(f"data/output/climate_types_raster2polygon/climate_types_{{shapefile_name}}.parquet", 
            shapefile_name=shapefile_list
        )

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
        f"data/input/shapefiles/{{shapefile_name}}/{{shapefile_name}}.shp"
    output:
        f"data/output/climate_types_raster2polygon/climate_types_{{shapefile_name}}.parquet",
        f"data/intermediate/climate_pcts/climate_pcts_{{shapefile_name}}.json",
        f"data/intermediate/climate_pcts/climate_types_{{shapefile_name}}.csv"
    shell:
        f"python src/aggregate_climate_types.py"
