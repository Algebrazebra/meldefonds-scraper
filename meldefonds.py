#!/usr/bin/env python

"""Download tax reporting fund data from the OeKB website."""


import json
import requests
import pandas as pd

OEKB_URL = "https://my.oekb.at/kms-reporting/public?report=steuerdaten-liste-mf-gesamt&format=CSV"


def download_meldefonds(fpath) -> None:
    """Download the tax reporting fund data from the OeKB website.
    
    Parameters
    ----------
    fpath : str
        File path the data will be downloaded to

    Raises
    ------
    requests.exceptions.HTTPError
        If request to OeKB servers fails
    """

    if fpath is None:
        fpath = DEFAULT_FPATH

    headers = {
        # User agent must be specified, otherwise response does not return data
        "user-agent": "", 
    }
    response = requests.get(OEKB_URL, headers=headers)
    response.raise_for_status()

    with open(fpath, 'wb') as f:
        f.write(response.content)

def csv_to_json(input_csv, output_json) -> None:
    """Convert downloaded tax reporting fund data from csv to json format.
    
    Parameters
    ----------
    input_csv : str
        File path to csv file to be converted to json
    output_json : str
        File path to which converted json file is written to
    """

    csv_data = pd.read_csv(input_csv, delimiter=";")
    json_data = csv_data.to_json(orient="records", force_ascii=False)
    parsed_json_data = json.loads(json_data)
    with open(output_json, "w") as f:
        json.dump(parsed_json_data, fp=f, ensure_ascii=False)


if __name__ == "__main__":
    download_meldefonds(fpath="./meldefonds.csv")
    csv_to_json(
        input_csv="./meldefonds.csv",
        output_json="./meldefonds.json"
    )