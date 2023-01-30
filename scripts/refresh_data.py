import requests
import json
from sqlite_utils import Database


db = Database("app/data.sqlite", recreate=True)

def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}

with open("tmp/startups.json", "w") as f:
    raw = requests.get("https://beta.gouv.fr/api/v2.4/startups.json").json()
    startups = [
        without_keys(r["attributes"], ["content_url_encoded_markdown", "events", "phases"]) | {"id": r["id"]}
        for r in raw["data"]
        if r["type"] == "startup"
    ]
    db["startups"].insert_all(startups, pk="id", replace=True)


