#!/usr/bin/env python
import csv
import re
import sys

import pygeohash

csv.field_size_limit(sys.maxsize)


def process_tsv(columns, filters, infile):
    reader = csv.DictReader(infile, delimiter="\t")

    # Print the header
    yield columns

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

            fields = [row[col] for col in columns]

            yield fields
        except Exception:
            pass  # be better than this


columns = ["osm_id", "type", "lon", "lat", "name", "geohash"]
filters = {
    "osm_type": "node",
    "class": "place",
    "type": "city|village|hamlet|borough|suburb|quarter|neighbourhood",
}


if __name__ == "__main__":
    for row in process_tsv(columns, filters, sys.stdin):
        print("\t".join(row))
