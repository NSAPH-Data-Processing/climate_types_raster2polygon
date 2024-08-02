import requests
import json
import os
import pycountry
from datetime import datetime
import geopandas as gpd
from shapely import wkt
import argparse


def get_global_shapefiles(output_dir):
    # Set directories
    out_dir = output_dir
    os.makedirs(out_dir, exist_ok=True)

    # Get the year and month
    date = datetime.today().strftime('%Y%m')

    # Define the baseline URL for the API
    URL = "https://www.geoboundaries.org/api/current/"

    # Release type
    RELEASE_TYPE = "gbOpen/"

    # Boundary types
    BOUNDARY_TYPE = ["/ADM0/", "/ADM1/", "/ADM2/", "/ADM3/", "/ADM4/", "/ADM5/"]

    # Get the country ISO codes
    # allISOcodes = [country.alpha_3 for country in list(pycountry.countries)[1:3]]
    countries_test = list(pycountry.countries)[1:3]

    with open(f"logfile_jsonfiles_{date}.txt", "w") as log_file:
        for i, c in enumerate(countries_test):
            log_file.write("---------------------------------------------------------------------\n")
            #find on ISO code
            ISO_CODE3 = c.alpha_3
            log_file.write(f"Beginning download of {c.name} — ISO Code {ISO_CODE3} — {i + 1} of {len(countries_test)}\n")
            
            for j, boundary in enumerate(BOUNDARY_TYPE):
                dl_link = f"{URL}{RELEASE_TYPE}{ISO_CODE3}{boundary}"
                dl_file = f"{out_dir}{ISO_CODE3}_{boundary.strip('/')}_{date}.txt"
                
                if os.path.exists(dl_file):
                    log_file.write("File already downloaded. Proceeding to next. \n")
                else:
                    try:
                        response = requests.get(dl_link)
                        response.raise_for_status()
                        with open(dl_file, "wb") as file:
                            file.write(response.content)
                        log_file.write(":) file downloaded successfully \n")
                    except requests.RequestException as e:
                        log_file.write(f"ERROR! {ISO_CODE3} {boundary} file did not download successfully \n")

    # Read in the JSON files to download the actual geometry features
    all_json = [f for f in os.listdir(out_dir) if f.endswith(f"{date}.txt")]
    unique_country_json = list(set(f[:3] for f in all_json))

    with open(f"logfile_shapefiles_{date}.txt", "w") as log_file:
        for i, country_code in enumerate(unique_country_json):
            log_file.write("----------------------------------------------------------------------\n")
            log_file.write(f"Processing country {i + 1} of {len(unique_country_json)} - {country_code}\n")

            files = [f for f in all_json if f.startswith(country_code)]
            all_admin_levels = sorted(set(int(f[7]) for f in files))
            log_file.write(f".....Highest admin. level: {max(all_admin_levels)}\n")
            log_file.write(f".....Total levels: {len(all_admin_levels)}\n")

            for outlevel in all_admin_levels:
                file = [f for f in files if f.startswith(country_code+'_ADM'+str(outlevel))][0]

                with open(os.path.join(out_dir, file)) as json_file:
                    input_json = json.load(json_file)

                year_boundary = input_json['boundaryYearRepresented']
                admin_level = input_json['boundaryType'][3]

                response = requests.get(input_json['gjDownloadURL'])
                input_geojson = gpd.read_file(response.text)
                
                input_geojson = input_geojson.apply(lambda x: wkt.loads(x) if isinstance(x, str) else x)
                input_geojson.rename(columns={c: c+"_"+admin_level for c in input_geojson.columns if c not in ['geometry']}, inplace=True)

                input_geojson[f"ABYear_{admin_level}"] = year_boundary
                final = input_geojson.drop(columns=[col for col in input_geojson.columns if 'shapeGroup' in col])

                outfilename = file.replace(".txt", ".gpkg")
                final.to_file(os.path.join(out_dir, outfilename), driver='GPKG')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot multiple shapefiles")
    parser.add_argument("output_dir", help="Output directory")
    args = parser.parse_args()

    get_global_shapefiles(args.output_dir)