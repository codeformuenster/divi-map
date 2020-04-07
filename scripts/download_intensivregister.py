""" Download intensivregister. """

import requests
import pandas as pd
from pathlib import Path

# download JSON from API
r = requests.get('https://www.intensivregister.de/api/public/intensivregister?page=0&size=2000')

# get data from JSON
result: dict = r.json()
assert result['rowCount'] == len(result['data'])
data = result['data']

# parse to pandas
df = pd.json_normalize(data)

# save to CSV
df.to_csv(Path("data/intenstivregister.csv"))
