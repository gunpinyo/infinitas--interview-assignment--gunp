import re
import json
import csv
import collections

import yaml
import requests
from bs4 import BeautifulSoup
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

data_columns = ["name", "zip_code", "longitude", "latitude", "location_office"]


def scrape_thaipost(url_thaipost : str) -> pd.DataFrame:
    req = requests.get(url_thaipost)
    soup = BeautifulSoup(req.text, "html.parser")

    # extract `<script>` tag from the entire html
    elem_list = soup.find_all("script")
    elem_list = list(filter(lambda elem: elem.string is not None,
                            soup.find_all("script")))
    # there will be multiple script tags but only one contains string
    assert len(elem_list) == 1

    # extract the json data from the rest of code in the script
    match = re.findall(r"office = (\[\{.*\}\])\n", elem_list[0].string)
    # this office variable is assigned (as a list) exactly once
    assert len(match) == 1

    # load this json data as a python object
    data_json_list = json.loads(match[0])

    # convert to list of list
    data_list_list = list()
    for item in data_json_list:
        data_list = list()
        for key in data_columns:
            data_list.append(item[key])
        data_list_list.append(data_list)

    # convert to pandas data frame
    df = pd.DataFrame(data_list_list, columns=data_columns)

    return df


# credit: this function is heavily influenced by
# https://medium.com/super-ai-engineer/
# วิเคราะห์ข้อมูล-spatial-data-โดยใช้-geopandas-part1-90be80866ea2
def plot_geopanda_thaipost(df : pd.DataFrame):
    geometry = gpd.points_from_xy(df["longitude"], df["latitude"])
    gdf_orig = gpd.GeoDataFrame(df, geometry=geometry)
    gdf_orig.crs = {"init": "epsg:4326"}

    # filter out invalid coordinates (not in Thailand)
    gdf_cond = gdf_orig[
        (gdf_orig["longitude"] >= 96)  &  (gdf_orig["latitude"] >= 4)  &
        (gdf_orig["longitude"] <= 106) &  (gdf_orig["latitude"] <= 22) ]

    gdf_cond.plot(markersize=0.5)
    plt.savefig("../build/points-only.png", dpi=600)


def get_thai_provinces(url_provinces : str):
    req = requests.get(url_provinces)
    data = json.loads(req.text)
    result = dict()
    for item in data:
        key = item["name_th"]
        assert key not in result.keys()
        result[key] = item
    return result


def sanity_check_address_consistency(province_dict : dict,
                                     df : pd.DataFrame):
    province_names = list(province_dict.keys()) + ["กทม"]
    with open("../build/addr_inconsistency.log",
              "wt", encoding="utf-8") as log_file:
        for address in df["location_office"]:
            found_list = list()
            for province_name in province_names:
                if province_name in address:
                    found_list.append(province_name)
            if len(found_list) != 1:
                log_file.write("found_provinces: " + str(found_list) + "\n")
                log_file.write(address + "\n")


def get_dict_zipcode_to_province_name():
    result = dict()
    with open("../assets/TH.csv", "rt") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")
        for row in csv_reader:
            zipcode = row[1]
            province_name = row[3]
            result[zipcode] = province_name
    return result


def generate_province_name_to_num_locations(df : pd.DataFrame):

    zipcode_to_province_name = get_dict_zipcode_to_province_name()
    
    province_name_to_num_locations = collections.Counter()
    for zip_code in df["zip_code"]:
        if zip_code not in zipcode_to_province_name.keys():
            continue
        key = zipcode_to_province_name[zip_code]
        province_name_to_num_locations[key] += 1

    result_list = list(province_name_to_num_locations.items())
    result_list.sort()
        
    with open("../build/province-name-to-num-locations.csv",
              "wt", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow(["province-name", "num-locations"])
        for key, val in result_list:
            csv_writer.writerow([key, val])


def main():
    with open("../config.yaml", "rt", encoding="utf-8") as config_file:
        config_data = yaml.safe_load(config_file)
        url_thaipost = config_data["url-thaipost"]
        url_provinces = config_data["url-thai-provinces"]
        df = scrape_thaipost(url_thaipost)
        # print(df)
        create_geopanda_dataframe(df)
        province_dict = get_thai_provinces(url_provinces)
        sanity_check_address_consistency(province_dict, df)
        generate_province_name_to_num_locations(df)

        
if __name__ == '__main__':
    main()
