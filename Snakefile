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
#print(shapefiles_cfg)
shapefiles_cfg_dict = {shapefile["name"]: "[" + json.dumps(shapefile).replace('"', '') + "]" for shapefile in shapefiles_cfg}
#print(shapefiles_cfg_dict)
shapefiles_list = list(shapefiles_cfg_dict.keys())
#print(shapefiles_list)
# print(f"""
#     python src/aggregate_climate_types.py "+shapefiles={shapefiles_cfg_dict[shapefiles_list[0]]}"
#     """)

#raise ValueError("stop here")

rule all:
    input:
        expand(f"data/output/climate_types_raster2polygon/climate_types_{{shapefile_name}}.parquet", 
            shapefile_name=shapefiles_list
        )

rule download_climate_types:
    output:
        f"data/input/climate_types/{cfg.climate_types_file}"
    shell:
        "python src/download_climate_types.py"

# temporarily removing download step in snakemake
# rule download_shapefiles:
#     output:
#         f"data/input/shapefiles/{{shapefile_name}}/{{shapefile_name}}.shp" #ext = ["shp", "shx", "dbf", "prj", "cpg", "xml"]
#     shell:
#         f"python src/download_us_shapefile.py"

rule aggregate_climate_types:
    input:
        f"data/input/climate_types/{cfg.climate_types_file}", 
        f"data/input/shapefiles/{{shapefile_name}}/{{shapefile_name}}.shp"
    output:
        f"data/output/climate_types_raster2polygon/climate_types_{{shapefile_name}}.parquet",
        f"data/intermediate/climate_pcts/climate_pcts_{{shapefile_name}}.json",
        f"data/intermediate/climate_pcts/climate_types_{{shapefile_name}}.csv"
    params:
        shapefile_name = lambda wildcards: shapefiles_cfg_dict[wildcards.shapefile_name]
    shell:
        (f"""
        echo {{wildcards.shapefile_name}}
        python src/aggregate_climate_types.py "+shapefiles={{params.shapefile_name}}"
        """)
#python src/aggregate_climate_types.py "+shapefiles=[{name: CAN_ADM2, url: null, idvar: shapeID, output_idvar: id}]"