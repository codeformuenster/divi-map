""" Download raw report from intensivregister. """

from datetime import datetime
from pathlib import Path

import requests

# DOWNLOAD JSON
r = requests.get(
    "https://www.intensivregister.de/api/public/intensivregister?page=0&size=2000"
)

# SAVE TO FILE
# get timestamp
utc_date = datetime.utcnow()
iso_utc = utc_date.strftime("%Y-%m-%dT%H:%M:%SZ")
filename: Path = Path(f"data/raw/icu_{iso_utc}.json")
# save raw JSON to file
with open(filename, "w") as f:
    f.write(r.text)
