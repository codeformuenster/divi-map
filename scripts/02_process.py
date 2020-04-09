""" Process data """

import json
from pathlib import Path
from typing import List

import pandas as pd
from functional import seq

# LOAD DATA
# index raw jsons
json_paths: List[Path] = list(Path("data/raw").glob("*.json"))
# read raw data sets to list
data_dicts: List[pd.DataFrame] = []
for json_path in json_paths:
    # read raw json to dict
    with open(json_path) as f:
        raw: dict = json.load(f)
    # get 'data' list
    data: List[dict] = raw["data"]
    data_dicts.append(data)

# JSONS TO SINGLE DATAFRAME
df = pd.DataFrame()
for data in data_dicts:
    df_new = pd.json_normalize(data)
    df = pd.concat([df, df_new], ignore_index=True)

# CLEAN DATA
# drop duplicates, remove duplicated id field, sort by hospital ID
assert all(df.id == df["krankenhausStandort.id"]), "id fields not redundant!"
df_clean = (
    df.drop_duplicates().drop(columns=["krankenhausStandort.id"]).sort_values("id")
)
# shorten column names
df_clean.columns = seq(df_clean.columns).map(lambda column: column.split(".")[-1])

# SAVE TO CSV
df_clean.to_csv(str(Path(f"data/processed/df_clean.csv")), index=False)
