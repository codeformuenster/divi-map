""" Download intensivregister. """

import requests
import pandas as pd
from pathlib import Path

from functional import seq

# download JSON from API
r = requests.get(
    "https://www.intensivregister.de/api/public/intensivregister?page=0&size=2000"
)

# get data from JSON
result: dict = r.json()
data = result["data"]

# JSON TO DATAFRAME
df = pd.json_normalize(data).drop(columns=["krankenhausStandort.id"])
# shorten column names
df.columns = seq(df.columns).map(lambda column: column.split(".")[-1])

# TESTS
assert result["rowCount"] == len(result["data"]) == len(df), "wrong number of rows"

# SAVE TO CSV
df.to_csv(Path("data/intenstivregister.csv"))
