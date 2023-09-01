import json
import os
import time
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from functools import partial

import httpx
from geo_dist_prep.data import GEONAMES_DB
from geo_dist_prep.data.docker.regions import group_countries_by_region
from geo_dist_prep.data.docker.run import running_docker_container
from geo_dist_prep.normalize import normalize_coords
from geo_dist_prep.schemas.geoname import GeoName
from geo_dist_prep.schemas.geoname_pair import GeoNamePair
from geo_dist_prep.schemas.job import Base, GeoNameEnrichJob, GeoNamePairJob
from geo_dist_prep.schemas.training_data import TrainingData  # noqa
from geo_dist_prep.utils import chunks
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

URL = "http://localhost:8080/ors/v2/directions/driving-car"
BATCH_SIZE = 10_000


def insert_data(session: Session, rows):
    if not rows:
        return

    session.execute(
        text(
            "INSERT INTO training_data "
            "(job_id, start_id, end_id, y1, x1, y2, x2, direction, distance, routable) "
            "VALUES (:job_id, :start_id, :end_id, :y1, :x1, :y2, :x2, :direction, :distance, :routable)"
        ),
        [
            dict(
                zip(
                    (
                        "job_id",
                        "start_id",
                        "end_id",
                        "y1",
                        "x1",
                        "y2",
                        "x2",
                        "direction",
                        "distance",
                        "routable",
                    ),
                    row,
                )
            )
            for row in rows
        ],
    )
    session.commit()


def result(job_id, pair, lat1, lon1, lat2, lon2, distance, routable):
    y1, x1 = normalize_coords(lat1, lon1)
    y2, x2 = normalize_coords(lat2, lon2)

    return [
        job_id,
        pair.start_id,
        pair.end_id,
        y1,
        x1,
        y2,
        x2,
        pair.direction,
        distance,
        routable,  # route found
    ]


def call_api(job_id, pairs):
    client = httpx.Client(http2=True)

    max_retries = 5
    results = []

    for i, pair in enumerate(pairs):
        lat1 = pair.lat1
        lat2 = pair.lat2
        lon1 = pair.lon1
        lon2 = pair.lon2
        params = {
            "start": f"{pair.lon1},{pair.lat1}",
            "end": f"{pair.lon2},{pair.lat2}",
        }
        response = None
        retry = 0
        while not response and retry < max_retries:
            try:
                response = client.get(URL, params=params).json()
            except httpx.ReadTimeout:
                print(f"timeout, retrying in {retry} seconds", params)
                time.sleep(retry)
                retry += 1
                client = httpx.Client(http2=True)
                continue

        if retry == max_retries:
            print("failed to get response, skipping")
            continue

        distance = -1.0

        if "error" in response:
            if response["error"]["code"] == 2004:
                # didn't configure the server to do 350km, only 100km
                continue
            if response["error"]["code"] == 2010:
                # one of the endpoints isn't in this data file
                continue
            if response["error"]["code"] in (2009, 2099):
                # no route found
                results.append(
                    result(job_id, pair, lat1, lon1, lat2, lon2, -1.0, False)
                )
                continue

        try:
            distance = response["features"][0]["properties"]["summary"]["distance"]
            lat1 = response["features"][0]["geometry"]["coordinates"][0][1]
            lon1 = response["features"][0]["geometry"]["coordinates"][0][0]
            lat2 = response["features"][0]["geometry"]["coordinates"][-1][1]
            lon2 = response["features"][0]["geometry"]["coordinates"][-1][0]

            distance = float(distance) / 1000.0
        except Exception:
            print(json.dumps(response, indent=2))
            continue

        results.append(result(job_id, pair, lat1, lon1, lat2, lon2, distance, True))

    return results


def enrich_country(country_code):
    print("enrich:", country_code)

    engine = create_engine(f"sqlite:///{GEONAMES_DB}")

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    pair_job = (
        session.query(GeoNamePairJob)
        .filter(GeoNamePairJob.success, GeoNamePairJob.country_code == country_code)
        .all()
    )[0]

    print("enrich: from pair job", pair_job.id)

    start_query = session.query(
        GeoName.osm_id.label("id1"),
        GeoName.lat.label("lat1"),
        GeoName.lon.label("lon1"),
    ).subquery()

    end_query = session.query(
        GeoName.osm_id.label("id2"),
        GeoName.lat.label("lat2"),
        GeoName.lon.label("lon2"),
    ).subquery()

    pairs = (
        session.query(
            GeoNamePair.id,
            GeoNamePair.job_id,
            GeoNamePair.start_id,
            GeoNamePair.end_id,
            GeoNamePair.direction,
            start_query,
            end_query,
        )
        .filter(GeoNamePair.job_id == pair_job.id)
        .join(start_query, start_query.c.id1 == GeoNamePair.start_id)
        .join(end_query, end_query.c.id2 == GeoNamePair.end_id)
    ).all()

    batch_size = BATCH_SIZE

    job = GeoNameEnrichJob()
    job.pair_job_id = pair_job.id
    session.add(job)
    session.commit()
    print("enrich: created enrich job", job.id)

    if len(pairs) < batch_size:
        batch_size = int(len(pairs) / os.cpu_count()) + 1
        print("enrich: data starved, batch size reduced to", batch_size)

    total = len(pairs)
    processed = 0
    start = datetime.now()

    call_api_job = partial(call_api, job.id)

    with ProcessPoolExecutor() as executor:
        for results in executor.map(call_api_job, chunks(pairs, batch_size)):
            insert_data(session, results)

            processed += len(results)
            print("enrich:", processed, "/", total, "pairs processed")

    end = datetime.now()
    total_s = (end - start).seconds + 0.001

    print(
        "enrich: finished processing", country_code, ",", processed, "of", total, "ok."
    )
    print(
        "enrich: took",
        int(total_s),
        "seconds;",
        round(total / total_s, 2),
        "requests per second",
    )

    job.success = True
    session.commit()


def get_pending_countries():
    engine = create_engine(f"sqlite:///{GEONAMES_DB}")

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    pair_jobs = session.query(GeoNamePairJob).filter(GeoNamePairJob.success).all()
    completed_enrich_jobs = (
        session.query(GeoNameEnrichJob).filter(GeoNameEnrichJob.success).all()
    )
    enriched_pair_job_ids = [job.pair_job_id for job in completed_enrich_jobs]
    pending_countries = [
        job.country_code for job in pair_jobs if job.id not in enriched_pair_job_ids
    ]

    session.close()

    return pending_countries


def main():
    pending_countries = get_pending_countries()
    print("enrich:", len(pending_countries), "left to go")

    groups = group_countries_by_region(pending_countries)

    for region, countries in groups.items():
        if region.too_large:
            print("enrich:", region.name, "skipped: not enough RAM")
            continue

        with running_docker_container(region.name):
            print("enrich:", region.name, countries)
            for country_code in countries:
                enrich_country(country_code)


if __name__ == "__main__":
    main()
