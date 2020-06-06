""" Process data """

import json
from pathlib import Path
from typing import Dict, List

import pandas as pd
from functional import seq

# LOAD DATA
# index raw jsons
json_paths: List[Path] = list(Path("data/raw").glob("*.json"))
# read raw data sets to list
print("Reading in raw JSON data...")
data_dicts: List[pd.DataFrame] = []
for json_path in json_paths:
    # read raw json to dict
    with open(json_path) as f:
        raw: Dict = json.load(f)
    # get 'data' list
    data: List[Dict] = raw["data"]
    data_dicts.append(data)

# JSONS TO SINGLE DATAFRAME
print("Combining data to DataFrame...")
df = pd.DataFrame()
for data in data_dicts:
    df_new = pd.json_normalize(data)
    df = pd.concat([df, df_new], ignore_index=True)

# CLEAN DATA
print("Cleaning data...")
# drop duplicates, remove duplicated id field, sort by hospital ID
assert all(df.id == df["krankenhausStandort.id"]), "id fields not redundant!"
df_clean = (
    df.drop(columns=["krankenhausStandort.id"])  # redundant ID
    .drop(columns=["meldebereiche"])  # field value is a list, fails with 'drop_duplicates'
    .drop_duplicates()
    .sort_values(["id", "meldezeitpunkt"])
)
# shorten column names
df_clean.columns = seq(df_clean.columns).map(lambda column: column.split(".")[-1])

# SAVE TO CSV
df_clean.to_csv(str(Path(f"data/processed/df_clean.csv")), index=False)
