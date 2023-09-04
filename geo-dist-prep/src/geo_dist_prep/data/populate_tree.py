from datetime import datetime

from geo_dist_prep.data import GEONAMES_DB
from geo_dist_prep.schemas.base import Base
from geo_dist_prep.schemas.geoname import GeoName
from geo_dist_prep.tree.globe import Globe
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def populate_tree(path: str = ".", limit=None):
    engine = create_engine(f"sqlite:///{path}/{GEONAMES_DB}")

    Base.metadata.create_all(engine)
    SessionMeker = sessionmaker(bind=engine)
    session = SessionMeker()

    print(f"populate_tree: loading geonames from {GEONAMES_DB}")

    if limit:
        geonames = session.query(GeoName).limit(limit).all()
    else:
        geonames = session.query(GeoName).all()

    globe = Globe()

    print(f"populate_tree: found {len(geonames)} geonames")

    count = 0

    for geoname in geonames:
        address = list(globe.get_address(geoname.lat, geoname.lon))
        current = globe
        for pos in address:
            current = current.add_child(pos)
        current.add_child(address[-1], geoname.name)

        count += 1

        if count % 10_000 == 0:
            print(f"populate_tree: {count} of {len(geonames)} geonames added to tree")

    # todo: save tree to file
    return globe


if __name__ == "__main__":
    populate_tree()

    print("populate_tree: Finished at", datetime.now().isoformat())
    raise Exception("Don't save success status")
