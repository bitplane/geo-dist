#!/usr/bin/env python
import csv
import math

from geo_dist_prep.data import DIST_DATA, NORMALIZED_DATA
from geo_dist_prep.geotree.node import location_to_pos

field_names = ["lat1", "lon1", "lat2", "lon2", "by_road", "by_air", "angle"]


def normalize_row(r: dict):
    """
    mutates the row
    """
    r["x1"], r["y1"] = location_to_pos(float(r["lat1"]), float(r["lon1"]))
    r["x2"], r["y2"] = location_to_pos(float(r["lat2"]), float(r["lon2"]))
    r["by_road_km"] = float(r["by_road"]) / 1_000  # km
    r["by_air_km"] = float(r["by_air"]) / 1_000  # km
    r["normalized_angle"] = (float(r["angle"]) + math.pi) / (2 * math.pi)


def normalize_data():
    reader = csv.DictReader(open(DIST_DATA, "rt"), delimiter="\t")

    yield reader.fieldnames

    for row in reader:
        new_row = {field: row[field] for field in field_names}
        normalize_row(new_row)

        yield []


def write_data(fout):
    for row in normalize_data():
        fout.write("\t".join(str(field) or "" for field in row) + "\n")


if __name__ == "__main__":
    with open(NORMALIZED_DATA, "wt") as fin:
        write_data(fin)
