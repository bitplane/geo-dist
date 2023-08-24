#!/usr/bin/env python

import csv
import sys

from geotree import Tree


def load_tree(infile):
    reader = csv.DictReader(infile, delimiter="\t")
    tree = Tree()

    for row in reader:
        lat = float(row["lat"])
        lon = float(row["lon"])

        tree.add(lat, lon, row)

    tree.finalize()

    return tree


if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    else:
        file_name = ".cache/filtered.tsv"

    with open(file_name) as infile:
        tree = load_tree(infile)

    # gctckgh7mybk

    pass