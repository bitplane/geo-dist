#!/usr/bin/env python
import csv
import gzip
import os
import re
import sys

from geo_dist_prep.data import GEONAMES_DB, GEONAMES_FILE
from geo_dist_prep.schemas.base import Base
from geo_dist_prep.schemas.geoname import GeoName
from geo_dist_prep.utils import format_int
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

filters = {
    "osm_type": r"node",
    "class": r"place",
    "type": r"borough|city|hamlet|neighbourhood|quarter|suburb|town|village",
    # "country_code": r"\b(gb|im|ie|gg|je)\b", # UK and Ireland
    # put the above line in somewhere else, so we can use it for other countries
    # later in the pipeline
}


def load_geonames(filters):
    if os.path.exists(GEONAMES_DB):
        os.remove(GEONAMES_DB)
    engine = create_engine(f"sqlite:///{GEONAMES_DB}")

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    csv.field_size_limit(sys.maxsize)
    infile = gzip.open(GEONAMES_FILE, "rt")
    reader = csv.DictReader(infile, delimiter="\t")

    total = 0
    kept = 0

    for row in reader:
        total += 1
        if total % 100_000 == 0:
            print(f"load: processed {format_int(total)} rows (kept {kept})")
            session.commit()

        filtered = not all(
            re.match(col_regex, row[col_name])
            for col_name, col_regex in filters.items()
            if row[col_name]
        )

        if filtered or not row["lat"] or not row["lon"]:
            continue

        data = {key: row[key] for key in GeoName.__table__.columns.keys()}
        data["class_"] = data.pop("class")
        data["type_"] = data.pop("type")
        geoname = GeoName(**data)

        session.add(geoname)

        kept += 1

    session.commit()
    session.close()

    print(f"load: processed {format_int(total)} total rows, kept {kept}")


if __name__ == "__main__":
    load_geonames(filters)
