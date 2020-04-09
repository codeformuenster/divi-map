""" Download raw report from intensivregister. """

from datetime import datetime
from pathlib import Path

import requests


# DOWNLOAD JSON
URL = "https://www.intensivregister.de/api/public/intensivregister?page=0&size=2000"
r = requests.get(URL)

# SAVE TO FILE
# get timestamp
utc_date = datetime.utcnow()
iso_utc = utc_date.strftime("%Y-%m-%dT%H:%M:%SZ")
# save raw JSON to file
filename = Path(f"data/raw/icu_{iso_utc}.json")
with open(filename, "w") as f:
    f.write(r.text)
