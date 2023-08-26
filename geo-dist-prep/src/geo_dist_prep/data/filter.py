#!/usr/bin/env python
import csv
import gzip
import re
import sys

import pygeohash
from geo_dist_prep.geotree.data import COLUMNS, FILTERED_FILE, GEONAMES_FILE

filters = {
    "osm_type": r"node",
    "class": r"place",
    "type": r"city|village|hamlet|borough|suburb|quarter|neighbourhood",
    "country_code": r"\b(gb|im|ie|gg|je)\b",
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

            if filtered or not row["lat"] or not row["lon"]:
                continue

            lat = float(row["lat"])
            lon = float(row["lon"])
            row["geohash"] = pygeohash.encode(lat, lon)

            fields = [row[col] for col in COLUMNS]

            yield fields
        except Exception:
            pass  # shame on me


def write_filtered_geonames():
    fin = gzip.open(GEONAMES_FILE, "rt")
    fout = open(FILTERED_FILE, "wt")
    writer = csv.writer(fout, delimiter="\t")
    for row in filter_geonames(filters, fin):
        writer.writerow(row)


if __name__ == "__main__":
    write_filtered_geonames()