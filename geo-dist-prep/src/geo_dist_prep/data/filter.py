#!/usr/bin/env python
import csv
import gzip
import re
import sys

from geo_dist_prep.geotree.data import COLUMNS, FILTERED_FILE, GEONAMES_FILE

filters = {
    "osm_type": r"node",
    "class": r"place",
    "type": r"borough|city|hamlet|neighbourhood|quarter|suburb|town|village",
    "country_code": r"\b(gb|im|ie|gg|je)\b",
}


def filter_geonames(filters, infile):
    csv.field_size_limit(sys.maxsize)

    reader = csv.DictReader(infile, delimiter="\t")

    yield COLUMNS

    total = 0
    kept = 0
    errors = 0

    for row in reader:
        try:
            total += 1
            if total % 500_000 == 0:
                print(
                    f"filter: processed {total/1_000_000}m rows (kept {kept}, {errors} errors)"
                )

            filtered = not all(
                re.match(col_regex, row[col_name])
                for col_name, col_regex in filters.items()
                if row[col_name]
            )

            if filtered or not row["lat"] or not row["lon"]:
                continue

            # lat = float(row["lat"])
            # lon = float(row["lon"])
            # row["geohash"] = pygeohash.encode(lat, lon)

            fields = [row[col] for col in COLUMNS]

            yield fields
            kept += 1
        except Exception:
            errors += 1
            pass  # shame on me

    print(f"Kept {kept} out of {total} rows")


def write_filtered_geonames():
    fin = gzip.open(GEONAMES_FILE, "rt")
    fout = open(FILTERED_FILE, "wt")
    writer = csv.writer(fout, delimiter="\t")
    for row in filter_geonames(filters, fin):
        writer.writerow(row)


if __name__ == "__main__":
    write_filtered_geonames()
