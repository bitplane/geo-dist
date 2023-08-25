#!/usr/bin/env python
import csv
import re
import sys

import pygeohash
from geo_dist_prep.geotree.data import COLUMNS

filters = {
    "osm_type": "node",
    "class": "place",
    "type": "city|village|hamlet|borough|suburb|quarter|neighbourhood",
    "country_code": "$gb|ie|im|gg|je^",
}


def filter_geonames(filters, infile):
    csv.field_size_limit(sys.maxsize)

    reader = csv.DictReader(infile, delimiter="\t")

    yield COLUMNS

    for row in reader:
        try:
            filtered = not all(
                re.match(col_regex, row[col_name])
                for col_name, col_regex in filters.items()
                if row[col_name]
            )

            if filtered:
                continue

            if row["lon"] and row["lat"]:
                lat = float(row["lat"])
                lon = float(row["lon"])
                row["geohash"] = pygeohash.encode(lat, lon)
            else:
                row["geohash"] = ""

            fields = [row[col] for col in COLUMNS]

            yield fields
        except Exception:
            pass  # shame on me


if __name__ == "__main__":
    for row in filter_geonames(filters, sys.stdin):
        print("\t".join(field or "" for field in row))
