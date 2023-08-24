#!/usr/bin/env python
"""
Experiment with a geohash tree. Probably not needed and is
complex and ugly.

todo: delete it
"""
import csv
import json
import sys
from typing import Any

base32 = "0123456789bcdefghjkmnpqrstuvwxyz"


class GeoHashes:
    """
    A dictionary-like object, keyed by geohash.
    """

    def __init__(self, max_length: int):
        self.max_depth = max_length + 1
        self.levels = [{} for _ in range(self.max_depth)]

    def __setitem__(self, key: str, value: Any) -> None:
        max_level = min(len(key), self.max_depth)

        for level in range(max_level):
            level_key = key[:level]
            level_dict = self.levels[level]
            if level_key not in level_dict:
                level_dict[level_key] = {}
            level_dict[level_key][key] = value

    def __getitem__(self, key: str) -> Any:
        level = min(len(key), self.max_depth)
        return self.levels[level][key]


def load_tree(infile):
    reader = csv.DictReader(infile, delimiter="\t")
    tree = GeoHashes(5)

    for row in reader:
        tree[row["geohash"]] = row

    return tree


if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    else:
        file_name = ".cache/filtered.tsv"

    with open(file_name) as infile:
        tree = load_tree(infile)
    # gctckgh7mybk

    print(json.dumps(tree.levels, indent=2))
