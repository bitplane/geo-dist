from datetime import datetime

from geo_dist_prep.data import GEONAMES_DB
from geo_dist_prep.schemas.base import Base
from geo_dist_prep.schemas.geoname import GeoName
from geo_dist_prep.schemas.geoname_pair import GeoNamePair
from geo_dist_prep.schemas.helpers import direction, distance, nearby
from geo_dist_prep.schemas.job import GeoNamePairJob
from sqlalchemy import Integer, create_engine, func, insert
from sqlalchemy.orm import sessionmaker

country_code = "gb"


def insert_pairs(geoname: GeoName, job: GeoNamePairJob, session):
    for dist in (10, 20, 40, 80, 160):
        select_statement = (
            session.query(
                func.cast(job.id, Integer).label("job_id"),
                func.cast(geoname.osm_id, Integer).label("start_id"),
                func.cast(GeoName.osm_id, Integer).label("end_id"),
                distance(geoname.lat, geoname.lon, GeoName.lat, GeoName.lon).label(
                    "distance"
                ),
                direction(geoname.lat, geoname.lon, GeoName.lat, GeoName.lon).label(
                    "direction"
                ),
            )
            .filter(
                GeoName.score >= dist / 10,
                nearby(geoname.lat, geoname.lon, dist),
            )
            .order_by(func.random())
            .limit(5)
        )
        insert_statement = (
            insert(GeoNamePair)
            .prefix_with("OR IGNORE")
            .from_select(
                ["job_id", "start_id", "end_id", "distance", "direction"],
                select_statement,
            )
        )
        session.execute(insert_statement)


def create_pairs(country_code):
    engine = create_engine(f"sqlite:///{GEONAMES_DB}")

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Start the job
    job = GeoNamePairJob(country_code=country_code)
    session.add(job)
    session.commit()
    print("started job: ", job.id)

    try:
        # Get all geonames in the country
        geonames = (
            session.query(GeoName)
            .filter(GeoName.country_code == country_code)
            .order_by(GeoName.osm_id)
            .all()
        )

        for i, geoname in enumerate(geonames):
            insert_pairs(geoname, job, session)

            if i % 100 == 0:
                print(
                    f"{datetime.now().isoformat()}: pair job {job.id}: committing {i} of {len(geonames)}"
                )
                session.commit()

        job.success = True
        session.commit()

    except Exception as e:
        print(e)
        session.rollback()
        job.message = str(e)

    finally:
        job.finished = int(datetime.now().timestamp())
        session.commit()
        session.close()


if __name__ == "__main__":
    create_pairs(country_code)
