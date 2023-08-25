#!/usr/bin/env python

import pickle

from geo_dist_prep.geotree import Tree
from geo_dist_prep.geotree.data import COLUMNS, DATA_FILE, TREE_FILE


def create_data():
    tree: Tree = pickle.load(open(TREE_FILE, "rb"))
    max_distance = 250_000

    yield COLUMNS

    for row in tree.sample_data(max_distance):
        yield row.items()


def write_data(fout):
    for row in create_data():
        fout.write("\t".join(str(field) or "" for field in row) + "\n")


if __name__ == "__main__":
    with open(DATA_FILE, "w") as f:
        write_data(f)
