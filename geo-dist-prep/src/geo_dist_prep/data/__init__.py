import sys

GEONAMES_FILE = ".cache/geonames.tsv.gz"
GEONAMES_DB = ".cache/geonames.db"

TREE_FILE = ".cache/tree.pkl"
NODE_PAIRS = ".cache/pairs.tsv"
DIST_DATA = ".cache/dist.tsv"
NORMALIZED_DATA = ".cache/normalized.tsv"


if __name__ == "__main__":
    # print out the requested variable
    print(locals()[sys.argv[1]])
