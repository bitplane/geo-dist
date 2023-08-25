#!/usr/bin/env python

import pickle

from geo_dist_prep.geotree import Tree
from geo_dist_prep.geotree.data import COLUMNS, TREE_FILE


def create_data():
    tree: Tree = pickle.load(open(TREE_FILE, "rb"))
    max_distance = 250_000

    yield COLUMNS

    for row in tree.sample_data(max_distance):
        yield row.items()


if __name__ == "__main__":
    for row in create_data():
        print("\t".join(field or "" for field in row))
