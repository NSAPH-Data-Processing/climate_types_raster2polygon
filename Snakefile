import hydra
from omegaconf import OmegaConf
import json

conda: "requirements.yaml"

# the workflow configuration file is orchestrated by hydra
# read config with hydra
with hydra.initialize(config_path="conf", version_base=None):
    cfg = hydra.compose(config_name="config", overrides=[])
    #print(OmegaConf.to_yaml(cfg))

# convert to dict of single shapefile dicts 
shapefiles_cfg = OmegaConf.to_container(cfg.shapefiles, resolve=True) 
# print(shapefiles_cfg)
shapefiles_cfg_dict = {shapefile["name"]: shapefile for shapefile in shapefiles_cfg}
#print(shapefiles_cfg_dict)
shapefiles_str_dict = {shapefile["name"]: "[" + json.dumps(shapefile).replace('"', '') + "]" for shapefile in shapefiles_cfg}
# print(shapefiles_str_dict)
shapefiles_list = list(shapefiles_str_dict.keys())
# print(shapefiles_list)
# print(f"""
#     python src/aggregate_climate_types.py "+shapefiles={shapefiles_str_dict[shapefiles_list[0]]}"
#     """)

#raise ValueError("stop here")

rule all:
    input:
        expand(f"{cfg.datapaths.base_path}/output/present/climate_types__koppen_geiger__{{shapefile_name}}.parquet", 
            shapefile_name=shapefiles_list
        )

rule download_climate_types:
    output:
        f"{cfg.datapaths.base_path}/input/climate_types/{cfg.climate_types_file}"
    shell:
        "python src/download_climate_types.py"

# considering removing download step in snakemake
# currently it is necessary to point to a folder populated with shapefiles for snakemake to run
# rule download_shapefiles:
#     output:
#         f"data/input/shapefiles/{{shapefile_name}}/{{shapefile_name}}.shp" #ext = ["shp", "shx", "dbf", "prj", "cpg", "xml"]
#     shell:
#         f"python src/download_us_shapefile.py"

rule aggregate_climate_types:
    input:
        f"{cfg.datapaths.base_path}/input/climate_types/{cfg.climate_types_file}", 
        lambda wildcards: f"{cfg.datapaths.base_path}/input/shapefiles/{shapefiles_cfg_dict[wildcards.shapefile_name]['filename']}"
    output:
        f"{cfg.datapaths.base_path}/intermediate/climate_pcts/climate_pcts_{{shapefile_name}}.json",
        f"{cfg.datapaths.base_path}/intermediate/climate_pcts/climate_types_{{shapefile_name}}.csv"
    params:
        shapefiles = lambda wildcards: shapefiles_str_dict[wildcards.shapefile_name]
    shell:
        (f"""
        echo {{wildcards.shapefile_name}}
        echo {{params.shapefiles}}
        python src/aggregate_climate_types.py "+shapefiles={{params.shapefiles}}"
        """)
#python src/aggregate_climate_types.py "+shapefiles=[{name: CAN_ADM2, url: null, idvar: shapeID, output_idvar: id}]"

rule format_climate_types:
    input:
        f"{cfg.datapaths.base_path}/intermediate/climate_pcts/climate_pcts_{{shapefile_name}}.json",
        f"{cfg.datapaths.base_path}/intermediate/climate_pcts/climate_types_{{shapefile_name}}.csv"
    output:
        f"{cfg.datapaths.base_path}/output/present/climate_types__koppen_geiger__{{shapefile_name}}.parquet"
    params:
        shapefiles = lambda wildcards: shapefiles_str_dict[wildcards.shapefile_name]
    shell:
        (f"""
        echo {{wildcards.shapefile_name}}
        echo {{params.shapefiles}}
        python src/format_climate_types.py "+shapefiles={{params.shapefiles}}"
        """)