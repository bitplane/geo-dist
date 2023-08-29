from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from functools import partial

from geo_dist_prep.data import GEONAMES_DB, PAIR_SENTINEL
from geo_dist_prep.schemas.base import Base
from geo_dist_prep.schemas.geoname import GeoName
from geo_dist_prep.schemas.geoname_pair import GeoNamePair
from geo_dist_prep.schemas.helpers import direction, distance, nearby
from geo_dist_prep.schemas.job import GeoNamePairJob
from sqlalchemy import Integer, create_engine, func, text
from sqlalchemy.orm import sessionmaker

# from geo_dist_prep.utils import print_time


def gather_pairs(job: GeoNamePairJob, geoname: GeoName):
    engine = create_engine(f"sqlite:///{GEONAMES_DB}")

    SessionMaker = sessionmaker(bind=engine)
    session = SessionMaker()
    connection = engine.connect()

    count = 5
    res = []
    for dist in (10, 20, 40, 80, 160, 200, 250, 300, 350):
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
                GeoName.osm_id != geoname.osm_id,
                nearby(geoname.lat, geoname.lon, dist),
            )
            .order_by(func.random())
            .limit(5)
        )

        compiled_sql = select_statement.statement.compile(
            compile_kwargs={"literal_binds": True}
        )
        results = connection.execute(compiled_sql).fetchall()
        res.extend(tuple(result) for result in results)

        if results:
            count -= 1
            if count == 0:
                break

    connection.close()
    session.close()
    return res


def insert_pairs(session, pairs):
    session.execute(
        text(
            "INSERT OR IGNORE INTO geoname_pair "
            "(job_id, start_id, end_id, distance, direction) "
            "VALUES (:job_id, :start_id, :end_id, :distance, :direction)"
        ),
        [
            dict(zip(("job_id", "start_id", "end_id", "distance", "direction"), pair))
            for pair in pairs
        ],
    )
    session.commit()


def create_pairs(country_code):
    engine = create_engine(f"sqlite:///{GEONAMES_DB}")

    Base.metadata.create_all(engine)
    SessionMeker = sessionmaker(bind=engine)
    session = SessionMeker()

    # Start the job
    job = GeoNamePairJob(country_code=country_code)
    session.add(job)
    print("pair job:", job.id, "for", country_code)

    try:
        # Get all geonames in the country
        geonames = (
            session.query(GeoName)
            .filter(GeoName.country_code == country_code)
            .order_by(GeoName.osm_id)
            .all()
        )
        print(f"pair job: {job.id} for {country_code} - with {len(geonames)} geonames")

        gather_and_extend = partial(gather_pairs, job)

        pairs = []

        with ProcessPoolExecutor() as executor:
            future_to_geoname = {
                executor.submit(gather_and_extend, geoname): geoname
                for geoname in geonames
            }
            last_percent = 0
            start = datetime.now()

            for i, future in enumerate(as_completed(future_to_geoname)):
                new_pairs = future.result()
                pairs.extend(new_pairs)
                percent = (i + 1) / len(geonames) * 100

                if percent - last_percent > 1:
                    t = datetime.now()
                    remaining_pc = float(100 - percent)
                    mins_so_far = (t - start).seconds / 60
                    remaining = round(mins_so_far / percent * remaining_pc, 2)
                    last_percent = percent
                    print(
                        f"pair job: gathering for {country_code} - "
                        f"{int(percent)}% ({len(pairs)} pairs), "
                        f"{remaining} mins to go"
                    )

        print(f"pair job: inserting {len(pairs)} pairs for {country_code}")
        insert_pairs(session, pairs)
        job.success = True
        session.commit()

    except Exception as e:
        print(e)
        session.rollback()
        job.message = str(e)
        raise

    finally:
        job.finished = int(datetime.now().timestamp())
        session.commit()
        session.close()


def get_missing_countries():
    engine = create_engine(f"sqlite:///{GEONAMES_DB}")

    Base.metadata.create_all(engine)
    SessionMeker = sessionmaker(bind=engine)
    session = SessionMeker()

    jobs = (
        session.query(GeoNamePairJob)
        .filter(GeoNamePairJob.success == True)  # noqa
        .all()
    )
    completed_codes = {job.country_code for job in jobs}
    all_codes = {code for code, in session.query(GeoName.country_code).distinct().all()}
    missing_codes = all_codes - completed_codes - {""}

    return sorted(list(missing_codes))


def get_pair_count():
    engine = create_engine(f"sqlite:///{GEONAMES_DB}")

    Base.metadata.create_all(engine)
    SessionMeker = sessionmaker(bind=engine)
    session = SessionMeker()

    return session.query(GeoNamePair).count()


if __name__ == "__main__":
    current_count = get_pair_count()
    print("Current pair count:", current_count)

    missing_countries = get_missing_countries()
    print("Missing countries:", len(missing_countries))

    for country_code in missing_countries:
        create_pairs(country_code)

    with open(PAIR_SENTINEL, "wt") as fout:
        fout.write(f"{datetime.now().isoformat()}")
