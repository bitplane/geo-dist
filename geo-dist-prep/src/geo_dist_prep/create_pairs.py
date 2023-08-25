#!/usr/bin/env python

import pickle

from geo_dist_prep.geotree import Tree
from geo_dist_prep.geotree.data import NODE_PAIRS, TREE_FILE


def create_data():
    tree: Tree = pickle.load(open(TREE_FILE, "rb"))
    max_distance = 250_000

    yield ["lon1", "lat1", "lon2", "lat2"]

    for row in tree.sample_data(max_distance):
        yield row


def write_data(fout):
    for row in create_data():
        fout.write("\t".join(str(field) or "" for field in row) + "\n")


if __name__ == "__main__":
    with open(NODE_PAIRS, "w") as fin:
        write_data(fin)
