import sys

GEONAMES_FILE = ".cache/geonames.tsv.gz"
GEONAMES_DB = ".cache/geonames.db"


if __name__ == "__main__":
    # print out the requested variable
    print(locals()[sys.argv[1]])
